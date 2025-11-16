#!/bin/bash
# 打包腳本 - Linux/Mac 版本

echo "🎄 聖誕抽籤系統打包工具 🎁"
echo "======================================"

# 檢查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 找不到 Python3，請先安裝 Python"
    exit 1
fi

# 激活虛擬環境（如果存在）
if [ -d ".venv" ]; then
    echo "激活虛擬環境..."
    source .venv/bin/activate
fi

# 安裝依賴
echo "檢查並安裝 PyInstaller..."
pip install pyinstaller

# 運行打包腳本
echo ""
echo "開始打包..."
python3 build.py

echo ""
echo "✅ 打包完成!"
