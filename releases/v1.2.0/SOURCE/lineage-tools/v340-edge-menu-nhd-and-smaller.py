#!/usr/bin/env python3
"""Extend the v339 EdgeSwipe icon treatment through nHD and smaller displays."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


BASE_APK = Path("build/v339-v338-edge-menu-320x480-release-signed.apk")
UNSIGNED_APK = Path("build/v340-v339-edge-menu-nhd-and-smaller-unsigned.apk")
SIGNED_APK = Path("build/v340-v339-edge-menu-nhd-and-smaller-release-signed.apk")
SIGNER = Path("tools/sign_apk_release.py")
BUILD_HELPERS = Path(__file__).with_name("v339-edge-menu-320x480.py")
EDGE_MENU = "Lcom/phoneme/corebridge/EdgeMenuOverlay;"

NHD_SIZE_METHOD = """\
.method private isNhdOrSmallerDisplay()Z
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

    move v3, v1

    invoke-static {v1, v2}, Ljava/lang/Math;->min(II)I

    move-result v1

    invoke-static {v3, v2}, Ljava/lang/Math;->max(II)I

    move-result v2

    const/16 v3, 0x168

    if-gt v1, v3, :edge_menu_not_nhd_or_smaller

    const/16 v3, 0x280

    if-gt v2, v3, :edge_menu_not_nhd_or_smaller

    const/4 v0, 0x1

    return v0

    :edge_menu_not_nhd_or_smaller
    const/4 v0, 0x0

    return v0
.end method
"""


def load_build_helpers():
    spec = importlib.util.spec_from_file_location("v339_edge_menu_build_helpers", BUILD_HELPERS)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load APK build helpers: {BUILD_HELPERS}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def patch_resolution_gate(decoded: Path, helpers) -> None:
    path = decoded / helpers.EDGE_MENU_PATH
    source = path.read_text(encoding="utf-8")
    old_call = "->is320x480Display()Z"
    new_call = "->isNhdOrSmallerDisplay()Z"
    if source.count(old_call) != 3 or new_call in source:
        raise RuntimeError("Expected the three v339 resolution-gate call sites")

    source = source.replace(old_call, new_call)
    source = helpers.replace_method(
        source,
        ".method private is320x480Display()Z",
        NHD_SIZE_METHOD,
    )
    if old_call in source or ".method private is320x480Display()Z" in source:
        raise RuntimeError("The old exact-resolution gate remains in the class")
    path.write_text(source, encoding="utf-8")


def build() -> None:
    if not BASE_APK.is_file():
        raise SystemExit(f"Missing signed v339 baseline APK: {BASE_APK}")
    if not SIGNER.is_file():
        raise SystemExit(f"Missing release signing helper: {SIGNER}")

    helpers = load_build_helpers()
    apktool = helpers.find_apktool()
    with tempfile.TemporaryDirectory(prefix="phoneme-v340-edge-menu-") as temp:
        work = Path(temp)
        decoded = work / "decoded"
        rebuilt = work / "rebuilt.apk"
        helpers.run([apktool, "d", "-f", "-o", str(decoded), str(BASE_APK)])
        patch_resolution_gate(decoded, helpers)
        helpers.run([apktool, "b", str(decoded), "-o", str(rebuilt)])
        helpers.merge_dex_only(BASE_APK, rebuilt, UNSIGNED_APK)

    helpers.run([sys.executable, str(SIGNER), str(UNSIGNED_APK), str(SIGNED_APK)])
    helpers.run(["jarsigner", "-verify", str(SIGNED_APK)])
    print(f"Created signed APK: {SIGNED_APK}")
    print("The 28px icon/cell and 10px gap rules apply when short edge <= 360")
    print("and long edge <= 640. Other displays retain the original v338 formula.")


if __name__ == "__main__":
    build()