# GitHub 推送設定腳本
# 請先在 GitHub 建立名為 SEO_article_transfer 的新儲存庫

# 設定你的 GitHub 使用者名稱
$GITHUB_USERNAME = "YOUR_USERNAME"  # 請修改這裡

# 確認當前分支
Write-Host "==> 當前 Git 狀態" -ForegroundColor Cyan
git status

# 重新命名分支為 main（如果需要）
Write-Host "`n==> 將分支重新命名為 main" -ForegroundColor Cyan
git branch -M main

# 新增遠端儲存庫（HTTPS）
Write-Host "`n==> 新增遠端儲存庫" -ForegroundColor Cyan
git remote add origin "https://github.com/$GITHUB_USERNAME/SEO_article_transfer.git"

# 檢查遠端設定
Write-Host "`n==> 檢查遠端設定" -ForegroundColor Cyan
git remote -v

# 推送到 GitHub
Write-Host "`n==> 推送到 GitHub" -ForegroundColor Cyan
Write-Host "即將執行: git push -u origin main" -ForegroundColor Yellow
Write-Host "這將會要求你輸入 GitHub 帳號密碼或 Personal Access Token" -ForegroundColor Yellow
Write-Host "按 Enter 繼續，或 Ctrl+C 取消..." -ForegroundColor Yellow
Read-Host

git push -u origin main

Write-Host "`n==> 完成！" -ForegroundColor Green
Write-Host "你的專案已成功推送到 GitHub" -ForegroundColor Green
Write-Host "儲存庫網址: https://github.com/$GITHUB_USERNAME/SEO_article_transfer" -ForegroundColor Green
