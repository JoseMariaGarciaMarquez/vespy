# VESPY - Guía de Solución de Problemas

## Problemas Comunes y Soluciones

### 1. Error de Importación: "PyQt5 could not be resolved"

**Problema:** El sistema no encuentra las librerías PyQt5.

**Solución:**
```bash
# Activar el entorno conda
conda activate pg

# Instalar PyQt5
pip install PyQt5>=5.15.0
```

### 2. Error de Importación: "pygimli could not be resolved"

**Problema:** PyGimli no está instalado correctamente.

**Solución:**
```bash
# Crear nuevo entorno con pygimli
conda create -n pg -c gimli -c conda-forge "pygimli>=1.5.0"
conda activate pg
```

### 3. Error: "pandas is not defined"

**Problema:** Falta la importación de pandas o no está instalado.

**Solución:**
```bash
# Instalar pandas
pip install pandas>=1.3.0
```

### 4. Error al cargar archivos .ods

**Problema:** No se pueden leer archivos de LibreOffice.

**Solución:**
```bash
# Instalar soporte para archivos ODS
pip install odfpy>=1.4.0
```

### 5. Problemas de Visualización en Gráficos

**Problema:** Los gráficos no se muestran correctamente.

**Solución:**
```bash
# Verificar instalación de matplotlib
pip install matplotlib>=3.4.0 seaborn>=0.11.0
```

### 6. Error: "No module named 'src'"

**Problema:** Python no encuentra los módulos del proyecto.

**Solución:**
- Asegúrate de ejecutar desde el directorio raíz del proyecto
- Verifica que todos los archivos .py estén en la carpeta `src/`

### 7. Rendimiento Lento en Inversión

**Problema:** La inversión tarda mucho tiempo.

**Solución:**
- Reduce el número de capas en la configuración
- Ajusta los parámetros lambda
- Verifica que scipy esté instalado correctamente

## Verificación del Entorno

Para verificar que todo está instalado correctamente:

```python
# Ejecutar este código en Python
import sys
print("Python version:", sys.version)

try:
    import PyQt5
    print("✓ PyQt5 instalado")
except ImportError:
    print("✗ PyQt5 no encontrado")

try:
    import pandas
    print("✓ pandas instalado")
except ImportError:
    print("✗ pandas no encontrado")

try:
    import matplotlib
    print("✓ matplotlib instalado")
except ImportError:
    print("✗ matplotlib no encontrado")

try:
    import pygimli
    print("✓ pygimli instalado")
except ImportError:
    print("✗ pygimli no encontrado")
```

## Contacto para Soporte

Si los problemas persisten:
1. Verifica que estés usando el entorno conda correcto (`conda activate pg`)
2. Revisa la documentación en el README.md
3. Utiliza el menú "¡Quiero aportar!" en la aplicación para obtener soporte
