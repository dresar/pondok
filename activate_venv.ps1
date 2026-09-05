# Script untuk aktivasi virtual environment
# Gunakan: .\activate_venv.ps1

# Bypass execution policy untuk session ini
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Aktifkan virtual environment
.\venv\Scripts\Activate.ps1

Write-Host "Virtual environment berhasil diaktifkan!" -ForegroundColor Green
Write-Host "Python version:" -ForegroundColor Yellow
python --version

