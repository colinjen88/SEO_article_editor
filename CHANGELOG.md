# 更新日誌 (Changelog)

本文件記錄 SEO 文章編輯器的所有重要變更。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，  
版本號遵循 [語意化版本 2.0.0](https://semver.org/lang/zh-TW/)。

---

## [1.6.0] - 2025-11-04

### 新增 (Added)
- ✨ **H3 子區塊功能**
  - 在 H2 段落內可新增多個 H3 子區塊
  - 每個 H3 子區塊包含標題和內容
  - 支援巢狀 `<section>` 結構輸出
  - 新增 `H3Block` 類別管理子區塊
  - 自動載入/儲存 H3 資料到 JSON

### 變更 (Changed)
- 🔄 **簡化專案定位**：從多工具套件改為專注的文章編輯器
- 📝 `main.py` 簡化為直接啟動編輯器（移除工具選單）
- 📖 `README.md` 完全改寫，聚焦於文章編輯功能
- 🎯 專案名稱從「SEO 文章工具」改為「SEO 文章編輯器」
- 🏷️ 版本號從 v1.5 更新為 v1.6

### 改進 (Improved)
- 📊 **更好的內容階層**：H1 > H2 > H3 完整結構
- 🎨 **更清晰的介面**：H3 子區塊有獨立邊框區分
- 💡 **更直覺的操作**：每個段落都有「+ H3」按鈕
- 📦 **更完整的資料**：JSON 自動包含所有階層資料

### 技術細節 (Technical)
- 新增 `H3Block` 類別（第 16-29 行）
- `SecBlock` 新增 `h3s` 列表和 `h3_container` 容器
- `SecBlock.to_dict()` 新增 `h3s` 欄位
- HTML 生成支援巢狀 section 結構
- 載入功能支援還原 H3 子區塊

---

## [1.5.0] - 2025-11-04

### 新增 (Added)
- ✨ **全新視覺化編輯器** - 完全重構 `tp_editor_gui.py`
  - 🎨 **完全視覺化介面**：無需學習任何標記語法
  - 📝 **表單式輸入**：透過輸入框和文字區域填寫內容
  - 📌 **固定區塊**：H1 主標題 + 前言（不可刪除）
  - ➕ **動態段落管理**：可新增/刪除文章段落（H2 + 內容）
  - ❓ **專門 FAQ 區塊**：自動套用 `visually-hidden` CSS 類別
  - 👁️ **雙面板設計**：左側表單編輯，右側 HTML 即時預覽
  - 💾 **JSON 資料格式**：使用 JSON 儲存/載入文章資料
  - 🌐 **瀏覽器預覽**：一鍵在瀏覽器查看完整樣式
  - 📤 **HTML 匯出**：產生包含 CSS 的完整 HTML 檔案
  - 🔒 **安全處理**：自動跳脫 HTML 特殊字元
  - ⏱️ **智慧更新**：500ms 延遲更新預覽，減少效能負擔
  - 📊 **滾動支援**：左側編輯區支援滑鼠滾輪捲動
  - 🎯 **範例內容**：啟動時自動載入黃金投資範例文章

### 變更 (Changed)
- 🔄 完全重寫 `tp_editor_gui.py`，從 tp 標記編輯器改為視覺化表單編輯器
- 📁 檔案格式從 `.txt` 改為 `.json`，更適合結構化資料
- 🎨 介面設計從文字編輯改為分區塊表單
- 更新 `README.md` 加入視覺化編輯器完整說明和介面圖示
- 版本號從 v1.4 更新為 v1.5

### 改進 (Improved)
- 🚀 **大幅降低入門門檻**：無需學習 tp 標記語法
- 👥 **更適合非技術使用者**：純視覺化操作
- 📦 **更好的資料管理**：JSON 格式易於編輯和擴充
- 🎯 **更精準的 SEO 控制**：FAQ h2 自動 visually-hidden
- ⚡ **更流暢的體驗**：即時預覽 + 智慧延遲更新
- 🛡️ **更安全的輸出**：自動處理 HTML 特殊字元

### 技術細節 (Technical)
- 使用 `tkinter.Canvas` + `Scrollbar` 實現可捲動編輯區
- 實作 `SectionBlock` 和 `FAQBlock` 類別管理動態區塊
- 使用 Lambda 函數實現區塊刪除回呼
- 使用 `after()` 和 `after_cancel()` 實現防抖動機制
- 支援 ttkbootstrap 主題（可選）

---

## [1.4.0] - 2025-11-04 (已廢棄)

### 新增 (Added)
- ✨ **全新 TP 標記編輯器** (`tp_editor_gui.py`)
  - 雙欄介面設計：左側編輯、右側即時預覽
  - 快速插入工具列：H1、H2、H3、前言、段落、FAQ
  - 即時 HTML 預覽功能（0.5 秒延遲自動更新）
  - 瀏覽器預覽功能，附完整 CSS 樣式
  - 檔案管理：開啟/儲存 .txt 檔案
  - HTML 匯出功能：產生完整獨立的 HTML 檔案
  - 狀態列顯示行列資訊
  - 未儲存提醒機制
- 新增工具選單系統到 `main.py`
  - 圖形化選單介面，可選擇要啟動的工具
  - 支援命令列參數快速啟動特定工具
  - 美觀的工具描述和分類
- 新增範例文章 `input_docs/example_tp_article.txt`
- 新增完整的編輯器使用手冊 `docs/TP_EDITOR_GUIDE.md`

### 變更 (Changed)
- 更新 `main.py` 從單一工具啟動改為多工具選單
- 更新 `README.md` 加入 TP 標記編輯器使用說明
- 改善專案結構說明，標示新增的編輯器

### 改進 (Improved)
- 提供更友善的入門工具（TP 標記編輯器）
- 降低新手使用門檻
- 改善使用者體驗和工作流程

---

## [1.3.0] - 2025-11-03

### 新增 (Added)
- 新增 `main.py` 作為統一程式入口
- 新增 `.gitignore` 檔案，排除不必要的版本控制檔案
- 新增 `requirements.txt` 管理專案依賴
- 新增根目錄 `README.md` 提供快速開始指南
- 新增 `CHANGELOG.md` 記錄版本變更

### 變更 (Changed)
- 重構專案目錄結構，所有 Python 模組移至 `src/` 目錄
- 更新所有文件至最新版本（README、技術文件、規格說明）
- 改善文件組織，新增完整的使用指南和常見問題

### 修正 (Fixed)
- 整理根目錄重複的檔案
- 移動測試用 HTML 檔案至 `output/` 目錄
- 移動示範 Word 檔案至 `input_docs/` 目錄

### 移除 (Removed)
- 移除根目錄的重複 Python 檔案（seo_layout_gui.py, tp_template_parser.py）
- 移除散落的測試檔案

---

## [1.2.0] - 2025-09-15

### 新增 (Added)
- 新增 JSON-LD 安全更新機制，使用 JSON 物件解析與回寫
- 新增 FAQ 區塊缺失時的自動插入功能
- 新增預設輸出檔名建議系統，避免覆蓋舊檔
- 新增 `(tp_intro)` 標記支援前言區塊

### 變更 (Changed)
- 改善 `tp_template_parser.py` 解析邏輯，避免多次執行的狀態殘留
- 優化 FAQ JSON-LD 生成方式，改為 JSON 安全組裝
- 增強 `seo_layout_gui.py` 的錯誤處理

### 修正 (Fixed)
- 修正 JSON-LD 正則替換可能破壞結構的問題
- 修正 FAQ 解析在某些情況下失敗的問題
- 修正檔案命名衝突問題

---

## [1.1.0] - 2025-01-15

### 新增 (Added)
- 新增 `in_faq_section` 狀態追蹤機制
- 新增詳細的技術文件和故障排除指南

### 變更 (Changed)
- 改善 FAQ section 解析邏輯
- 優化 section 區塊的結束條件判斷

### 修正 (Fixed)
- 修正 `tp_template_parser.py` 中的正則表達式群組編號錯誤（`r'\2'` → `r'\1'`）
- 修正 `tp_template_gui.py` 中的相同問題
- 修正 FAQ 內容無法正確分組到專用 section 的問題
- 修正 section 內容被錯誤截斷的問題

---

## [1.0.0] - 2024-09-15

### 新增 (Added)
- 初始版本發布
- 實作 Word 轉 HTML 核心功能
- 實作 tp 標記解析系統
- 建立四個主要 GUI 工具：
  - `seo_layout_gui.py` - 完整的模板化工具
  - `seo_article_gui.py` - 手動編輯工具
  - `docx_to_seo_html_gui.py` - Word 快速轉換工具
  - `tp_template_gui.py` - tp 標記專用工具
- 實作 SEO 結構化資料自動生成（JSON-LD）
- 實作文章編號自動管理系統
- 建立 HTML 模板系統（`seo_layout.html`, `seo_article.html`）
- 支援以下 tp 標記：
  - `(tp_h1)`, `(tp_h2)`, `(tp_h3)` - 標題層級
  - `(tp_sec)` - 段落區塊
  - `(tp_sec_qa)` - FAQ 區塊
  - `(tp_h3_q)` - FAQ 問題
  - `(tp_ans)` - FAQ 答案

---

## 版本號說明

本專案使用 [語意化版本](https://semver.org/lang/zh-TW/)：

- **主版號（MAJOR）**：不相容的 API 變更
- **次版號（MINOR）**：向下相容的功能新增
- **修訂號（PATCH）**：向下相容的錯誤修正

---

## 變更類型說明

- **新增 (Added)**：新功能
- **變更 (Changed)**：既有功能的變更
- **棄用 (Deprecated)**：即將移除的功能
- **移除 (Removed)**：已移除的功能
- **修正 (Fixed)**：錯誤修正
- **安全性 (Security)**：安全性相關修正

---

**維護團隊：** SEO 工具開發團隊  
**最後更新：** 2025-11-03
