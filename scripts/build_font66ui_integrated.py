from pathlib import Path
import os
import shutil
import hashlib
import json

ROOT = Path(os.environ.get('PHONEME_ROOT', '.')).resolve()
BASE = ROOT / 'work/heap32m_grid_jar_prepend_font66_ui'
OUT = ROOT / 'work/font66ui_integrated_decode'
AUDIO_SOURCE = Path(os.environ.get('PHONEME_AUDIO_SOURCE', str(ROOT / 'work/audio_source_decoded'))).resolve()
IF63 = ROOT / 'work/inputfix63_decode'
HARD = ROOT / 'work/inputfix63_systemfont_scan'

for required in (BASE, AUDIO_SOURCE, IF63, HARD):
    if not required.exists():
        raise SystemExit(f'Missing required tree: {required}')

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(BASE, OUT)

FPM = OUT / 'smali/be/preuveneers/phoneme/fpmidp'
CRASH = OUT / 'smali/com/phoneme/crash'
CRASH.mkdir(parents=True, exist_ok=True)


def copy(src: Path, dst: Path):
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def method_block(text: str, signature: str) -> str:
    start = text.find(signature)
    if start < 0:
        raise ValueError(f'Method not found: {signature}')
    end = text.find('\n.end method', start)
    if end < 0:
        raise ValueError(f'Method terminator not found: {signature}')
    return text[start:end + len('\n.end method')]


def replace_method(text: str, signature: str, replacement: str) -> str:
    old = method_block(text, signature)
    return text.replace(old, replacement, 1)


# 1) Audio: port only the stable MediaPlayerProxy family from the
# configured audio source. This leaves Font66-UI's bitmap/font scaling, UI,
# CVM and native assets untouched.
for name in ('MediaPlayerProxy.smali', 'MediaPlayerProxy$1.smali', 'MediaPlayerProxy$2.smali'):
    copy(AUDIO_SOURCE / 'smali/be/preuveneers/phoneme/fpmidp' / name, FPM / name)

# 2) InputFix63: port the input bridge classes, but replace only the outer
# FrameBufferView input-connection methods rather than the entire renderer.
copy(IF63 / 'smali/be/preuveneers/phoneme/fpmidp/FrameBufferView$1.smali', FPM / 'FrameBufferView$1.smali')

# Keep this build script focused on renderer/font mode. InputConnection is
# intentionally not modified here: copy-paste testing proves the missing
# Vietnamese glyphs are not caused by the keyboard bridge.

copy(IF63 / 'smali/be/preuveneers/phoneme/fpmidp/FrameBufferActivity$1.smali', FPM / 'FrameBufferActivity$1.smali')

fb_path = FPM / 'FrameBufferView.smali'
fb_text = fb_path.read_text(encoding='utf-8')

# InputFix63's copied methods use both fields below. Keep the exact
# descriptor of the concrete inner connection class because resetState() is
# called on it directly; using the InputConnection interface descriptor would
# create a different unresolved field reference in DEX.
field_marker = '.field private static apiVersion:I'
if field_marker not in fb_text:
    raise ValueError('Font66-UI FrameBufferView apiVersion field not found')
if 'activeInputConnection:Lbe/preuveneers/phoneme/fpmidp/FrameBufferView$1;' not in fb_text:
    fb_text = fb_text.replace(
        field_marker,
        '.field private static activeInputConnection:Lbe/preuveneers/phoneme/fpmidp/FrameBufferView$1;\n\n' + field_marker,
        1,
    )
if '.field public static inputConnectionActive:Z' not in fb_text:
    field_after = '.field private static fbPaint:Landroid/graphics/Paint;'
    if field_after not in fb_text:
        raise ValueError('Font66-UI FrameBufferView fbPaint field not found')
    fb_text = fb_text.replace(
        field_after,
        field_after + '\n\n.field public static inputConnectionActive:Z',
        1,
    )
# Remove a stale field declaration from an earlier generated tree if the
# script is ever run against that tree instead of a fresh copy.
fb_text = fb_text.replace(
    '.field private static activeInputConnection:Landroid/view/inputmethod/InputConnection;\n\n',
    '',
    1,
)

src_fb_text = (IF63 / 'smali/be/preuveneers/phoneme/fpmidp/FrameBufferView.smali').read_text(encoding='utf-8')
fb_text = replace_method(
    fb_text,
    '.method public onCreateInputConnection(Landroid/view/inputmethod/EditorInfo;)Landroid/view/inputmethod/InputConnection;',
    method_block(src_fb_text, '.method public onCreateInputConnection(Landroid/view/inputmethod/EditorInfo;)Landroid/view/inputmethod/InputConnection;'),
)
if '.method public static resetInputConnectionState()V' not in fb_text:
    reset = method_block(src_fb_text, '.method public static resetInputConnectionState()V')
    fb_text = fb_text.rstrip() + '\n\n' + reset + '\n'
