# SEO 文章編輯器 - 現況報告

**報告日期：** 2025-11-04  
**當前版本：** v1.7.0  
**狀態：** 🟡 功能完整，存在已知 UI 問題

---

## 📊 專案概況

### 基本資訊
- **專案名稱**：SEO Article Editor（SEO 文章編輯器）
- **主程式**：`SEO_Article_Editor.py`
- **核心模組**：`src/tp_editor_gui.py` (747 行)
- **介面框架**：tkinter + ttkbootstrap (darkly 主題)
- **資料格式**：JSON（專案檔）+ HTML（匯出檔）

### 專案定位
從原本的「多工具套件」演進為「專注的 SEO 文章編輯器」，提供：
- 視覺化表單編輯（無需標記語法）
- 完整 SEO 元數據控制
- Schema.org 結構化資料自動生成
- 語意化 HTML 輸出

---

## ✅ 已完成功能

### 1. 內容編輯功能
- ✅ H1 主標題輸入
- ✅ 前言區塊（多行文字）
- ✅ 動態 H2 段落（可新增/刪除）
- ✅ H2 段落內可新增多個 H3 子區塊
- ✅ H3 子區塊包含標題與內容
- ✅ 段落內容**支援原生 HTML**（可貼表格）
- ✅ 動態 FAQ 區塊（可新增/刪除）
- ✅ FAQ 答案支援 HTML/純文字切換

### 2. SEO 元數據控制
- ✅ 作者姓名
- ✅ 發布日期（預設今日）
- ✅ 修改日期（預設今日）
- ✅ 組織名稱
- ✅ 文章編號（自動遞增）
- ✅ 標題（Headline）
- ✅ 描述（Description）
- ✅ 作者型別（Organization/Person 切換）
- ✅ Publisher Logo URL
- ✅ Publisher URL
- ✅ Publisher Logo 寬度/高度
- ✅ Publisher sameAs（社群連結，逗號分隔）

### 3. 預覽與匯出
- ✅ 即時 HTML 原始碼預覽（右側面板）
- ✅ Schema JSON-LD 預覽（獨立分頁）
- ✅ 瀏覽器預覽（完整 CSS + 結構化資料）
- ✅ 匯出完整 HTML 檔案
  - 包含內嵌 CSS
  - 包含 Article Schema
  - 包含 FAQPage Schema（如有 FAQ）
  - 使用語意化標籤（article, section）

### 4. 資料管理
- ✅ JSON 格式儲存專案
- ✅ 開啟既有 JSON 專案
- ✅ 自動載入範例內容（首次啟動）
- ✅ 未儲存提醒機制
- ✅ 檔案路徑顯示

### 5. 使用者體驗
- ✅ 防抖動更新（500ms 延遲）
- ✅ 滾動條支援（左側編輯區）
- ✅ 滑鼠滾輪捲動
- ✅ 按鈕加大（+ 段落、+ QA 寬度 3 倍）
- ✅ 底部版本與作者資訊
- ✅ Darkly 暗色專業主題

---

## ⚠️ 已知問題

### 1. 輸入欄位顏色問題（高優先度）

**問題描述：**
- 在 ttkbootstrap darkly 主題下，部分輸入欄位（Entry/Text）可能顯示暗色背景，導致黑色文字看不清楚
- 預期：所有輸入欄位應顯示白底黑字（`bg="#ffffff"`, `fg="black"`）
- 實際：部分欄位仍顯示主題預設的暗色背景

**已嘗試的解決方案：**
1. ✅ 將所有輸入欄位從 `ttk.Entry` 改為 `tk.Entry`
2. ✅ 明確設定 `bg="#ffffff"` 和 `fg="black"`
3. ✅ 使用 `root.option_add()` 設定全域樣式
4. ✅ 配置 `ttk.Style()` 覆蓋 TEntry 樣式
5. ❌ 上述方法在部分系統/環境下仍可能被主題覆蓋

**根本原因：**
- ttkbootstrap 的主題系統對某些 tk 原生元件也有影響
- Tkinter 的樣式優先權在不同平台/版本可能有差異
- darkly 主題的 ttk 樣式覆蓋優先權高於 option_add

