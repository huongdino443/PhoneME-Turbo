#!/usr/bin/env python3
"""Build the v337 release APK without the ASCII launch-stager class or call."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import shutil
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_APK = ROOT / "build/v337-v336-tom-jerry-nokia-sound-signed.apk"
V10_DONOR_APK = ROOT / "build/v10-ascii-import-release-signed.apk"
WORK_DIR = ROOT / "build/v337-no-ascii-stager-work"
BASE_DECODE = WORK_DIR / "v337"
DONOR_DECODE = WORK_DIR / "v10"
REBUILT_APK = WORK_DIR / "rebuilt.apk"
VERIFY_DECODE = WORK_DIR / "verify"
UNSIGNED_APK = ROOT / "build/v337-no-ascii-stager-unsigned.apk"


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def load_staging_helpers():
    path = ROOT / "tools/v338-v10-import-staging-variants.py"
    spec = importlib.util.spec_from_file_location("v338_staging_helpers", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load staging helpers: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_signature_entry(name: str) -> bool:
    upper = name.upper()
    if upper == "META-INF/MANIFEST.MF":
        return True
    return upper.startswith("META-INF/") and upper.endswith(
        (".SF", ".RSA", ".DSA", ".EC")
    )


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    apktool = shutil.which("apktool")
    if not apktool:
        raise SystemExit("apktool is required")
    for path in (BASE_APK, V10_DONOR_APK):
        if not path.is_file():
            raise SystemExit(f"Required APK does not exist: {path}")

    helpers = load_staging_helpers()
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    WORK_DIR.mkdir(parents=True)
    run([apktool, "d", "-f", str(BASE_APK), "-o", str(BASE_DECODE)])
    run([apktool, "d", "-f", str(V10_DONOR_APK), "-o", str(DONOR_DECODE)])

    caller_path = helpers.locate_smali(BASE_DECODE, helpers.CALLER_CLASS)
    stager_path = helpers.locate_smali(BASE_DECODE, helpers.STAGER_CLASS)
    caller_text = caller_path.read_text(encoding="utf-8")
    if f"AsciiSuiteLaunchStager;->{helpers.STAGER_METHOD}" not in caller_text:
        raise SystemExit("v337 caller does not have the expected stager invocation")
    caller_path.write_text(helpers.bypass_stager_call(caller_text), encoding="utf-8")
    stager_path.unlink()

    remaining_refs = [
        path.relative_to(BASE_DECODE).as_posix()
        for path in BASE_DECODE.rglob("*.smali")
        if "AsciiSuiteLaunchStager" in path.read_text(encoding="utf-8")
    ]
    if remaining_refs:
        raise SystemExit(f"Stager references remain in v337 sources: {remaining_refs}")

    v337_helper = helpers.locate_smali(BASE_DECODE, helpers.HELPER_CLASS).read_text(
        encoding="utf-8"
    )
    v10_helper = helpers.locate_smali(DONOR_DECODE, helpers.HELPER_CLASS).read_text(
        encoding="utf-8"
    )
    for signature in helpers.IMPORT_METHODS:
        if helpers.extract_method(v337_helper, signature) != helpers.extract_method(
            v10_helper, signature
        ):
            raise SystemExit(f"v337 import method differs from v10: {signature}")

    run([apktool, "b", str(BASE_DECODE), "-o", str(REBUILT_APK)])
    with zipfile.ZipFile(REBUILT_APK) as rebuilt:
        dex_names = [
            name
            for name in rebuilt.namelist()
            if name == "classes.dex"
            or (name.startswith("classes") and name.endswith(".dex"))
        ]
        if dex_names != ["classes.dex"]:
            raise SystemExit(f"Unexpected DEX entries: {dex_names}")
        new_dex = rebuilt.read("classes.dex")
    if b"AsciiSuiteLaunchStager" in new_dex:
        raise SystemExit("Rebuilt DEX still contains the stager name")

    run([apktool, "d", "-f", "-r", str(REBUILT_APK), "-o", str(VERIFY_DECODE)])
    if list(VERIFY_DECODE.rglob("AsciiSuiteLaunchStager.smali")):
        raise SystemExit("Rebuilt DEX still contains the stager class")
    verify_caller = helpers.locate_smali(VERIFY_DECODE, helpers.CALLER_CLASS).read_text(
        encoding="utf-8"
    )
    if "AsciiSuiteLaunchStager" in verify_caller:
        raise SystemExit("Rebuilt caller still references the stager")
    if "val$jadpath:Ljava/lang/String;" not in verify_caller or "move-object v1, v6" not in verify_caller:
        raise SystemExit("Rebuilt caller lost the original-path fallback")
    verify_helper = helpers.locate_smali(VERIFY_DECODE, helpers.HELPER_CLASS).read_text(
        encoding="utf-8"
    )
    for signature in helpers.IMPORT_METHODS:
        if helpers.extract_method(verify_helper, signature) != helpers.extract_method(
            v10_helper, signature
        ):
            raise SystemExit(f"Rebuilt DEX changed v10 import method: {signature}")

    temp_unsigned = UNSIGNED_APK.with_suffix(".tmp.apk")
    with zipfile.ZipFile(BASE_APK) as original, zipfile.ZipFile(
        temp_unsigned, "w", allowZip64=True
    ) as output:
        output.comment = original.comment
        for info in original.infolist():
            if is_signature_entry(info.filename):
                continue
            data = new_dex if info.filename == "classes.dex" else original.read(info.filename)
            cloned = copy.copy(info)
            compression = (
                zipfile.ZIP_DEFLATED if info.filename == "classes.dex" else info.compress_type
            )
            cloned.compress_type = compression
            output.writestr(
                cloned,
                data,
                compress_type=compression,
                compresslevel=9 if compression == zipfile.ZIP_DEFLATED else None,
            )
    temp_unsigned.replace(UNSIGNED_APK)

    with zipfile.ZipFile(BASE_APK) as original, zipfile.ZipFile(UNSIGNED_APK) as result:
        expected = [
            info.filename
            for info in original.infolist()
            if not is_signature_entry(info.filename)
        ]
        if result.namelist() != expected:
            raise SystemExit("v337 output changed ZIP entry order")
        if len(result.namelist()) != len(set(result.namelist())):
            raise SystemExit("Duplicate ZIP entries in v337 output")
        if result.testzip() is not None:
            raise SystemExit("v337 output ZIP integrity check failed")
        changed = [
            name
            for name in expected
            if name != "classes.dex" and result.read(name) != original.read(name)
        ]
        if changed:
            raise SystemExit(f"Non-DEX payloads changed: {changed}")
        if result.read("classes.dex") != new_dex:
            raise SystemExit("Merged DEX differs from Apktool output")

    print(f"v337 no-stager unsigned APK: {UNSIGNED_APK}")
    print(f"classes.dex SHA-256: {sha256(new_dex)}")
    print("The original v337 manifest and all non-DEX payloads are preserved.")
    print("The stager call and class are removed; the original-path fallback remains.")
    print(f"All {len(helpers.IMPORT_METHODS)} v10 import helpers match the donor.")


if __name__ == "__main__":
    main()