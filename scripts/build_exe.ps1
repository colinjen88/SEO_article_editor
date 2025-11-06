# SEO 文章編輯器 - 自動打包腳本
# 版本: v1.8
# 日期: 2025-11-06

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  SEO 文章編輯器 - 執行檔打包工具" -ForegroundColor Cyan
Write-Host "  版本: v1.8" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 檢查是否安裝 PyInstaller
Write-Host "[1/5] 檢查 PyInstaller..." -ForegroundColor Yellow
$pyinstallerCheck = pip show pyinstaller 2>$null
if (-not $pyinstallerCheck) {
    Write-Host "  未安裝 PyInstaller，正在安裝..." -ForegroundColor Red
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  安裝失敗！請手動執行: pip install pyinstaller" -ForegroundColor Red
        exit 1
    }
    Write-Host "  ✓ PyInstaller 安裝成功" -ForegroundColor Green
} else {
    Write-Host "  ✓ PyInstaller 已安裝" -ForegroundColor Green
}

# 清理舊的打包檔案
Write-Host ""
Write-Host "[2/5] 清理舊檔案..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "  ✓ 已刪除 build 目錄" -ForegroundColor Green
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "  ✓ 已刪除 dist 目錄" -ForegroundColor Green
}
if (Test-Path "SEO_Article_Editor.spec") {
    Remove-Item -Force "SEO_Article_Editor.spec"
    Write-Host "  ✓ 已刪除舊 spec 檔" -ForegroundColor Green
}

# 確認必要檔案存在
Write-Host ""
Write-Host "[3/5] 檢查必要檔案..." -ForegroundColor Yellow
$requiredFiles = @(
    "SEO_Article_Editor.py",
    "src\tp_editor_gui.py",
    "templates",
    "output"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (缺少)" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host ""
    Write-Host "錯誤：缺少必要檔案！" -ForegroundColor Red
    exit 1
}

# 執行打包
Write-Host ""
Write-Host "[4/5] 開始打包執行檔..." -ForegroundColor Yellow
Write-Host "  這可能需要 1-2 分鐘，請稍候..." -ForegroundColor Gray

# 使用現有的 spec 檔案
if (Test-Path "SEO_Article_Editor.spec") {
    Write-Host "  使用現有 spec 檔案進行打包..." -ForegroundColor Gray
    $buildCommand = "pyinstaller --noconfirm --clean SEO_Article_Editor.spec"
} else {
    Write-Host "  使用預設參數進行打包..." -ForegroundColor Gray
    $buildCommand = "pyinstaller --noconfirm --onefile --windowed --add-data `"templates;templates`" --add-data `"output;output`" --add-data `"src;src`" --hidden-import `"tp_editor_gui`" --hidden-import `"tp_template_parser`" --paths `"src`" SEO_Article_Editor.py"
}

Write-Host "  執行指令: $buildCommand" -ForegroundColor Gray
Invoke-Expression $buildCommand

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "錯誤：打包失敗！" -ForegroundColor Red
    Write-Host "請查看上方錯誤訊息。" -ForegroundColor Red
    exit 1
}

# 檢查結果
Write-Host ""
Write-Host "[5/5] 檢查打包結果..." -ForegroundColor Yellow
if (Test-Path "dist\SEO_Article_Editor.exe") {
    $exeSize = (Get-Item "dist\SEO_Article_Editor.exe").Length
    $exeSizeMB = [math]::Round($exeSize / 1MB, 2)
    Write-Host "  ✓ 執行檔已生成" -ForegroundColor Green
    Write-Host "  位置: dist\SEO_Article_Editor.exe" -ForegroundColor Gray
    Write-Host "  大小: $exeSizeMB MB" -ForegroundColor Gray
} else {
    Write-Host "  ✗ 執行檔未生成" -ForegroundColor Red
    exit 1
}

# 完成
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  打包完成！" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "執行檔位置: dist\SEO_Article_Editor.exe" -ForegroundColor White
Write-Host ""
Write-Host "使用方式:" -ForegroundColor Yellow
Write-Host "  1. 直接雙擊執行: dist\SEO_Article_Editor.exe" -ForegroundColor Gray
Write-Host "  2. 或在命令列執行: .\dist\SEO_Article_Editor.exe" -ForegroundColor Gray
Write-Host ""
Write-Host "提示:" -ForegroundColor Yellow
Write-Host "  - 首次執行可能需要 5-10 秒啟動時間" -ForegroundColor Gray
Write-Host "  - 如遇防毒軟體警告，請加入信任清單" -ForegroundColor Gray
Write-Host "  - 可將 dist\SEO_Article_Editor.exe 複製到任何電腦使用" -ForegroundColor Gray
Write-Host ""

# 詢問是否立即執行
$runNow = Read-Host "是否立即執行測試？(Y/N)"
if ($runNow -eq "Y" -or $runNow -eq "y") {
    Write-Host ""
    Write-Host "正在啟動執行檔..." -ForegroundColor Yellow
    Start-Process "dist\SEO_Article_Editor.exe"
    Write-Host "✓ 已啟動" -ForegroundColor Green
}

Write-Host ""
Write-Host "感謝使用！" -ForegroundColor Cyan
Write-Host ""