**影響範圍：**
- SEO 資訊區的所有輸入欄位
- H1、前言、段落、H3、FAQ 的所有輸入欄位
- 預覽區的 ScrolledText（已設定白底但可能被覆蓋）

**暫時解決方案：**
1. **選項 A**：改用淺色主題（如 flatly）
   - 修改 `src/tp_editor_gui.py` 最後一行：
   ```python
   root = tb.Window(themename="flatly")  # 改為 flatly
   ```
2. **選項 B**：完全移除 ttkbootstrap
   - 修改 `src/tp_editor_gui.py` 最後一行：
   ```python
   root = tk.Tk()  # 使用原生 tkinter
   ```
3. **選項 C**：使用者自行調整螢幕對比度/亮度（不建議）

**長期解決方案研究方向：**
- 完全自訂 ttkbootstrap 主題檔案
- 使用 CustomTkinter 或其他現代化 GUI 框架
- 建立 Web 版本（Flask + 前端框架）

---

## 📁 檔案結構

```
SEO_article_editor/
├── SEO_Article_Editor.py          # 主程式入口（啟動點）
├── article_number.txt              # 文章編號追蹤（自動遞增）
├── requirements.txt                # Python 依賴套件
├── CHANGELOG.md                    # 版本變更記錄
├── README.md                       # 使用說明（已更新至 v1.7）
├── STATUS_REPORT_2025-11-04.md    # 本報告
│
├── src/
│   ├── tp_editor_gui.py           # 編輯器核心（747 行）
│   ├── tp_template_parser.py     # TP 標記解析器（備用）
│   └── legacy/                     # 舊版工具（已棄用）
│       ├── seo_layout_gui.py
│       ├── seo_article_gui.py
│       ├── docx_to_seo_html_gui.py
│       └── tp_template_gui.py
│
├── templates/                      # HTML 模板（備用）
│   ├── seo_layout.html
│   └── seo_article.html
│
├── output/                         # HTML 輸出資料夾
│   ├── preview_temp.html          # 瀏覽器預覽暫存檔
│   └── *.html                      # 使用者匯出的檔案
│
├── docs/                           # 完整文件
│   ├── README.md
│   ├── TECHNICAL_DOCUMENTATION.md
│   ├── HTML_MODE_GUIDE.md
│   ├── TP_EDITOR_GUIDE.md
│   └── PROJECT_COMPLETION_REPORT.md
│
└── input_docs/                     # 範例檔案（備用）
```

---

## 🎯 核心程式分析

### `src/tp_editor_gui.py` 結構

**類別定義：**
1. **`H3Block`** (16-29 行)
   - 管理 H3 子區塊
   - 包含 H3 標題 + 內容
   - 可刪除

2. **`SecBlock`** (31-83 行)
   - 管理 H2 段落
   - 包含 H2 標題 + 內容 + H3 列表
   - 內容預設支援 HTML (`is_html = True`)
   - 可新增/刪除 H3 子區塊

3. **`FaqBlock`** (85-109 行)
   - 管理 FAQ 問答
   - 包含問題 + 答案
   - 答案支援 HTML/純文字切換 (`is_html` BooleanVar)

4. **`Editor`** (111-747 行)
   - 主編輯器類別
   - `_ui()` 方法：建立完整介面 (122-330 行)
   - `_gen()` 方法：生成 HTML 內容 (440-492 行)
   - `_gen_schema_jsonld()` 方法：生成 JSON-LD (362-438 行)
   - `sv()` / `_load()` 方法：儲存/載入專案 (537-607 行)
   - `ex()` 方法：匯出完整 HTML (609-639 行)

**關鍵方法：**
- **`_gen_schema_jsonld()`**：完整的 Schema.org 資料生成
  - 讀取所有 SEO 欄位
  - 生成 Article Schema（包含 author、publisher、datePublished 等）
  - 生成 FAQPage Schema（如有 FAQ）
  - 返回兩個獨立的 `<script>` 標籤

- **`_gen()`**：生成語意化 HTML
  - H1 使用 `<h1>` 標籤
  - 前言使用 `<section class="intro-summary">`
  - 段落使用 `<section>` + `<h2>`
  - H3 子區塊使用巢狀 `<section>` + `<h3>`
  - FAQ 使用 `<section id="faq">`

