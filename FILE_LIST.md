# SEO Article Editor - 檔案清單

> **版本：** v1.7  
> **更新日期：** 2025-11-04

## 📂 根目錄檔案

### 主要執行檔
- `SEO_Article_Editor.py` - **主程式入口**，啟動視覺化編輯器
- `clean.ps1` - 專案清理腳本（清除快取、暫存檔等）
- `push_to_github.ps1` - GitHub 推送腳本

### 設定與資料檔
- `requirements.txt` - Python 依賴套件清單
- `settings.json` - 使用者設定檔（自動生成）
- `article_number.txt` - 文章編號追蹤（自動遞增）
- `.gitignore` - Git 版本控制忽略清單

### 說明文件
- `README.md` - **主要說明文件**（使用指南）
- `CHANGELOG.md` - 版本更新記錄
- `QUICKSTART.md` - 快速啟動指南
- `PROJECT_STRUCTURE.md` - 專案結構說明
- `STATUS_REPORT_2025-11-04.md` - 專案現況報告
- `GITHUB_SETUP.md` - GitHub 設定說明
- `FILE_LIST.md` - 本檔案（檔案清單）

---

## 📁 src/ 目錄

### 主要程式
- `tp_editor_gui.py` - **核心編輯器**（747 行）
  - `H3Block` 類別：管理 H3 子區塊
  - `SecBlock` 類別：管理 H2 段落
  - `FaqBlock` 類別：管理 FAQ 問答
  - `Editor` 類別：主編輯器介面與邏輯

### 輔助程式
- `tp_template_parser.py` - TP 標記解析器（備用）

### legacy/ 子目錄（舊版工具，已封存）
- `seo_layout_gui.py` - 舊版 SEO Layout 工具
- `seo_article_gui.py` - 舊版文章編輯器
- `docx_to_seo_html_gui.py` - Word 轉 HTML 工具
- `tp_template_gui.py` - 舊版 TP 模板編輯器
- `convent_seo_article.py` - 轉換工具

**註：** legacy 目錄僅供參考，功能已整合至新版編輯器。

---

## 📁 docs/ 目錄

### 完整文件
- `README.md` - 文件目錄索引
- `TECHNICAL_DOCUMENTATION.md` - 技術架構文件
- `SEO_TOOL_SPEC.md` - SEO 工具規格說明
- `HTML_MODE_GUIDE.md` - HTML 模式使用指南
- `PROJECT_COMPLETION_REPORT.md` - 專案完成報告
- `TP_EDITOR_GUIDE.md` - TP 編輯器指南（舊版）
- `TP_QUICK_REFERENCE.md` - TP 快速參考（舊版）

---

## 📁 templates/ 目錄

HTML 模板檔案（用於匯出）：
- `seo_article.html` - 文章模板
- `seo_layout.html` - 版面模板

---

## 📁 output/ 目錄

HTML 輸出資料夾：
- `preview_temp.html` - 瀏覽器預覽暫存檔（自動生成）
- `*.html` - 使用者匯出的 HTML 檔案

**註：** 此目錄的檔案會被 `.gitignore` 忽略（除了 `preview_temp.html`）

---

## 📁 input_docs/ 目錄

範例與輸入文件資料夾（備用）

---

## 🗑️ 不需要的檔案（可安全刪除）

### 已清理
以下檔案已在 2025-11-04 清理：
- `output/20251002-第2篤.html` ✓
- `output/20251002.html` ✓
- `output/output_20250930.html` ✓
- `output/preview.html` ✓
- `output/Untitled-2.html` ✓
- `__pycache__/` 目錄 ✓
- `src/__pycache__/` 目錄 ✓

### 可選清理
以下檔案可根據需求保留或刪除：
- `docs/TP_EDITOR_GUIDE.md` - 舊版 TP 編輯器指南（功能已整合）
- `docs/TP_QUICK_REFERENCE.md` - 舊版 TP 快速參考（功能已整合）
- `src/legacy/` 整個目錄 - 舊版工具（僅供參考）

---

## 📊 檔案統計

### 程式碼檔案
- **主要程式**：2 個（`SEO_Article_Editor.py`, `tp_editor_gui.py`）
- **舊版程式**：5 個（`src/legacy/` 內）
- **總行數**：約 1,500 行（包含舊版）

### 文件檔案
- **說明文件**：12 個
- **技術文件**：5 個

### 模板與資料
- **HTML 模板**：2 個
- **設定檔**：3 個

---

## 🔍 快速查找

### 我想...

**啟動程式**
→ `SEO_Article_Editor.py`

**看使用說明**
→ `README.md`

**查版本更新**
→ `CHANGELOG.md`

**看技術細節**
→ `docs/TECHNICAL_DOCUMENTATION.md`

**查專案現況**
→ `STATUS_REPORT_2025-11-04.md`

**修改程式**
→ `src/tp_editor_gui.py`

**清理專案**
→ 執行 `clean.ps1`

**查看輸出**
→ `output/` 目錄

---

## 🚀 建議閱讀順序

### 新手
1. `README.md` - 了解基本功能
2. `QUICKSTART.md` - 5 分鐘快速上手
3. 啟動 `SEO_Article_Editor.py` 開始使用

### 進階使用者
1. `STATUS_REPORT_2025-11-04.md` - 完整專案現況
2. `CHANGELOG.md` - 版本更新歷史
3. `docs/TECHNICAL_DOCUMENTATION.md` - 技術架構

### 開發者
1. `PROJECT_STRUCTURE.md` - 專案結構
2. `src/tp_editor_gui.py` - 核心程式碼
3. `docs/TECHNICAL_DOCUMENTATION.md` - 技術細節

---

**維護：** Colinjen (colinjen88@gmail.com)  
**最後更新：** 2025-11-04
