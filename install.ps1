# VESPY - Instalador de Dependencias (PowerShell)
# Configuración automática del entorno para VESPY

Write-Host "=====================================================`n" -ForegroundColor Green
Write-Host "VESPY - Instalador de Dependencias`n" -ForegroundColor Green
Write-Host "=====================================================`n" -ForegroundColor Green
Write-Host "Este script configurará el entorno necesario para VESPY`n"

Write-Host "1. Creando entorno conda con PyGimli..." -ForegroundColor Yellow
conda create -n pg -c gimli -c conda-forge "pygimli>=1.5.0" -y

Write-Host "`n2. Instalando dependencias adicionales..." -ForegroundColor Yellow
conda activate pg
pip install PyQt5>=5.15.0
pip install pandas>=1.3.0
pip install numpy>=1.21.0
pip install matplotlib>=3.4.0
pip install seaborn>=0.11.0
pip install scipy>=1.7.0
pip install odfpy>=1.4.0

Write-Host "`n=====================================================" -ForegroundColor Green
Write-Host "Instalación completada!" -ForegroundColor Green
Write-Host "`nPara usar VESPY:" -ForegroundColor Cyan
Write-Host "1. Activa el entorno: conda activate pg" -ForegroundColor Cyan
Write-Host "2. Ejecuta: python src/vespy.py" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Green

Read-Host -Prompt "`nPresiona Enter para continuar"
