# SEO文章工具 - 技術文件說明

## 專案概述

本專案是一個完整的SEO文章自動化生成系統，專為將Word文件轉換為符合SEO標準的HTML文章而設計。系統支援多種輸入模式和輸出格式，並自動生成FAQ結構化資料以提升搜尋引擎優化效果。

## 系統架構

### 核心模組架構圖
```
SEO文章工具系統
├── GUI界面層
│   ├── seo_article_gui.py          # 手動編輯界面
│   ├── docx_to_seo_html_gui.py     # Word轉換界面
│   ├── seo_layout_gui.py           # 模板化界面（主要）
│   └── tp_template_gui.py          # tp標記解析界面
├── 核心處理層
│   ├── tp_template_parser.py       # tp標記解析引擎
│   └── convent_seo_article.py      # 基礎Word轉換
├── 模板與配置層
│   ├── seo_article.html            # 完整範例模板
│   ├── seo_layout.html             # 變數化模板
│   └── article_number.txt          # 文章編號管理
└── 輸出層
    └── 自動生成的HTML文件
```

## 詳細模組分析

### 1. GUI界面模組

#### 1.1 seo_article_gui.py - 手動文章編輯工具
**功能描述：** 提供手動輸入文章內容的GUI界面

**核心功能：**
- 手動輸入主標題（h1）
- 動態新增段落（section + h2）
- 手動輸入FAQ問答對（最多3組）
- 自動生成SEO結構化資料
- 即時預覽和HTML輸出

**技術特點：**
- 使用tkinter.ScrolledText支援多行文字輸入
- 動態表單生成（add_section方法）
- 自動FAQ JSON-LD生成
- 檔案對話框整合

**使用場景：** 適合需要完全手動控制文章內容的用戶

#### 1.2 docx_to_seo_html_gui.py - Word轉HTML工具
**功能描述：** 直接將Word文件轉換為SEO HTML

**核心功能：**
- Word文件選擇和解析
- 自動標題層級識別（Heading 1-3）
- 清單和表格自動轉換
- 基本SEO結構化資料生成

**技術特點：**
- 使用python-docx庫解析Word文件
- 自動樣式識別（style.name.lower()）
- 表格結構保持（thead/tbody）
- 簡化的SEO資料生成

**使用場景：** 適合已有Word文件需要快速轉換的用戶

#### 1.3 seo_layout_gui.py - 模板化文章生成工具（推薦）
**功能描述：** 結合Word文件和HTML模板的完整解決方案

**核心功能：**
- 完整的欄位管理（作者、日期、標題、描述、組織、文章編號）
- 自動文章編號管理
- Word文件選擇和模板文件選擇
- 自動tp標記解析
- 動態FAQ生成

**技術特點：**
- 文章編號自動化（get_article_number/set_article_number）
- 模板變數替換系統
- 正則表達式 FAQ 解析（tp_sec_qa / tp_h3_q / tp_ans，多行答案）
- FAQ JSON-LD 安全生成（以 JSON 物件更新，不使用正則直接替換）
- FAQ 區塊缺失時自動插入 `<section id="faq-section">`
- 預設輸出 `output_YYYYMMDD[_N].html`

**使用場景：** 主要推薦使用，功能最完整

#### 1.4 tp_template_gui.py - tp標記模板解析工具
**功能描述：** 專門處理Word文件中的tp標記語法

**核心功能：**
- tp標記語法解析
- 自動HTML結構生成
- FAQ結構化資料生成
- 自動檔案命名

**技術特點：**
- 正則表達式標記識別
- 狀態機解析邏輯
- 自動檔案命名（日期+流水號）

**使用場景：** 適合使用tp標記語法的專業用戶

### 2. 核心處理引擎

#### 2.1 tp_template_parser.py - tp標記解析核心
**功能描述：** 解析Word文件中的tp標記並生成對應HTML結構

