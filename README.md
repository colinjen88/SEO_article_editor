# SEO 文章工具 

> **版本：** v1.5  
> **更新日期：** 2025-11-04

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

---

## 💡 使用指南

### 🎯 工具選單（v1.3 新增）

啟動主程式會顯示工具選單，可選擇要使用的工具：

```powershell
python main.py
```

**快速啟動特定工具：**
```powershell
python main.py editor    # TP 標記編輯器
python main.py layout    # SEO Layout GUI
python main.py article   # SEO 文章編輯
```

---

### 🎨 視覺化編輯器（推薦新手）✨

**最直覺的操作方式！** 完全視覺化表單界面，無需學習任何標記語法。

```powershell
python src/tp_editor_gui.py
```

**核心特色：**
- 📝 **表單式輸入**：所有內容透過輸入框填寫，完全視覺化
- 📌 **固定區塊**：H1 主標題 + 前言（不可刪除）
- ➕ **動態段落**：可隨時新增/刪除文章段落（H2 + 內容）
- ❓ **FAQ 專區**：專門的 FAQ 區塊，自動套用 visually-hidden 樣式
- 👁️ **即時預覽**：右側面板即時顯示 HTML 效果
- 🌐 **瀏覽器預覽**：一鍵在瀏覽器中查看完整樣式
- 💾 **JSON 儲存**：文章資料以 JSON 格式儲存，易於編輯和管理
- 📤 **匯出 HTML**：產生完整的 HTML 檔案，包含 CSS 樣式

**介面說明：**

```
┌─────────────────────────────────────────┐
│ 📂開啟 💾儲存 📤匯出HTML │ 🔄更新 🌐預覽 │
├───────────────┬─────────────────────────┤
│ 📌 主標題     │  👁️ HTML 預覽          │
│ [H1 輸入框]   │                         │
│               │  <h1>黃金投資...</h1>   │
│ 📝 前言       │  <section>              │
│ [前言輸入框]  │    <p>黃金一直...</p>   │
│               │  </section>             │
│ 📄 文章段落   │                         │
│ ┌───────────┐ │  <section>              │
│ │ H2: xxx   │ │    <h2>為什麼...</h2>  │
│ │ 內容: ... │ │    <p>黃金具有...</p>  │
│ │ [🗑️刪除]  │ │  </section>             │
│ └───────────┘ │                         │
│ [➕ 新增段落] │  <section id="faq">     │
│               │    <h2 class="hidden">  │
│ ❓ FAQ 區塊   │    <h3>新手適合?</h3>   │
│ ┌───────────┐ │    <p>非常適合...</p>   │
│ │ Q: xxx    │ │  </section>             │
│ │ A: ...    │ │                         │
│ │ [🗑️刪除]  │ │                         │
│ └───────────┘ │                         │
│ [➕ 新增FAQ]  │                         │
└───────────────┴─────────────────────────┘
```

**操作流程：**
1. **填寫固定欄位**：輸入 H1 標題和前言
2. **新增段落**：點擊「➕ 新增段落」，填寫 H2 和內容
3. **新增 FAQ**：點擊「➕ 新增FAQ」，填寫問答
4. **即時預覽**：右側自動顯示 HTML 效果
5. **儲存專案**：儲存為 JSON 檔案，方便日後修改
6. **匯出 HTML**：產生最終的 HTML 檔案

**特殊說明：**
- FAQ 區塊的 H2 標題會自動套用 `visually-hidden` CSS 類別
- 所有內容支援雙行換行（`\n\n`）自動轉換為段落
- 使用者輸入的特殊字元會自動跳脫，確保 HTML 安全

---

### 推薦：SEO Layout GUI ⭐

**完整功能版本！** 從 Word 直接轉換為 SEO HTML。

```powershell
python src/seo_layout_gui.py
```

**操作步驟：**

1. **填寫基本資訊**（大部分會自動填入）
   - 作者、日期、組織、文章編號
   
2. **選擇檔案**
   - 模板：`templates/seo_layout.html`（預設）
   - Word 檔案：選擇要轉換的 .docx

