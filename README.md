# VESPY - Visualización y Procesamiento de Datos de Sondeo Eléctrico Vertical

VESPY es una aplicación de escritorio desarrollada en Python que permite visualizar y procesar datos de Sondeo Eléctrico Vertical (VES) para estudios geofísicos. La aplicación incluye herramientas para análisis de datos, inversión de resistividad, y generación de gráficos 2D para interpretación geológica.

## 🎯 Características Principales

### 🔧 Procesamiento de Datos
- Carga datos desde archivos Excel (.xlsx, .xls), CSV (.csv) y LibreOffice Calc (.ods)
- Verificación automática de formatos de columnas requeridas
- Promediado de datos con mismo AB/2 pero diferente MN/2 (empalme)
- Filtros de suavizado: Media Móvil, Savitzky-Golay, Exponencial

### 📊 Análisis Estadístico
- Estadísticas descriptivas completas
- Análisis de frecuencias y distribuciones
- Análisis de Fourier (FFT) para identificar periodicidades
- Detección automática de outliers
- Recomendaciones de preprocesamiento

### ⚙️ Inversión de Resistividad
- Algoritmos de inversión: Occam's razor y Levenberg-Marquardt
- Configuración personalizable de parámetros (número de capas, lambda, factor lambda)
- Cálculo automático del Error Cuadrático Medio (RMSE)
- Visualización de resultados de inversión

### 🎨 Visualización Avanzada
- Gráficos de curvas de resistividad aparente vs AB/2
- Gráficos de empalme y datos suavizados
- Gráficos 2D interpolados con múltiples algoritmos
- Múltiples mapas de colores (jet, rainbow, viridis, plasma, etc.)
- **NUEVO**: Interfaz moderna con temas claro y oscuro
- **NUEVO**: Barra de herramientas profesional con iconos y tooltips
- **NUEVO**: Paneles redimensionables y organizados
- Exportación de figuras en alta resolución

### 🔍 Clasificación de Acuíferos
- Análisis automático para identificar posibles acuíferos
- Clasificación basada en valores de resistividad
- Recomendaciones de profundidad de perforación

### ✨ Características de la Interfaz Mejorada

#### 🎨 Diseño Profesional
- **Tema Claro y Oscuro**: Alterne entre temas con un solo clic
- **Barra de Estado Inteligente**: Muestra progreso, información del archivo y hora actual
- **Paneles Redimensionables**: Splitters para ajustar el tamaño de cada panel
- **Scrollbars Estilizados**: Diseño moderno y funcional

#### ⌨️ Atajos de Teclado
- `Ctrl+O`: Cargar datos
- `Ctrl+S`: Guardar tabla
- `F5`: Invertir modelo
- `F6`: Generar gráfico 2D
- `F7`: Clasificar agua

#### 🛠️ Herramientas Avanzadas
- **Auto-guardado**: Guarda automáticamente cada 5 minutos
- **Barra de Progreso**: Seguimiento visual de operaciones
- **Tooltips Informativos**: Ayuda contextual en cada herramienta
- **Iconos con Emojis**: Navegación visual intuitiva

## Instalación y Configuración

### **Opción 1: Instalación Automática (Recomendada)**
Ejecuta uno de los siguientes scripts para configurar automáticamente el entorno:

**Windows (Batch):**
```batch
install.bat
```

**Windows (PowerShell):**
```powershell
.\install.ps1
```

### **Opción 2: Instalación Manual**
Para ejecutar VESPY, es necesario tener activado el ambiente `pg` de `pygimli`. Sigue estos pasos para configurarlo:

```bash
# 1. Instalar pygimli
conda create -n pg -c gimli -c conda-forge "pygimli>=1.5.0"

# 2. Activar el ambiente
conda activate pg

# 3. Instalar dependencias adicionales
pip install -r requirements.txt
```

### **Ejecución**
Una vez instaladas las dependencias:
```bash
# Activar el entorno
conda activate pg

# Ejecutar VESPY
python src/vespy.py
```

