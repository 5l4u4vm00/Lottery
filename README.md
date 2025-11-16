# 聖誕交換禮物抽籤系統 🎄

一個功能完整的聖誕交換禮物抽籤桌面應用程式，使用 Python 和 Tkinter 開發，具有美觀的聖誕主題界面和雪花動畫效果。

## 功能特色 ✨

### 雙重抽籤模式

1. **🎁 禮物抽籤**
   - 隨機抽取參與者進行禮物交換
   - 支援避免重複抽取功能
   - 可選顯示模式或郵件通知模式

2. **🎲 關鍵字抽籤**
   - 每位參與者隨機抽取 2 個關鍵字作為禮物選購指南
   - 智能避免抽到自己的關鍵字
   - 確保每次抽籤中關鍵字不重複
   - 支援具名或匿名顯示模式

### 核心功能

- ✅ **參與者管理**
  - 新增/刪除參與者
  - 批次匯入參與者資料（格式：姓名,郵箱）
  - 即時顯示參與者狀態

- 🔤 **關鍵字管理**
  - 為每位參與者設定專屬關鍵字
  - 支援單個新增或批次匯入
  - 關鍵字清單管理

- 📧 **郵件通知系統**
  - SMTP 郵件自動發送
  - 支援多種郵件服務商（Gmail、Outlook、QQ、163 等）
  - 測試郵件功能確保設定正確

- 📊 **歷史記錄**
  - 完整記錄每次抽籤結果
  - 分別記錄禮物抽籤和關鍵字抽籤歷史
  - 支援查看和清空歷史記錄

- 🎨 **聖誕主題界面**
  - 深藍色聖誕夜配色方案
  - 動態雪花背景動畫
  - 聖誕紅、綠、金色彩點綴
  - 直觀的分頁式界面設計

## 系統需求 📋

- Python 3.6 或更高版本
- Tkinter（Python 標準庫）
- 所有依賴均為 Python 標準庫，無需額外安裝

### 平台支援

- ✅ **Windows**: Python 內建 Tkinter
- ✅ **macOS**: Python 內建 Tkinter
- ✅ **Linux**: 需要安裝 `python3-tk`
  ```bash
  sudo apt-get install python3-tk  # Debian/Ubuntu
  sudo yum install python3-tkinter  # CentOS/RHEL
  ```

## 安裝與使用 🚀

### 方法一：直接執行 Python 腳本

1. **下載專案**
   ```bash
   git clone <repository-url>
   cd lottery
   ```

