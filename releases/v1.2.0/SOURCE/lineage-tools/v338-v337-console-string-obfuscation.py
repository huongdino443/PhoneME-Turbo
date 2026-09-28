#!/usr/bin/env python3
"""Obfuscate selected console attribution strings in the v337 PhoneME APK.

The displayed text stays the same. It is stored as Base64 of XORed UTF-8 bytes
and decoded only when the console or deployment status needs it. This is a
basic-search deterrent, not encryption against someone who can reverse DEX.
"""

from __future__ import annotations

import argparse
import base64
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


DEFAULT_INPUT = Path("build/v337-v336-tom-jerry-nokia-sound-signed.apk")
DEFAULT_OUTPUT = Path("build/v338-v337-console-string-obfuscation-unsigned.apk")
CONSOLE_DIR = Path("smali/be/preuveneers/phoneme/fpmidp")
DECODER_METHOD = "decodeConsoleLabel"
XOR_KEY = 0x5A
DEX_NAME = re.compile(r"classes(?:[0-9]+)?\.dex$")

# Values are the exact escaped literals used by Apktool's smali output.
# Includes console status lines containing the same identifying terms.
TARGETS = (
    (
        "ConsoleActivity.smali",
        "v0",
        r"PhoneME Advanced Foundation Profile-MIDP Wrapper for Android 2.2. "
        r"Copyright (C) 2010-2014 by Davy Preuveneers.\n"
        r"Modified, extended, and APK rebuilt in 2026 by "
        r"Tr\u1ea7n V\u0103n H\u01b0\u1edfng.\n",
    ),
    (
        "ConsoleActivity$1.smali",
        "v0",
        r"\nDeploying PhoneME Advanced Foundation Profile-MIDP. "
        r"Please wait ...\n",
    ),
    (
        "ConsoleActivity$3.smali",
        "v0",
        r"\nPhoneME VM - M\u00f4i tr\u01b0\u1eddng ch\u1ea1y "
        r"\u1ee9ng d\u1ee5ng Java ME (JAR/JAD), "
        r"b\u1ea3n t\u00f9y ch\u1ec9nh.\n",
    ),
    (
        "ConsoleActivity.smali",
        "v2",
        "PhoneME VM is not yet deployed (build.revision ",
    ),
    (
        "ConsoleActivity.smali",
        "v4",
        "PhoneME VM needs updating (build.revision ",
    ),
    (
        "ConsoleActivity.smali",
        "v2",
        "PhoneME VM is up to date (build.revision ",
    ),
)