## Dependencias
- **PyQt5** (>=5.15.0) - Interfaz gráfica
- **pandas** (>=1.3.0) - Manipulación de datos
- **numpy** (>=1.21.0) - Cálculos numéricos
- **matplotlib** (>=3.4.0) - Visualización
- **seaborn** (>=0.11.0) - Gráficos estadísticos
- **scipy** (>=1.7.0) - Procesamiento científico
- **pygimli** (>=1.5.0) - Inversión geofísica
- **odfpy** (>=1.4.0) - Lectura de archivos LibreOffice

## Nota sobre la Estructura de Archivos
VESPY ahora está organizado en una carpeta con la siguiente estructura:
```
project_folder/
│── src/
│   ├── vespy.py
│── images/
```

## Formato de Datos Requerido
Para garantizar un correcto procesamiento, los datos deben estar en el siguiente formato:
```
AB/2    MN/2    K    PN    PI    I (Ma)    ∆V (Mv)    pa (Ω*m)
```

## Funcionalidades
### **Carga y Guardado de Datos**
- `load_data()`: Carga datos desde un archivo Excel.
- `save_curve()`: Guarda la curva de resistividad suavizada.
- `save_inversion_table()`: Guarda la tabla del modelo de inversión.
- `load_inverted_models()`: Carga modelos invertidos desde archivos.
- `save_model()`: Guarda el modelo de inversión actual.
- `save_inversion_model()`: Guarda el modelo de inversión sin expandir los puntos.

### **Preprocesamiento de Datos**
- `realizar_empalme()`: Genera el empalme de los datos.
- `apply_filter()`: Aplica un filtro de suavizado.

### **Procesamiento y Análisis**
- `analyze_data()`: Realiza un análisis estadístico completo.
- `invert_model()`: Realiza la inversión de resistividad.
- `find_water()`: Clasifica los datos para identificar posibles acuíferos.

### **Visualización Gráfica**
- `plot_data()`: Grafica los datos de resistividad.
- `generate_2d_plot()`: Genera un gráfico 2D interpolado.
- `plot_classified_layers()`: Visualiza el modelo con clasificaciones litológicas.

## Variables de Almacenamiento
- `self.data`: Datos de resistividad cargados.
- `self.smoothed_data`: Datos suavizados.
- `self.empalme_data`: Datos de empalme.
- `self.saved_models`: Modelos de capas invertidos.
- `self.loaded_models`: Modelos cargados.
- `self.depths`: Profundidades calculadas.
- `self.resistivity`: Resistividades calculadas.
- `self.model_path`: Ruta para guardar modelos.
- `self.distances`, `self.grid_x`, `self.grid_y`, `self.grid_z`: Parámetros para el gráfico 2D.

## Instalación y Uso
1. **Ejecutar la aplicación:**
   ```markdown
   python src/vespy.py
   ```

## Contribución
Si deseas contribuir a VESPY, puedes hacer un fork del repositorio, realizar mejoras y enviar un pull request.

## Licencia
Este proyecto está bajo la licencia MIT.

## PATREON
```markdown
Apoya el desarrollo continuo de VESPY uniéndote a nuestra comunidad en Patreon. Cada nivel de apoyo viene con beneficios exclusivos:

    Gratis: Acceso limitado a funcionalidades básicas.
    Café: Ayúdanos con un café y accede a actualizaciones de desarrollo.
    Principiante: Disfruta de acceso anticipado a nuevas funciones.
    Frecuencias: Obtén soporte prioritario y acceso completo a todas las herramientas avanzadas.

Lista de patrocinadores actuales
Café:
    Jorge Mario Manjarres Contreras ☕

Gratis:
    Christhofer Omar Urquizo Quiroz
    José David Sanabria Gómez
    Antonio Suero Moreno
    Pablo Armando Topes Rojas
    Diego Gonzalez
    Francisco Lopez
    Timeslice
    Esthefany Astudillo
    Cursos Olegario
    RODRIGO TELLO
    Abril Fuentes
    Arturo Ortiz
    Reis dedektor yeralti goruntuleme
    Velnia Chacca Luna
    Jorge Mario Manjarres Contreras
    Gustavo Medina
    Jorge Victor Obregon Leon
    Leonardo Nicolas Quispe Mendoza
    Ricardo Pizarro
    Homero Loaiza Sanchez
    Jesús Limón
    Erik Robinson Trincado Cabezas
```
