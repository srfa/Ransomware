# -*- mode: python -*-

block_cipher = None

a = Analysis(['srfa.py'],
             pathex=['/root/Desktop/Ransomware/final'],
             binaries=[],
             datas=[],
             hiddenimports=['PIL._tkinter_finder'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('skull.png','/root/Desktop/Ransomware/final/skull.png', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='srfa',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
