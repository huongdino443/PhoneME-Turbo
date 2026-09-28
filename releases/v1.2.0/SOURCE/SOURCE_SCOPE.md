# Source and provenance scope

## Included

- `v340-base-unsigned.apk`: the exact unsigned APK input for this release's
  metadata-only version update.
- `tools/v120-public-release.py`: rebuilds the unsigned APK with version name
  `1.2.0` and version code `10`, preserving the v340 DEX and all other
  non-manifest payloads.
- `lineage-tools/`: selected v337–v340 APK patch scripts for provenance and
  review.

## Not included

The workspace is an APK-level patch and recovery workspace, not a complete
upstream PhoneME Turbo source tree. It does not include the complete Turbo CVM,
ROMizer, native build system, or all historical inputs needed to reproduce v340
from the original 1.1.2 binary. The included patch scripts are not a complete
from-source rebuild recipe.

The 1.1.2 comparison reference was the historical device-oriented
`PhoneME-Turbo-nHD-v112.2.apk` inside the private workspace input bundle.
The current product name is PhoneME Turbo; the historical nHD label is retained
only for provenance.
Its SHA-256 was
`51e60854b35955e0ce30bbd4e2cfd699c7da575b858127cd7f966075ec5d9aec`; the
reference APK itself is intentionally not redistributed in this release ZIP.

The source handoff archives were inspected but not embedded wholesale. They
contain historical APKs, third-party game samples, reference applications,
logs, screenshots, and unrelated experiments. Private signing-key files and
key-containing archives were excluded.