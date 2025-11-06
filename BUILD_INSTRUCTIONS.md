# 執行檔製作說明

> **版本：** v1.7  
> **更新日期：** 2025-11-06

## 📦 如何製作執行檔

### 方法一：使用 PowerShell 腳本（推薦）

```powershell
# 執行自動打包腳本
.\build_exe.ps1
```

執行檔會產生在 `dist/SEO_Article_Editor.exe`

### 方法二：手動使用 PyInstaller

#### 1. 安裝 PyInstaller
```powershell
pip install pyinstaller
```

#### 2. 執行打包指令
```powershell
pyinstaller --noconfirm --onefile --windowed `
  --add-data "templates;templates" `
  --add-data "output;output" `
  SEO_Article_Editor.py
```

#### 參數說明
- `--noconfirm` - 不詢問，覆蓋舊檔案
- `--onefile` - 打包成單一 .exe 檔案
- `--windowed` - 不顯示命令提示字元視窗（GUI 模式）
- `--add-data "templates;templates"` - 包含 templates 目錄
- `--add-data "output;output"` - 包含 output 目錄

### 3. 輸出位置

執行檔會產生在：
```
dist/SEO_Article_Editor.exe
```

檔案大小約：**7-8 MB**

---

## 🚀 執行檔使用說明

### 執行方式

**方式 1：直接雙擊**
- 在 Windows 檔案總管中雙擊 `SEO_Article_Editor.exe`

**方式 2：命令列執行**
```powershell
.\SEO_Article_Editor.exe
```

### 注意事項

1. **首次執行可能較慢**
   - PyInstaller 打包的執行檔需要解壓暫存檔到臨時目錄
   - 首次啟動可能需要 5-10 秒

2. **防毒軟體警告**
   - 某些防毒軟體可能誤判 PyInstaller 打包的執行檔
   - 這是正常現象，請加入信任清單

3. **資料檔案**
   - `article_number.txt` 會在執行檔所在目錄自動建立
   - `output/` 目錄會儲存匯出的 HTML 檔案

4. **相依性**
   - 執行檔已包含所有 Python 依賴套件
   - 不需要安裝 Python 或任何套件
   - 可在任何 Windows 10/11 電腦執行

---

## 🔧 打包進階設定

### 自訂圖示

如果要使用自訂圖示：

```powershell
pyinstaller --noconfirm --onefile --windowed `
  --icon="icon.ico" `
  --add-data "templates;templates" `
  --add-data "output;output" `
  SEO_Article_Editor.py
```

### 包含額外檔案

如果需要包含其他檔案（如圖片、設定檔）：

```powershell
pyinstaller --noconfirm --onefile --windowed `
  --add-data "templates;templates" `
  --add-data "output;output" `
  --add-data "images;images" `
  --add-data "config.ini;." `
  SEO_Article_Editor.py
```

### 優化執行檔大小

使用 UPX 壓縮（需先安裝 UPX）：

```powershell
pyinstaller --noconfirm --onefile --windowed `
  --upx-dir="C:\path\to\upx" `
  --add-data "templates;templates" `
  --add-data "output;output" `
  SEO_Article_Editor.py
```

---

## 📂 打包後的目錄結構

```
SEO_article_editor/
├── build/                      # 打包暫存檔（可刪除）
├── dist/                       # 輸出目錄
│   └── SEO_Article_Editor.exe  # 主執行檔 ★
├── SEO_Article_Editor.spec     # PyInstaller 設定檔
└── ... (其他原始碼檔案)
```

---

## 🐛 常見問題排除

### Q1: 執行檔無法啟動？

**可能原因：**
1. 防毒軟體阻擋
2. 缺少 Visual C++ Redistributable

**解決方案：**
```powershell
# 檢查是否被防毒軟體隔離
# 安裝 Visual C++ Redistributable 2015-2022
# 下載：https://aka.ms/vs/17/release/vc_redist.x64.exe
```

### Q2: 執行時出現 "Failed to execute script" 錯誤？

**解決方案：**
```powershell
# 使用 --debug all 參數重新打包，查看詳細錯誤
pyinstaller --noconfirm --onefile --windowed --debug all `
  --add-data "templates;templates" `
  --add-data "output;output" `
  SEO_Article_Editor.py

# 或使用 console 模式查看錯誤訊息
pyinstaller --noconfirm --onefile --console `
  --add-data "templates;templates" `
  --add-data "output;output" `
  SEO_Article_Editor.py
```

### Q3: tkinter 相關錯誤？

**可能原因：** Python 環境缺少 tkinter

**解決方案：**
```powershell
# 確認 tkinter 可用
python -m tkinter

# 如果不可用，重新安裝 Python 並勾選 tcl/tk 選項
```

### Q4: ttkbootstrap 主題無法載入？

**解決方案：**
```powershell
# 確認 ttkbootstrap 已安裝
pip install ttkbootstrap

# 重新打包
pyinstaller --noconfirm --onefile --windowed `
  --hidden-import=ttkbootstrap `
  --add-data "templates;templates" `
  --add-data "output;output" `
  SEO_Article_Editor.py
```

---

## 🎯 分發執行檔

### 單一檔案分發

最簡單的方式：
1. 將 `dist/SEO_Article_Editor.exe` 複製給使用者
2. 使用者雙擊執行即可

### 完整套件分發

如果要包含說明文件：

```
SEO_Article_Editor_v1.7/
├── SEO_Article_Editor.exe     # 主程式
├── README.md                   # 使用說明
├── QUICKSTART.md              # 快速開始
└── 範例檔案/
    └── example_article.json   # 範例專案
```

壓縮成 ZIP 檔案分發。

---

## 📊 效能比較

| 執行方式 | 啟動時間 | 檔案大小 | 相依性 |
|---------|---------|---------|--------|
| Python 直接執行 | 1-2 秒 | ~1 MB | 需要 Python + 套件 |
| PyInstaller 執行檔 | 3-5 秒 | ~7-8 MB | 無需 Python |

---

## 🔐 程式碼簽章（選用）

如果要讓執行檔更可信，可以購買程式碼簽章憑證：

```powershell
# 使用 signtool 簽章（需要憑證）
signtool sign /f certificate.pfx /p password `
  /t http://timestamp.digicert.com `
  dist\SEO_Article_Editor.exe
```

---

## 📝 更新記錄

### 2025-11-06
- ✅ 首次建立執行檔打包說明
- ✅ 修正 `runpy.run_path()` 在 PyInstaller 中的相容性問題
- ✅ 改用 `from tp_editor_gui import main` 方式啟動
- ✅ 成功產生 7.3 MB 的單一執行檔

---

**製作者：** Colinjen (colinjen88@gmail.com)  
**最後更新：** 2025-11-06