fb_path.write_text(fb_text, encoding='utf-8')

# 3) Conditional logger from the hardened InputFix63 build. It remains idle
# unless cbDebug is enabled; no manifest or application structure is changed.
copy(HARD / 'smali/com/phoneme/crash/CrashLogger.smali', CRASH / 'CrashLogger.smali')
copy(HARD / 'smali/com/phoneme/crash/CrashLogger$1.smali', CRASH / 'CrashLogger$1.smali')

pme_path = FPM / 'PhoneMEActivity.smali'
pme_text = pme_path.read_text(encoding='utf-8')
needle = '    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V\n'
install = needle + '\n    invoke-static {p0}, Lcom/phoneme/crash/CrashLogger;->install(Landroid/content/Context;)V\n'
if 'Lcom/phoneme/crash/CrashLogger;->install' not in pme_text:
    if needle not in pme_text:
        raise ValueError('PhoneMEActivity onCreate super call not found')
    pme_text = pme_text.replace(needle, install, 1)
pme_path.write_text(pme_text, encoding='utf-8')

# 4) Make the existing bitmap-font preference listener real. The class already
# implements OnSharedPreferenceChangeListener and has the correct callback, but
# the old tree never registered it. Register/unregister only the listener; the
# native setBitmapFonts(true/false) path remains unchanged, so the two modes are
# never mixed and system-font rendering can receive the full Unicode string.
act_path = FPM / 'FrameBufferActivity.smali'
act_text = act_path.read_text(encoding='utf-8')

# Do not apply font mode inside onCreate before runMidlet(). The
# intent registers v0/v1/v2 are still holding jad/jar/mainClass at that
# point; inserting PreferenceManager/setBitmapFonts there corrupts the
# runMidlet argument types and crashes on launch. The safe application points
# remain onStart and onSharedPreferenceChanged below.

start_sig = '.method protected onStart()V'
start_method = method_block(act_text, start_sig)
register_anchor = (
    '    invoke-static {v0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;\n\n'
    '    move-result-object v0\n'
)
register_call = register_anchor + (
    '\n    invoke-interface {v0, p0}, Landroid/content/SharedPreferences;->registerOnSharedPreferenceChangeListener(Landroid/content/SharedPreferences$OnSharedPreferenceChangeListener;)V\n'
)
if '->registerOnSharedPreferenceChangeListener' not in start_method:
    if register_anchor not in start_method:
        raise ValueError('FrameBufferActivity onStart SharedPreferences anchor not found')
    start_method = start_method.replace(register_anchor, register_call, 1)
act_text = replace_method(act_text, start_sig, start_method)

stop_sig = '.method public onStop()V'
stop_method = method_block(act_text, stop_sig)
if '->unregisterOnSharedPreferenceChangeListener' not in stop_method:
    stop_anchor = '    .prologue\n'
    unregister = stop_anchor + (
        '\n    invoke-virtual {p0}, Lbe/preuveneers/phoneme/fpmidp/FrameBufferActivity;->getBaseContext()Landroid/content/Context;\n\n'
        '    move-result-object v0\n\n'
        '    invoke-static {v0}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;\n\n'
        '    move-result-object v0\n\n'
        '    invoke-interface {v0, p0}, Landroid/content/SharedPreferences;->unregisterOnSharedPreferenceChangeListener(Landroid/content/SharedPreferences$OnSharedPreferenceChangeListener;)V\n'
    )
    if stop_anchor not in stop_method:
        raise ValueError('FrameBufferActivity onStop prologue not found')
    stop_method = stop_method.replace(stop_anchor, unregister, 1)
act_text = replace_method(act_text, stop_sig, stop_method)

