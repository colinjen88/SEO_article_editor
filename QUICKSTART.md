# 🚀 快速啟動指南

> **版本：** v1.7  
> **更新日期：** 2025-11-04

## 最快速的開始方式

### 啟動 SEO 文章編輯器

```powershell
python SEO_Article_Editor.py
```

這會啟動視覺化編輯器，包含：
- ✅ 完整 SEO 控制（10+ 欄位）
- ✅ Schema.org JSON-LD 自動生成
- ✅ 三重預覽（編輯 + Schema + 瀏覽器）
- ✅ 語意化 HTML 輸出
- ✅ H1/H2/H3 階層結構 + FAQ

---

## 📦 安裝依賴（首次使用）

```powershell
pip install -r requirements.txt
```

主要套件：
- `ttkbootstrap` - darkly 暗色主題（強烈建議）
- 其他為 Python 內建套件（tkinter 等）

---

## 📝 首次使用建議

### 5 分鐘上手

1. 執行 `python SEO_Article_Editor.py` 啟動編輯器
2. 查看預載的範例內容（黃金投資指南）
3. 填寫 **SEO 資訊區**（作者、日期、標題等）
4. 點擊「**+ 段落**」新增 H2 區塊
5. 在段落內點擊「**+ H3**」新增子區塊
6. 點擊「**+ QA**」新增 FAQ
7. 查看右側即時預覽
8. 點擊「**🌐 在瀏覽器開啟**」查看完整效果
9. 切換到「**Schema 預覽**」分頁查看 JSON-LD
10. 點擊「**儲存**」存為 JSON 或「**匯出HTML**」產生完整檔案

**預計學習時間：5-10 分鐘**

### 進階功能

- **HTML 表格支援**：段落內容可直接貼入 `<table>` 標籤
- **FAQ HTML 模式**：勾選「HTML 模式」讓 FAQ 答案支援 HTML
- **Publisher 設定**：設定 Logo URL、尺寸、社群連結（sameAs）
- **作者型別**：切換 Organization（組織）或 Person（個人）

---

## 📚 文件位置

- **主要說明**：`README.md` - 完整使用指南
- **版本記錄**：`CHANGELOG.md` - 所有更新內容
- **現況報告**：`STATUS_REPORT_2025-11-04.md` - 專案狀態
- **專案結構**：`PROJECT_STRUCTURE.md` - 檔案架構說明
- **技術文件**：`docs/TECHNICAL_DOCUMENTATION.md` - 技術細節

---

## 🆘 遇到問題？

### 輸入欄位顏色異常（暗色看不清）？
這是 ttkbootstrap darkly 主題的已知問題。解決方案：
1. 重新啟動程式
2. 或修改 `src/tp_editor_gui.py` 最後一行，將 `themename="darkly"` 改為 `themename="flatly"`
3. 詳見 `README.md` 的「已知問題」章節

### 其他問題
1. 檢查 Python 版本：`python --version`（需 3.8+）
2. 安裝依賴：`pip install -r requirements.txt`
3. 測試 tkinter：`python -m tkinter`
4. 查看完整文件：`README.md`

---

## ⚡ 一鍵安裝與啟動

```powershell
# 完整安裝並啟動
git clone <repository-url>
cd SEO_article_editor
pip install -r requirements.txt
python SEO_Article_Editor.py
```

---

## 🎯 專案特色

- ✅ **零學習曲線**：完全視覺化，無需標記語法
- ✅ **SEO 完整度**：包含所有 Google 建議的結構化資料
- ✅ **專業輸出**：語意化 HTML + JSON-LD + 內嵌 CSS
- ✅ **彈性編輯**：支援 HTML 表格、多層標題、FAQ
- ✅ **即時預覽**：所見即所得，三種預覽模式

---

**祝您使用愉快！** 🎉  
**© 2025 SEO Article Editor v1.7**
