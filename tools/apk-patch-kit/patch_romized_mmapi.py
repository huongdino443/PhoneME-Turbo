#!/usr/bin/env python3
"""Patch Turbo's ROMized JSR-135 dispatch in libcvm.so.

Turbo preloads javax.microedition.media.Manager from its ROM image, so
replacing Manager.class alone does not affect the createPlayer(String) method
used by the bundled CVM.  This patch keeps the original method size and
changes only the MP3 dispatch test: a URL containing a query marker is sent
through the existing Android media-player path instead of the broken
createDataSource fallback.

The narrow transformation is intentional.  It recognizes the signed HTTP
URLs this patch targets without changing the URL passed to Android.  Other
media types should continue through the original dispatch logic.

The APK stores libcvm.so in seven split ZIP entries.  This tool reconstructs
the complete ARM ELF, validates the exact ROM method bytes, patches it, then
splits it back at the original boundaries.  The result is unsigned because
the APK contents changed.
"""

from __future__ import annotations

import argparse
import hashlib
import struct
import zipfile
from pathlib import Path


LIB_PATH = "assets/foundation/bin/libcvm.so"
LIB_PARTS = tuple([LIB_PATH] + [f"{LIB_PATH}.{i}" for i in range(1, 7)])
REVISION_PATH = "assets/foundation/build.revision"
SIGNATURE_SUFFIXES = (".SF", ".RSA", ".DSA", ".EC")

# The ROM symbol
# javax_microedition_media_Manager_createPlayer_String_MD is not exported in
# this build, but the method-table mapping identifies this JMD unambiguously.
CREATE_PLAYER_JMD_OFFSET = 0x3EA8EC
CREATE_PLAYER_CODE_OFFSET = CREATE_PLAYER_JMD_OFFSET + 12
CREATE_PLAYER_CODE_LENGTH = 517

# Original bytes:
#   aload_1; ldc_w ".mp3"; invokenonvirtual endsWith; ifeq +12
# Replacement:
#   aload_1; bipush '?'; invokenonvirtual indexOf(int); iflt +13; nop
#
# d5 63 60 is the already-ROMized String.indexOf(int) call used earlier in
# this same method.  Keeping that resolved target avoids editing ROM constant
# pool pointers or method tables.
ORIGINAL_TEST = bytes.fromhex("2b e4 10 66 d5 68 bd 99 00 0c")
PATCHED_TEST = bytes.fromhex("2b 10 3f d5 63 60 9b 00 0d 00")


def clone_info(info: zipfile.ZipInfo, *, compression: int | None = None) -> zipfile.ZipInfo:
    result = zipfile.ZipInfo(info.filename, date_time=info.date_time)
    result.compress_type = info.compress_type if compression is None else compression
    result.comment = info.comment
    result.extra = info.extra
    result.internal_attr = info.internal_attr
    result.external_attr = info.external_attr
    result.create_system = info.create_system
    result.create_version = info.create_version
    result.extract_version = info.extract_version
    result.flag_bits = info.flag_bits & ~0x08
    return result


def reconstruct(parts: dict[str, bytes]) -> tuple[bytes, list[int]]:
    missing = [name for name in LIB_PARTS if name not in parts]
    if missing:
        raise RuntimeError(f"Missing split libcvm entries: {', '.join(missing)}")
    sizes = [len(parts[name]) for name in LIB_PARTS]
    payload = b"".join(parts[name] for name in LIB_PARTS)
    return payload, sizes


def validate_elf(payload: bytes) -> None:
    if payload[:4] != b"\x7fELF":
        raise RuntimeError("Reconstructed libcvm.so is not an ELF")
    if payload[4] != 1 or payload[5] != 1:
        raise RuntimeError("Expected little-endian 32-bit libcvm.so")
    machine = struct.unpack_from("<H", payload, 18)[0]
    if machine != 40:  # EM_ARM
        raise RuntimeError(f"Expected ARM ELF (machine 40), got {machine}")