- **`ex()`**：匯出完整 HTML 檔案
  - 組合 CSS（內嵌樣式）
  - 組合 JSON-LD（兩個 script 標籤）
  - 使用 `<article class="seo-article-content">` 包裹內容

---

## 📊 資料格式

### JSON 專案檔格式

```json
{
  "seo": {
    "author": "炫麗鑫",
    "pub_date": "2025-11-04",
    "mod_date": "2025-11-04",
    "org_name": "Shiny黃金白銀",
    "article_num": "1",
    "headline": "黃金投資完整指南",
    "description": "了解黃金投資的優勢與策略",
    "author_type": "Organization",
    "publisher_logo_url": "https://pm.shiny.com.tw/images/logo.png",
    "publisher_url": "https://pm.shiny.com.tw/",
    "publisher_logo_width": "600",
    "publisher_logo_height": "60",
    "publisher_sameas": ["https://facebook.com/...", "https://twitter.com/..."]
  },
  "h1": "黃金投資指南",
  "intro": "黃金是重要的避險資產。",
  "sections": [
    {
      "h2": "為何投資?",
      "content": "<p>保值、避險。</p>",
      "h3s": [
        {
          "h3": "適合新手",
          "content": "黃金投資門檻低..."
        }
      ]
    }
  ],
  "faqs": [
    {
      "question": "適合新手嗎?",
      "answer": "非常適合。",
      "is_html": false
    }
  ]
}
```

### HTML 匯出檔格式

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>黃金投資指南</title>
  <style>/* 內嵌 CSS，包含 .seo-article-content 樣式 */</style>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "author": {"@type": "Organization", "name": "炫麗鑫"},
    "publisher": {
      "@type": "Organization",
      "name": "Shiny黃金白銀",
      "logo": {
        "@type": "ImageObject",
        "url": "https://pm.shiny.com.tw/images/logo.png",
        "width": 600,
        "height": 60
      },
      "url": "https://pm.shiny.com.tw/",
      "sameAs": ["https://facebook.com/...", "https://twitter.com/..."]
    },
    "headline": "黃金投資完整指南",
    "description": "了解黃金投資的優勢與策略",
    "datePublished": "2025-11-04",
    "dateModified": "2025-11-04",
    "mainEntityOfPage": {
      "@id": "https://pm.shiny.com.tw/news-detail.php?id=1",
      "@type": "WebPage"
    }
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "適合新手嗎?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "非常適合。"
        }
      }
    ]
  }
  </script>
</head>
<body>
  <article class="seo-article-content">
    <h1>黃金投資指南</h1>
    <section class="intro-summary">
      <h2>前言</h2>
      <p>黃金是重要的避險資產。</p>
    </section>
    <section>
      <h2>為何投資?</h2>
      <p>保值、避險。</p>
      <section>
        <h3>適合新手</h3>
        <p>黃金投資門檻低...</p>
      </section>
    </section>
    <hr />
    <section id="faq">
      <h2>常見問答 (Q&A)</h2>
      <h3>適合新手嗎?</h3>
      <p>非常適合。</p>
    </section>
  </article>
