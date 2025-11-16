# 安裝說明

## 快速開始

### 1. 安裝 Python3-tk (必需)

GUI 介面需要 Tkinter 支援,請先安裝:

```bash
sudo apt-get update
sudo apt-get install python3-tk
```

### 2. 驗證安裝

```bash
python3 -c "import tkinter; print('Tkinter 安裝成功!')"
```

如果沒有報錯,說明安裝成功。

### 3. 執行程式

```bash
# 方式 1: 直接執行
python3 lottery_system.py

# 方式 2: 使用虛擬環境(推薦)
source .venv/bin/activate
python lottery_system.py
```

## 完整安裝步驟(推薦)

### 1. 安裝 uv(現代化套件管理工具)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 建立並啟動虛擬環境

```bash
# 建立虛擬環境
uv venv

# 啟動虛擬環境
source .venv/bin/activate
```

### 3. 安裝 Tkinter

```bash
sudo apt-get install python3-tk
```

### 4. 執行程式

```bash
python lottery_system.py
```

## 測試核心功能

如果暫時無法安裝 Tkinter,可以先測試核心功能:

```bash
python3 test_core.py
```

這將測試:
- 參與者資料載入
- 抽籤邏輯
- JSON 檔案讀寫
- 歷史記錄功能

## 故障排除

### 問題 1: 提示找不到 tkinter

**解決方法:**
```bash
sudo apt-get install python3-tk
```

### 問題 2: uv 指令找不到

**解決方法:**
```bash
# 加入到 PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 問題 3: 虛擬環境啟動失敗

**解決方法:**
```bash
# 使用完整路徑
source /home/aries/Desktop/project/lottery/.venv/bin/activate
```

## 下一步

安裝完成後,請查看 [README.md](README.md) 了解詳細使用說明。
