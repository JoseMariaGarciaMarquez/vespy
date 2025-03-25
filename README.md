# VESPY - Visualización y Procesamiento de Datos de Sondeo Eléctrico Vertical (VES) en Python
![logo](https://github.com/user-attachments/assets/7eba99dd-6a3a-4225-b45b-0cb5354e2507)

## Descripción
VESPY es una aplicación en Python diseñada para la visualización y el procesamiento de datos de Sondeo Eléctrico Vertical (VES). Ofrece herramientas para la carga, preprocesamiento, análisis e inversión de datos de resistividad, permitiendo una mejor interpretación geofísica.

## Características Principales
- **Interfaz intuitiva:** Ventana principal con título "VESPY" y dimensiones de 1600x900 píxeles.
- **Gestor de archivos:** Permite cargar datos de resistividad desde archivos Excel y guardar curvas y modelos invertidos.
- **Preprocesamiento de datos:** Funciones para empalme y suavizado de datos.
- **Procesamiento de datos:** Inversión de resistividad para modelado geofísico.
- **Visualización avanzada:** Gráficos de curvas de resistividad, empalme de datos, análisis estadístico, resultados de inversión y representación 2D.
- **Terminal integrada:** Muestra estadísticas descriptivas y análisis de datos.
- **Tablas interactivas:** Visualización y edición de los datos cargados y del modelo de inversión.

## Requisitos Previos
Para ejecutar VESPY, es necesario tener activado el ambiente `pg` de `pygimli`. Sigue estos pasos para configurarlo:
```markdown
# Instalar pygimli si no lo tienes
conda create -n pg -c gimli -c conda-forge "pygimli>=1.5.0"

# Activar el ambiente
conda activate pg

# Instalar dependencias adicionales
pip install numpy pandas matplotlib scipy tkinter
```

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
