#!/usr/bin/env python3
"""Slightly enlarge the Turbo EdgeSwipe menu only on 320x480 displays."""

from __future__ import annotations

import hashlib
import re
import shutil
import struct
import subprocess
import tempfile
import zipfile
import zlib
from pathlib import Path
from zipfile import ZipInfo


BASE_APK = Path("build/v338-v337-console-strings-api19-release-signed.apk")
UNSIGNED_APK = Path("build/v339-v338-edge-menu-320x480-unsigned.apk")
SIGNED_APK = Path("build/v339-v338-edge-menu-320x480-release-signed.apk")
SIGNER = Path("tools/sign_apk_release.py")
DEX_ENTRY = re.compile(r"classes(?:[0-9]+)?\.dex$")
EDGE_MENU_PATH = Path("smali/com/phoneme/corebridge/EdgeMenuOverlay.smali")
EDGE_MENU = "Lcom/phoneme/corebridge/EdgeMenuOverlay;"

ICON_SIZE_METHOD = """\
.method private iconSizePx()I
    .locals 2

    invoke-direct {p0}, Lcom/phoneme/corebridge/EdgeMenuOverlay;->is320x480Display()Z

    move-result v1

    if-eqz v1, :edge_menu_default_icon_size

    iget v0, p0, Lcom/phoneme/corebridge/EdgeMenuOverlay;->iconCellHeight:I

    const/16 v1, 0x1c

    invoke-static {v0, v1}, Ljava/lang/Math;->min(II)I

    move-result v0

    const/16 v1, 0x18

    invoke-static {v0, v1}, Ljava/lang/Math;->max(II)I

    move-result v0

    return v0

    :edge_menu_default_icon_size
    iget v0, p0, Lcom/phoneme/corebridge/EdgeMenuOverlay;->iconCellHeight:I

    mul-int/lit8 v1, v0, 0x40

    div-int/lit8 v1, v1, 0x64

    invoke-static {v0, v1}, Ljava/lang/Math;->min(II)I

    move-result v0

    const/16 v1, 0x18

    invoke-static {v1, v0}, Ljava/lang/Math;->max(II)I

    move-result v0

    return v0
.end method
"""

DISPLAY_HELPER = """\
.method private is320x480Display()Z
    .locals 4

    iget-object v0, p0, Lcom/phoneme/corebridge/EdgeMenuOverlay;->activity:Landroid/app/Activity;

    invoke-virtual {v0}, Landroid/app/Activity;->getWindowManager()Landroid/view/WindowManager;

    move-result-object v0

    invoke-interface {v0}, Landroid/view/WindowManager;->getDefaultDisplay()Landroid/view/Display;

    move-result-object v0

    invoke-virtual {v0}, Landroid/view/Display;->getWidth()I

    move-result v1

    invoke-virtual {v0}, Landroid/view/Display;->getHeight()I

    move-result v2

    const/16 v3, 0x140

    if-ne v1, v3, :edge_menu_try_landscape

    const/16 v3, 0x1e0

    if-ne v2, v3, :edge_menu_not_320x480

    const/4 v0, 0x1

    return v0

    :edge_menu_try_landscape
    const/16 v3, 0x1e0

    if-ne v1, v3, :edge_menu_not_320x480

    const/16 v3, 0x140

    if-ne v2, v3, :edge_menu_not_320x480

    const/4 v0, 0x1

    return v0

    :edge_menu_not_320x480
    const/4 v0, 0x0

    return v0
.end method
"""


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


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


def replace_method(source: str, marker: str, replacement: str) -> str:
    start = source.find(marker)
    if start < 0 or source.find(marker, start + len(marker)) >= 0:
        raise RuntimeError(f"Expected one smali method marker: {marker}")
    end_marker = ".end method"
    end = source.find(end_marker, start)
    if end < 0:
        raise RuntimeError(f"Missing .end method after {marker}")
    end += len(end_marker)
    return source[:start] + replacement.rstrip() + source[end:]


def patch_edge_menu(decoded: Path) -> None:
    path = decoded / EDGE_MENU_PATH
    source = path.read_text(encoding="utf-8")
    if "->is320x480Display()Z" in source:
        raise RuntimeError("The 320x480 EdgeSwipe sizing patch is already present")

    source = replace_method(
        source,
        ".method private iconSizePx()I",
        ICON_SIZE_METHOD,
    )

    cell_anchor = (
        f"    iput v2, p0, {EDGE_MENU}->iconCellHeight:I\n\n"
        "    mul-int/lit8 v0, v0, 0xc"
    )
    cell_patch = (
        f"    iput v2, p0, {EDGE_MENU}->iconCellHeight:I\n\n"
        f"    invoke-direct {{p0}}, {EDGE_MENU}->is320x480Display()Z\n\n"
        "    move-result v2\n\n"
        "    if-eqz v2, :edge_menu_base_cell_size\n\n"
        f"    iget v2, p0, {EDGE_MENU}->iconCellHeight:I\n\n"
        "    const/16 v3, 0x1c\n\n"
        "    invoke-static {v2, v3}, Ljava/lang/Math;->max(II)I\n\n"
        "    move-result v2\n\n"
        f"    iput v2, p0, {EDGE_MENU}->iconCellHeight:I\n\n"
        "    :edge_menu_base_cell_size\n"
        "    mul-int/lit8 v0, v0, 0xc"
    )
    if source.count(cell_anchor) != 1:
        raise RuntimeError("Could not uniquely locate the icon-cell sizing block")
    source = source.replace(cell_anchor, cell_patch, 1)

    gap_anchor = (
        f"    iput v0, p0, {EDGE_MENU}->itemGap:I\n\n"
        "    invoke-direct {p0}, Lcom/phoneme/corebridge/EdgeMenuOverlay;->refreshPanelContentLayout()V"
    )
    gap_patch = (
        f"    iput v0, p0, {EDGE_MENU}->itemGap:I\n\n"
        f"    invoke-direct {{p0}}, {EDGE_MENU}->is320x480Display()Z\n\n"
        "    move-result v2\n\n"
        "    if-eqz v2, :edge_menu_base_icon_gap\n\n"
        f"    iget v2, p0, {EDGE_MENU}->itemGap:I\n\n"
        "    const/16 v3, 0xa\n\n"
        "    invoke-static {v2, v3}, Ljava/lang/Math;->max(II)I\n\n"
        "    move-result v2\n\n"
        f"    iput v2, p0, {EDGE_MENU}->itemGap:I\n\n"
        "    :edge_menu_base_icon_gap\n"
        "    invoke-direct {p0}, Lcom/phoneme/corebridge/EdgeMenuOverlay;->refreshPanelContentLayout()V"
    )
    if source.count(gap_anchor) != 1:
        raise RuntimeError("Could not uniquely locate the menu icon-gap block")
    source = source.replace(gap_anchor, gap_patch, 1)

    helper_anchor = ".method private installInternal("
    if source.count(helper_anchor) != 1:
        raise RuntimeError("Could not uniquely locate EdgeMenuOverlay helper insertion point")
    source = source.replace(helper_anchor, DISPLAY_HELPER + "\n" + helper_anchor, 1)
    path.write_text(source, encoding="utf-8")


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


