# VESPY - Vertical Electrical Sounding in Python

![VESPY Banner](images/logo.png)

VESPY es una aplicación de escritorio moderna y potente desarrollada en Python para el análisis completo de datos de Sondeos Eléctricos Verticales (SEV/VES). Diseñada para geofísicos, hidrogeólogos e investigadores, VESPY ofrece un flujo de trabajo completo desde la carga de datos hasta la generación de perfiles 2D interpolados.

---

## 🌟 Características Principales

### 📂 Carga de Datos Inteligente

- **Mapeo interactivo de columnas**: Diálogo intuitivo para mapear columnas de archivos con nombres no estándar
- **Detección automática**: Reconoce automáticamente columnas AB/2, MN/2 y resistividad aparente
- **Formatos soportados**: Excel (.xlsx, .xls), CSV (.csv), TXT separado por tabuladores
- **Limpieza automática**: Elimina espacios en blanco y valores nulos

### 🔧 Preprocesamiento de Datos

- **Empalme (Averaging)**: Promedia datos con mismo AB/2 pero diferente MN/2 para eliminar duplicados
- **Filtros de suavizado**:
  - 📊 Media Móvil: Reduce ruido preservando tendencias
  - 📈 Savitzky-Golay: Suavizado polinomial avanzado
  - 📉 Exponencial: Suavizado adaptativo exponencial
- **Flujo coherente**: Los datos preprocesados se usan automáticamente en la inversión

### ⚡ Inversión de Resistividad

- **PyGIMLi integrado**: Inversión de alta calidad con VESManager
- **Algoritmo de Occam**: Busca el modelo más simple que explique los datos
- **Parámetros configurables**:
  - Número de capas (1-20)
  - Lambda (λ): Factor de regularización (1-100)
  - Factor Lambda: Reducción por iteración (0.5-1.0)
- **Métricas de calidad**: Chi² y RMS para evaluar el ajuste
- **Fallback inteligente**: Inversión simple si PyGIMLi no está disponible

### 📊 Análisis Estadístico Avanzado

- Estadísticas descriptivas (media, mediana, desviación estándar)
- Análisis de asimetría y curtosis
- Transformada de Fourier (FFT) para detectar periodicidades
- Visualización con histogramas, boxplots y scatter plots
- Identificación de valores atípicos

### 🎨 Visualización de Alta Calidad

- **Gráfico de curvas**: Visualiza datos originales, empalme y suavizado en escala log-log
- **Análisis estadístico**: Múltiples gráficos estadísticos en una sola vista
- **Resultados de inversión**: Ajuste del modelo y perfil 1D de capas
- **Perfiles 2D interpolados**:
  - Interpolación lineal, cúbica o vecino más cercano
  - Mapas de colores profesionales (jet, rainbow, viridis, plasma, inferno, magma)
  - Marcadores de posición de SEV
  - Exportación en alta resolución

### 💾 Gestión de Modelos

- **Guardar modelos con posición X**: Sistema de coordenadas para perfiles 2D
- **Sugerencias inteligentes**: Auto-sugiere posiciones (0, 20, 40, 60...)
- **Múltiples modelos**: Almacena varios modelos invertidos para perfiles
- **Exportación**: Guarda modelos en formato estructurado

### 📚 Tutorial Notebooks

VESPY incluye una serie completa de tutoriales Jupyter para enseñar procesamiento de SEV paso a paso:

- **01_Introduccion_SEV.ipynb**: Conceptos básicos y teoría de SEV
- **02_Preprocesamiento_SEV.ipynb**: Empalme, filtros y limpieza de datos
- **03_Inversion_PyGIMLi.ipynb**: Inversión avanzada con PyGIMLi, parámetros y evaluación
- **04_Visualizacion_2D.ipynb**: Generación de perfiles 2D interpolados

### ✨ Interfaz de Usuario Moderna

- **Diseño horizontal optimizado**: Proporción 18:57:25 (controles:gráficos:tablas)
- **Iconos emoji**: Sin dependencia de archivos de imágenes externos
- **Pestañas organizadas**: Navegación clara entre diferentes vistas
- **Terminal integrado**: Feedback en tiempo real de operaciones
- **Tablas interactivas**: Visualiza datos cargados y modelos invertidos

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.8 o superior
- Conda (Anaconda o Miniconda)
- Windows, macOS o Linux

### Instalación con Conda (Recomendado)

```bash
# 1. Crear entorno con PyGIMLi
conda create -n vespy -c gimli -c conda-forge pygimli

# 2. Activar el entorno
conda activate vespy

# 3. Instalar dependencias
pip install PyQt5 pandas numpy matplotlib seaborn scipy
```

### Instalación sin PyGIMLi (Funcionalidad Limitada)

Si no puedes instalar PyGIMLi, VESPY funcionará con inversión simplificada:

```bash
# Crear entorno Python
python -m venv vespy-env

# Activar entorno (Windows)
vespy-env\Scripts\activate

# Activar entorno (Linux/macOS)
source vespy-env/bin/activate

# Instalar dependencias básicas
pip install PyQt5 pandas numpy matplotlib seaborn scipy
```

### Ejecutar VESPY

```bash
# Activar el entorno
conda activate vespy

# Ejecutar la aplicación
python src/vespy.py
```

---

## 📦 Dependencias

### Obligatorias