# Apply the saved font mode immediately before the VM starts, but use only
# scratch registers v6-v8. At this point v0/v1/v2 contain mainClass/jar/jad
# and must remain untouched for runMidlet(). This is intentionally the only
# early font-mode call; the listener/onStart path remains for later changes.
create_sig = '.method public onCreate(Landroid/os/Bundle;)V'
create_method = method_block(act_text, create_sig)
run_anchor = '    invoke-virtual {p0, v2, v1, v0}, Lbe/preuveneers/phoneme/fpmidp/FrameBufferActivity;->runMidlet(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V\n'
if ':font_mode_before_vm_done' not in create_method:
    if run_anchor not in create_method:
        raise ValueError('FrameBufferActivity runMidlet anchor not found for safe font-mode application')
    early_font = (
        '    invoke-virtual {p0}, Lbe/preuveneers/phoneme/fpmidp/FrameBufferActivity;->getBaseContext()Landroid/content/Context;\n\n'
        '    move-result-object v8\n\n'
        '    invoke-static {v8}, Landroid/preference/PreferenceManager;->getDefaultSharedPreferences(Landroid/content/Context;)Landroid/content/SharedPreferences;\n\n'
        '    move-result-object v8\n\n'
        '    const-string v7, "cbBitmapFonts"\n\n'
        '    const/4 v6, 0x0\n\n'
        '    invoke-interface {v8, v7, v6}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z\n\n'
        '    move-result v8\n\n'
        '    sget-object v7, Lbe/preuveneers/phoneme/fpmidp/FrameBufferActivity;->fbView:Lbe/preuveneers/phoneme/fpmidp/FrameBufferView;\n\n'
        '    if-eqz v7, :font_mode_before_vm_done\n\n'
        '    invoke-virtual {v7, v8}, Lbe/preuveneers/phoneme/fpmidp/FrameBufferView;->setBitmapFonts(Z)V\n\n'
        '    :font_mode_before_vm_done\n\n'
    )
    create_method = create_method.replace(run_anchor, early_font + run_anchor, 1)
act_text = replace_method(act_text, create_sig, create_method)
act_path.write_text(act_text, encoding='utf-8')

# 5) Minimal showSoftInput hardening. The method is replaced only after the
# exact guard anchor is found, so a structural mismatch aborts instead of
# silently corrupting the smali.
act_text = act_path.read_text(encoding='utf-8')
show_sig = '.method public showSoftInput()V'
show = method_block(act_text, show_sig)
if ':show_soft_input_return' not in show:
    anchor = '    const/4 v7, 0x0\n'
    if anchor not in show:
        raise ValueError('Font66-UI showSoftInput register anchor not found')
    guard = (
        anchor + '\n'
        '    sget-object v6, Lbe/preuveneers/phoneme/fpmidp/FrameBufferActivity;->fbView:Lbe/preuveneers/phoneme/fpmidp/FrameBufferView;\n'
        '    if-eqz v6, :show_soft_input_return\n\n'
        '    invoke-virtual {v6}, Landroid/view/View;->getWindowToken()Landroid/os/IBinder;\n'
        '    move-result-object v5\n'
        '    if-eqz v5, :show_soft_input_return\n'
    )
    show = show.replace(anchor, guard, 1)
    show = show.replace(
        '    check-cast v0, Landroid/view/inputmethod/InputMethodManager;\n',
        '    check-cast v0, Landroid/view/inputmethod/InputMethodManager;\n\n'
        '    if-eqz v0, :show_soft_input_return\n',
        1,
    )
    # Put the return label immediately before the existing return-void. This
    # avoids depending on source line numbers that vary between builds.
    ret = '    return-void\n'
    pos = show.rfind(ret)
    if pos < 0:
        raise ValueError('showSoftInput return-void not found')
    show = show[:pos] + '    :show_soft_input_return\n' + show[pos:]
act_text = replace_method(act_text, show_sig, show)
act_path.write_text(act_text, encoding='utf-8')

# 6) Surface lifecycle guards. These are deliberately narrow and do not alter
# Font66 rendering methods or bitmap font calculations.
fb_text = fb_path.read_text(encoding='utf-8')
sc_sig = '.method public surfaceChanged(Landroid/view/SurfaceHolder;III)V'
sc = method_block(fb_text, sc_sig)
if ':surface_changed_return' not in sc:
    target = '    sget-object v1, Lbe/preuveneers/phoneme/fpmidp/FrameBufferView;->fbBitmap:Landroid/graphics/Bitmap;\n\n    monitor-enter v1\n'
    if target not in sc:
        raise ValueError('Font66-UI surfaceChanged bitmap anchor not found')
    sc = sc.replace(
        target,
        '    sget-object v1, Lbe/preuveneers/phoneme/fpmidp/FrameBufferView;->fbBitmap:Landroid/graphics/Bitmap;\n\n    if-eqz v1, :surface_changed_return\n\n    monitor-enter v1\n',
        1,
    )
    activity_target = (
        '    move-result-object v0\n\n'
        '    const/16 v2, 0x15\n\n'
        '    invoke-virtual {v0, v2}, Lbe/preuveneers/phoneme/fpmidp/FrameBufferActivity;->keyboardEvent(C)V\n'
    )
    if activity_target in sc:
        sc = sc.replace(
            activity_target,
            '    move-result-object v0\n\n'
            '    if-eqz v0, :surface_changed_return\n\n'
            '    const/16 v2, 0x15\n\n'
            '    invoke-virtual {v0, v2}, Lbe/preuveneers/phoneme/fpmidp/FrameBufferActivity;->keyboardEvent(C)V\n',
            1,
        )
    ret = '    return-void\n'
    pos = sc.rfind(ret)
    if pos < 0:
        raise ValueError('surfaceChanged return-void not found')
    sc = sc[:pos] + '    :surface_changed_return\n' + sc[pos:]
