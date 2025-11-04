# SEO Article Editor - 專案結構說明

## 如何啟動程式

**主程式入口:**
```bash
python SEO_Article_Editor.py
```

這會啟動 SEO 文章編輯器的視覺化介面。

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

### SEO 文章編輯器 (`src/tp_editor_gui.py`)
- 視覺化編輯介面
- 支援階層式結構:
  - H1 標題
  - H2 段落 (SecBlock)
    - H3 子段落 (H3Block)
  - FAQ 區塊
- SEO 欄位:
  - 作者、組織名稱
  - 發布日期、修改日期
  - 文章標題、描述
  - 文章編號 (自動遞增)
- 即時預覽
- 瀏覽器預覽
- FAQ 預覽分頁
- JSON 格式儲存/載入
- 輸出 HTML Schema 文章

## 技術特色

- **介面主題**: ttkbootstrap darkly 風格
- **編輯模式**: 區塊式編輯 (H2 段落 + H3 子段落)
- **輸出格式**: 符合 Schema.org Article 標準的 HTML
- **資料格式**: JSON (包含 SEO metadata)
- **預覽功能**: 
  - 視窗內即時預覽 (階層式縮排)
  - 瀏覽器完整預覽
  - FAQ 專用預覽分頁

## 使用流程

1. 啟動 `SEO_Article_Editor.py`
2. 填寫 SEO 欄位 (作者、日期、標題等)
3. 編輯文章內容:
   - 使用 "+" 按鈕新增 H2 段落
   - 在段落內使用 "+" 按鈕新增 H3 子段落
   - 切換到 FAQ 預覽分頁編輯常見問答
4. 隨時查看預覽或在瀏覽器中預覽
5. 儲存為 JSON (File > Save) 或輸出 HTML (File > Output HTML)

## 封存檔案說明

`src/legacy/` 資料夾中的檔案為舊版工具,功能已整合到新版編輯器中:
- `seo_layout_gui.py` - Word 轉 HTML 工具
- `seo_article_gui.py` - 舊版文章編輯器
- `docx_to_seo_html_gui.py` - DOCX 轉換工具
- `tp_template_gui.py` - TP 樣板編輯器
- `convent_seo_article.py` - 轉換工具程式

這些檔案保留供參考,但不建議直接使用。

## 相關文件

- [README.md](README.md) - 專案說明
- [docs/SEO_TOOL_SPEC.md](docs/SEO_TOOL_SPEC.md) - 工具規格
- [docs/TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md) - 技術文件
- [CHANGELOG.md](CHANGELOG.md) - 更新紀錄

---

**作者**: Colinjen (colinjen88@gmail.com)
**最後更新**: 2025
