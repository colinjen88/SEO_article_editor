# SEO Article Editor v2.3

專為 SEO 文章寫作設計的視覺化編輯器，支援即時預覽、Schema JSON-LD 結構化資料生成、自訂 CSS 樣式以及 HTML 匯出功能。

## v2.3 更新重點
- **UI 優化**: 重新編排欄位配置，提升操作流暢度
- **預設值更新**: 作者與組織名稱預設為「炫麗黃金白銀交易所」
- **圖片設定**: 新增圖片路徑、寬度 (預設 100%) 與高度 (預設 auto) 設定
- **CSS 支援**: 新增外部 CSS 檔案瀏覽功能，並更新預設 CSS 樣式
- **主題優化**: 改用標準 tkinter，自訂深色主題 (#2c4c52)
- **Footer 更新**: 頁尾新增 "Design by Colinjen" 及聯絡連結

## 核心功能
- 🔍 **完整 SEO 控制**：作者、日期、組織、文章編號、描述等
- 📊 **Schema.org 結構化資料**：自動生成 Article 與 FAQPage JSON-LD
- 🏢 **進階出版者設定**：支援 Logo URL/尺寸、sameAs 社群連結
- 👁️ **多重預覽**：編輯 + HTML 原始碼 + Schema JSON-LD
- 🌐 **瀏覽器預覽**：一鍵在瀏覽器查看完整樣式
- 📤 **完整 HTML 輸出**：包含 Schema、CSS、內容與 Footer
- 🎨 **CSS 管理**：支援內置 Style 或外部 .css 檔引入
- 📋 **共用模板**：CSS 與 Footer 可共用編輯與儲存
- 💾 **JSON 專案儲存**：所有設定與內容完整保存
- 🎨 **Darkly 主題**：專業暗色介面（ttkbootstrap）

---

## 🚀 快速開始

### 方式一：使用執行檔（推薦給一般使用者）

**無需安裝 Python，直接執行！**

1. **下載執行檔**
   - 從 [Releases](../../releases) 下載最新版本的 `SEO_Article_Editor.exe`
   - 或自行打包（見下方說明）

2. **執行程式**
   - 雙擊 `SEO_Article_Editor.exe` 即可啟動
   - 首次執行可能需要 5-10 秒

3. **注意事項**
   - Windows 10/11 適用
   - 某些防毒軟體可能誤判，請加入信任清單
   - 執行檔大小約 7-8 MB

### 方式二：Python 環境執行（開發者）

#### 環境需求
- Python 3.8 以上
- tkinter（通常隨 Python 安裝）

#### 安裝步驟

1. **複製專案**
```powershell
git clone <repository-url>
cd SEO_article_editor
```

2. **安裝依賴**
```powershell
pip install -r requirements.txt
```
   *註：ttkbootstrap 提供 darkly 主題，強烈建議安裝*

3. **啟動編輯器**
```powershell
python SEO_Article_Editor.py
```

### 製作執行檔

如果想自行打包執行檔：

```powershell
# 方法 1：使用自動化腳本（推薦）
.\scripts\build_exe.ps1

# 方法 2：手動打包
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --add-data "templates;templates" --add-data "output;output" SEO_Article_Editor.py
```

完整打包說明請參考 [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

---

## 💡 使用指南

### 📋 SEO 資訊區

編輯器頂部提供完整的 SEO 元數據控制：

**基本資訊：**
- **作者**：內容創作者姓名
- **文章日期**：發布日期（YYYY-MM-DD）
- **修改日期**：最後修改日期
- **組織名稱**：發布組織/公司名稱
- **文章編號**：自動遞增的唯一識別碼
- **作者型別**：Organization（組織）或 Person（個人）

**進階設定：**
- **標題（Headline）**：SEO 標題，用於 JSON-LD
- **描述（Description）**：文章摘要描述
- **Publisher Logo**：出版者 Logo 圖片 URL
- **Publisher URL**：出版者官網 URL
- **Logo 寬/高**：Logo 圖片尺寸（像素）
- **Publisher sameAs**：社群媒體連結（逗號分隔）

### ✍️ 內容編輯

**核心操作：**
- 📝 **H1 主標題**：文章最上層標題（必填）
- 📄 **前言**：文章開場摘要（選填）
  - 可自訂 H2 標題（預設為「前言」）
  - 支援 **HTML 模式**切換（可插入 HTML 標籤）
- ➕ **+ 段落**：新增 H2 段落區塊
  - 每個段落包含：H2 標題 + 內容
  - 內容支援**原生 HTML**（可貼入表格）
  - 可新增多個 H3 子區塊
- ➕ **+ QA**：新增 FAQ 問答
  - 支援 HTML/純文字模式切換
  - FAQ 答案預設為純文字，可切換為 HTML

### 💾 專案檔案管理

- 📂 **開啟編輯檔**：載入之前儲存的 JSON 專案檔
- 💾 **儲存編輯檔**：將當前內容存為 JSON 格式（可隨時重新開啟繼續編輯）
- 📤 **匯出HTML**：生成最終的 HTML 檔案（包含完整 Schema JSON-LD）

### 👁️ 三重預覽

1. **編輯分頁**：左側編輯 + 右側 HTML 原始碼即時預覽
2. **Schema 預覽分頁**：查看生成的 JSON-LD 結構化資料
3. **瀏覽器預覽**：點擊工具列「🌐 在瀏覽器開啟」查看完整樣式

**介面說明：**

```
┌─────────────────────────────────────────────────┐
│ 📂開啟編輯檔 💾儲存編輯檔 📤匯出HTML           │
├───────────────┬─────────────────────────────────┤
│ 📌 H1         │  👁️ HTML 預覽                  │
│ [標題輸入]    │                                 │
│               │  <h1>黃金投資...</h1>           │
│ 📝 前言       │  <section class="intro">        │
│ H2標題: [前言]│    <h2>前言</h2>                │
│ ☑ HTML模式   │    <p>黃金一直...</p>           │
│ [前言輸入]    │  </section>                     │
│ 📄 主內容     │                         │
│ ┌───────────┐ │  <section>              │
│ │ H2: 標題  │ │    <h2>為什麼...</h2>  │
│ │ 內容...   │ │    <p>黃金具有...</p>  │
│ │ [+ H3]    │ │    <section>            │
│ │ ┌───────┐ │ │      <h3>小標...</h3>  │
│ │ │H3:小標│ │ │      <p>詳細...</p>    │
│ │ │內容...│ │ │    </section>           │
│ │ │[刪H3] │ │ │  </section>             │
│ │ └───────┘ │ │                         │
│ │[刪除段落] │ │  <section id="faq">     │
│ └───────────┘ │    <h2 class="hidden">  │
│ [+ 段落]      │    <h3>新手適合?</h3>   │
│               │    <p>非常適合...</p>   │
│ ❓ FAQ        │  </section>             │
│ ┌───────────┐ │                         │
│ │ Q: 問題?  │ │                         │
│ │ A: 答案   │ │                         │
│ │ [刪除]    │ │                         │
│ └───────────┘ │                         │
│ [+ QA]        │                         │
└───────────────┴─────────────────────────┘
```

### 📖 操作流程

1. **填寫 SEO 資訊**（必填）
   - 作者、組織名稱
   - 發布日期、修改日期（預設今日）
   - 文章標題（Headline）、描述
   - 文章編號（自動遞增）
   - 作者型別（Organization/Person）
   - Publisher 資訊（Logo、URL、社群連結等）

2. **編輯文章內容**
   - H1：主標題（必填）
   - 前言：開場摘要（選填）
   - 點擊「**+ 段落**」新增 H2 區塊
   - 填寫 H2 標題和內容（支援貼入 HTML 表格）
   - 在段落內點擊「**+ H3**」新增子區塊
   - H3 子區塊可包含標題和內容

3. **新增 FAQ 區塊**（選填）
   - 點擊「**+ QA**」新增問答
   - 填寫問題和答案
   - 勾選「**HTML 模式**」讓答案支援 HTML

4. **查看預覽**
   - **編輯分頁**：右側即時顯示 HTML 原始碼
   - **Schema 預覽分頁**：查看生成的 JSON-LD
   - 點擊「**🌐 在瀏覽器開啟**」查看完整效果

5. **儲存與匯出**
   - 點擊「**儲存**」存為 JSON 專案檔（可重複編輯）
   - 點擊「**匯出HTML**」產生完整 HTML 檔案（包含 CSS + JSON-LD）

### 快捷鍵與技巧

- **自動儲存**：輸入時自動觸發預覽更新（500ms 延遲）
- **段落換行**：內容區使用雙換行（Enter Enter）產生新段落
- **HTML 安全**：特殊字元自動跳脫（`<`, `>`, `&`）
- **FAQ 最佳實踐**：FAQ H2 自動套用 `visually-hidden` 類別

---

## 📂 專案結構

```
SEO_article_editor/
├── SEO_Article_Editor.py      # 主程式入口
├── src/
│   ├── tp_editor_gui.py      # 編輯器核心程式
│   └── legacy/               # 舊版工具（已棄用）
├── templates/                 # HTML 模板
├── output/                    # HTML 輸出資料夾
├── docs/                      # 完整文件
├── requirements.txt           # Python 依賴套件
├── article_number.txt         # 文章編號追蹤
└── README.md                  # 本文件
```

---

## 🎨 主題設定

本編輯器使用 **ttkbootstrap darkly 主題**（暗色專業風格）。

如要更換主題，編輯 `src/tp_editor_gui.py` 最後一行：
```python
root = tb.Window(themename="darkly")  # 改為其他主題名稱
```

支援主題：`flatly`、`cosmo`、`darkly`、`morph`、`sandstone`、`solar`

---

## 🔧 常見問題

### Q: 輸入欄位顏色異常（暗色背景看不清）？
**A:** 這是 ttkbootstrap darkly 主題的已知限制。目前程式已設定白底黑字，但主題可能覆蓋設定。解決方案：
1. 確認已安裝 `ttkbootstrap`：`pip install ttkbootstrap`
2. 重新啟動程式
3. 如持續異常，可編輯 `src/tp_editor_gui.py` 最後一行：
   ```python
   # 改用淺色主題
   root = tb.Window(themename="flatly")
   # 或使用原生 tkinter
   root = tk.Tk()
   ```

### Q: 如何產生多段落？
**A:** 在內容文字區使用雙換行（Enter Enter），會自動轉換為 `<p>` 段落。

### Q: 段落內容支援 HTML 嗎？
**A:** 是的！段落內容預設為 HTML 模式，可直接貼入 `<table>` 等標籤。FAQ 答案則可透過「HTML 模式」勾選框切換。

### Q: Schema JSON-LD 包含哪些資料？
**A:** 自動生成兩個結構化資料腳本：
1. **Article Schema**：包含作者、發布日期、標題、描述、出版者等
2. **FAQPage Schema**：包含所有 FAQ 問答（如有）

### Q: 匯出的 HTML 可以直接使用嗎？
**A:** 是的，匯出的 HTML 包含：
- 完整的語意化標籤（`<article>`, `<section>`）
- 內嵌 CSS 樣式
- JSON-LD 結構化資料
- 可直接部署或嵌入網頁

---

## � 已知問題

### 輸入欄位顏色問題
- **現象**：在 darkly 主題下，部分輸入欄位可能顯示暗色背景而非白色
- **原因**：ttkbootstrap 主題的 ttk 元件樣式覆蓋優先權問題
- **狀態**：已在程式中加入 `tk.Entry` 與 `option_add` 強制設定，但仍可能被主題覆蓋
- **暫時解決方案**：
  1. 改用 `flatly` 主題（淺色背景較不明顯）
  2. 或直接使用原生 tkinter（移除 ttkbootstrap）

---

## 📝 技術資訊

**核心依賴：**
- Python 3.8+
- tkinter（內建）
- ttkbootstrap >= 1.10.0（darkly 主題）

**架構特色：**
- 使用 `tk.Entry` 和 `tk.Text` 確保輸入框可控樣式
- 動態區塊管理（`SecBlock`, `H3Block`, `FaqBlock` 類別）
- JSON-LD 安全生成（避免字串拼接錯誤）
- 語意化 HTML 輸出（符合 HTML5 標準）
- 防抖動更新機制（500ms 延遲）

**輸出格式：**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>文章標題</title>
  <style>/* 內嵌 CSS */</style>
  <script type="application/ld+json">/* Article Schema */</script>
  <script type="application/ld+json">/* FAQPage Schema */</script>
</head>
<body>
  <article class="seo-article-content">
    <h1>標題</h1>
    <section class="intro-summary">...</section>
    <section>
      <h2>段落標題</h2>
      <section><h3>子標題</h3></section>
    </section>
    <section id="faq">...</section>
  </article>
</body>
</html>
```

---

## � 專案結構

```
SEO_article_editor/
├── SEO_Article_Editor.py      # 主程式入口
├── requirements.txt            # Python 依賴套件
├── README.md                   # 專案說明（本檔案）
├── CHANGELOG.md                # 版本變更記錄
├── QUICKSTART.md               # 快速啟動指南
├── BUILD_INSTRUCTIONS.md       # 執行檔製作說明
│
├── src/                        # 原始碼目錄
│   ├── tp_editor_gui.py        # 主編輯器 GUI（747 行）
│   ├── tp_template_parser.py   # 模板解析器
│   └── legacy/                 # 舊版工具（已棄用）
│
├── templates/                  # HTML 模板
│   ├── seo_article.html        # 文章模板
│   └── seo_layout.html         # 版面模板
│
├── scripts/                    # 工具腳本
│   ├── build_exe.ps1           # 自動打包腳本
│   ├── clean.ps1               # 清理腳本
│   └── push_to_github.ps1      # Git 推送腳本
│
├── docs/                       # 文件目錄
│   ├── TECHNICAL_DOCUMENTATION.md  # 技術文件
│   ├── HTML_MODE_GUIDE.md      # HTML 模式指南
│   ├── TP_EDITOR_GUIDE.md      # 編輯器使用指南
│   ├── TP_QUICK_REFERENCE.md   # 快速參考
│   └── archive/                # 歷史文件
│
├── output/                     # 輸出目錄
│   └── preview_temp.html       # 預覽暫存檔
│
├── input_docs/                 # 範例文件
│   └── example_tp_article.txt  # TP 格式範例
│
└── dist/                       # 執行檔輸出目錄
    └── SEO_Article_Editor.exe  # Windows 執行檔
```

---

## �📚 相關文件

- [CHANGELOG.md](CHANGELOG.md) - 完整版本變更記錄
- [QUICKSTART.md](QUICKSTART.md) - 快速啟動指南
- [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) - 執行檔製作說明
- [docs/TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md) - 技術架構說明
- [docs/HTML_MODE_GUIDE.md](docs/HTML_MODE_GUIDE.md) - HTML 模式使用指南
- [docs/TP_EDITOR_GUIDE.md](docs/TP_EDITOR_GUIDE.md) - 編輯器完整指南

---

**© 2025 SEO Article Editor v2.3**  
Produced by Colinjen (colinjen88@gmail.com)
