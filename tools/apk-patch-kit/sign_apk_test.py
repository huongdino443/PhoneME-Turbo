#!/usr/bin/env python3
"""Create a temporary v1-signed test APK without persisting a private key.

This is only for installing the generated APK on a test device after an
APK-level patch. The original Turbo-nHD signing key was not supplied, so this
cannot be an in-place update over the original installation.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import subprocess
import tempfile
import zipfile
from pathlib import Path


SIGNATURE_PREFIX = "META-INF/TEST"
SIGNATURE_SUFFIXES = (".SF", ".RSA", ".DSA", ".EC")


def fold_attribute(name: str, value: str) -> bytes:
    """Fold a JAR manifest attribute so each physical line is <= 72 bytes."""

    text = f"{name}: {value}"
    remaining = text.encode("utf-8")
    lines: list[bytes] = []
    first = True
    while remaining:
        capacity = 72 if first else 71
        chunk = remaining[:capacity]
        remaining = remaining[capacity:]
        lines.append(chunk if first else b" " + chunk)
        first = False
    return b"\r\n".join(lines) + b"\r\n"


def section(name: str, payload: bytes) -> bytes:
    digest = base64.b64encode(hashlib.sha256(payload).digest()).decode("ascii")
    return (
        fold_attribute("Name", name)
        + fold_attribute("SHA-256-Digest", digest)
        + b"\r\n"
    )


def copy_zip_info(source: zipfile.ZipInfo) -> zipfile.ZipInfo:
    target = zipfile.ZipInfo(source.filename, date_time=source.date_time)
    target.compress_type = source.compress_type
    target.comment = source.comment
    target.extra = source.extra
    target.internal_attr = source.internal_attr
    target.external_attr = source.external_attr
    target.create_system = source.create_system
    target.create_version = source.create_version
    target.extract_version = source.extract_version
    target.flag_bits = source.flag_bits & ~0x08
    return target


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_apk", type=Path)
    parser.add_argument("output_apk", type=Path)
    args = parser.parse_args()

    if not args.input_apk.is_file():
        raise SystemExit(f"Input APK does not exist: {args.input_apk}")
    args.output_apk.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="phoneme-sign-") as temp_name:
        temp = Path(temp_name)
        key = temp / "test-key.pem"
        cert = temp / "test-cert.pem"
        manifest_path = temp / "MANIFEST.MF"
        sf_path = temp / "TEST.SF"
        rsa_path = temp / "TEST.RSA"

        run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-keyout",
                str(key),
                "-out",
                str(cert),
                "-days",
                "1",
                "-subj",
                "/C=XX/O=PhoneME/OU=Test/CN=PhoneME Turbo nHD Test",
            ]
        )

        with zipfile.ZipFile(args.input_apk, "r") as source:
            entries: list[tuple[zipfile.ZipInfo, bytes]] = []
            for info in source.infolist():
                upper_name = info.filename.upper()
                if upper_name.startswith("META-INF/") and (
                    upper_name.endswith("MANIFEST.MF")
                    or upper_name.endswith(SIGNATURE_SUFFIXES)
                ):
                    continue
                entries.append((info, source.read(info)))

        signed_entries = [
            (info.filename, payload)
            for info, payload in entries
            if not info.is_dir() and not info.filename.endswith("/")
        ]
        main_attributes = (
            fold_attribute("Manifest-Version", "1.0")
            + fold_attribute("Created-By", "1.0 (PhoneME test signer)")
            + b"\r\n"
        )
        manifest = main_attributes + b"".join(
            section(name, payload) for name, payload in signed_entries
        )
        manifest_path.write_bytes(manifest)

        main_digest = base64.b64encode(
            hashlib.sha256(main_attributes).digest()
        ).decode("ascii")
        manifest_digest = base64.b64encode(
            hashlib.sha256(manifest).digest()
        ).decode("ascii")
        sf = (
            fold_attribute("Signature-Version", "1.0")
            + fold_attribute("Created-By", "1.0 (PhoneME test signer)")
            + fold_attribute(
                "SHA-256-Digest-Manifest-Main-Attributes", main_digest
            )
            + fold_attribute("SHA-256-Digest-Manifest", manifest_digest)
            + b"\r\n"
        )

        cursor = len(main_attributes)
        for name, _payload in signed_entries:
            next_cursor = manifest.find(b"\r\n\r\n", cursor)
            if next_cursor < 0:
                raise RuntimeError(f"Could not find manifest section for {name}")
            next_cursor += 4
            manifest_section = manifest[cursor:next_cursor]
            section_digest = base64.b64encode(
                hashlib.sha256(manifest_section).digest()
            ).decode("ascii")
            sf += (
                fold_attribute("Name", name)
                + fold_attribute("SHA-256-Digest", section_digest)
                + b"\r\n"
            )
            cursor = next_cursor
        sf_path.write_bytes(sf)

        run(
            [
                "openssl",
                "smime",
                "-sign",
                "-binary",
                "-in",
                str(sf_path),
                "-signer",
                str(cert),
                "-inkey",
                str(key),
                "-outform",
                "DER",
                "-out",
                str(rsa_path),
                "-noattr",
            ]
        )

        with zipfile.ZipFile(
            args.output_apk,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            allowZip64=True,
        ) as target:
            target.writestr(
                "META-INF/MANIFEST.MF",
                manifest,
                compress_type=zipfile.ZIP_DEFLATED,
            )
            target.writestr(
                "META-INF/TEST.SF",
                sf,
                compress_type=zipfile.ZIP_DEFLATED,
            )
            target.writestr(
                "META-INF/TEST.RSA",
                rsa_path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
            )
            for info, payload in entries:
                target.writestr(copy_zip_info(info), payload)

    print(f"Wrote v1-signed test APK: {args.output_apk}")
    print("The signing key was temporary and was not written to the workspace.")


if __name__ == "__main__":
    main()