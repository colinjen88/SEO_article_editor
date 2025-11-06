# SEO Article Editor - 專案結構說明

> **版本：** v1.7  
> **更新日期：** 2025-11-04

## 如何啟動程式

**主程式入口：**
```bash
python SEO_Article_Editor.py
```

這會啟動 SEO 文章編輯器的視覺化介面（包含完整 SEO 控制與 Schema.org 支援）。

## 檔案結構

```
SEO_Article_Editor/
│
├── SEO_Article_Editor.py       # 主程式 (啟動這個檔案)
├── requirements.txt            # Python 套件依賴
├── settings.json              # 設定檔
├── article_number.txt         # 文章編號追蹤
│
├── src/
│   ├── tp_editor_gui.py       # SEO 文章編輯器 (主要程式)
│   ├── tp_template_parser.py  # TP 標記解析器
│   │
│   └── legacy/                # 舊版工具 (已封存)
│       ├── seo_layout_gui.py
│       ├── seo_article_gui.py
│       ├── docx_to_seo_html_gui.py
│       ├── tp_template_gui.py
│       └── convent_seo_article.py
│
├── templates/                 # HTML 樣板
│   ├── seo_article.html
│   └── seo_layout.html
│
├── input_docs/               # 輸入文件
├── output/                   # 輸出 HTML 檔案
│
└── docs/                     # 文件
    ├── README.md
    ├── SEO_TOOL_SPEC.md
    └── TECHNICAL_DOCUMENTATION.md
```

## 主要功能

### SEO 文章編輯器 (`src/tp_editor_gui.py`) - v1.7
- **視覺化編輯介面**（darkly 暗色主題）
- **階層式結構**:
  - H1 主標題
  - 前言區塊
  - H2 段落 (SecBlock)
    - H3 子段落 (H3Block) - 可多個
  - FAQ 區塊 (FaqBlock)
- **完整 SEO 控制** (10+ 欄位):
  - 作者、組織名稱
  - 發布日期、修改日期
  - 文章標題（Headline）、描述
  - 文章編號（自動遞增）
  - 作者型別（Organization/Person）
  - Publisher Logo URL、Publisher URL
  - Publisher Logo 寬高、sameAs 社群連結
- **Schema.org 結構化資料**:
  - 自動生成 Article JSON-LD
  - 自動生成 FAQPage JSON-LD（如有 FAQ）
- **三重預覽**:
  - 編輯分頁：左側編輯 + 右側 HTML 原始碼
  - Schema 預覽分頁：JSON-LD 結構化資料
  - 瀏覽器預覽：完整 CSS + 語意化 HTML
- **內容增強**:
  - 段落內容支援原生 HTML（可貼表格）
  - FAQ 答案支援 HTML/純文字切換
- **資料管理**:
  - JSON 格式儲存/載入（包含完整 SEO 資訊）
  - 語意化 HTML 匯出（`<article>`, `<section>` 標籤）

## 技術特色

- **介面主題**：ttkbootstrap darkly 風格（專業暗色）
- **編輯模式**：區塊式編輯（H1 + 前言 + H2 段落 + H3 子段落 + FAQ）
- **輸出格式**：符合 Schema.org Article + FAQPage 標準的語意化 HTML
- **資料格式**：JSON（包含完整 SEO metadata + 內容結構）
- **結構化資料**：自動生成雙 JSON-LD 腳本（Article + FAQPage）
- **預覽功能**：
  - 編輯分頁即時預覽（HTML 原始碼）
  - Schema 預覽分頁（JSON-LD）
  - 瀏覽器完整預覽（CSS + 語意化標籤）
- **內容支援**：HTML 表格、多段落、FAQ HTML 模式

## 使用流程

1. 啟動 `SEO_Article_Editor.py`
2. 填寫 **SEO 資訊區**（10+ 欄位）：
   - 作者、日期、組織、文章編號
   - 標題、描述
   - 作者型別、Publisher 資訊
3. 編輯 **文章內容**：
   - 填寫 H1 主標題
   - 填寫前言（選填）
   - 點擊「+ 段落」新增 H2 段落
   - 在段落內點擊「+ H3」新增子區塊
   - 點擊「+ QA」新增 FAQ 問答
   - 段落內容可直接貼入 HTML 表格
   - FAQ 可切換 HTML 模式
4. 查看 **預覽**：
   - 右側即時 HTML 原始碼預覽
   - 切換「Schema 預覽」分頁查看 JSON-LD
   - 點擊「🌐 在瀏覽器開啟」查看完整效果
5. **儲存與匯出**：
   - 點擊「儲存」存為 JSON 專案檔
   - 點擊「匯出HTML」產生完整 HTML 檔案

## 封存檔案說明

`src/legacy/` 資料夾中的檔案為舊版工具，功能已整合到新版編輯器中：
- `seo_layout_gui.py` - Word 轉 HTML 工具
- `seo_article_gui.py` - 舊版文章編輯器
- `docx_to_seo_html_gui.py` - DOCX 轉換工具
- `tp_template_gui.py` - TP 樣板編輯器
- `convent_seo_article.py` - 轉換工具程式

**注意：** 這些檔案保留僅供參考，不建議直接使用。主程式不依賴 legacy 目錄。

## 版本控制說明

### 不應納入版本控制的檔案
以下檔案已在 `.gitignore` 中排除：
- `settings.json` - 使用者個人設定（包含絕對路徑）
- `article_number.txt` - 文章編號追蹤（使用者資料）
- `output/*.html` - 除了 `preview_temp.html` 外的所有輸出檔案
- `__pycache__/` - Python 快取檔案
- `.vscode/` - IDE 設定檔

### 必須納入版本控制的檔案
- 所有 `.py` 程式檔案
- 所有 `.md` 文件檔案
- `requirements.txt` - 依賴套件清單
- `templates/` - HTML 模板
- `output/preview_temp.html` - 預覽範本

## 相關文件

- [README.md](README.md) - 專案說明
- [docs/SEO_TOOL_SPEC.md](docs/SEO_TOOL_SPEC.md) - 工具規格
- [docs/TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md) - 技術文件
- [CHANGELOG.md](CHANGELOG.md) - 更新紀錄

---

**作者**: Colinjen (colinjen88@gmail.com)
**最後更新**: 2025