**支援的tp標記：**
```python
TP_H1 = r'\(tp_h1\)(.*)'        # 主標題
TP_H2 = r'\(tp_h2\)(.*)'        # 副標題
TP_H3 = r'\(tp_h3\)(.*)'        # 小標題
TP_SEC = r'\(tp_sec\)'          # 段落區塊開始
TP_SEC_QA = r'\(tp_sec_qa\)'    # FAQ區塊開始
TP_H3_Q = r'\(tp_h3_q\)(.*)'    # FAQ問題
TP_ANS = r'\(tp_ans\)(.*)'      # FAQ答案
TP_MARK = r'\(tp_[a-zA-Z0-9_]+\)' # 通用標記識別
```

**解析邏輯：**
1. 逐行掃描Word文件內容
2. 使用正則表達式識別tp標記
3. 根據標記類型生成對應HTML結構
4. 收集FAQ問答對用於結構化資料生成
5. 保持內容的層次結構

**技術特點：**
- 狀態機解析模式
- 動態 FAQ 收集
- 解析起始重置全域狀態（避免跨次殘留）
- JSON 安全組裝（FAQ 列表與 JSON-LD）
- 模組化設計

#### 2.2 convent_seo_article.py - 基礎Word轉換
**功能描述：** 提供基本的Word到HTML轉換功能

**核心功能：**
- Word文件段落解析
- 樣式識別和轉換
- 表格結構轉換
- 基本SEO結構化資料生成

### 3. 模板與配置系統

#### 3.1 seo_article.html - 完整範例模板
**功能描述：** 提供完整的SEO文章範例，包含所有樣式和結構

**包含內容：**
- 完整的CSS樣式表
- SEO結構化資料範例
- 文章內容結構範例
- FAQ區塊範例

#### 3.2 seo_layout.html - 變數化模板
**功能描述：** 使用變數標記的模板文件，支援動態內容替換

**支援的變數：**
```html
{{author_name}}      # 作者名稱
{{TheDate}}          # 文章日期
{{headline}}         # 文章標題
{{description}}      # 文章描述
{{OrganizationName}} # 組織名稱
{{article_number}}   # 文章編號
{{Question1}}        # FAQ問題1
{{Answer1}}          # FAQ答案1
{{Question2}}        # FAQ問題2
{{Answer2}}          # FAQ答案2
{{Question3}}        # FAQ問題3
{{Answer3}}          # FAQ答案3
```

#### 3.3 article_number.txt - 文章編號管理
**功能描述：** 管理文章編號的自動遞增

**管理機制：**
- 自動讀取當前編號
- 支援手動修改
- 確認更新機制
- 持久化儲存

### 4. SEO結構化資料系統

#### 4.1 JSON-LD結構
系統自動生成符合Schema.org標準的結構化資料：

```json
{
    "@context": "https://schema.org",
    "@type": "Article",
    "author": {"@type": "Organization", "name": "作者名稱"},
    "dateModified": "日期",
    "datePublished": "日期",
    "description": "文章描述",
    "headline": "文章標題",
    "mainEntity": {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "acceptedAnswer": {"@type": "Answer", "text": "答案"},
                "name": "問題"
            }
        ]
    },
    "mainEntityOfPage": {"@id": "URL", "@type": "WebPage"},
    "publisher": {"@type": "Organization", "name": "組織名稱"}
}
```

#### 4.2 FAQ動態生成
- 自動從Word文件解析FAQ內容
- 動態生成對應數量的問答對
- 同步更新HTML內容和JSON-LD資料

## 技術規格

### 開發環境
- **程式語言：** Python 3.x
- **GUI框架：** tkinter
- **Word處理：** python-docx
- **正則表達式：** re模組
- **檔案處理：** os, datetime模組

### 依賴套件
```python
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import docx
import json
import os
import re
from datetime import datetime
```

### 檔案命名規則
- 輸出檔案：`output_YYYYMMDD.html`
- 重複檔案：`output_YYYYMMDD_N.html`（N為流水號）
- 自動日期生成：使用當前日期

