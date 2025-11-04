# SEO 文章工具 | 專案說明文件

> **版本：** v1.3  
> **更新日期：** 2025-11-03

## 📌 專案簡介

本工具專為 **SEO 文章製作與自動化轉換** 設計，支援 Word 檔案解析、FAQ 結構化資料產生、手動/批次編輯，並可直接產出符合 SEO 標準的 HTML 原始碼。

### ✨ 核心特色
- 🚀 **Word 一鍵轉 HTML**：支援 tp 標記自動解析
- 📊 **FAQ 結構化資料**：自動產生 Schema.org JSON-LD
- 🎨 **美觀 GUI 介面**：支援主題切換與日期選擇器
- 📝 **文章編號管理**：自動遞增，避免衝突
- 🔒 **安全輸出**：自動檔名建議，不覆蓋舊檔
- 🌐 **即時預覽**：支援瀏覽器與內嵌預覽

---

## 📂 專案結構

```
SEO_article_transfer/
├── main.py                    # 主程式入口
├── article_number.txt         # 文章編號記錄
├── settings.json              # 使用者設定（自動產生）
├── requirements.txt           # Python 依賴套件
├── .gitignore                 # Git 忽略規則
├── docs/                      # 文件目錄
│   ├── README.md             # 本說明文件
│   ├── SEO_TOOL_SPEC.md      # 規格說明
│   └── TECHNICAL_DOCUMENTATION.md  # 技術文件
├── src/                       # 原始碼目錄
│   ├── seo_layout_gui.py     # 主要工具（推薦使用）✨
│   ├── seo_article_gui.py    # 手動編輯工具
│   ├── docx_to_seo_html_gui.py  # Word 轉換工具
│   ├── tp_template_gui.py    # tp 標記解析工具
│   ├── tp_template_parser.py # tp 解析核心
│   └── convent_seo_article.py   # 基礎轉換模組
├── templates/                 # HTML 模板
│   ├── seo_layout.html       # 變數化模板（主要）
│   └── seo_article.html      # 完整範例模板
├── input_docs/                # Word 檔案目錄
└── output/                    # HTML 輸出目錄
```

---

## 🚀 快速開始

### 環境需求
- Python 3.8 以上
- pip 套件管理工具

### 安裝步驟

1. **複製專案**
```powershell
git clone <repository-url>
cd SEO_article_transfer
```

2. **安裝依賴**
```powershell
pip install -r requirements.txt
```

3. **啟動程式**
```powershell
python main.py
```

或直接執行：
```powershell
python src/seo_layout_gui.py
```

---

## 💡 使用指南

### 方法一：SEO Layout GUI（推薦）⭐

這是最完整的工具，整合了所有功能。

**操作步驟：**

1. **填寫基本資訊**
   - 作者：預設「炫麗鑫」
   - 日期：預設今天（支援日期選擇器）
   - 標題：會從 Word 自動抓取 `(tp_h1)`
   - 描述：會從 Word 自動抓取第一個 `(tp_h2)`
   - 組織：預設「Shiny黃金白銀」
   - 文章編號：自動遞增（可手動修改）

2. **選擇檔案**
   - 模板檔案：預設 `templates/seo_layout.html`
   - Word 檔案：選擇要轉換的 .docx

3. **操作選項**
   - **解析 FAQ 預覽**：查看解析出的問答對
   - **預覽 HTML（瀏覽器）**：在瀏覽器中預覽最終效果
   - **產生 HTML**：儲存成 HTML 檔案

**Word 檔案標記規則：**

```
(tp_h1)文章主標題
(tp_intro)前言內容...
(tp_sec)
(tp_h2)段落標題
段落內容...
(tp_sec_qa)
(tp_h3_q)問題一？
(tp_ans)答案一的內容...
(tp_h3_q)問題二？
(tp_ans)答案二的內容...
```

### 方法二：手動編輯模式

適合不使用 Word，直接在 GUI 輸入內容的場景。

```powershell
python src/seo_article_gui.py
```

### 方法三：快速 Word 轉換

適合已有 Word 文件，需要快速轉換成 HTML。

```powershell
python src/docx_to_seo_html_gui.py
```

---

## 🎯 主要功能模組
### 1. SEO Layout GUI（主要工具）⭐

**完整的模板化文章生成解決方案**

**核心功能：**
- 支援所有 meta 欄位編輯（作者、日期、標題、描述、組織、文章編號）
- 自動文章編號管理（從 `article_number.txt` 讀取並遞增）
- Word 檔案 tp 標記解析
- FAQ 自動抓取與 JSON-LD 生成
- 即時預覽（瀏覽器 / WebView）
- 自動檔名建議（`output_YYYYMMDD.html`）
- 主題切換（支援 6 種主題）
- 日期選擇器（ttkbootstrap / tkcalendar）

**適用場景：** 日常文章製作的主要工具

### 2. Word 轉 SEO 標準 HTML
- 支援 docx 檔案解析，標題、段落、清單、表格自動轉換。
- 產生 FAQ 結構化資料（JSON-LD），利於 SEO。
- 可自訂 meta 欄位（如日期、描述、mainEntityOfPage id）。
- 產出格式完全仿照 `seo_article.html` 範例。