fb_text = replace_method(fb_text, sc_sig, sc)

cr_sig = '.method public surfaceCreated(Landroid/view/SurfaceHolder;)V'
cr = method_block(fb_text, cr_sig)
if ':surface_created_return' not in cr:
    activity_target = (
        '    invoke-static {}, Lbe/preuveneers/phoneme/fpmidp/FrameBufferActivity;->getInstance()Lbe/preuveneers/phoneme/fpmidp/FrameBufferActivity;\n\n'
        '    move-result-object v0\n\n'
        '    const-string v1, "window"\n'
    )
    if activity_target not in cr:
        raise ValueError('Font66-UI surfaceCreated Activity anchor not found')
    cr = cr.replace(
        activity_target,
        '    invoke-static {}, Lbe/preuveneers/phoneme/fpmidp/FrameBufferActivity;->getInstance()Lbe/preuveneers/phoneme/fpmidp/FrameBufferActivity;\n\n'
        '    move-result-object v0\n\n'
        '    if-eqz v0, :surface_created_return\n\n'
        '    const-string v1, "window"\n',
        1,
    )
    wm_target = (
        '    move-result-object v0\n\n'
        '    invoke-interface {v0}, Landroid/view/WindowManager;->getDefaultDisplay()Landroid/view/Display;\n'
    )
    if wm_target in cr:
        cr = cr.replace(
            wm_target,
            '    move-result-object v0\n\n'
            '    if-eqz v0, :surface_created_return\n\n'
            '    invoke-interface {v0}, Landroid/view/WindowManager;->getDefaultDisplay()Landroid/view/Display;\n',
            1,
        )
    ret = '    return-void\n'
    pos = cr.rfind(ret)
    if pos < 0:
        raise ValueError('surfaceCreated return-void not found')
    cr = cr[:pos] + '    :surface_created_return\n' + cr[pos:]
fb_text = replace_method(fb_text, cr_sig, cr)

# Fail closed if any copied method still references the old interface descriptor
if '->registerOnSharedPreferenceChangeListener' not in act_text:
    raise ValueError('Preferences listener registration was not applied')
if '->unregisterOnSharedPreferenceChangeListener' not in act_text:
    raise ValueError('Preferences listener unregistration was not applied')

# or the boolean field was not declared. Apktool can assemble unresolved field
# references, so these checks must happen before the build step.
required_field_decls = (
    '.field private static activeInputConnection:Lbe/preuveneers/phoneme/fpmidp/FrameBufferView$1;',
    '.field public static inputConnectionActive:Z',
)
for decl in required_field_decls:
    if decl not in fb_text:
        raise ValueError(f'Missing required FrameBufferView field: {decl}')
if 'activeInputConnection:Landroid/view/inputmethod/InputConnection;' in fb_text:
    raise ValueError('Stale activeInputConnection interface descriptor remains')

fb_path.write_text(fb_text, encoding='utf-8')

# Record exact changed files and base invariants for later verification.
tracked = [
    FPM / 'MediaPlayerProxy.smali', FPM / 'MediaPlayerProxy$1.smali', FPM / 'MediaPlayerProxy$2.smali',
    FPM / 'FrameBufferView.smali', FPM / 'FrameBufferView$1.smali', FPM / 'FrameBufferActivity$1.smali',
    FPM / 'FrameBufferActivity.smali', FPM / 'PhoneMEActivity.smali',
    CRASH / 'CrashLogger.smali', CRASH / 'CrashLogger$1.smali',
]
manifest = {str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
(OUT / 'integration_manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(f'Created Font66-UI integrated decode: {OUT}')
print(f'Files tracked: {len(manifest)}')
print('Font66/UI renderer and assets remain from the Font66-UI base; only audio/input/logger/lifecycle classes were changed.')