</body>
</html>
```

---

## 🔄 最近更新內容（v1.6 → v1.7）

### 主要新增
1. **完整 SEO 控制介面**（10+ 欄位）
2. **Schema.org JSON-LD 自動生成**（Article + FAQPage）
3. **HTML 模式支援**（段落 + FAQ）
4. **語意化 HTML 輸出**（article, section 標籤）
5. **Schema 預覽分頁**

### UI 改進嘗試
1. 將所有輸入改為 `tk.Entry` / `tk.Text`
2. 明確設定 `bg="#ffffff"`, `fg="black"`
3. 使用 `root.option_add()` 全域設定
4. 配置 `ttk.Style()` 覆蓋設定
5. 按鈕加大（width=20）
6. 底部加入版本號與作者連結

**結果：** 功能完整，但樣式問題仍存在於部分環境

---

## 🎯 建議後續行動

### 短期（緊急）
1. **UI 顏色問題**
   - 提供使用者快速切換主題的選項（內建在設定選單）
   - 或提供「移除 ttkbootstrap」的簡易指令

2. **文件完善**
   - ✅ 更新 README.md（已完成）
   - ✅ 更新 CHANGELOG.md（已完成）
   - ✅ 撰寫現況報告（本文件）
   - 補充「已知問題」章節到所有文件

### 中期（功能增強）
1. **圖片管理**
   - 新增「插��圖片」功能
   - 支援圖片 URL 輸入
   - 支援本機圖片上傳（Base64 或複製到 output/images/）
   - 在 JSON-LD 中加入 `image` 欄位

2. **內容增強**
   - 支援段落內容的表格編輯器（視覺化表格）
   - 支援列表編輯（ul/ol）
   - 支援粗體/斜體快捷按鈕

3. **SEO 增強**
   - 關鍵字密度分析
   - 字數統計與建議
   - H2/H3 數量建議
   - FAQ 數量建議

### 長期（架構升級）
1. **框架遷移**
   - 評估 CustomTkinter（更現代化的 tkinter）
   - 或考慮 Web 版本（Flask + Vue.js）
   - 或考慮 Electron 桌面版

2. **雲端整合**
   - 支援 Google Drive / Dropbox 同步
   - 多人協作編輯
   - 版本控制系統

3. **AI 整合**
   - AI 內容建議
   - SEO 關鍵字推薦
   - 自動生成描述

---

## 📈 效能與品質指標

### 程式碼品質
- ✅ 無語法錯誤（Pylance 檢查通過）
- ✅ 模組化設計（H3Block, SecBlock, FaqBlock, Editor）
- ✅ 功能分離（生成 HTML / 生成 JSON-LD / 儲存載入分開）
- ⚠️ 單一檔案過長（747 行，建議拆分）

### 使用者體驗
- ✅ 即時預覽（500ms 防抖動）
- ✅ 自動儲存提醒
- ✅ 檔案路徑顯示
- ✅ 範例內容載入
- ⚠️ 輸入欄位顏色問題（影響可讀性）

### SEO 合規性
- ✅ 完整 Schema.org 支援
- ✅ 語意化 HTML
- ✅ 元數據完整
- ✅ FAQ 結構化資料
- ✅ 符合 Google Search Console 要求

### 穩定性
- ✅ 錯誤處理（try-except）
- ✅ 資料驗證（hasattr 檢查）
- ✅ 預設值處理
- ⚠️ 跨平台樣式一致性待確認

---

## 🧪 測試狀況

### 已測試功能
- ✅ 新增/刪除段落
- ✅ 新增/刪除 H3
- ✅ 新增/刪除 FAQ
- ✅ HTML 模式切換（FAQ）
- ✅ 儲存/載入 JSON
- ✅ 匯出 HTML
- ✅ 瀏覽器預覽
- ✅ Schema 生成
- ✅ 所有 SEO 欄位儲存/載入

### 待測試項目
- ⏳ 大型文章（100+ 段落）效能
- ⏳ 複雜 HTML 表格貼入
- ⏳ 不同作業系統（Windows/Mac/Linux）
- ⏳ 不同 Python 版本（3.8/3.9/3.10/3.11）
- ⏳ 不同 ttkbootstrap 版本

### 已知 Bug
1. **輸入欄位顏色**（高優先度）
   - 如上述「已知問題」章節

---

## 📞 聯絡資訊

**專案維護：** Colinjen  
**Email：** colinjen88@gmail.com  
**版本：** v1.7.0  
**最後更新：** 2025-11-04

---

## 📝 總結

SEO 文章編輯器 v1.7 已完成核心功能開發，提供：
- ✅ 完整的視覺化編輯介面
- ✅ 專業的 SEO 元數據控制
- ✅ 標準的 Schema.org 結構化資料
- ✅ 語意化的 HTML 輸出
- ⚠️ 但存在 UI 樣式問題（ttkbootstrap 主題覆蓋）

**建議優先處理：**
1. 提供使用者快速切換主題的方式
2. 在 README 中明確標註已知問題
3. 考慮長期遷移到更可控的 GUI 框架

**整體評估：** 🟡 功能完整，實用性高，但 UI 體驗需改進

---

*本報告由 GitHub Copilot 協助整理，基於實際程式碼分析與開發歷程記錄。*
