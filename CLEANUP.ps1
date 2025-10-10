# 🧹 PRE-SEND CLEANUP SCRIPT (Windows PowerShell)
# Run this before sending to client to remove unnecessary files

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  RareVault Project Cleanup Script" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

$PROJECT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $PROJECT_DIR

$removedSize = 0

# Function to remove directory and calculate size
function Remove-DirectoryWithSize {
    param($Path, $Name)
    if (Test-Path $Path) {
        $size = (Get-ChildItem $Path -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        $sizeMB = [math]::Round($size / 1MB, 2)
        Remove-Item $Path -Recurse -Force -ErrorAction SilentlyContinue
        if (-not (Test-Path $Path)) {
            Write-Host "✓ Removed $Name ($sizeMB MB)" -ForegroundColor Green
            return $size
        } else {
            Write-Host "✗ Could not remove $Name" -ForegroundColor Red
            return 0
        }
    } else {
        Write-Host "○ $Name not found (already clean)" -ForegroundColor Gray
        return 0
    }
}

Write-Host "Cleaning Backend..." -ForegroundColor Yellow
$removedSize += Remove-DirectoryWithSize "backend\venv" "Python virtual environment"
$removedSize += Remove-DirectoryWithSize "backend\__pycache__" "Backend cache"
$removedSize += Remove-DirectoryWithSize "backend\app\__pycache__" "App cache"
$removedSize += Remove-DirectoryWithSize "backend\app\models\__pycache__" "Models cache"
$removedSize += Remove-DirectoryWithSize "backend\app\routes\__pycache__" "Routes cache"
$removedSize += Remove-DirectoryWithSize "backend\app\admin\__pycache__" "Admin cache"
$removedSize += Remove-DirectoryWithSize "backend\app\seller\__pycache__" "Seller cache"
$removedSize += Remove-DirectoryWithSize "backend\app\user\__pycache__" "User cache"

Write-Host ""
Write-Host "Cleaning Frontend..." -ForegroundColor Yellow
$removedSize += Remove-DirectoryWithSize "frontend\node_modules" "Node modules"
$removedSize += Remove-DirectoryWithSize "frontend\dist" "Build output"
$removedSize += Remove-DirectoryWithSize "frontend\.vite" "Vite cache"

Write-Host ""
Write-Host "Cleaning System Files..." -ForegroundColor Yellow

# Remove .pyc files
$pycFiles = Get-ChildItem -Path . -Filter "*.pyc" -Recurse -Force -ErrorAction SilentlyContinue
if ($pycFiles) {
    $pycFiles | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "✓ Removed $($pycFiles.Count) .pyc files" -ForegroundColor Green
}

# Remove log files
$logFiles = Get-ChildItem -Path . -Filter "*.log" -Recurse -Force -ErrorAction SilentlyContinue
if ($logFiles) {
    $logFiles | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "✓ Removed $($logFiles.Count) log files" -ForegroundColor Green
}

# Remove DS_Store (Mac)
$dsFiles = Get-ChildItem -Path . -Filter ".DS_Store" -Recurse -Force -ErrorAction SilentlyContinue
if ($dsFiles) {
    $dsFiles | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "✓ Removed $($dsFiles.Count) .DS_Store files" -ForegroundColor Green
}

# Remove Thumbs.db (Windows)
$thumbsFiles = Get-ChildItem -Path . -Filter "Thumbs.db" -Recurse -Force -ErrorAction SilentlyContinue
if ($thumbsFiles) {
    $thumbsFiles | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "✓ Removed $($thumbsFiles.Count) Thumbs.db files" -ForegroundColor Green
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host "  Cleanup Complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

$totalMB = [math]::Round($removedSize / 1MB, 2)
Write-Host "Total space freed: $totalMB MB" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚠️  IMPORTANT SECURITY CHECK:" -ForegroundColor Yellow
Write-Host "Before sending to client:" -ForegroundColor White
Write-Host "1. Review backend\.env file for sensitive data" -ForegroundColor White
Write-Host "2. Check rarevault_db.sql for personal information" -ForegroundColor White
Write-Host "3. Verify no hardcoded passwords in code" -ForegroundColor White
Write-Host ""
Write-Host "See PACKAGE_CHECKLIST.md for complete pre-send checklist" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