2. **建立虛擬環境（推薦）**
   ```bash
   uv venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

3. **執行程式**
   ```bash
   python lottery_system.py
   ```

### 方法二：使用打包後的執行檔

1. **建置執行檔**
   ```bash
   # 使用自動化腳本
   python build.py           # 跨平台
   ./build.sh                # Linux/macOS
   build.bat                 # Windows

   # 或手動建置
   pip install pyinstaller
   pyinstaller --onefile --windowed --name="聖誕抽籤系統" lottery_system.py
   ```

2. **執行檔位置**
   - 建置完成後，執行檔位於 `dist/聖誕抽籤系統` 目錄
   - 雙擊即可執行，無需 Python 環境

## 使用指南 📖

### 1. 新增參與者

進入「👥 參與者管理」頁面：
- **單個新增**：輸入姓名和郵箱，點擊「➕ 新增」
- **批次匯入**：在文字框中輸入參與者資料（每行格式：`姓名,郵箱`），點擊「📥 批次匯入」

範例：
```
張三,zhang@example.com
李四,li@example.com
王五,wang@example.com
```

### 2. 管理關鍵字

進入「🔤 關鍵字管理」頁面：
1. 從下拉選單選擇參與者
2. 輸入關鍵字並新增，或批次匯入（每行一個關鍵字）
3. 每位參與者可以擁有多個關鍵字

範例關鍵字：
```
咖啡
文具
玩具
書籍
運動用品
```

### 3. 執行禮物抽籤

進入「🎁 禮物抽籤」頁面：
1. 選擇抽籤模式：
   - 📺 顯示在畫面上：結果顯示在應用程式中
   - 📧 僅傳送郵件通知：結果透過郵件發送給中獎者
2. 設定抽取數量
3. 勾選「🔒 避免重複抽取」（建議開啟）
4. 點擊「🎁 開始抽籤」

### 4. 執行關鍵字抽籤

進入「🎲 關鍵字抽籤」頁面：
1. 選擇通知模式：
   - 📺 顯示在畫面上
   - 📧 僅傳送郵件通知
   - 📱 畫面顯示且傳送郵件
2. 選擇顯示模式：
   - 顯示人名與關鍵字
   - 僅顯示關鍵字組合（匿名）
3. 設定參與人數
4. 點擊「🎲 開始抽籤」

**注意**：每位參與者會抽取 2 個關鍵字，且不會抽到自己的關鍵字。

### 5. 設定郵件通知

進入「⚙️ 設定」頁面：
1. 填寫 SMTP 伺服器資訊：
   - SMTP 伺服器（例如：smtp.gmail.com）
   - SMTP 連接埠（通常是 587）
   - SMTP 使用者名稱
   - SMTP 密碼（應用專用密碼或授權碼）
   - 寄件人郵箱
2. 點擊「儲存設定」
3. 輸入測試郵箱並點擊「傳送測試郵件」確認設定正確

#### 常用郵件服務商設定

| 服務商 | SMTP 伺服器 | 連接埠 | 備註 |
|--------|------------|--------|------|
| Gmail | smtp.gmail.com | 587 | 需要啟用兩步驟驗證並生成應用專用密碼 |
| Outlook | smtp-mail.outlook.com | 587 | 使用帳號密碼 |
| QQ 郵箱 | smtp.qq.com | 587 | 需要開啟 SMTP 服務並使用授權碼 |
| 163 郵箱 | smtp.163.com | 587 | 需要開啟 SMTP 服務並使用授權碼 |

## 資料存儲 💾

所有資料以 JSON 格式儲存在程式目錄中：

- `participants.json` - 參與者清單（包含姓名、郵箱、關鍵字）
- `lottery_history.json` - 禮物抽籤歷史記錄
- `keyword_lottery_history.json` - 關鍵字抽籤歷史記錄
- `config.json` - SMTP 郵件設定（**注意**：包含明文密碼，請勿分享）

**安全提醒**：
- `config.json` 已加入 `.gitignore`，不會被提交到版本控制
- 建議使用應用專用密碼而非主密碼
- 定期備份資料檔案

## 專案結構 📁

```
lottery/
├── lottery_system.py          # 主程式（1699 行）
│   ├── LotterySystem          # 業務邏輯類別
│   ├── Snowflake              # 雪花動畫類別
│   ├── ChristmasTheme         # 聖誕主題配置
│   └── LotteryGUI             # GUI 界面類別
├── test_core.py               # 核心功能測試
├── build.py                   # PyInstaller 建置腳本
├── build.sh                   # Linux/macOS 建置腳本
├── build.bat                  # Windows 建置腳本
├── requirements.txt           # 依賴清單（空檔案，僅標準庫）
├── README.md                  # 專案說明文件
├── INSTALL.md                 # 安裝指南
├── PACKAGE.md                 # 打包指南
├── CLAUDE.md                  # Claude Code 開發指南
└── .gitignore                 # Git 忽略檔案

