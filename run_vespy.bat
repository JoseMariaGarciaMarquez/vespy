@echo off
cls
echo.
echo ================================
echo    VESPY - Iniciando aplicacion
echo ================================
echo.

echo [1/3] Activando entorno conda 'pg'...
call conda activate pg
if errorlevel 1 (
    echo.
    echo ERROR: No se pudo activar el entorno 'pg'
    echo.
    echo Solucion:
    echo 1. Verificar que Anaconda/Miniconda este instalado
    echo 2. Crear el entorno con: conda create -n pg -c gimli -c conda-forge "pygimli>=1.5.0"
    echo 3. Instalar dependencias con: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [2/3] Verificando Python y dependencias...
python -c "import PyQt5; print('✓ PyQt5 disponible')" 2>nul || (
    echo ERROR: PyQt5 no esta disponible
    echo Instale con: pip install PyQt5
    pause
    exit /b 1
)

echo [3/3] Ejecutando VESPY...
echo.
echo ================================
echo    VESPY - Aplicacion iniciada
echo ================================
echo.

python src\vespy.py

if errorlevel 1 (
    echo.
    echo ERROR: VESPY termino con errores
    echo Revise los mensajes de error arriba
    echo.
) else (
    echo.
    echo VESPY terminado correctamente.
)

echo.
pause
