@echo off
REM 打包腳本 - Windows 版本
chcp 65001 > nul

echo 🎄 聖誕抽籤系統打包工具 🎁
echo ======================================

REM 檢查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 找不到 Python，請先安裝 Python
    pause
    exit /b 1
)

REM 激活虛擬環境（如果存在）
if exist ".venv\Scripts\activate.bat" (
    echo 激活虛擬環境...
    call .venv\Scripts\activate.bat
)

REM 安裝依賴
echo 檢查並安裝 PyInstaller...
pip install pyinstaller

REM 運行打包腳本
echo.
echo 開始打包...
python build.py

echo.
echo ✅ 打包完成!
pause
