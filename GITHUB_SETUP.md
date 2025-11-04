# 推送到 GitHub 的步驟

## ✅ 已完成
- [x] Git 儲存庫已初始化
- [x] 所有檔案已提交（16 個檔案，3247 行程式碼）
- [x] 建立了 initial commit

## 📝 接下來的步驟

### 1. 在 GitHub 建立新儲存庫

前往：https://github.com/new

**儲存庫設定：**
- **Repository name**: `SEO_article_transfer`
- **Description**: `SEO 文章自動化工具 - Word 轉 HTML，支援 tp 標記解析與 FAQ 結構化資料產生`
- **Visibility**: Public 或 Private（依需求選擇）
- ⚠️ **重要**: 不要勾選任何初始化選項（README、.gitignore、License）

### 2. 連結遠端儲存庫並推送

建立儲存庫後，GitHub 會顯示指令。執行以下命令（替換 YOUR_USERNAME）：

#### 選項 A：使用 HTTPS（推薦給初學者）
```powershell
git remote add origin https://github.com/YOUR_USERNAME/SEO_article_transfer.git
git branch -M main
git push -u origin main
```

#### 選項 B：使用 SSH（如果你已設定 SSH key）
```powershell
git remote add origin git@github.com:YOUR_USERNAME/SEO_article_transfer.git
git branch -M main
git push -u origin main
```

### 3. 驗證推送成功

推送完成後，前往你的 GitHub 儲存庫查看：
```
https://github.com/YOUR_USERNAME/SEO_article_transfer
```

## 🔐 如果使用 HTTPS 需要驗證

GitHub 不再接受密碼驗證，你需要使用：

1. **Personal Access Token (PAT)**
   - 前往：https://github.com/settings/tokens
   - 點擊 "Generate new token" → "Generate new token (classic)"
   - 勾選至少 `repo` 權限
   - 生成後複製 token（只會顯示一次！）
   - 推送時使用 token 代替密碼

2. **或使用 GitHub Desktop / Git Credential Manager**
   - 下載：https://desktop.github.com/

## 🚀 快速執行腳本

如果你想使用自動化腳本：

1. 編輯 `push_to_github.ps1`
2. 將 `$GITHUB_USERNAME = "YOUR_USERNAME"` 改為你的 GitHub 使用者名稱
3. 執行：
   ```powershell
   .\push_to_github.ps1
   ```

## 📚 後續推送（未來更新時）

完成初始設定後，未來要推送更新只需：

```powershell
git add .
git commit -m "你的更新說明"
git push
```

## ❓ 常見問題

**Q: 推送時要求輸入使用者名稱和密碼？**
A: 使用 Personal Access Token (PAT) 代替密碼

**Q: 出現 "remote origin already exists"？**
A: 先執行 `git remote remove origin`，再重新添加

**Q: 想改用 SSH？**
A: 執行以下命令：
```powershell
git remote set-url origin git@github.com:YOUR_USERNAME/SEO_article_transfer.git
```

## 📞 需要協助？

如果遇到問題，請告訴我：
1. 你的 GitHub 使用者名稱
2. 執行命令時的錯誤訊息
3. 是否已設定 Personal Access Token 或 SSH key
