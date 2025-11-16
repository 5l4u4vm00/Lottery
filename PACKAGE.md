# 打包說明文檔

## 📦 打包聖誕抽籤系統成可執行文件

本文檔說明如何將抽籤系統打包成 Windows 和 Linux 可執行文件。

---

## 🛠️ 打包方法

### 方法一: 自動打包（推薦）

#### Linux / macOS
```bash
# 1. 安裝 PyInstaller
pip3 install pyinstaller

# 2. 運行打包腳本
chmod +x build.sh
./build.sh

# 或直接使用 Python 運行
python3 build.py
```

#### Windows
```cmd
REM 1. 安裝 PyInstaller
pip install pyinstaller

REM 2. 運行打包腳本
build.bat

REM 或直接使用 Python 運行
python build.py
```

---

### 方法二: 手動打包

#### 基本打包命令

**Linux:**
```bash
pyinstaller --onefile --windowed --name="聖誕抽籤系統" lottery_system.py
```

**Windows:**
```cmd
pyinstaller --onefile --windowed --name="聖誕抽籤系統" lottery_system.py
```

#### 詳細參數說明

```bash
pyinstaller \
  --onefile \                    # 打包成單一執行檔
  --windowed \                   # 不顯示控制台窗口（GUI 模式）
  --name="聖誕抽籤系統" \         # 設定執行檔名稱
  --clean \                      # 清理暫存檔案
  --noconfirm \                  # 不詢問確認
  lottery_system.py              # 主程式文件
```

---

## 📂 打包後的文件結構

```
dist/
├── 聖誕抽籤系統              # 可執行文件（Linux）
├── 聖誕抽籤系統.exe          # 可執行文件（Windows）
├── README.md                  # 說明文檔
├── INSTALL.md                 # 安裝說明
├── participants.json          # 參與者數據（空）
├── keywords.json              # 關鍵字數據（空）
├── lottery_history.json       # 歷史記錄（空）
└── keyword_lottery_history.json  # 關鍵字歷史（空）
```

---

## 🌐 跨平台打包

### 在 Linux 上打包 Linux 版本
```bash
pyinstaller --onefile --windowed --name="聖誕抽籤系統_Linux" lottery_system.py
```

### 在 Windows 上打包 Windows 版本
```cmd
pyinstaller --onefile --windowed --name="聖誕抽籤系統_Windows" lottery_system.py
```

**注意:** PyInstaller 不支持跨平台打包。要生成 Windows 版本必須在 Windows 上打包，生成 Linux 版本必須在 Linux 上打包。

---

## 🔧 進階配置

### 添加圖標（可選）

如果你有圖標文件，可以添加到可執行文件:

**Linux/macOS:**
```bash
pyinstaller --onefile --windowed --icon=icon.png lottery_system.py
```

**Windows:**
```cmd
pyinstaller --onefile --windowed --icon=icon.ico lottery_system.py
```

### 包含額外文件

如果需要包含額外的數據文件:

```bash
pyinstaller --onefile --windowed \
  --add-data "README.md:." \
  --add-data "templates:templates" \
  lottery_system.py
```

---

## 📋 完整打包清單

打包完成後，建議包含以下文件一起發布:

1. **可執行文件**
   - 聖誕抽籤系統 (Linux)
   - 聖誕抽籤系統.exe (Windows)

2. **說明文檔**
   - README.md - 項目說明
   - INSTALL.md - 安裝說明
   - 使用範例.md - 使用教程
   - 聖誕主題UI說明.md - UI 說明
   - 關鍵字抽籤功能說明.md - 功能說明

3. **空數據文件**（首次運行時自動創建）
   - participants.json
   - keywords.json
   - lottery_history.json
   - keyword_lottery_history.json
   - config.json

---

## 🐛 常見問題

### 問題 1: 打包後執行文件很大
**解決:** 使用 `--exclude-module` 排除不需要的模塊:
```bash
pyinstaller --onefile --windowed \
  --exclude-module matplotlib \
  --exclude-module numpy \
  lottery_system.py
```

### 問題 2: Linux 下無法執行
**解決:** 添加執行權限:
```bash
chmod +x dist/聖誕抽籤系統
```

### 問題 3: Windows 防毒軟件報警
**解決:** 這是 PyInstaller 打包的常見問題。可以:
- 添加到防毒軟件白名單
- 使用代碼簽名證書簽名可執行文件

### 問題 4: 找不到 tkinter
**解決:** 確保已安裝 Python tkinter 模塊:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-tkinter
```

**Windows:**
tkinter 通常隨 Python 一起安裝

---

## ✅ 測試打包結果

打包完成後，建議進行以下測試:

1. **基本啟動測試**
   - 雙擊運行可執行文件
   - 確認 GUI 界面正常顯示

2. **功能測試**
   - 添加參與者
   - 執行抽籤
   - 查看歷史記錄

3. **數據持久化測試**
   - 關閉程序
   - 重新打開
   - 確認數據已保存

---

## 📦 發布建議

### 創建壓縮包

**Linux:**
```bash
cd dist
tar -czf 聖誕抽籤系統_Linux_v1.0.tar.gz *
```

**Windows:**
```cmd
cd dist
powershell Compress-Archive -Path * -DestinationPath 聖誕抽籤系統_Windows_v1.0.zip
```

### 發布檢查清單

- [ ] 在目標平台測試運行
- [ ] 檢查所有功能正常
- [ ] 包含完整的說明文檔
- [ ] 添加版本號
- [ ] 創建 Release Notes
- [ ] 測試首次安裝流程

---

## 📝 版本管理建議

建議使用以下命名規範:

- `聖誕抽籤系統_Windows_v1.0.zip`
- `聖誕抽籤系統_Linux_v1.0.tar.gz`
- `聖誕抽籤系統_macOS_v1.0.dmg`

---

## 🎯 快速開始（給最終用戶）

### Windows 用戶
1. 下載 `聖誕抽籤系統_Windows_v1.0.zip`
2. 解壓縮到任意位置
3. 雙擊 `聖誕抽籤系統.exe` 運行

### Linux 用戶
1. 下載 `聖誕抽籤系統_Linux_v1.0.tar.gz`
2. 解壓: `tar -xzf 聖誕抽籤系統_Linux_v1.0.tar.gz`
3. 添加執行權限: `chmod +x 聖誕抽籤系統`
4. 運行: `./聖誕抽籤系統`

---

## 📞 技術支持

如有打包問題，請檢查:
1. Python 版本 (建議 3.8+)
2. PyInstaller 版本 (建議 5.0+)
3. 操作系統版本
4. 錯誤日誌信息

---

**最後更新:** 2025-11-15
