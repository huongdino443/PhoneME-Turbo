#!/usr/bin/env python3
"""Patch a decoded PhoneME tree with WakeLock/WifiLock lifecycle handling.

Usage:
  python3 apply_network_keepalive.py --tree path/to/decoded-tree

The script changes only PhoneMEMonitorService.smali and AndroidManifest.xml.
It does not build, align, sign, or upload an APK.
"""

from __future__ import annotations

import argparse
from pathlib import Path

PACKAGE = "be/preuveneers/phoneme/fpmidp"
SERVICE_REL = Path("smali") / PACKAGE / "PhoneMEMonitorService.smali"
MANIFEST_REL = Path("AndroidManifest.xml")

ACQUIRE = r'''
.method private acquireNetworkLocks()V
    .locals 4

    sget-object v0, Lbe/preuveneers/phoneme/fpmidp/PhoneMEMonitorService;->wakeLock:Landroid/os/PowerManager$WakeLock;
    if-nez v0, :cond_wifi
    const-string v0, "power"
    invoke-virtual {p0, v0}, Lbe/preuveneers/phoneme/fpmidp/PhoneMEMonitorService;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;
    move-result-object v0
    check-cast v0, Landroid/os/PowerManager;
    if-eqz v0, :cond_wifi
    const/4 v1, 0x1
    const-string v2, "PhoneME:Game"
    invoke-virtual {v0, v1, v2}, Landroid/os/PowerManager;->newWakeLock(ILjava/lang/String;)Landroid/os/PowerManager$WakeLock;
    move-result-object v0
    sput-object v0, Lbe/preuveneers/phoneme/fpmidp/PhoneMEMonitorService;->wakeLock:Landroid/os/PowerManager$WakeLock;
    const/4 v1, 0x0
    invoke-virtual {v0, v1}, Landroid/os/PowerManager$WakeLock;->setReferenceCounted(Z)V
    invoke-virtual {v0}, Landroid/os/PowerManager$WakeLock;->acquire()V

    :cond_wifi
    sget-object v0, Lbe/preuveneers/phoneme/fpmidp/PhoneMEMonitorService;->wifiLock:Landroid/net/wifi/WifiManager$WifiLock;
    if-nez v0, :cond_done
    const-string v0, "wifi"
    invoke-virtual {p0, v0}, Lbe/preuveneers/phoneme/fpmidp/PhoneMEMonitorService;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;
    move-result-object v0
    check-cast v0, Landroid/net/wifi/WifiManager;
    if-eqz v0, :cond_done
    const/4 v1, 0x1
    const-string v2, "PhoneME:Game"
    invoke-virtual {v0, v1, v2}, Landroid/net/wifi/WifiManager;->createWifiLock(ILjava/lang/String;)Landroid/net/wifi/WifiManager$WifiLock;
    move-result-object v0
    sput-object v0, Lbe/preuveneers/phoneme/fpmidp/PhoneMEMonitorService;->wifiLock:Landroid/net/wifi/WifiManager$WifiLock;
    const/4 v1, 0x0
    invoke-virtual {v0, v1}, Landroid/net/wifi/WifiManager$WifiLock;->setReferenceCounted(Z)V
    invoke-virtual {v0}, Landroid/net/wifi/WifiManager$WifiLock;->acquire()V

    :cond_done
    return-void
.end method
'''