資料檔案（執行時生成）：
├── participants.json          # 參與者資料
├── lottery_history.json       # 抽籤歷史
├── keyword_lottery_history.json  # 關鍵字抽籤歷史
└── config.json                # SMTP 設定（不納入版控）
```

## 架構設計 🏗️

### 關注點分離架構

1. **業務邏輯層** (`LotterySystem` 類別)
   - 處理所有資料操作（參與者、關鍵字、歷史）
   - 實現抽籤演算法和郵件發送
   - 無 GUI 依賴，可作為獨立函式庫使用
   - 資料持久化到 JSON 檔案

2. **表現層** (`LotteryGUI` 類別)
   - 使用 Tkinter 建立跨平台桌面 UI
   - 七個分頁式功能頁面
   - 呼叫 `LotterySystem` 方法處理業務邏輯
   - 聖誕主題設計和雪花動畫

### 抽籤演算法

**禮物抽籤** (`draw()` 方法):
- 維護 `drawn_items` 清單追蹤已抽取參與者
- 當 `avoid_repeat=True` 時，過濾已抽取項目
- 使用 `random.sample()` 進行無偏隨機選擇
- 抽籤後更新 `drawn_items` 清單

**關鍵字抽籤** (`draw_keywords()` 方法):
- 每位參與者獲得 2 個關鍵字
- 驗證關鍵字總數充足（需要 `參與人數 * 2`）
- 使用 `used_keywords` 累加器確保單次抽籤中無重複
- 智能過濾，確保不會抽到自己的關鍵字
- 返回字典格式：`email -> {name, email, keywords: [kw1, kw2]}`

## 測試 🧪

執行核心功能測試（不啟動 GUI）：

```bash
python test_core.py
```

測試覆蓋：
- JSON 檔案格式驗證
- 抽籤演算法邏輯
- 資料持久化
- 歷史記錄格式

## 常見問題 ❓

### Q: 郵件發送失敗？

A: 請檢查：
1. SMTP 設定是否正確
2. 是否使用了應用專用密碼或授權碼（而非主密碼）
3. 郵件服務商是否已開啟 SMTP 服務
4. 網路連線是否正常
5. 使用「傳送測試郵件」功能驗證設定

### Q: Linux 系統無法啟動？

A: 請確認已安裝 python3-tk：
```bash
sudo apt-get install python3-tk
```

### Q: 如何重置所有資料？

A: 刪除以下 JSON 檔案：
```bash
rm participants.json lottery_history.json keyword_lottery_history.json config.json
```

### Q: 關鍵字抽籤提示「可用關鍵字不足」？

A: 確保：
- 每位參與者至少有 2 個關鍵字
- 關鍵字總數 ≥ 參與人數 × 2
- 除了要抽籤的參與者自己的關鍵字外，其他參與者有足夠的關鍵字

### Q: 可以自訂介面語言嗎？

A: 目前僅支援繁體中文，如需其他語言，可修改程式碼中的字串常數。

## 技術細節 🔧

- **程式語言**: Python 3.6+
- **GUI 框架**: Tkinter (標準庫)
- **資料格式**: JSON (UTF-8 編碼)
- **郵件協定**: SMTP with TLS
- **編碼**: UTF-8 支援繁體中文
- **執行緒**: 單執行緒（郵件發送會阻塞 UI）

## 授權條款 📄

本專案採用 MIT 授權條款。

## 貢獻指南 🤝

歡迎提交 Issue 和 Pull Request！

建議改進方向：
- [ ] 多語言支援（英文、簡體中文）
- [ ] 非同步郵件發送（避免 UI 阻塞）
- [ ] 匯出抽籤結果為 PDF/Excel
- [ ] 資料庫支援（SQLite）
- [ ] 自訂主題配色
- [ ] 抽籤動畫效果
- [ ] 雲端同步功能

## 更新日誌 📝

### v1.0.0 (2025)
- 首次發布
- 實現禮物抽籤功能
- 實現關鍵字抽籤功能
- 參與者和關鍵字管理
- SMTP 郵件通知
- 歷史記錄功能
- 聖誕主題 UI 和雪花動畫

## 聯絡方式 📮

如有問題或建議，歡迎透過 Issue 回報。

---

🎄 **祝您聖誕快樂，抽籤愉快！Merry Christmas!** 🎁