- **PyQt5** (>=5.15.0) - Interfaz gráfica moderna
- **pandas** (>=1.3.0) - Manipulación y análisis de datos
- **numpy** (>=1.21.0) - Cálculos numéricos
- **matplotlib** (>=3.4.0) - Visualización de gráficos
- **seaborn** (>=0.11.0) - Gráficos estadísticos avanzados
- **scipy** (>=1.7.0) - Procesamiento científico e interpolación

### Opcionales

- **pygimli** (>=1.5.0) - Inversión geofísica de alta calidad (recomendado)

---

## 📁 Estructura del Proyecto

```text
vespy/
├── src/
│   └── vespy.py           # Aplicación principal (monolítica)
├── notebooks/
│   ├── 01_Introduccion_SEV.ipynb
│   ├── 02_Preprocesamiento_SEV.ipynb
│   ├── 03_Inversion_PyGIMLi.ipynb
│   └── 04_Visualizacion_2D.ipynb
├── images/
│   └── logo.png
├── aditional-data/
│   └── members.csv        # Datos de ejemplo
├── README.md
└── LICENSE
```

---

## 📋 Formato de Datos

VESPY acepta archivos con las siguientes columnas (nombres flexibles gracias al mapeo interactivo):

**Columnas requeridas:**

- **AB/2**: Espaciamiento del arreglo de corriente (metros)
- **pa (Ω·m)**: Resistividad aparente (ohm-metro)

**Columnas opcionales:**

- **MN/2**: Espaciamiento del arreglo de potencial (metros)
- Otras columnas son ignoradas automáticamente

**Ejemplo de formato:**

```csv
AB/2,MN/2,pa (Ω*m)
1.5,0.5,45.2
2.0,0.5,52.3
3.0,0.5,68.5
4.5,0.5,85.2
```

💡 **Nota**: Si tus columnas tienen nombres diferentes (ej: "Resistividad", "Espaciamiento"), el diálogo de mapeo te permitirá seleccionarlas manualmente.

---

## 🔧 Flujo de Trabajo

### 1️⃣ Cargar Datos

```text
📂 Cargar → Seleccionar archivo → Mapear columnas → ✅ Datos cargados
```

### 2️⃣ Preprocesar (Opcional)

```text
🔗 Empalme: Promediar datos con mismo AB/2
✨ Suavizado: Aplicar filtro para reducir ruido
```

**⚠️ Importante**: Los datos preprocesados se usan automáticamente en la inversión.

### 3️⃣ Invertir

```text
⚡ Configurar parámetros → Inversión → 📊 Modelo de capas 1D
```

### 4️⃣ Guardar Modelo

```text
💾 Guardar con posición X → Repetir para múltiples SEV
```

### 5️⃣ Generar Perfil 2D

```text
🗺️ Interpolación → Visualización 2D → 💾 Exportar PNG
```

---

## 🎓 Tutoriales Jupyter

Los notebooks en la carpeta `notebooks/` cubren:

1. **01_Introduccion_SEV**: Teoría de SEV, configuración Schlumberger, interpretación de curvas
2. **02_Preprocesamiento_SEV**: Técnicas de empalme, filtros de suavizado, detección de outliers
3. **03_Inversion_PyGIMLi**: Uso de PyGIMLi, parámetros de regularización, evaluación de ajuste
4. **04_Visualizacion_2D**: Interpolación espacial, generación de perfiles, exportación

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Si deseas mejorar VESPY:

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## ☕ Apoya el Proyecto

[![Patreon](https://img.shields.io/badge/Patreon-Support%20VESPY-orange?style=for-the-badge&logo=patreon)](https://www.patreon.com/chemitas)

Si VESPY te resulta útil, considera apoyar su desarrollo:

- ☕ **Café**: Apoyo básico y acceso a actualizaciones
- 🌱 **Principiante**: Acceso anticipado a nuevas funciones
- ⚡ **Frecuencias**: Soporte prioritario y herramientas avanzadas

### 🏆 Patrocinadores

**Buy Me a Coffee ☕:**

- Jose David Carrillo - $9.90 USD

**Nivel Café ☕:**

- Jorge Mario Manjarres Contreras

**Comunidad 🌟:**

- Christhofer Omar Urquizo Quiroz
- José David Sanabria Gómez
- Antonio Suero Moreno
- Pablo Armando Topes Rojas
- Diego Gonzalez
- Francisco Lopez
- Timeslice
- Esthefany Astudillo
- Cursos Olegario
- RODRIGO TELLO
- Abril Fuentes
- Arturo Ortiz
- Reis dedektor yeralti goruntuleme
- Velnia Chacca Luna
- Gustavo Medina
- Jorge Victor Obregon Leon
- Leonardo Nicolas Quispe Mendoza
- Ricardo Pizarro
- Homero Loaiza Sanchez
- Jesús Limón
- Erik Robinson Trincado Cabezas

---

## 📧 Contacto

**Autor**: Jose Maria Garcia Marquez  
**Email**: josemariagarciamarquez2.72@gmail.com  
**Web**: [josemariagarciamarquez.github.io/webjoma](https://josemariagarciamarquez.github.io/webjoma/)  
**GitHub**: [@JoseMariaGarciaMarquez](https://github.com/JoseMariaGarciaMarquez)  
**Patreon**: [patreon.com/chemitas](https://www.patreon.com/chemitas)

---

<div align="center">

**VESPY** - Vertical Electrical Sounding in Python  
*Desarrollado con ❤️ para la comunidad geofísica*

</div>
