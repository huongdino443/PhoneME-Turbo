#!/usr/bin/env python3
"""Align uncompressed APK ZIP entries to four-byte boundaries without changing payloads."""

from __future__ import annotations

import os
import struct
import tempfile
import zipfile
from pathlib import Path


ALIGNMENT_FIELD_ID = 0xD935
LOCAL_FILE_HEADER_SIZE = 30


def _filename_bytes(info: zipfile.ZipInfo) -> bytes:
    try:
        return info.filename.encode("ascii")
    except UnicodeEncodeError:
        return info.filename.encode("utf-8")


def _without_alignment_field(extra: bytes) -> bytes:
    kept = bytearray()
    cursor = 0
    while cursor < len(extra):
        if len(extra) - cursor < 4:
            raise RuntimeError("Malformed ZIP extra field")
        field_id, field_size = struct.unpack_from("<HH", extra, cursor)
        end = cursor + 4 + field_size
        if end > len(extra):
            raise RuntimeError("ZIP extra field extends beyond its data")
        if field_id != ALIGNMENT_FIELD_ID:
            kept.extend(extra[cursor:end])
        cursor = end
    return bytes(kept)


def _local_data_offset(raw, info: zipfile.ZipInfo) -> int:
    raw.seek(info.header_offset)
    header = raw.read(LOCAL_FILE_HEADER_SIZE)
    if len(header) != LOCAL_FILE_HEADER_SIZE or header[:4] != b"PK\x03\x04":
        raise RuntimeError(f"Invalid local ZIP header for {info.filename}")
    filename_length, extra_length = struct.unpack_from("<HH", header, 26)
    return (
        info.header_offset
        + LOCAL_FILE_HEADER_SIZE
        + filename_length
        + extra_length
    )


def verify_aligned(path: Path, alignment: int = 4) -> None:
    with path.open("rb") as raw, zipfile.ZipFile(path, "r") as archive:
        if archive.testzip() is not None:
            raise RuntimeError(f"ZIP CRC verification failed: {path}")
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise RuntimeError(f"Duplicate ZIP entries found: {path}")
        for info in archive.infolist():
            if info.compress_type == zipfile.ZIP_STORED:
                offset = _local_data_offset(raw, info)
                if offset % alignment:
                    raise RuntimeError(
                        f"Unaligned stored entry {info.filename}: "
                        f"data offset {offset} is not divisible by {alignment}"
                    )


def align_apk(
    input_path: Path,
    output_path: Path,
    alignment: int = 4,
) -> None:
    if input_path.resolve() == output_path.resolve():
        raise RuntimeError("Input and output APK paths must differ")
    if output_path.exists() and output_path.stat().st_size != 0:
        raise RuntimeError(f"Refusing to overwrite nonempty output: {output_path}")
    if alignment < 1 or alignment & (alignment - 1):
        raise ValueError("Alignment must be a positive power of two")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pending_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            dir=output_path.parent,
            delete=False,
        ) as pending:
            pending_path = Path(pending.name)

        with zipfile.ZipFile(input_path, "r") as source, zipfile.ZipFile(
            pending_path, "w", allowZip64=True
        ) as target:
            source_names = source.namelist()
            if len(source_names) != len(set(source_names)):
                raise RuntimeError(f"Duplicate ZIP entries found: {input_path}")
            if source.testzip() is not None:
                raise RuntimeError(f"Input ZIP CRC verification failed: {input_path}")

            for info in source.infolist():
                data = source.read(info.filename)
                if info.compress_type == zipfile.ZIP_STORED:
                    info.extra = _without_alignment_field(info.extra)
                    start = (
                        target.fp.tell()
                        + LOCAL_FILE_HEADER_SIZE
                        + len(_filename_bytes(info))
                        + len(info.extra)
                    )
                    padding = (-start) % alignment
                    if padding:
                        info.extra += (
                            struct.pack("<HH", ALIGNMENT_FIELD_ID, padding)
                            + bytes(padding)
                        )
                target.writestr(info, data)

        verify_aligned(pending_path, alignment)
        with zipfile.ZipFile(input_path, "r") as source, zipfile.ZipFile(
            pending_path, "r"
        ) as aligned:
            if aligned.namelist() != source.namelist():
                raise RuntimeError("ZIP entry names or order changed during alignment")
            for name in source.namelist():
                if source.read(name) != aligned.read(name):
                    raise RuntimeError(
                        f"ZIP payload changed during alignment: {name}"
                    )

        os.replace(pending_path, output_path)
        pending_path = None
    finally:
        if pending_path is not None:
            pending_path.unlink(missing_ok=True)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_apk", type=Path)
    parser.add_argument("output_apk", type=Path)
    args = parser.parse_args()
    align_apk(args.input_apk, args.output_apk)
    print(f"Four-byte APK alignment verified: {args.output_apk}")


if __name__ == "__main__":
    main()