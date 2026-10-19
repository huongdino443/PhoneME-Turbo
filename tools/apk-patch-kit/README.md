# PhoneME Turbo community APK patch kit

A small set of APK-level utilities and one carefully scoped PhoneME Turbo patch. This is not the full PhoneME Turbo source tree.

## Included files

- apk_zipalign.py — aligns uncompressed ZIP entries on 4-byte boundaries, verifies the result, and checks that payloads and entry order remain unchanged.
- sign_apk_test.py — creates a temporary one-day test certificate with OpenSSL, signs the APK with JAR/v1 signing, and removes the temporary private key when it exits.
- patch_romized_mmapi.py — narrowly patches the ROMized JSR-135 dispatch in PhoneME Turbo so HTTP MP3 URLs containing a query string can use the existing Android media-player path.

## Requirements

- Python 3.
- OpenSSL and jarsigner are required only for temporary test signing / verification.
- Android SDK Build Tools zipalign is recommended for an independent final alignment check.

## Example: test the ROMized MP3 URL patch

Use a copy of an APK. The patcher validates a 32-bit ARM ELF, the ROMized Manager method descriptor, its length, and the exact original bytecode sequence; it stops if the expected structure is absent or ambiguous.

```sh
python3 tools/apk-patch-kit/patch_romized_mmapi.py input.apk patched-unsigned.apk
python3 tools/apk-patch-kit/apk_zipalign.py patched-unsigned.apk patched-aligned.apk
python3 tools/apk-patch-kit/sign_apk_test.py patched-aligned.apk patched-test.apk
jarsigner -verify -verbose patched-test.apk
```

The native patch was smoke-tested against both PhoneME Turbo 1.2.4 variants (standard and API 8). That is not a guarantee for every PhoneME build, ABI, game, or URL. Keep the original APK and test on-device before relying on a patched build.

## Test-signing warning

The generated certificate is temporary and is not PhoneME Turbo's release identity. A test-signed APK cannot update an installation signed with the official release key. Do not distribute it as an official release. To publish a release build, sign it with your own release key using your own protected signing workflow; no release key or password is included here.

## Scope and licenses

These tools operate on APK files; they do not provide the complete upstream PhoneME source, CVM build system, ROMizer, games, or game JARs. The native patch changes only the validated byte sequence and bumps foundation/build.revision so the wrapper redeploys the changed asset. See the repository NOTICE and upstream/component licenses before redistributing modified software.