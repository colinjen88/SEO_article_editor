# 更新日誌 (Changelog)

本文件記錄 SEO 文章編輯器的所有重要變更。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，  
版本號遵循 [語意化版本 2.0.0](https://semver.org/lang/zh-TW/)。

---

## [2.0.2] - 2025-11-07

### 變更 (Changed)
- 🎨 將內嵌 fallback CSS 外部化：新增 `templates/default_common.css`；
  `_get_style_html()` 優先順序：編輯器內容 → 外部 URL → `templates/common.css` → `templates/default_common.css` → 極簡內建字串。
- 📄 清理與整併文件：移除過時 `docs/README.md` 與 archive 中冗餘文件（FILE_LIST、PROJECT_STRUCTURE、DOCUMENTATION_CHECK）。
- 🏷 版本號更新：`2.0.1` → `2.0.2`，同步更新 GUI 頁尾與文件版本標示。

### 打包 (Build)
- 🔧 重新打包執行檔以反映最新變更。

---

## [2.0.1] - 2025-11-07

### 修正 (Fixed)
- 🛠 修正打包後執行檔缺少 `tkinter` 導致程式啟動錯誤 `ModuleNotFoundError: No module named 'tkinter'`。
  - 新增動態收集 `tcl/`、`tk/` 目錄至 PyInstaller `datas`。
  - 新增 runtime hook `tk_rthook.py` 設定 `TCL_LIBRARY` 與 `TK_LIBRARY`。
  - 擴充 hidden imports：`_tkinter`、`tkinter.*`、`ttkbootstrap.*`。
  - 調整打包策略：移除把整個 `src` 當資料資料夾的方式，改用 `pathex`。
  - 主程式預先 import tkinter 以避免分析遺漏。

### 變更 (Changed)
- 🔧 打包改為先驗證目錄模式 (onedir) 後再提供單檔 (onefile) 方案。
- 🏷 版本號：`2.0.0` → `2.0.1`。

### 建議 (Notes)
- 若需最小單檔執行檔，可在確認 `dist/SEO_Article_Editor.exe` 正常後執行：
  `pyinstaller --noconfirm --onefile --windowed SEO_Article_Editor.spec`

---

## [2.0.0] - 2025-11-07

### 新增 (Added)
- ✨ **CSS 與 Footer 編輯分頁**
  - 新增「CSS」分頁：可編輯共用 CSS 樣式
  - 新增「Footer」分頁：可編輯共用 Footer HTML
  - 支援載入/儲存至 `templates/common.css` 和 `templates/common_footer.html`
- 🎨 **CSS 引入方式選擇**
  - 支援「內置 Style」模式（直接嵌入 `<style>` 標籤）
  - 支援「外部 .css 檔」模式（使用 `<link rel="stylesheet">`）
  - 可自訂外部 CSS URL
- 👁️ **檢視輸出 HTML 功能**
  - 「複製完整HTML原始碼」改為「檢視輸出HTML」
  - 點擊後彈出預覽視窗，顯示完整 HTML 程式碼
  - 視窗內提供「複製 HTML 碼」按鈕
  - 可先檢視再決定是否複製
- 📋 **輸入欄位背景色調整**
  - 所有輸入欄位從純白 (#ffffff) 改為淡灰白 (#f8f9f9)
  - 提供更舒適的視覺對比
- 🔄 **HTML 輸出順序優化**
  - Schema JSON-LD 排在第一段
  - Style/Link 樣式排在第二段
  - 符合 SEO 最佳實踐

### 變更 (Changed)
- 📝 **版本資訊更新**
  - 版本號：v1.8 → v2.0
  - 底部版權資訊：「SEO Article Editor v2.0 by Colinjen」
  - Colinjen 文字保持白色並連結至 mailto:colinjen88@gmail.com
- 🔔 **啟動提示優化**
  - CSS 和 Footer 載入訊息合併為單一提示視窗
  - 減少啟動時的彈窗干擾
  - 僅在檔案不存在時顯示提示

### 改進 (Improved)
- 🎨 **組織名稱預設值更新**
  - 從「Shiny黃金白銀」改為「Shiny黃金白銀交易所」
- 📦 **執行檔編譯**
  - 重新編譯為 v2.0 版本執行檔
  - 檔案大小約 7.2 MB

---

## [1.8.0] - 2025-11-06

### 新增 (Added)
- ✨ **前言區塊完整編輯功能**
  - 前言 H2 標題可自訂編輯（預設為「前言」）
  - 前言內容支援 **HTML 模式**切換
  - HTML 模式下可插入自訂 HTML 標籤（如 `<p class="highlight">`）

### 變更 (Changed)
- 🔄 **工具列按鈕文字優化**
  - 「開啟」→ 「開啟編輯檔」
  - 「儲存」→ 「儲存編輯檔」
  - 更清楚表達檔案管理功能

### 改進 (Improved)
- 📝 **JSON 檔案格式擴充**
  - 新增 `intro_h2` 欄位（前言標題）
  - 新增 `intro_is_html` 欄位（前言 HTML 模式）
  - 向下相容舊版 JSON 檔案

---

## [1.7.0] - 2025-11-04

### 新增 (Added)
- ✨ **完整 SEO 元數據控制介面**
  - 新增「SEO 資訊」專區，包含 10+ 欄位
  - 作者、發布/修改日期、組織名稱、文章編號
  - 標題（Headline）、描述（Description）
  - 作者型別選擇（Organization / Person）
  - Publisher Logo URL、Publisher URL
  - Publisher Logo 寬高設定
  - Publisher sameAs 社群連結（多個，逗號分隔）
- 📊 **完整 Schema.org JSON-LD 支援**
  - 自動生成 Article Schema（包含所有 SEO 資訊）
  - 自動生成 FAQPage Schema（如有 FAQ）
  - 兩個獨立的 `<script type="application/ld+json">` 區塊
  - 新增「Schema 預覽」分頁，可即時查看 JSON-LD
- 🎨 **HTML 模式支援**
  - 段落內容預設支援原生 HTML（可貼表格）
  - FAQ 答案新增「HTML 模式」切換開關
  - 內容標籤提示：「[支援 HTML 表格]」
- 🌐 **語意化 HTML 輸出**
  - 使用 `<article class="seo-article-content">` 包裹
  - 使用 `<section>` 標籤區分段落
  - 前言使用 `<section class="intro-summary">`
  - FAQ 使用 `<section id="faq">`
  - H3 子區塊也用 `<section>` 包裹
- 🎨 **介面美化與易用性**
  - 採用 ttkbootstrap darkly 主題（暗色專業風格）
  - 「+ 段落」和「+ QA」按鈕加大至 3 倍寬度（`width=20`）
  - 新增檔案路徑顯示標籤（顯示當前開啟的檔案）
  - 底部加入版本號與作者資訊

### 變更 (Changed)
- 🔄 **主程式入口更名**：`main.py` → `SEO_Article_Editor.py`
- 📁 **舊版工具歸檔**：`src/seo_layout_gui.py` 等移至 `src/legacy/`
- 🎯 **預設範例更新**：載入時使用包含完整 SEO 資訊的範例
- 📄 **JSON 格式擴充**：儲存檔案包含完整 `seo` 物件（10+ 欄位）
- 🎨 **CSS 模板更新**：匯出 HTML 使用新的 CSS 樣式（符合模板）

### 改進 (Improved)
- 🚀 **SEO 完整度大幅提升**：從基本文章編輯器升級為專業 SEO 工具
- 📊 **符合 Google 搜尋最佳實踐**：完整的結構化資料支援
- 🎯 **更靈活的內容編輯**：支援 HTML 表格等複雜內容
- 👁️ **三重預覽系統**：編輯 + HTML + Schema，全方位檢視
- 📦 **更完整的資料保存**：JSON 包含所有設定，無資料遺失

### 已知問題 (Known Issues)
- ⚠️ **輸入欄位顏色問題**：在 darkly 主題下，部分輸入欄位可能未正確顯示白底黑字
  - 原因：ttkbootstrap 主題樣式覆蓋優先權
  - 已嘗試：使用 `tk.Entry`/`tk.Text` + `option_add` 強制設定
  - 狀態：主題覆蓋機制仍可能影響部分元件
  - 暫時方案：可改用 `flatly` 主題或移除 ttkbootstrap

### 技術細節 (Technical)
- 新增 `Editor._gen_schema_jsonld()` 方法生成 JSON-LD
- 新增 `Editor._strip_tags()` 方法處理 HTML 轉純文字
- `SecBlock.is_html` 固定為 `True`（段落內容預設 HTML）
- `FaqBlock.is_html` 使用 `BooleanVar`（可切換）
- JSON 儲存新增 `seo` 頂層物件（包含 10+ SEO 欄位）
- HTML 匯出整合 CSS 模板與 JSON-LD 生成
- 使用 `tk.Entry` 和 `tk.Text` 取代 `ttk.Entry`（確保樣式可控）
- 新增 `root.option_add()` 全域樣式設定（嘗試覆蓋主題）

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