### 3. 文章手動編輯 GUI

**純手動輸入模式**

- 無需 Word 檔案，直接在 GUI 輸入
- 支援主標題、段落、FAQ 手動編輯
- 動態新增段落功能
- 自動產生 SEO 結構化資料
- 自動檔名建議

**適用場景：** 快速建立簡短文章或測試用途

### 4. tp 標記模板解析工具

**專業的 tp 標記解析引擎**

- 支援完整的 tp 標記語法
- 自動生成 HTML 結構與 FAQ JSON-LD
- 狀態機解析邏輯
- JSON 安全組裝（避免正則破壞結構）

**適用場景：** 已熟悉 tp 標記語法的進階使用者

### 5. HTML 模板系統
**模板檔案：**

- **`seo_layout.html`**：變數化模板，支援動態內容替換
- **`seo_article.html`**：完整範例，包含所有樣式和結構

**支援的模板變數：**

```
{{author_name}}      - 作者名稱
{{TheDate}}          - 文章日期
{{headline}}         - 文章標題
{{description}}      - 文章描述
{{OrganizationName}} - 組織名稱
{{article_number}}   - 文章編號
```

---

## 📖 tp 標記語法說明

### 標記規則

使用者只需在 Word 檔內依規則標記 `(tp_xxx)`，系統會自動解析並產生 HTML。

| 標記 | 說明 | 輸出 |
|------|------|------|
| `(tp_h1)` | 主標題 | `<h1>` |
| `(tp_h2)` | 副標題 | `<h2>` |
| `(tp_h3)` | 小標題 | `<h3>` |
| `(tp_intro)` | 前言區塊 | `<section class="intro-summary">` |
| `(tp_sec)` | 一般段落區塊開始 | `<section>` |
| `(tp_sec_qa)` | FAQ 區塊開始 | `<section id="faq-section">` |
| `(tp_h3_q)` | FAQ 問題 | `<h3>` + JSON-LD Question |
| `(tp_ans)` | FAQ 答案 | `<p>` + JSON-LD Answer |

### Word 檔案範例

```
(tp_h1)黃金投資指南

(tp_intro)
本文將介紹黃金投資的基本知識...

(tp_sec)
(tp_h2)黃金的種類
黃金投資主要分為實體黃金和紙黃金...

(tp_sec)
(tp_h2)投資策略
長期持有是最穩健的策略...

(tp_sec_qa)
(tp_h3_q)黃金價格如何決定？
(tp_ans)黃金價格主要由國際市場供需、美元匯率、地緣政治等因素決定...

(tp_h3_q)適合投資黃金的時機？
(tp_ans)建議在經濟不確定時期、通膨預期升高時適度配置黃金...
```

---

## ⚙️ 技術特點

### FAQ 結構化資料

系統自動產生符合 Schema.org 標準的 JSON-LD：

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "mainEntity": {
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "問題內容",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "答案內容"
        }
      }
    ]
  }
}
```

### JSON-LD 安全更新機制

- 使用 JSON 物件解析與回寫，避免正則替換破壞結構
- 自動更新所有 meta 欄位
- 動態生成 FAQ mainEntity 陣列
- 若模板缺少 FAQ 區塊，自動插入

### 檔案命名規則

- 預設：`output_YYYYMMDD.html`
- 重複時：`output_YYYYMMDD_1.html`, `output_YYYYMMDD_2.html`...
- 確保不會覆蓋舊檔

### 設定持久化

- 自動儲存使用者設定至 `settings.json`
- 下次啟動自動載入上次的設定
- 包含：作者、日期、模板路徑、Word 路徑等

---

## 🎨 GUI 功能

### 主題切換

支援 6 種 ttkbootstrap 主題：
- flatly（預設）
- cosmo
- darkly
- morph
- sandstone
- solar

### 日期選擇器

- 支援 **ttkbootstrap DateEntry**（推薦）
- 支援 **tkcalendar DateEntry**
- 降級至普通文字欄位（若未安裝上述套件）

### 分頁介面

- **基本與檔案**：主要設定與操作
- **FAQ 預覽**：即時查看解析結果

---
---

## FAQ 與 JSON-LD 規則（重點）
- JSON-LD 更新改為「解析後更新」：避免以正則替換破壞 JSON 結構
- `seo_layout_gui.py` 會：
  - 以 JSON 物件安全更新 `author/dateModified/datePublished/headline/description/mainEntityOfPage/publisher`
  - 從 Word 的 `(tp_sec_qa)` 區塊動態收集 `Question/Answer` 並同步到：
    - HTML 可見區塊：`<section id="faq-section">`
    - JSON-LD 的 `mainEntity` 陣列
  - 若模板缺少 `<section id="faq-section">`，會自動在 `</article>` 前插入 FAQ 區塊

## 文章編號（article_number.txt）
- 啟動 `seo_layout_gui.py` 時，欄位預設為目前檔案數值 + 1
- 點擊「確認號碼」會立即寫回檔案

## 檔名規則
- 預設輸出 `output_YYYYMMDD.html`
- 若檔名已存在，自動建議 `output_YYYYMMDD_1.html`、`output_YYYYMMDD_2.html`…

---
如需更多自訂功能、格式或技術支援，請聯絡開發者。