3. **解析與預覽**
   - 點擊「解析 FAQ 預覽」查看問答對
   - 點擊「預覽 HTML」在瀏覽器中查看

4. **產生 HTML**
   - 點擊「產生 HTML」儲存檔案
   - 檔名會自動建議為 `output_YYYYMMDD.html`

---

## 📖 Word 檔案標記語法

在 Word 檔案中使用以下標記：

```
(tp_h1)文章主標題

(tp_intro)前言內容...

(tp_sec)
(tp_h2)段落標題
段落內容...

(tp_sec_qa)
(tp_h2)FAQ常見問題
(tp_h3_q)問題一？
(tp_ans)答案一的內容...

(tp_h3_q)問題二？
(tp_ans)答案二的內容...
```

### 標記說明

| 標記 | 說明 | 輸出 |
|------|------|------|
| `(tp_h1)` | 主標題 | `<h1>` |
| `(tp_h2)` | 副標題 | `<h2>` |
| `(tp_h3)` | 小標題 | `<h3>` |
| `(tp_intro)` | 前言區塊 | `<section class="intro-summary">` |
| `(tp_sec)` | 段落區塊開始 | `<section>` |
| `(tp_sec_qa)` | FAQ 區塊開始 | `<section id="faq-section">` |
| `(tp_h3_q)` | FAQ 問題 | `<h3>` + JSON-LD |
| `(tp_ans)` | FAQ 答案 | `<p>` + JSON-LD |

---

## 📂 專案結構

```
SEO_article_transfer/
├── main.py                       # 主程式入口（工具選單）
├── requirements.txt              # 依賴套件
├── article_number.txt            # 文章編號
├── settings.json                 # 設定檔（自動產生）
├── src/                          # 原始碼
│   ├── tp_editor_gui.py         # TP 標記編輯器 ✨新
│   ├── seo_layout_gui.py        # 主工具 ⭐
│   ├── seo_article_gui.py       # 手動編輯
│   ├── docx_to_seo_html_gui.py  # Word 轉換
│   ├── tp_template_gui.py       # tp 解析
│   └── tp_template_parser.py    # 解析引擎
├── templates/                    # HTML 模板
│   ├── seo_layout.html          # 主模板
│   └── seo_article.html         # 範例
├── input_docs/                   # Word 檔案
├── output/                       # HTML 輸出
└── docs/                         # 詳細文件
```

---

## 🎨 GUI 功能

### 主題切換
- flatly（預設）、cosmo、darkly、morph、sandstone、solar

### 日期選擇器
- 支援視覺化日期選擇（需安裝 ttkbootstrap 或 tkcalendar）

### 即時預覽
- 瀏覽器預覽
- 內嵌預覽（需安裝 pywebview）

---

## 🔧 常見問題

### Q: 視窗沒有跳出？
A: 測試 tkinter：`python -m tkinter`

### Q: FAQ 沒有正確解析？
A: 
1. 檢查標記格式：`(tp_sec_qa)`, `(tp_h3_q)`, `(tp_ans)`
2. 使用「解析 FAQ 預覽」檢查結果

### Q: 缺少套件？
A: 執行 `pip install -r requirements.txt`

---

## 📚 文件

- **[README.md](./README.md)** - 本文件（快速開始）
- **[docs/README.md](./docs/README.md)** - 完整說明
- **[docs/SEO_TOOL_SPEC.md](./docs/SEO_TOOL_SPEC.md)** - 功能規格
- **[docs/TECHNICAL_DOCUMENTATION.md](./docs/TECHNICAL_DOCUMENTATION.md)** - 技術文件
- **[CHANGELOG.md](./CHANGELOG.md)** - 更新記錄

---

## 📝 技術資訊

**核心依賴：**
- python-docx >= 0.8.11
- Jinja2 >= 3.0.0

**選用套件：**
- ttkbootstrap >= 1.10.0（美化介面）
- tkcalendar >= 1.6.0（日期選擇）
- pywebview >= 4.0.0（內嵌預覽）

---

## 🤝 支援

如需技術支援或功能建議，請聯絡開發團隊。

---

**© 2025 SEO 文章工具**
