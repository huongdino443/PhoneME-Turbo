# Public release checklist

## Prepared

- [x] Set Android version name to `1.2.0`.
- [x] Advance Android version code to `10`.
- [x] Keep the requested APK filename: `PhoneME-Turbo-1.2.0.apk`.
- [x] Sign with the existing PhoneME Turbo release certificate.
- [x] Include the public certificate and its SHA-256 fingerprint.
- [x] Include major-change notes, source-scope notes, and bundled upstream
  notices.
- [x] Exclude private keys, old handoff archives, test/game APKs, game samples,
  logs, and screenshots.

## Before publishing

- [ ] Review the embedded PhoneME and third-party license notices and confirm
  that the available source materials satisfy the applicable redistribution
  terms. The workspace does not contain the complete upstream Turbo CVM/native
  build source.
- [ ] Confirm rights to use the PhoneME Turbo name, artwork, and any included
  assets for the intended distribution.
- [ ] Decide how to communicate the signing-certificate change for people
  upgrading from the canonical 1.1.2 reference; they must uninstall that build
  first, which can remove app-private data.
- [ ] Perform any additional clean-install/device testing required for the
  specific Android versions and screen sizes you intend to support.

The source handoff ZIPs were not copied into this release archive wholesale:
they contain old/reference APKs, game samples, screenshots, logs, and other
historical material that is not appropriate for a public binary release.