## 使用流程

### 1. 手動編輯模式
```
啟動 seo_article_gui.py
↓
輸入文章基本資訊
↓
新增段落內容
↓
輸入FAQ問答
↓
生成HTML檔案
```

### 2. Word轉換模式
```
啟動 docx_to_seo_html_gui.py
↓
選擇Word檔案
↓
設定SEO參數
↓
生成HTML檔案
```

### 3. 模板模式（推薦）
```
啟動 seo_layout_gui.py
↓
設定所有欄位
↓
選擇Word檔案和模板
↓
自動解析並生成HTML
```

### 4. tp標記模式
```
在Word中使用tp標記語法
↓
啟動 tp_template_gui.py
↓
選擇Word檔案
↓
自動解析並生成HTML
```

## 樣式系統

### CSS樣式特點
- **字體：** Noto Sans TC / Noto Serif TC（中文優化）
- **主題色：** 金色系（#b08d57, #D8AB4C）
- **響應式：** 支援各種螢幕尺寸
- **專業設計：** 表格、清單、標題層次分明

### 樣式結構
```css
.seo-article-content          # 主容器
├── h1, h2, h3               # 標題層級
├── p                        # 段落文字
├── ul, li                   # 清單項目
├── table, th, td            # 表格結構
├── .intro-summary           # 摘要區塊
└── .article-footer          # 文章頁尾
```

## 錯誤處理機制

### 1. 檔案驗證
- Word檔案存在性檢查
- 模板檔案存在性檢查
- 檔案格式驗證

### 2. 內容驗證
- 必填欄位檢查
- FAQ格式驗證
- 文章編號格式檢查

### 3. 輸出處理
- 檔案覆蓋保護
- 自動備份機制
- 錯誤訊息提示

## 擴展性設計

### 1. 模組化架構
- 各功能模組獨立
- 易於新增功能
- 便於維護和更新

### 2. 模板系統
- 支援自訂HTML模板
- 變數替換機制
- 樣式自訂能力

### 3. 標記系統
- 可擴展的tp標記語法
- 正則表達式規則
- 自訂解析邏輯

## 最佳實踐建議

### 1. 使用建議
- **主要工具：** 推薦使用`seo_layout_gui.py`
- **Word準備：** 使用tp標記語法組織內容
- **模板管理：** 定期更新HTML模板
- **編號管理：** 定期確認文章編號

### 2. 內容組織
- 使用清晰的標題層級
- FAQ內容要完整且相關
- 保持文章結構的一致性
- 注意SEO關鍵字密度

### 3. 技術維護
- 定期備份模板文件
- 監控文章編號檔案
- 測試新功能前先備份
- 保持依賴套件更新

## 故障排除

### 常見問題
1. **Word檔案無法開啟：** 檢查檔案格式和路徑
2. **FAQ解析失敗：** 檢查tp標記語法
3. **HTML輸出錯誤：** 檢查模板檔案完整性
4. **文章編號問題：** 檢查article_number.txt權限

### 除錯步驟
1. 檢查錯誤訊息
2. 驗證輸入檔案
3. 檢查模板完整性
4. 重新啟動程式
5. 檢查檔案權限

## 修正記錄

### v1.1 修正 (2025年1月)
**修正內容：**
1. **正則表達式群組編號錯誤**
   - 修正 `tp_template_parser.py` 中的 `r'\2'` 改為 `r'\1'`
   - 修正 `tp_template_gui.py` 中的相同問題
   - 影響：標題和FAQ內容無法正確提取

2. **FAQ解析邏輯問題**
   - 重新設計FAQ section的解析邏輯
   - 添加 `in_faq_section` 狀態追蹤
   - 確保FAQ section正確開始和結束
   - 影響：FAQ內容無法正確分組到專用section

3. **Section結束標籤問題**
   - 修正section區塊的結束條件
   - 從 `not re.match(TP_SEC, lines[i])` 改為 `not re.match(TP_MARK, lines[i])`
   - 影響：section內容可能被錯誤截斷

