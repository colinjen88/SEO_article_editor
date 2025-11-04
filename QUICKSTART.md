# 🚀 快速啟動指南

## 最快速的開始方式

### 方式 1：主選單（推薦新手）

```powershell
python main.py
```

然後從圖形化選單選擇要使用的工具。

---

### 方式 2：直接啟動 TP 編輯器

```powershell
python main.py editor
```

或

```powershell
python src/tp_editor_gui.py
```

---

### 方式 3：啟動其他工具

```powershell
# SEO Layout GUI（完整功能）
python main.py layout

# SEO 文章編輯
python main.py article

# TP 模板解析
python main.py template

# Word 轉 HTML
python main.py docx
```

---

## 📝 首次使用建議

### 給新手

1. 執行 `python main.py editor` 啟動編輯器
2. 閱讀啟動時的範例文章
3. 試著修改範例，看右側預覽變化
4. 點擊工具列的快速插入按鈕試試
5. 點擊「瀏覽器預覽」看完整效果
6. 開始撰寫您的第一篇文章！

**預計學習時間：10-15 分鐘**

### 給進階使用者

1. 直接執行 `python main.py layout` 使用完整功能
2. 選擇 Word 檔案自動轉換
3. 或使用編輯器快速產出 tp 標記文本
4. 整合到您的工作流程

---

## 📚 文件位置

- **快速參考**：`docs/TP_QUICK_REFERENCE.md`
- **完整手冊**：`docs/TP_EDITOR_GUIDE.md`
- **範例文章**：`input_docs/example_tp_article.txt`
- **專案說明**：`README.md`

---

## 🆘 遇到問題？

1. 檢查 Python 版本：`python --version`（需 3.8+）
2. 安裝依賴：`pip install -r requirements.txt`
3. 測試 tkinter：`python -m tkinter`
4. 查看文件：`docs/TP_EDITOR_GUIDE.md`

---

## ⚡ 一鍵命令

```powershell
# 完整安裝並啟動
git clone <repository-url>
cd SEO_article_editor
pip install -r requirements.txt
python main.py editor
```

---

**祝您使用愉快！** 🎉
