# Arquitectura de VESPY

## Estructura de Carpetas

```
src/
├── calculos/              # Módulos de cálculo
│   ├── __init__.py
│   ├── empalme.py        # Empalme de curvas
│   ├── suavizado.py      # Filtrado y suavizado
│   └── estadisticas.py   # Análisis estadístico
│
├── data/                  # Carga de datos
│   ├── __init__.py
│   └── loader.py         # Cargador de archivos
│
├── gui/                   # Interfaz gráfica
│   ├── __init__.py
│   ├── main_gui.py       # Ventana principal (alternativa)
│   └── dialogs.py        # Diálogos personalizados
│
├── inversion/             # Inversión de datos
│   ├── __init__.py
│   └── inversion.py      # Motor de inversión (PyGIMLi/Simple)
│
├── plotting/              # Visualización
│   ├── __init__.py
│   ├── plotter.py        # Graficador base
│   └── plot_2d.py        # Gráficos 2D
│
├── utils/                 # Utilidades
│   ├── __init__.py
│   ├── preprocessing.py  # Diálogos de preprocesamiento
│   └── inversion_dialog.py
│
└── vespy.py              # Aplicación principal
```

## Módulos Principales

### 1. `calculos/`
**Propósito**: Funciones de cálculo matemático y procesamiento de datos.

- `empalme.py`: Empalme automático de curvas de resistividad
  - `realizar_empalme()`: Empalma segmentos detectando rupturas
  - `detectar_segmentos()`: Identifica cambios bruscos en la curva

- `suavizado.py`: Filtrado y suavizado de señales
  - `apply_smoothing()`: Aplica diferentes métodos de suavizado
  - `moving_average()`: Media móvil
  - `exponential_smoothing()`: Suavizado exponencial
  - `remove_outliers()`: Elimina valores atípicos

- `estadisticas.py`: Análisis estadístico
  - `calcular_estadisticas()`: Estadísticas descriptivas
  - `detectar_anomalias()`: Detección de outliers con Z-score
  - `calcular_tendencia()`: Regresión lineal log-log
  - `calcular_rango_investigacion()`: Estima profundidad de investigación

### 2. `inversion/`
**Propósito**: Inversión de datos SEV.

- `inversion.py`: Motor de inversión
  - `VESInverter`: Clase principal de inversión
  - `invert()`: Inversión discreta (PyGIMLi o simple)
  - `invert_smooth_model()`: Inversión suavizada continua

### 3. `plotting/`
**Propósito**: Visualización de datos y resultados.

- `plot_2d.py`: Gráficos 2D
  - `generate_2d_plot()`: Genera perfiles 2D de resistividad
  - `plot_single_sev()`: Grafica curva de resistividad aparente
  - `plot_inversion_model()`: Grafica modelo de capas

### 4. `gui/`
**Propósito**: Componentes de interfaz gráfica.

- `dialogs.py`: Diálogos personalizados
  - `SaveModelDialog`: Diálogo para guardar modelo con X y número SEV
  - `ColumnMappingDialog`: Mapeo de columnas de archivo
  - `InversionParametersDialog`: Configuración de parámetros de inversión

### 5. `data/`
**Propósito**: Carga y manejo de archivos.

- `loader.py`: Cargador de datos
  - `DataLoader`: Clase para cargar Excel, CSV, TXT

## Flujo de Datos

```
1. Carga de Datos
   data/loader.py → vespy.py
   
2. Preprocesamiento
   vespy.py → calculos/empalme.py
   vespy.py → calculos/suavizado.py
   
3. Análisis
   vespy.py → calculos/estadisticas.py
   
4. Inversión
   vespy.py → inversion/inversion.py
   
5. Visualización
   vespy.py → plotting/plot_2d.py
```

## Ventajas de esta Arquitectura

1. **Modularidad**: Cada módulo tiene una responsabilidad única
2. **Reutilización**: Funciones pueden usarse independientemente
3. **Mantenibilidad**: Fácil ubicar y corregir errores
4. **Escalabilidad**: Fácil agregar nuevas funcionalidades
5. **Testing**: Cada módulo puede probarse por separado

## Convenciones de Código

- Cada módulo tiene docstrings descriptivos
- Funciones documentadas con Args, Returns, Raises
- Imports organizados (estándar, terceros, locales)
- Nombres descriptivos en español para interfaz de usuario
- Nombres en inglés para código interno

## Próximos Pasos

- [ ] Migrar más código de `vespy.py` a módulos
- [ ] Crear tests unitarios por módulo
- [ ] Documentar API de cada función
- [ ] Agregar ejemplos de uso