RELEASE = r'''
.method private releaseNetworkLocks()V
    .locals 2

    sget-object v0, Lbe/preuveneers/phoneme/fpmidp/PhoneMEMonitorService;->wifiLock:Landroid/net/wifi/WifiManager$WifiLock;
    if-eqz v0, :cond_wifi_done
    invoke-virtual {v0}, Landroid/net/wifi/WifiManager$WifiLock;->isHeld()Z
    move-result v1
    if-eqz v1, :cond_wifi_clear
    invoke-virtual {v0}, Landroid/net/wifi/WifiManager$WifiLock;->release()V
    :cond_wifi_clear
    const/4 v1, 0x0
    sput-object v1, Lbe/preuveneers/phoneme/fpmidp/PhoneMEMonitorService;->wifiLock:Landroid/net/wifi/WifiManager$WifiLock;

    :cond_wifi_done
    sget-object v0, Lbe/preuveneers/phoneme/fpmidp/PhoneMEMonitorService;->wakeLock:Landroid/os/PowerManager$WakeLock;
    if-eqz v0, :cond_done
    invoke-virtual {v0}, Landroid/os/PowerManager$WakeLock;->isHeld()Z
    move-result v1
    if-eqz v1, :cond_clear
    invoke-virtual {v0}, Landroid/os/PowerManager$WakeLock;->release()V
    :cond_clear
    const/4 v1, 0x0
    sput-object v1, Lbe/preuveneers/phoneme/fpmidp/PhoneMEMonitorService;->wakeLock:Landroid/os/PowerManager$WakeLock;

    :cond_done
    return-void
.end method
'''


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tree", type=Path, required=True,
                        help="decoded APK directory")
    return parser.parse_args()


def patch_service(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "->wakeLock:Landroid/os/PowerManager$WakeLock;" in text:
        return False
    field_marker = ".field private static timertask:Ljava/util/TimerTask;"
    if field_marker not in text:
        raise RuntimeError(f"service field marker not found: {path}")
    text = text.replace(
        field_marker,
        field_marker + "\n\n.field private static wakeLock:Landroid/os/PowerManager$WakeLock;\n\n.field private static wifiLock:Landroid/net/wifi/WifiManager$WifiLock;",
        1,
    )
    on_bind = "\n.method public onBind("
    if on_bind not in text:
        raise RuntimeError(f"onBind marker not found: {path}")
    text = text.replace(on_bind, ACQUIRE + on_bind, 1)

    create_marker = "    :cond_0\n    new-instance v0, Landroid/app/Notification;"
    create_replacement = "    :cond_0\n    invoke-direct {p0}, Lbe/preuveneers/phoneme/fpmidp/PhoneMEMonitorService;->acquireNetworkLocks()V\n\n    new-instance v0, Landroid/app/Notification;"
    if create_marker not in text:
        raise RuntimeError(f"onCreate insertion marker not found: {path}")
    text = text.replace(create_marker, create_replacement, 1)

    destroy_marker = "    .line 132\n    :cond_0\n    const/4 v0, 0x1\n"
    destroy_replacement = "    .line 132\n    :cond_0\n    invoke-direct {p0}, Lbe/preuveneers/phoneme/fpmidp/PhoneMEMonitorService;->releaseNetworkLocks()V\n\n    const/4 v0, 0x1\n"
    if destroy_marker not in text:
        raise RuntimeError(f"onDestroy insertion marker not found: {path}")
    text = text.replace(destroy_marker, destroy_replacement, 1)
    text += RELEASE
    path.write_text(text, encoding="utf-8")
    return True


def patch_manifest(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    additions = [
        '    <uses-permission android:name="android.permission.WAKE_LOCK"/>',
        '    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>',
        '    <uses-permission android:name="android.permission.CHANGE_WIFI_STATE"/>',
    ]
    marker = '    <uses-permission android:name="android.permission.INTERNET"/>\n'
    if marker not in text:
        raise RuntimeError(f"INTERNET permission marker not found: {path}")
    changed = False
    for line in additions:
        if line not in text:
            text = text.replace(marker, marker + line + "\n", 1)
            changed = True
    path.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    parsed = args()
    tree = parsed.tree.resolve()
    service = tree / SERVICE_REL
    manifest = tree / MANIFEST_REL
    if not service.is_file() or not manifest.is_file():
        raise SystemExit("decoded tree does not contain the expected PhoneME files")
    changed_service = patch_service(service)
    changed_manifest = patch_manifest(manifest)
    print(f"service_changed={changed_service}")
    print(f"manifest_changed={changed_manifest}")
    print("Next steps: rebuild with apktool, zipalign, sign privately, then verify with apksigner.")


if __name__ == "__main__":
    main()
