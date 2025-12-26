# SEO Article Editor - Technical Documentation (v2.6)

## 1. 系統架構 (System Architecture)

本專案已從舊版的 Word 解析工具轉型為**全功能的視覺化 SEO 文章編輯器**。

### 核心組成
- **入口程式**: `SEO_Article_Editor.py` (負責環境初始化與模組載入)
- **核心邏輯**: `src/tp_editor_gui.py` (包含 GUI 介面、資料模型、HTML 生成邏輯)
- **資料儲存**: JSON 格式專案檔 (取代舊版 .txt 模板)

### 模組關係
```text
SEO_Article_Editor.py
└── src/tp_editor_gui.py
    ├── Editor Class (主要控制器)
    │   ├── _gen() (HTML生成核心)
    │   ├── _gen_schema_jsonld() (結構化資料生成核心)
    │   └── _generate_complete_html() (完整頁面組裝)
    └── Block Classes (區塊元件)
        ├── SecBlock (H2區塊)
        ├── H3Block (H3區塊)
        └── FaqBlock (問答區塊)
```

## 2. 核心邏輯 (Core Logic)

系統不再依賴外部解析器，而是直接在 GUI 編輯器中維護資料狀態，並在匯出時組裝內容。

### 2.1 HTML 組裝邏輯 (`_gen`)

文章主體的 HTML 生成由 `Editor._gen()` 方法負責，流程如下：

1.  **文章容器**: 建立 `<article class="seo-article-content">`
2.  **圖片處理**: 檢查 JSON 資料中的 `image_filename`，若有則組合 URL 並生成 `<div class="img"><img src="..."></div>`，置於 H1 之前（符合 SEO 最佳實踐）。
3.  **H1 標題**: 生成 `<h1>`。
4.  **前言區塊 (Intro)**:
    - 生成 `<section class="intro-summary">`。
    - 根據 `intro_is_html` 屬性決定是直接插入 HTML 內容還是進行轉義並包裹 `<p>`。
5.  **主要段落 (Sections)**:
    - 迭代所有 `SecBlock`。
    - 生成 `<section>` 與 `<h2>`。
    - 遞迴處理內部的 `H3Block`，生成嵌套的 `<section>` 與 `<h3>`。
    - 支援 `is_html` 屬性，允許使用者直接貼入複雜 HTML（如表格）。
6.  **常見問答 (FAQ)**:
    - 生成 `<section id="faq">`。
    - 迭代所有 `FaqBlock`。
    - 生成 `<h3>` 作為問題，內容作為答案。

### 2.2 SEO 結構化資料 (`_gen_schema_jsonld`)

系統自動產生並且分離兩組 JSON-LD 腳本，以最大化搜尋引擎兼容性：

1.  **Article Schema**: 
    - 包含 Headline, Helper, Publisher (含 Logo 設定), Author (含 Type), DateModified, DatePublished, Description。
    - 自動處理 `mainEntityOfPage`。
2.  **FAQPage Schema**: 
    - 獨立生成的 FAQ 結構化資料，包含問題與答案陣列。

**邏輯特點**:
- 使用 Python `json.dumps` 確保輸出格式絕對安全。
- 自動移除答案中的 HTML 標籤 (`_strip_tags`) 以符合 JSON-LD text 欄位規範。

## 3. 資料格式與模板 (Data Format)

v2.6 使用 **JSON** 作為標準專案儲存格式（即模板）。不再使用舊版的 `(tp_tag)` 標記。

### 3.1 完整 JSON 範例 (`.json`)

以下是標準的專案檔案結構：

```json
{
  "seo": {
    "author": "測試作者",
    "pub_date": "2025-11-06",
    "mod_date": "2025-11-06",
    "org_name": "測試組織",
    "article_num": "999",
    "headline": "測試 Headline：這是給搜尋引擎看的標題",
    "description": "這是測試用的 Description，會出現在搜尋結果摘要中。",
    "author_type": "Organization",
    "publisher_logo_url": "https://example.com/logo.png",
    "publisher_url": "https://example.com/",
    "publisher_logo_width": "",
    "publisher_logo_height": "",
    "publisher_sameas": [],
    "image_url_prefix": "https://example.com/",
    "image_filename": "cover.jpg",
    "image_alt": "封面圖片說明",
    "image_width": "100%",
    "image_height": "auto"
  },
  "h1": "這是網頁上顯示的主要標題 (H1)",
  "intro": "這是前言內容，簡述文章重點。",
  "intro_h2": "前言小標 (H2)",
  "intro_is_html": false,
  "sections": [
    {
      "h2": "第一章：為什麼要投資黃金？ (H2)",
      "content": "這是第一章的詳細內容...",
      "is_html": true,
      "h3s": [
        {
          "h3": "1.1 保值功能 (H3)",
          "content": "黃金具有抗通膨的效果...",
          "is_html": false
        }
      ]
    }
  ],
  "faqs": [
    {
      "question": "Q: 黃金投資適合新手嗎？",
      "answer": "A: 是的，相對簡單且風險可控。",
      "is_html": false
    }
  ]
}
```

## 4. 棄用模組 (Deprecated)

以下模組屬於 v1.x 架構，目前均已移除：
- **`src/tp_template_parser.py`**: 舊版正則表達式解析器 (Regex-based parser)。
- **`src/legacy/`**: 存放所有舊版實驗性代碼。

## 5. 版本歷史 (Version History)

### v2.6 (Current)
- **架構重構**: 轉型為純視覺化編輯器 (GUI-first)。
- **資料移植**: 全面採用 JSON 作為資料交換標準。
- **預覽增強**: 新增瀏覽器預覽與完整 HTML 原始碼檢視。

### v1.3 (Legacy)
- 基於 Word/Text 模板解析的自動化工具。

---
**文件版本**: 2.6 (Updated)
**文件日期**: 2025-12-21
