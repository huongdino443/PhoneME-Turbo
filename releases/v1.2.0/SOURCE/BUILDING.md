# Rebuilding the 1.2.0 metadata package

This source folder contains the unsigned v340 APK used as the build input and
the script that changes its Android version metadata to 1.2.0. It also includes
the patch scripts relevant to the v337–v340 lineage for inspection.

From this directory, create the unsigned 1.2.0 APK with:

```sh
python3 tools/v120-public-release.py \
  v340-base-unsigned.apk \
  PhoneME-Turbo-1.2.0-unsigned.apk
```

Requirements: Python 3 and Apktool 2.x. The script verifies that the input is
the expected v340 baseline, preserves all non-manifest payloads, and refuses
to complete if DEX changes during the metadata build.

The private release key is not included. Signing is a separate operation and
must use a release key controlled by the project owner. The already signed
release APK is at the root of this bundle.

The patch scripts document APK-level changes; they do not rebuild the original
Turbo CVM, ROMized classes, or native libraries from upstream source.