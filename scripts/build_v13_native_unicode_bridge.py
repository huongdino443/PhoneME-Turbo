#!/usr/bin/env python3
"""Apply the PhoneME InputFix7 native Unicode bridge.

This script intentionally patches only libcvm.so.2 and libcvm.so.4 inside an
APK ZIP. It does not sign the APK. Use a private signing key outside this
repository after the output has been verified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

CHUNK_NAMES = [
    "assets/foundation/bin/libcvm.so",
    "assets/foundation/bin/libcvm.so.1",
    "assets/foundation/bin/libcvm.so.2",
    "assets/foundation/bin/libcvm.so.3",
    "assets/foundation/bin/libcvm.so.4",
    "assets/foundation/bin/libcvm.so.5",
    "assets/foundation/bin/libcvm.so.6",
]
CHUNK_SIZES = [1048000, 1048000, 1048000, 1048000, 1048000, 1048000, 53260]
BRANCH_OFFSET = 0x2A80A4
HELPER_OFFSET = 0x468C14
HELPER_SIZE = 40


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-apk", type=Path, required=True,
                        help="decoded/unsigned-compatible base APK")
    parser.add_argument("--patch-elf", type=Path, required=True,
                        help="concatenated CVM patch ELF containing the bridge")
    parser.add_argument("--output-apk", type=Path, required=True,
                        help="unsigned patched APK output")
    parser.add_argument("--manifest", type=Path, required=True,
                        help="JSON provenance manifest output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.base_apk.is_file():
        raise SystemExit(f"missing base APK: {args.base_apk}")
    if not args.patch_elf.is_file():
        raise SystemExit(f"missing patch ELF: {args.patch_elf}")

    with zipfile.ZipFile(args.base_apk, "r") as zin:
        infos = zin.infolist()
        payloads = {info.filename: zin.read(info.filename) for info in infos}

    missing = [name for name in CHUNK_NAMES if name not in payloads]
    if missing:
        raise SystemExit(f"base APK is missing CVM chunks: {missing}")

    original_chunks = [payloads[name] for name in CHUNK_NAMES]
    if [len(chunk) for chunk in original_chunks] != CHUNK_SIZES:
        raise SystemExit(
            "unexpected base chunk sizes: "
            f"{[len(chunk) for chunk in original_chunks]}"
        )
    original_elf = b"".join(original_chunks)

    patch_elf = args.patch_elf.read_bytes()
    if len(patch_elf) != sum(CHUNK_SIZES):
        raise SystemExit(f"unexpected patch ELF size: {len(patch_elf)}")

    expected_branch = bytes.fromhex("0c0000ea")
    patched_branch = bytes.fromhex("da0207ea")
    if original_elf[BRANCH_OFFSET:BRANCH_OFFSET + 4] != expected_branch:
        raise SystemExit("base branch site is not the expected unpatched ARM branch")
    if original_elf[HELPER_OFFSET:HELPER_OFFSET + HELPER_SIZE] != b"\x00" * HELPER_SIZE:
        raise SystemExit("base helper cave is not zero-filled; refusing unsafe overwrite")
    if patch_elf[BRANCH_OFFSET:BRANCH_OFFSET + 4] != patched_branch:
        raise SystemExit("patch ELF has an unexpected branch instruction")
    patched_helper = patch_elf[HELPER_OFFSET:HELPER_OFFSET + HELPER_SIZE]
    if patched_helper == b"\x00" * HELPER_SIZE:
        raise SystemExit("patch ELF helper is empty")

    merged = bytearray(original_elf)
    merged[BRANCH_OFFSET:BRANCH_OFFSET + 4] = patched_branch
    merged[HELPER_OFFSET:HELPER_OFFSET + HELPER_SIZE] = patched_helper

    replacements: dict[str, bytes] = {}
    cursor = 0
    for name, size in zip(CHUNK_NAMES, CHUNK_SIZES):
        replacements[name] = bytes(merged[cursor:cursor + size])
        cursor += size
    changed = [name for name in CHUNK_NAMES if replacements[name] != payloads[name]]
    expected_changed = [CHUNK_NAMES[2], CHUNK_NAMES[4]]
    if changed != expected_changed:
        raise SystemExit(f"unexpected changed chunks: {changed}")

    args.output_apk.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    if args.output_apk.exists():
        args.output_apk.unlink()
    with zipfile.ZipFile(args.base_apk, "r") as zin, zipfile.ZipFile(args.output_apk, "w") as zout:
        for info in zin.infolist():
            zout.writestr(info, replacements.get(info.filename, zin.read(info.filename)))

    manifest = {
        "base_apk_sha256": sha256_bytes(args.base_apk.read_bytes()),
        "output_apk_sha256": sha256_bytes(args.output_apk.read_bytes()),
        "patch_elf_sha256": sha256_bytes(patch_elf),
        "changed_entries": changed,
        "branch_offset": hex(BRANCH_OFFSET),
        "branch_before": expected_branch.hex(),
        "branch_after": patched_branch.hex(),
        "helper_offset": hex(HELPER_OFFSET),
        "helper_size": HELPER_SIZE,
        "helper_sha256": sha256_bytes(patched_helper),
        "native_scope": "only libcvm.so.2 and libcvm.so.4",
        "protocol_basis": "InputFix7-nativeUnicodeTextCave; writable BSS scratch KeyMapping for BMP Unicode",
        "signed_by_this_script": False,
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
