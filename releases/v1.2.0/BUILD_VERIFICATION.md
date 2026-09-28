# Build verification

## Result

- Android package: `be.preuveneers.phoneme.fpmidp`
- Version name/code: `1.2.0` / `10`
- Final APK: `PhoneME-Turbo-1.2.0.apk`
- Final APK SHA-256: `51a83ec158dbcf38ddbab4e3e9ca73d60519a57180917b80a2a626e7272bd55a`
- v340 unsigned input SHA-256: `873ecb86ba414b34183c35178c2a7465c220eed46a79d027ef23afad055c144c`
- Generated unsigned 1.2.0 APK SHA-256: `a75d2b821939066de403ac1014b920370c7fcd3411d7aaec7f500cc7ce5f6279`
- Release signer SHA-256: `1C:7E:35:CC:46:1E:96:1C:CA:67:5B:E8:C2:33:05:91:11:D4:75:59:0A:4E:01:55:E3:77:A9:CB:86:6B:A0:17`

## Checks performed

- Rebuilt the unsigned APK using the release-bundle copy of
  `v120-public-release.py`; the output matched the original unsigned build
  byte-for-byte.
- Compared the v340 input and the unsigned 1.2.0 output: only
  `AndroidManifest.xml` changed. The other 261 ZIP entries, including DEX,
  resources, foundation assets, and native library, were preserved.
- Confirmed package identity and version metadata after decoding the final APK.
- Confirmed ZIP integrity and `jarsigner` signature verification. The
  certificate is self-signed, so Java reports trust-chain and timestamp
  warnings; the signature verifies and the fingerprint matches the included
  public certificate.
- Confirmed the final APK signer differs from the canonical 1.1.2 reference
  signer. See the update warning in `README.md`.

The v340 baseline was user-approved. The version-only 1.2.0 build was not
installed on a physical device as a separate test.