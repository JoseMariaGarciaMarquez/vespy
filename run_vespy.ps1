# VESPY Launcher - PowerShell Script
Clear-Host

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "   VESPY - Iniciando aplicacion" -ForegroundColor White
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Activando entorno conda 'pg'..." -ForegroundColor Yellow

# Verificar si conda está disponible
try {
    $condaVersion = & conda --version 2>$null
    if (-not $condaVersion) {
        throw "Conda no encontrado"
    }
} catch {
    Write-Host ""
    Write-Host "ERROR: Conda no está disponible" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solución:" -ForegroundColor Yellow
    Write-Host "1. Instalar Anaconda o Miniconda" -ForegroundColor White
    Write-Host "2. Agregar conda al PATH del sistema" -ForegroundColor White
    Write-Host ""
    Read-Host "Presiona Enter para continuar"
    exit 1
}

# Activar el entorno
try {
    & conda activate pg
    if ($LASTEXITCODE -ne 0) {
        throw "Error al activar entorno"
    }
} catch {
    Write-Host ""
    Write-Host "ERROR: No se pudo activar el entorno 'pg'" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solución:" -ForegroundColor Yellow
    Write-Host "1. Crear el entorno: conda create -n pg -c gimli -c conda-forge `"pygimli>=1.5.0`"" -ForegroundColor White
    Write-Host "2. Instalar dependencias: pip install -r requirements.txt" -ForegroundColor White
    Write-Host ""
    Read-Host "Presiona Enter para continuar"
    exit 1
}

Write-Host "[2/3] Verificando Python y dependencias..." -ForegroundColor Yellow

# Verificar PyQt5
try {
    $null = & python -c "import PyQt5; print('PyQt5 disponible')" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "PyQt5 no disponible"
    }
    Write-Host "✓ PyQt5 disponible" -ForegroundColor Green
} catch {
    Write-Host "ERROR: PyQt5 no está disponible" -ForegroundColor Red
    Write-Host "Instale con: pip install PyQt5" -ForegroundColor Yellow
    Read-Host "Presiona Enter para continuar"
    exit 1
}

Write-Host "[3/3] Ejecutando VESPY..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "   VESPY - Aplicacion iniciada" -ForegroundColor White
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Ejecutar VESPY
try {
    & python src\vespy.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "ERROR: VESPY terminó con errores" -ForegroundColor Red
        Write-Host "Revise los mensajes de error arriba" -ForegroundColor Yellow
    } else {
        Write-Host ""
        Write-Host "VESPY terminado correctamente." -ForegroundColor Green
    }
} catch {
    Write-Host ""
    Write-Host "ERROR: No se pudo ejecutar VESPY" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host ""
Read-Host "Presiona Enter para continuar"
