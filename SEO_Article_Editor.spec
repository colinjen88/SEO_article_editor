# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['SEO_Article_Editor.py'],
    pathex=['src'],
    binaries=[],
    datas=[('templates', 'templates')],
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.filedialog', 'tkinter.messagebox', '_tkinter', 'ttkbootstrap'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['tk_rthook.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SEO_Article_Editor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
