# 数据库验证脚本 - Windows 版本
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "数据库验证和健康检查" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 检查虚拟环境
if (-not (Test-Path "backend\venv")) {
    Write-Host "× 后端虚拟环境不存在" -ForegroundColor Red
    Write-Host "请先运行: .\setup.ps1`n" -ForegroundColor Yellow
    pause
    exit 1
}

# 检查 .env 文件
if (-not (Test-Path "backend\.env")) {
    Write-Host "× 配置文件不存在" -ForegroundColor Red
    Write-Host "请先运行: .\setup.ps1`n" -ForegroundColor Yellow
    pause
    exit 1
}

# 运行数据库检查
Write-Host "运行数据库初始化和检查...`n" -ForegroundColor Cyan

cd backend
& .\venv\Scripts\python.exe init_db.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "✓ 数据库验证成功!" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Green
} else {
    Write-Host "`n========================================" -ForegroundColor Red
    Write-Host "✗ 数据库验证失败" -ForegroundColor Red
    Write-Host "========================================`n" -ForegroundColor Red
    cd ..
    pause
    exit 1
}

cd ..
pause
