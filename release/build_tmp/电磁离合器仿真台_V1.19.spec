# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/Administrator/Desktop/DocumentEdit/电磁离合器/仿真模型/release/app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/Administrator/Desktop/DocumentEdit/电磁离合器/仿真模型/release/app.html', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
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
    name='电磁离合器仿真台_V1.19',
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
    icon=['C:/Users/Administrator/Desktop/DocumentEdit/电磁离合器/仿真模型/release/assets/icon.ico'],
)
