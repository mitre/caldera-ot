# -*- mode: python ; coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# PyInstaller spec: bundle s7comm_cli into a single executable, including the
# native libsnap7 shared library that python-snap7 loads at runtime.
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = [], [], []
for pkg in ("snap7",):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

block_cipher = None

a = Analysis(
    ["s7comm_cli.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
    name="s7comm_cli",
    debug=False, bootloader_ignore_signals=False, strip=False, upx=False,
    console=True, disable_windowed_traceback=False,
    target_arch=None, codesign_identity=None, entitlements_file=None,
)