**測試結果：**
- tp標記解析功能正常
- FAQ問答對正確提取和分組
- HTML結構輸出正確
- JSON-LD結構化資料生成正常

### v1.2 強化 (2025年9月)
**變更內容：**
1. JSON-LD 更新改為以 JSON 物件解析與回寫，消除正則替換風險
2. `seo_layout_gui.py` 若缺 FAQ 區塊會自動插入
3. 新增預設輸出檔名建議，避免覆蓋舊檔
4. `tp_template_parser.py` 解析前重置全域狀態，避免多次執行的殘留問題
5. `tp_template_gui.py`、`tp_template_parser.py` 的 FAQ JSON-LD 生成改為 JSON 安全組裝

---

---

## 📦 依賴套件管理

### requirements.txt
專案依賴已整理至 `requirements.txt`，包含：

**核心依賴（必需）：**
- python-docx >= 0.8.11 - Word 文件解析
- Jinja2 >= 3.0.0 - 模板引擎

**選用依賴（增強功能）：**
- ttkbootstrap >= 1.10.0 - GUI 美化與主題
- tkcalendar >= 1.6.0 - 日期選擇器
- pywebview >= 4.0.0 - 內嵌 HTML 預覽

### 安裝方式
```powershell
pip install -r requirements.txt
```

---

## 🗂️ 專案組織

### 目錄結構說明

- **`main.py`** - 程式入口點，載入 `src/seo_layout_gui.py`
- **`src/`** - 所有原始碼模組
- **`templates/`** - HTML 模板檔案
- **`input_docs/`** - 輸入的 Word 檔案
- **`output/`** - 產生的 HTML 檔案
- **`docs/`** - 專案文件
- **`.gitignore`** - Git 版本控制忽略規則
- **`requirements.txt`** - Python 依賴套件清單
- **`article_number.txt`** - 文章編號管理
- **`settings.json`** - 使用者設定（自動產生）

---

## 🎯 主程式入口

### main.py
```python
import os
import sys
import runpy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(BASE_DIR, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# 執行主要 GUI 工具
runpy.run_path(os.path.join(src_dir, 'seo_layout_gui.py'), run_name='__main__')
```

這種設計的優點：
- 統一入口，方便使用
- 動態載入，不需要修改 PYTHONPATH
- 可以輕易切換要執行的工具

---

## 🔄 版本歷史

### v1.3 (2025-11-03)
**專案整理與文件更新**
- 整理專案目錄結構
- 新增 `main.py` 統一入口
- 新增 `.gitignore` 版本控制規則
- 新增 `requirements.txt` 依賴管理
- 新增根目錄 `README.md` 快速開始文件
- 更新所有文件至最新版本
- 移動測試檔案至適當目錄

### v1.2 (2025-09-15)
**JSON-LD 與 FAQ 強化**
- JSON-LD 更新改為以 JSON 物件解析與回寫，消除正則替換風險
- `seo_layout_gui.py` 若缺 FAQ 區塊會自動插入
- 新增預設輸出檔名建議，避免覆蓋舊檔
- `tp_template_parser.py` 解析前重置全域狀態
- FAQ JSON-LD 生成改為 JSON 安全組裝

### v1.1 (2025-01-15)
**正則表達式與解析邏輯修正**
- 修正 `tp_template_parser.py` 中的正則群組編號錯誤
- 修正 `tp_template_gui.py` 中的相同問題
- 重新設計 FAQ section 解析邏輯
- 添加 `in_faq_section` 狀態追蹤
- 修正 section 結束標籤問題

### v1.0 (2024-09-15)
**初始版本**
- 完成基本 Word 轉 HTML 功能
- 實作 tp 標記解析系統
- 建立 GUI 工具集
- SEO 結構化資料自動生成

---

**文件版本：** 1.3  
**最後更新：** 2025-11-03  
**維護者：** SEO 工具開發團隊