def apktool_version(executable: str) -> tuple[int, int, int] | None:
    try:
        result = subprocess.run(
            [executable, "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    match = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", result.stdout + result.stderr)
    if not match:
        return None
    return tuple(int(value or 0) for value in match.groups())


def find_apktool() -> str:
    override = os.environ.get("APKTOOL")
    if override:
        if not Path(override).is_file() or apktool_version(override) is None:
            raise SystemExit(f"APKTOOL is not a working Apktool executable: {override}")
        return override

    candidates: set[str] = set()
    configured = shutil.which("apktool")
    if configured:
        candidates.add(configured)
    candidates.update(
        str(path) for path in Path("/nix/store").glob("*-apktool-*/bin/apktool")
    )
    available = [
        (version, executable)
        for executable in candidates
        if (version := apktool_version(executable)) is not None
    ]
    if not available:
        raise SystemExit("A working Apktool installation is required")
    return max(available, key=lambda candidate: candidate[0])[1]


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def clone_info(info: zipfile.ZipInfo) -> zipfile.ZipInfo:
    cloned = zipfile.ZipInfo(info.filename, info.date_time)
    cloned.compress_type = info.compress_type
    cloned.comment = info.comment
    cloned.extra = b""
    cloned.internal_attr = info.internal_attr
    cloned.external_attr = info.external_attr
    cloned.create_system = info.create_system
    cloned.create_version = info.create_version
    cloned.extract_version = info.extract_version
    cloned.flag_bits = info.flag_bits & ~0x08
    return cloned


def is_apk_signature(name: str) -> bool:
    parts = name.upper().split("/")
    if len(parts) != 2 or parts[0] != "META-INF":
        return False
    filename = parts[1]
    return (
        filename == "MANIFEST.MF"
        or filename.startswith("SIG-")
        or filename.endswith((".SF", ".RSA", ".DSA", ".EC"))
    )


def decode_smali_literal(value: str) -> str:
    value = re.sub(
        r"\\u([0-9a-fA-F]{4})",
        lambda match: chr(int(match.group(1), 16)),
        value,
    )
    return (
        value.replace(r"\n", "\n")
        .replace(r"\r", "\r")
        .replace(r"\t", "\t")
        .replace(r"\"", '"')
        .replace(r"\\", "\\")
    )


def encode_literal(smali_literal: str) -> str:
    clear_bytes = decode_smali_literal(smali_literal).encode("utf-8")
    cipher_bytes = bytes(byte ^ XOR_KEY for byte in clear_bytes)
    return base64.b64encode(cipher_bytes).decode("ascii")


def obfuscate_call(register: str, smali_literal: str) -> str:
    encoded = encode_literal(smali_literal)
    return (
        f'    const-string {register}, "{encoded}"\n'
        f"    invoke-static {{{register}}}, "
        "Lbe/preuveneers/phoneme/fpmidp/ConsoleActivity;"
        f"->{DECODER_METHOD}(Ljava/lang/String;)Ljava/lang/String;\n"
        f"    move-result-object {register}"
    )


DECODER = """\
.method public static decodeConsoleLabel(Ljava/lang/String;)Ljava/lang/String;
    .locals 4

    const/4 v0, 0x0

    invoke-static {p0, v0}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B

    move-result-object v0

    const/4 v1, 0x0

    array-length v2, v0

    :decode_console_loop
    if-ge v1, v2, :decode_console_done

    aget-byte v3, v0, v1

    xor-int/lit16 v3, v3, 0x5a

    int-to-byte v3, v3

    aput-byte v3, v0, v1

    add-int/lit8 v1, v1, 0x1

    goto :decode_console_loop

    :decode_console_done
    new-instance v1, Ljava/lang/String;

    const-string v2, "UTF-8"

    invoke-direct {v1, v0, v2}, Ljava/lang/String;-><init>([BLjava/lang/String;)V

    return-object v1
.end method
"""


def patch_console(decoded: Path) -> int:
    console_path = decoded / CONSOLE_DIR / "ConsoleActivity.smali"
    text = console_path.read_text(encoding="utf-8")
    if f"->{DECODER_METHOD}(" in text or DECODER_METHOD in text:
        raise RuntimeError("Console string decoder already exists in the baseline")
    direct_methods = "# direct methods\n"
    if text.count(direct_methods) != 1:
        raise RuntimeError("ConsoleActivity direct-method insertion point is not unique")
    text = text.replace(direct_methods, direct_methods + "\n" + DECODER, 1)
    console_path.write_text(text, encoding="utf-8")

    replacements = 0
    for filename, register, raw_literal in TARGETS:
        path = decoded / CONSOLE_DIR / filename
        source = path.read_text(encoding="utf-8")
        old = f'    const-string {register}, "{raw_literal}"'
        if source.count(old) != 1:
            raise RuntimeError(
                f"Expected one matching console string in {filename}; "
                f"found {source.count(old)} for {register}"
            )
        source = source.replace(old, obfuscate_call(register, raw_literal), 1)
        path.write_text(source, encoding="utf-8")
        replacements += 1
    return replacements


def bump_version(decoded: Path) -> None:
    path = decoded / "apktool.yml"
    text = path.read_text(encoding="utf-8")
    if text.count("versionCode: 8") != 1 or text.count("versionName: 1.1.7") != 1:
        raise RuntimeError("unexpected v337 APK version metadata")
    text = text.replace("versionCode: 8", "versionCode: 9", 1)
    text = text.replace("versionName: 1.1.7", "versionName: 1.1.8", 1)
    path.write_text(text, encoding="utf-8")


def merge_payloads(source_apk: Path, rebuilt_apk: Path, output_apk: Path) -> None:
    with zipfile.ZipFile(source_apk, "r") as source, zipfile.ZipFile(
        rebuilt_apk, "r"
    ) as rebuilt:
        source_names = source.namelist()
        if len(source_names) != len(set(source_names)):
            raise RuntimeError("input APK contains duplicate ZIP entries")
        source_dex = {name for name in source_names if DEX_NAME.fullmatch(name)}
        rebuilt_dex = {name for name in rebuilt.namelist() if DEX_NAME.fullmatch(name)}
        if not source_dex or source_dex != rebuilt_dex:
            raise RuntimeError(
                f"APK DEX entry mismatch: source={sorted(source_dex)}, "
                f"rebuilt={sorted(rebuilt_dex)}"
            )

        output_apk.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(
            output_apk, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True
        ) as output:
            for info in source.infolist():
                if is_apk_signature(info.filename):
                    continue
                if DEX_NAME.fullmatch(info.filename) or info.filename == "AndroidManifest.xml":
                    payload = rebuilt.read(info.filename)
                else:
                    payload = source.read(info)
                output.writestr(clone_info(info), payload)


def patch_apk(input_apk: Path, output_apk: Path) -> int:
    if not input_apk.is_file():
        raise SystemExit(f"Input APK does not exist: {input_apk}")

    with tempfile.TemporaryDirectory(prefix="phoneme-v338-console-strings-") as name:
        work = Path(name)
        decoded = work / "decoded"
        rebuilt = work / "rebuilt.apk"
        apktool = find_apktool()
        run([apktool, "d", "-f", "-o", str(decoded), str(input_apk)])
        bump_version(decoded)
        replacements = patch_console(decoded)
        run([apktool, "b", str(decoded), "-o", str(rebuilt)])
        merge_payloads(input_apk, rebuilt, output_apk)
    return replacements


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_apk", type=Path, nargs="?", default=DEFAULT_INPUT)
    parser.add_argument("output_apk", type=Path, nargs="?", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    count = patch_apk(args.input_apk, args.output_apk)
    print(f"Wrote unsigned APK: {args.output_apk}")
    print(f"Obfuscated {count} console/about/status strings for runtime decoding.")
    print("Displayed wording is preserved; this only deters basic string search.")
    print("Bumped versionCode 8 -> 9 and versionName 1.1.7 -> 1.1.8.")


if __name__ == "__main__":
    main()