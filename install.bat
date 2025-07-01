@echo off
echo =====================================================
echo VESPY - Instalador de Dependencias
echo =====================================================
echo.
echo Este script configurará el entorno necesario para VESPY
echo.

echo 1. Creando entorno conda con PyGimli...
conda create -n pg -c gimli -c conda-forge "pygimli>=1.5.0" -y

echo.
echo 2. Activando entorno...
call conda activate pg

echo.
echo 3. Instalando dependencias adicionales...
pip install PyQt5>=5.15.0
pip install pandas>=1.3.0
pip install numpy>=1.21.0
pip install matplotlib>=3.4.0
pip install seaborn>=0.11.0
pip install scipy>=1.7.0
pip install odfpy>=1.4.0

echo.
echo =====================================================
echo Instalación completada!
echo.
echo Para usar VESPY:
echo 1. Activa el entorno: conda activate pg
echo 2. Ejecuta: python src/vespy.py
echo =====================================================
pause