def clone_info(info: ZipInfo) -> ZipInfo:
    cloned = ZipInfo(info.filename, info.date_time)
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


def verify_dex(name: str, data: bytes) -> None:
    if len(data) < 0x70 or data[:8] != b"dex\n035\x00":
        raise RuntimeError(f"{name} is not a complete DEX 035 file")
    if struct.unpack_from("<I", data, 32)[0] != len(data):
        raise RuntimeError(f"{name} DEX file_size does not match its payload")
    if struct.unpack_from("<I", data, 36)[0] != 0x70:
        raise RuntimeError(f"{name} DEX header size is invalid")
    if hashlib.sha1(data[32:]).digest() != data[12:32]:
        raise RuntimeError(f"{name} DEX SHA-1 signature is invalid")
    if (zlib.adler32(data[12:]) & 0xFFFFFFFF) != struct.unpack_from("<I", data, 8)[0]:
        raise RuntimeError(f"{name} DEX Adler-32 checksum is invalid")


def merge_dex_only(base_apk: Path, rebuilt_apk: Path, output_apk: Path) -> None:
    with zipfile.ZipFile(base_apk, "r") as base, zipfile.ZipFile(
        rebuilt_apk, "r"
    ) as rebuilt:
        base_names = base.namelist()
        if len(base_names) != len(set(base_names)):
            raise RuntimeError("Baseline APK contains duplicate ZIP entries")
        base_dex = {name for name in base_names if DEX_ENTRY.fullmatch(name)}
        rebuilt_dex = {name for name in rebuilt.namelist() if DEX_ENTRY.fullmatch(name)}
        if not base_dex or base_dex != rebuilt_dex:
            raise RuntimeError("Baseline and Apktool output have different DEX entries")

        for name in base_dex:
            verify_dex(f"baseline {name}", base.read(name))
            verify_dex(f"rebuilt {name}", rebuilt.read(name))

        with zipfile.ZipFile(
            output_apk, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True
        ) as output:
            for info in base.infolist():
                if is_apk_signature(info.filename):
                    continue
                payload = (
                    rebuilt.read(info.filename)
                    if DEX_ENTRY.fullmatch(info.filename)
                    else base.read(info)
                )
                output.writestr(clone_info(info), payload)

    with zipfile.ZipFile(base_apk, "r") as base, zipfile.ZipFile(
        output_apk, "r"
    ) as output:
        expected_order = [
            info.filename
            for info in base.infolist()
            if not is_apk_signature(info.filename)
        ]
        if output.namelist() != expected_order:
            raise RuntimeError("Non-signature ZIP entry order changed")
        for name in expected_order:
            before = base.read(name)
            after = output.read(name)
            if DEX_ENTRY.fullmatch(name):
                if before == after:
                    raise RuntimeError(f"{name} did not contain the EdgeSwipe patch")
                verify_dex(f"merged {name}", after)
            elif before != after:
                raise RuntimeError(f"Unexpected non-DEX payload change: {name}")


def build() -> None:
    if not BASE_APK.is_file():
        raise SystemExit(f"Missing tested v338 baseline APK: {BASE_APK}")
    if not SIGNER.is_file():
        raise SystemExit(f"Missing release signing helper: {SIGNER}")

    apktool = find_apktool()
    with tempfile.TemporaryDirectory(prefix="phoneme-v339-edge-menu-") as temp:
        work = Path(temp)
        decoded = work / "decoded"
        rebuilt = work / "rebuilt.apk"
        run([apktool, "d", "-f", "-o", str(decoded), str(BASE_APK)])
        patch_edge_menu(decoded)
        run([apktool, "b", str(decoded), "-o", str(rebuilt)])
        merge_dex_only(BASE_APK, rebuilt, UNSIGNED_APK)

    run(["python", str(SIGNER), str(UNSIGNED_APK), str(SIGNED_APK)])
    run(["jarsigner", "-verify", str(SIGNED_APK)])
    print(f"Created signed APK: {SIGNED_APK}")
    print("320x480/480x320 only: icon cell/size 28px; item gap at least 10px.")
    print("Other display dimensions, EdgeSwipe hitbox, and bar geometry remain unchanged.")


if __name__ == "__main__":
    build()