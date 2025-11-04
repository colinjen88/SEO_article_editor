# SEO Article Editor - Project Cleanup Script
# Purpose: Clean temporary files, cache, test outputs

Write-Host "=== SEO Article Editor - Project Cleanup ===" -ForegroundColor Cyan
Write-Host ""

# Clean Python cache
Write-Host "[1/4] Cleaning Python cache..." -ForegroundColor Yellow
Remove-Item -Path "__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "src\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "src\legacy\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "*.pyc" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  OK Python cache cleaned" -ForegroundColor Green

# Clean output folder (preserve preview_temp.html)
Write-Host "[2/4] Cleaning output folder..." -ForegroundColor Yellow
$outputFiles = Get-ChildItem -Path "output" -Filter "*.html" | Where-Object { $_.Name -ne "preview_temp.html" }
if ($outputFiles.Count -gt 0) {
    $outputFiles | Remove-Item -Force
    Write-Host "  OK Cleaned $($outputFiles.Count) old HTML files" -ForegroundColor Green
} else {
    Write-Host "  OK Output folder already clean" -ForegroundColor Green
}

# Clean temporary files
Write-Host "[3/4] Cleaning temporary files..." -ForegroundColor Yellow
Remove-Item -Path "*.tmp" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "*.bak" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "*.log" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "temp_*.py" -Force -ErrorAction SilentlyContinue
Write-Host "  OK Temporary files cleaned" -ForegroundColor Green

# Display project size
Write-Host "[4/4] Calculating project size..." -ForegroundColor Yellow
$size = (Get-ChildItem -Path . -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "  OK Total project size: $([math]::Round($size, 2)) MB" -ForegroundColor Green

Write-Host ""
Write-Host "=== Cleanup Complete! ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Preserved files:" -ForegroundColor White
Write-Host "  - output/preview_temp.html (browser preview cache)" -ForegroundColor Gray
Write-Host "  - article_number.txt (article number tracker)" -ForegroundColor Gray
Write-Host "  - settings.json (settings file)" -ForegroundColor Gray
Write-Host ""
