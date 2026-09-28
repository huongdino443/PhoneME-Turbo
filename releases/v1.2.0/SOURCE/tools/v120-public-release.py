#!/usr/bin/env python3
"""Create the unsigned 1.2.0 APK from the approved v340 APK baseline."""

from __future__ import annotations

import argparse
import copy
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


SOURCE_VERSION_CODE = "8"
SOURCE_VERSION_NAME = "1.1.7"
RELEASE_VERSION_CODE = "10"
RELEASE_VERSION_NAME = "1.2.0"
DEX_ENTRY = re.compile(r"classes(?:[0-9]+)?\.dex\Z")


def is_apk_signature(name: str) -> bool:
    upper = name.upper()
    if not upper.startswith("META-INF/"):
        return False
    base = upper.rsplit("/", 1)[-1]
    return (
        base == "MANIFEST.MF"
        or base.endswith((".SF", ".RSA", ".DSA", ".EC"))
        or base.startswith("SIG-")
    )


def unique_names(archive: zipfile.ZipFile, label: str) -> set[str]:
    names = [item.filename for item in archive.infolist()]
    if len(names) != len(set(names)):
        raise RuntimeError(f"{label} contains duplicate ZIP entries")
    return set(names)


def update_version_metadata(decoded: Path) -> None:
    path = decoded / "apktool.yml"
    text = path.read_text(encoding="utf-8")
    code_pattern = re.compile(
        rf"(?m)^(\s*versionCode:\s*){re.escape(SOURCE_VERSION_CODE)}(\s*)$"
    )
    name_pattern = re.compile(
        rf"(?m)^(\s*versionName:\s*){re.escape(SOURCE_VERSION_NAME)}(\s*)$"
    )
    if len(code_pattern.findall(text)) != 1 or len(name_pattern.findall(text)) != 1:
        raise RuntimeError(
            "Input is not the expected v340 baseline "
            f"({SOURCE_VERSION_CODE}/{SOURCE_VERSION_NAME})"
        )
    text = code_pattern.sub(
        lambda match: f"{match.group(1)}{RELEASE_VERSION_CODE}{match.group(2)}",
        text,
        count=1,
    )
    text = name_pattern.sub(
        lambda match: f"{match.group(1)}{RELEASE_VERSION_NAME}{match.group(2)}",
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8")


def build_unsigned(input_apk: Path, output_apk: Path) -> None:
    apktool = shutil.which("apktool")
    if not apktool:
        raise SystemExit("apktool is required to update Android version metadata")
    if not input_apk.is_file():
        raise SystemExit(f"Input APK does not exist: {input_apk}")
    if input_apk.resolve() == output_apk.resolve():
        raise SystemExit("Input and output APK paths must be different")

    output_apk.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="phoneme-v120-release-") as temp_name:
        work = Path(temp_name)
        decoded = work / "decoded"
        rebuilt = work / "rebuilt.apk"
        staged_output = work / "versioned-unsigned.apk"

        subprocess.run(
            [apktool, "d", "-f", "-s", "-o", str(decoded), str(input_apk)],
            check=True,
        )
        update_version_metadata(decoded)
        subprocess.run(
            [apktool, "b", str(decoded), "-o", str(rebuilt)],
            check=True,
        )

        with zipfile.ZipFile(input_apk, "r") as source, zipfile.ZipFile(
            rebuilt, "r"
        ) as rebuilt_zip:
            source_names = unique_names(source, "Input APK")
            rebuilt_names = unique_names(rebuilt_zip, "Rebuilt APK")
            source_dex = {name for name in source_names if DEX_ENTRY.fullmatch(name)}
            rebuilt_dex = {name for name in rebuilt_names if DEX_ENTRY.fullmatch(name)}
            if not source_dex or source_dex != rebuilt_dex:
                raise RuntimeError(
                    f"APK DEX entry mismatch: source={sorted(source_dex)}, "
                    f"rebuilt={sorted(rebuilt_dex)}"
                )
            if "AndroidManifest.xml" not in source_names or (
                "AndroidManifest.xml" not in rebuilt_names
            ):
                raise RuntimeError("AndroidManifest.xml is missing from an APK")
            for name in source_dex:
                if source.read(name) != rebuilt_zip.read(name):
                    raise RuntimeError(f"DEX unexpectedly changed during build: {name}")

            with zipfile.ZipFile(
                staged_output, "w", allowZip64=True
            ) as output:
                for info in source.infolist():
                    if is_apk_signature(info.filename):
                        continue
                    payload = (
                        rebuilt_zip.read(info.filename)
                        if info.filename == "AndroidManifest.xml"
                        else source.read(info)
                    )
                    output.writestr(copy.copy(info), payload)

        with zipfile.ZipFile(staged_output, "r") as result:
            if result.testzip() is not None:
                raise RuntimeError("Generated APK failed ZIP integrity validation")
            if "AndroidManifest.xml" not in unique_names(result, "Output APK"):
                raise RuntimeError("Generated APK has no AndroidManifest.xml")

        temporary_output = output_apk.with_name(output_apk.name + ".tmp")
        shutil.copy2(staged_output, temporary_output)
        os.replace(temporary_output, output_apk)

    digest = hashlib.sha256(output_apk.read_bytes()).hexdigest()
    print(f"Wrote unsigned APK: {output_apk}")
    print(f"SHA-256: {digest}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_apk", type=Path, help="approved v340 unsigned APK")
    parser.add_argument("output_apk", type=Path, help="output unsigned 1.2.0 APK")
    args = parser.parse_args()
    build_unsigned(args.input_apk, args.output_apk)


if __name__ == "__main__":
    main()