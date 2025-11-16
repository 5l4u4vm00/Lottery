#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包腳本 - 用於將抽籤系統打包成可執行文件
支援 Windows 和 Linux 平台
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def check_pyinstaller():
    """檢查 PyInstaller 是否已安裝"""
    try:
        import PyInstaller
        print("✓ PyInstaller 已安裝")
        return True
    except ImportError:
        print("✗ PyInstaller 未安裝")
        print("正在安裝 PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller 安裝成功")
            return True
        except subprocess.CalledProcessError:
            print("✗ PyInstaller 安裝失敗")
            return False


def clean_build_dirs():
    """清理舊的構建目錄"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目錄: {dir_name}")
            shutil.rmtree(dir_name)

    # 清理 .spec 文件
    spec_files = list(Path('.').glob('*.spec'))
    for spec_file in spec_files:
        print(f"刪除文件: {spec_file}")
        spec_file.unlink()


def create_spec_file():
    """創建 PyInstaller spec 文件"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['lottery_system.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='聖誕抽籤系統',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不顯示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
"""

    with open('lottery_system.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print("✓ 已創建 spec 文件")


def build_executable():
    """構建可執行文件"""
    print("\n開始打包...")
    print("=" * 60)

    # 使用 spec 文件構建
    cmd = [
        'pyinstaller',
        '--clean',
        'lottery_system.spec'
    ]

    try:
        subprocess.check_call(cmd)
        print("=" * 60)
        print("✓ 打包成功!")
        return True
    except subprocess.CalledProcessError as e:
        print("=" * 60)
        print(f"✗ 打包失敗: {e}")
        return False


def copy_additional_files():
    """複製額外的文件到 dist 目錄"""
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("✗ dist 目錄不存在")
        return

    # 要複製的文件列表
    files_to_copy = [
        'README.md',
        'INSTALL.md',
        '使用範例.md',
        '聖誕主題UI說明.md',
        '關鍵字抽籤功能說明.md',
    ]

    print("\n複製文檔文件...")
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, dist_dir / file_name)
            print(f"✓ 已複製: {file_name}")

    # 創建空的數據文件（示例）
    sample_files = {
        'participants.json': '[]',
        'keywords.json': '[]',
        'lottery_history.json': '[]',
        'keyword_lottery_history.json': '[]',
    }

    print("\n創建示例數據文件...")
    for file_name, content in sample_files.items():
        with open(dist_dir / file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已創建: {file_name}")


def create_archive():
    """創建壓縮包"""
    import platform

    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("✗ dist 目錄不存在")
        return

    system = platform.system()
    if system == 'Windows':
        archive_name = '聖誕抽籤系統_Windows'
        ext = 'zip'
    elif system == 'Linux':
        archive_name = '聖誕抽籤系統_Linux'
        ext = 'tar.gz'
    else:
        archive_name = '聖誕抽籤系統'
        ext = 'zip'

    print(f"\n創建壓縮包: {archive_name}.{ext}")

    try:
        if ext == 'zip':
            shutil.make_archive(archive_name, 'zip', 'dist')
        else:
            shutil.make_archive(archive_name, 'gztar', 'dist')

        print(f"✓ 壓縮包創建成功: {archive_name}.{ext}")
    except Exception as e:
        print(f"✗ 壓縮包創建失敗: {e}")


def main():
    """主函數"""
    print("🎄 聖誕抽籤系統打包工具 🎁")
    print("=" * 60)

    # 檢查 PyInstaller
    if not check_pyinstaller():
        print("\n請手動安裝 PyInstaller:")
        print("  pip install pyinstaller")
        return

    # 清理舊的構建
    print("\n清理舊的構建文件...")
    clean_build_dirs()

    # 創建 spec 文件
    print("\n創建打包配置...")
    create_spec_file()

    # 構建可執行文件
    if not build_executable():
        print("\n打包失敗,請檢查錯誤信息")
        return

    # 複製額外文件
    copy_additional_files()

    # 創建壓縮包
    create_archive()

    print("\n" + "=" * 60)
    print("🎉 打包完成!")
    print("\n輸出位置:")
    print(f"  - 可執行文件: dist/聖誕抽籤系統")
    print(f"  - 壓縮包: 聖誕抽籤系統_{sys.platform}")
    print("\n使用說明:")
    print("  1. 將 dist 目錄中的所有文件複製到目標電腦")
    print("  2. 雙擊運行'聖誕抽籤系統'可執行文件")
    print("  3. 首次運行會創建必要的配置文件")
    print("=" * 60)


if __name__ == '__main__':
    main()