def patch_libcvm(payload: bytes) -> tuple[bytes, int]:
    validate_elf(payload)
    end = CREATE_PLAYER_CODE_OFFSET + CREATE_PLAYER_CODE_LENGTH
    if end > len(payload):
        raise RuntimeError("ROMized Manager method is outside libcvm.so")

    jmd = payload[CREATE_PLAYER_JMD_OFFSET:CREATE_PLAYER_CODE_OFFSET]
    if len(jmd) != 12:
        raise RuntimeError("ROMized Manager JMD is truncated")
    max_locals, flags, capacity, exceptions, code_length = struct.unpack(
        "<HHIHH", jmd
    )
    expected = (11, 0, 23, 3, CREATE_PLAYER_CODE_LENGTH)
    if (max_locals, flags, capacity, exceptions, code_length) != expected:
        raise RuntimeError(
            "Manager.createPlayer(String) JMD mismatch: "
            f"{(max_locals, flags, capacity, exceptions, code_length)!r}"
        )

    code = payload[CREATE_PLAYER_CODE_OFFSET:end]
    marker = code.find(ORIGINAL_TEST)
    if marker < 0:
        raise RuntimeError(
            "Expected ROMized MP3 dispatch sequence was not found in "
            "Manager.createPlayer(String)"
        )
    if code.find(ORIGINAL_TEST, marker + 1) >= 0:
        raise RuntimeError("Dispatch sequence is unexpectedly ambiguous")

    patched = bytearray(payload)
    absolute = CREATE_PLAYER_CODE_OFFSET + marker
    patched[absolute : absolute + len(PATCHED_TEST)] = PATCHED_TEST
    result = bytes(patched)

    changed = [i for i, (before, after) in enumerate(zip(payload, result)) if before != after]
    expected_changed = [
        absolute + index
        for index, (before, after) in enumerate(zip(ORIGINAL_TEST, PATCHED_TEST))
        if before != after
    ]
    if changed != expected_changed:
        raise RuntimeError("Native patch changed bytes outside the validated sequence")
    return result, marker


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_apk", type=Path)
    parser.add_argument("output_apk", type=Path)
    args = parser.parse_args()

    if not args.input_apk.is_file():
        raise SystemExit(f"Input APK does not exist: {args.input_apk}")
    args.output_apk.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.input_apk, "r") as source:
        infos = source.infolist()
        payloads = {info.filename: source.read(info) for info in infos}
        original_lib, part_sizes = reconstruct(
            {name: payloads[name] for name in LIB_PARTS if name in payloads}
        )
        patched_lib, marker = patch_libcvm(original_lib)

        split_payloads: dict[str, bytes] = {}
        cursor = 0
        for name, size in zip(LIB_PARTS, part_sizes):
            split_payloads[name] = patched_lib[cursor : cursor + size]
            cursor += size
        if cursor != len(patched_lib):
            raise RuntimeError("Patched libcvm.so split size does not match input")

        entries: list[tuple[zipfile.ZipInfo, bytes]] = []
        stripped_signatures: list[str] = []
        for info in infos:
            upper_name = info.filename.upper()
            if upper_name.startswith("META-INF/") and (
                upper_name.endswith("MANIFEST.MF")
                or upper_name.endswith(SIGNATURE_SUFFIXES)
            ):
                stripped_signatures.append(info.filename)
                continue

            payload = split_payloads.get(info.filename, payloads[info.filename])
            if info.filename == REVISION_PATH:
                payload = payload.rstrip(b"\r\n") + b"-native-mmapi1\n"
            entries.append((info, payload))

    with zipfile.ZipFile(
        args.output_apk, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True
    ) as target:
        for info, payload in entries:
            target.writestr(clone_info(info), payload)

    # Re-open the output and validate the actual APK asset, not just the
    # in-memory buffer used to create it.
    with zipfile.ZipFile(args.output_apk, "r") as check:
        rebuilt, _ = reconstruct({name: check.read(name) for name in LIB_PARTS})
        validate_elf(rebuilt)
        if rebuilt != patched_lib:
            raise RuntimeError("Output APK libcvm.so does not reconstruct exactly")
        if check.read(REVISION_PATH) != (
            payloads[REVISION_PATH].rstrip(b"\r\n") + b"-native-mmapi1\n"
        ):
            raise RuntimeError("Output APK foundation revision was not updated")

    print(f"Wrote {args.output_apk}")
    print(f"Original libcvm SHA-256: {hashlib.sha256(original_lib).hexdigest()}")
    print(f"Patched libcvm SHA-256:  {hashlib.sha256(patched_lib).hexdigest()}")
    changed_count = sum(
        before != after for before, after in zip(ORIGINAL_TEST, PATCHED_TEST)
    )
    print(
        f"Changed native bytes: {changed_count} at "
        f"0x{CREATE_PLAYER_CODE_OFFSET + marker:08x}"
    )
    print(f"Stripped signatures: {len(stripped_signatures)}")


if __name__ == "__main__":
    main()