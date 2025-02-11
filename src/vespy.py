"""
VESPY - Visualización y Procesamiento de Datos de Sondeo Eléctrico Verticale (VES) en Python

Funcionalidades Principales:
- Ventana principal con título "VESPY" y tamaño 1600x900 píxeles.
- Barra de herramientas para cargar datos, guardar curvas suavizadas y cargar modelos invertidos.
- Panel de control con pestañas para preprocesamiento (empalme y suavizado) y procesamiento (inversión de resistividad).
- Visualización de gráficos: curva y empalme, análisis estadístico, resultados de inversión y gráfico 2D.
- Terminal de texto para mostrar estadísticas descriptivas y análisis.
- Tablas de datos cargados y modelo de inversión.

Métodos Principales:
- load_data: Carga datos desde un archivo Excel.
- save_curve: Guarda la curva de resistividad suavizada.
- save_inversion_table: Guarda la tabla del modelo de inversión.
- realizar_empalme: Genera el empalme de los datos.
- apply_filter: Aplica un filtro de suavizado.
- plot_data: Grafica los datos de resistividad.
- analyze_data: Realiza un análisis estadístico completo.
- invert_model: Realiza la inversión de resistividad.
- generate_2d_plot: Genera un gráfico 2D interpolado.
- load_inverted_models: Carga modelos invertidos desde archivos.
- save_model: Guarda el modelo de inversión actual.
- save_inversion_model: Guarda el modelo de inversión sin expandir los puntos.
- find_water: Clasifica los datos para identificar posibles acuíferos.
- plot_classified_layers: Visualiza el modelo con clasificaciones litológicas.

Variables de Almacenamiento:
- self.data: Datos de resistividad cargados.
- self.smoothed_data: Datos suavizados.
- self.empalme_data: Datos de empalme.
- self.saved_models: Modelos de capas invertidos.
- self.loaded_models: Modelos cargados.
- self.depths: Profundidades calculadas.
- self.resistivity: Resistividades calculadas.
- self.model_path: Ruta para guardar modelos.
- self.distances, self.grid_x, self.grid_y, self.grid_z: Parámetros para el gráfico 2D.

PATREON

Apoya el desarrollo continuo de vespy uniéndote a nuestra comunidad en Patreon. Cada nivel de apoyo viene con beneficios exclusivos:

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
"""
import sys
import os
import scipy
import webbrowser
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.fft import fft, fftfreq
from scipy.interpolate import griddata
from scipy.signal import savgol_filter
import pygimli as pg
from pygimli.physics import VESManager
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QInputDialog, QFileDialog
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, 
                             QTableWidget, QTableWidgetItem, QComboBox, QDoubleSpinBox, 
                             QSpinBox, QLabel, QGroupBox, QToolBar, QAction, QPushButton, 
                             QTabWidget, QTextEdit, QLineEdit, QApplication)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import Normalize, Colormap
from scipy.optimize import least_squares
from matplotlib import cm

from mpl_toolkits.mplot3d import Axes3D
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QToolBar,
    QAction, QLabel, QPushButton, QSpinBox, QDoubleSpinBox, QGroupBox,
    QComboBox, QTextEdit, QTableWidget
)
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bienvenida")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Imagen de Patreon
        image_label = QLabel(self)
        pixmap = QPixmap("images/patreon.png")
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        # Lista de patrocinadores
        sponsors_label = QLabel(self)
        sponsors_text = (
            "Este proyecto se ha hecho gracias a las aportaciones en Patreon de:\n"
            "Jorge Mario Manjarres Contreras ☕"
        )
        sponsors_label.setText(sponsors_text)
        sponsors_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(sponsors_label)

        # Botón de Patreon
        patreon_button = QPushButton("Patrocíname", self)
        patreon_button.clicked.connect(self.open_patreon)
        layout.addWidget(patreon_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_patreon(self):
        webbrowser.open("https://www.patreon.com/chemitas")

    def closeEvent(self, event):
        self.main_window = SEVApp()
        self.main_window.show()
        event.accept()

class SEVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.setWindowTitle("VESPY")
        self.setGeometry(100, 100, 1600, 900)  # Ventana más grande
        
        # Obtener ruta de la carpeta de imágenes
        
        image_path = Path(__file__).parent.parent / 'images'
        self.setWindowIcon(QIcon(str(image_path / "logo.png")))

        # Crear widget central
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        # Layout principal: HBox dividido en paneles de control, visualización y tablas
        main_layout = QHBoxLayout(self.main_widget)
        
        # Panel izquierdo - Controles y Procesamiento
        control_panel = QVBoxLayout()
        
        # Barra de herramientas con botones de acciones principales
        toolbar = QToolBar("Herramientas")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Acción para cargar datos con icono "cargar.png"
        load_action = QAction(QIcon(str(image_path / "cargar.png")), "Cargar Datos", self)
        load_action.triggered.connect(self.load_data)
        toolbar.addAction(load_action)

        # Acción para guardar la curva suavizada con icono "inversion.png"
        save_action = QAction(QIcon(str(image_path / "inversion.png")), "Guardar Curva Suavizada", self)
        save_action.triggered.connect(self.save_curve)
        toolbar.addAction(save_action)
        
        # Acción para cargar modelos invertidos con icono "cargar_modelo.png"
        load_model_action = QAction(QIcon(str(image_path / "cargar_modelo.png")), "Cargar Modelos Invertidos", self)
        load_model_action.triggered.connect(self.load_inverted_models)
        toolbar.addAction(load_model_action)

        # Acción para guardar la tabla del resultado de la inversión con icono "guardar_tabla.png"
        save_table_action = QAction(QIcon(str(image_path / "guardar_tabla.png")), "Guardar Tabla de Inversión", self)
        save_table_action.triggered.connect(self.save_inversion_table)
        toolbar.addAction(save_table_action)

        
        # Controles de preprocesamiento y procesamiento en pestañas de control
        control_tabs = QTabWidget()
        control_tabs.setStyleSheet("background-color: #e8e8e8;")
        
        # Pestaña Preprocesamiento
        preprocessing_tab = QWidget()
        preprocessing_layout = QVBoxLayout(preprocessing_tab)
        preprocessing_layout.addWidget(QLabel("Preprocesamiento"))
        
        self.empalme_button = QPushButton("Realizar Empalme")
        self.empalme_button.clicked.connect(self.realizar_empalme)
        preprocessing_layout.addWidget(self.empalme_button)
        
        # Opciones de suavizado
        filter_group = QGroupBox("Suavizado")
        filter_layout = QVBoxLayout()
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Media Móvil", "Savitzky-Golay", "Exponencial"])
        
        self.window_size_spin = QSpinBox()
        self.window_size_spin.setRange(1, 100)
        self.window_size_spin.setValue(5)
        
        self.apply_filter_button = QPushButton("Aplicar Suavizado")
        self.apply_filter_button.clicked.connect(self.apply_filter)
        
        filter_layout.addWidget(QLabel("Tipo de Filtro"))
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(QLabel("Tamaño de Ventana"))
        filter_layout.addWidget(self.window_size_spin)
        filter_layout.addWidget(self.apply_filter_button)
        filter_group.setLayout(filter_layout)
        preprocessing_layout.addWidget(filter_group)

        # Crear el botón para guardar el archivo filtrado
        self.save_filtered_button = QPushButton("Crear Nuevo Archivo")
        self.save_filtered_button.clicked.connect(self.save_filtered_data)
        preprocessing_layout.addWidget(self.save_filtered_button)

        control_tabs.addTab(preprocessing_tab, "Preprocesamiento")
        
        # Pestaña de Procesamiento e Inversión
        processing_tab = QWidget()
        processing_layout = QVBoxLayout(processing_tab)

        # Selector de Modelo (Solo "Occam's razor")
        self.model_selector = QComboBox()
        self.model_selector.addItems(["Occam's razor", "Levenberg-Marquardt"])
        processing_layout.addWidget(QLabel("Seleccione el Modelo de Inversión:"))
        processing_layout.addWidget(self.model_selector)
        
        # Parámetros de Inversión (Occam's razor)
        occam_group = QGroupBox("Parámetros - Occam's razor")
        occam_layout = QVBoxLayout()
        
        self.layer_spin = QSpinBox()
        self.layer_spin.setRange(2, 50)
        self.layer_spin.setValue(5)
        
        self.lambda_spin = QSpinBox()
        self.lambda_spin.setRange(1, 1000)
        self.lambda_spin.setValue(20)

        self.lambda_factor_spin = QDoubleSpinBox()
        self.lambda_factor_spin.setRange(0.1, 10.0)
        self.lambda_factor_spin.setSingleStep(0.1)
        self.lambda_factor_spin.setValue(0.8)

        occam_layout.addWidget(QLabel("Número de Capas"))
        occam_layout.addWidget(self.layer_spin)
        occam_layout.addWidget(QLabel("Lambda"))
        occam_layout.addWidget(self.lambda_spin)
        occam_layout.addWidget(QLabel("Factor Lambda"))
        occam_layout.addWidget(self.lambda_factor_spin)
        
        occam_group.setLayout(occam_layout)
        processing_layout.addWidget(occam_group)

        # Botón de Inversión
        self.invert_button = QPushButton("Invertir Modelo")
        self.invert_button.clicked.connect(self.invert_model)
        processing_layout.addWidget(self.invert_button)

        # Botón para clasificar los datos
        self.water_button = QPushButton("Agua")
        self.water_button.clicked.connect(self.find_water)
        processing_layout.addWidget(self.water_button)

        # Botón para guardar el modelo
        self.save_model_button = QPushButton("Guardar Modelo")
        self.save_model_button.clicked.connect(self.save_model)
        processing_layout.addWidget(self.save_model_button)

        control_tabs.addTab(processing_tab, "Procesamiento")
        
        # Añadir control_tabs al panel izquierdo
        control_panel.addWidget(control_tabs)
        
        # Área central - Visualización de Gráficos
        visualization_layout = QVBoxLayout()
        
        # Pestañas de gráficos
        self.tabs = QTabWidget()
        
        # Tab 1: Gráfica principal (curva y empalme)
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.tabs.addTab(self.canvas, "Curva y Empalme")
        
        # Tab 2: Análisis estadístico completo (histogramas y FFT)
        self.analysis_figure = Figure(figsize=(12, 8))
        self.analysis_canvas = FigureCanvas(self.analysis_figure)
        self.tabs.addTab(self.analysis_canvas, "Análisis Estadístico Completo")

        # Tab 3: Resultados de Inversión
        self.inversion_figure = Figure(figsize=(10, 6))
        self.inversion_canvas = FigureCanvas(self.inversion_figure)
        self.tabs.addTab(self.inversion_canvas, "Inversión")
        
        # Tab 4: Gráfico 2D
        self.figure_2d = Figure(figsize=(10, 6))
        self.canvas_2d = FigureCanvas(self.figure_2d)
        self.tabs.addTab(self.canvas_2d, "Gráfico 2D")
        
        visualization_layout.addWidget(self.tabs)

        # Tab 5: Gráfico 3D
        self.figure_3d = Figure(figsize=(10, 6))
        self.canvas_3d = FigureCanvas(self.figure_3d)
        self.tabs.addTab(self.canvas_3d, "Gráfico 3D")
        
        # Terminal de texto para mostrar estadísticas descriptivas y análisis
        self.eda_output = QTextEdit()
        self.eda_output.setReadOnly(True)
        self.eda_output.setFixedHeight(150)
        visualization_layout.addWidget(self.eda_output)
        
        # Área de tablas de datos e inversión
        table_layout = QVBoxLayout()
        self.table_tabs = QTabWidget()
        
        # Tabla de datos cargados
        self.data_table = QTableWidget()
        self.table_tabs.addTab(self.data_table, "Datos Cargados")
        
        # Tabla de modelo de inversión
        self.model_table = QTableWidget()
        self.table_tabs.addTab(self.model_table, "Modelo de Inversión")
        
        table_layout.addWidget(self.table_tabs)
        
        # Configuración del layout principal
        main_layout.addLayout(control_panel, 18)
        main_layout.addLayout(visualization_layout, 57)
        main_layout.addLayout(table_layout, 25)

        # Variables para almacenar datos y resultados
        self.data = None
        self.smoothed_data = None
        self.empalme_data = None
        self.saved_models = []  # Lista para almacenar modelos de capas invertidos
        self.loaded_models = []  # Lista para almacenar modelos cargados
        self.depths = None
        self.resistivity = None
        self.model_path = "modelos"
        
        # Parámetros para el gráfico 2D
        self.distances = None
        self.grid_x = None
        self.grid_y = None
        self.grid_z = None

        # Controles para el gráfico 2D
        self.interpolation_combo = QComboBox()
        self.interpolation_combo.addItems(["linear", "nearest", "cubic"])
        self.contour_levels_spin = QSpinBox()
        self.contour_levels_spin.setRange(1, 100)
        self.contour_levels_spin.setValue(10)
        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems(["jet","rainbow","viridis", "plasma", "inferno", "magma", "cividis"])

        # Añadir controles al panel de control
        plot2d_controls = QGroupBox("Controles de Gráfico 2D")
        plot2d_layout = QVBoxLayout()
        plot2d_layout.addWidget(QLabel("Método de Interpolación"))
        plot2d_layout.addWidget(self.interpolation_combo)
        plot2d_layout.addWidget(QLabel("Niveles de Contorno"))
        plot2d_layout.addWidget(self.contour_levels_spin)
        plot2d_layout.addWidget(QLabel("Mapa de Colores"))
        plot2d_layout.addWidget(self.colormap_combo)

        # Añadir control para la resolución de la interpolación
        self.resolution_spin = QSpinBox()
        self.resolution_spin.setRange(10, 500)
        self.resolution_spin.setValue(100)
        plot2d_layout.addWidget(QLabel("Resolución de Interpolación"))
        plot2d_layout.addWidget(self.resolution_spin)

        # Añadir control para el título de la gráfica
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Ingrese el título de la gráfica")
        plot2d_layout.addWidget(QLabel("Título de la Gráfica"))
        plot2d_layout.addWidget(self.title_input)

        plot2d_controls.setLayout(plot2d_layout)
        control_panel.addWidget(plot2d_controls)

        # Botón para generar el gráfico 2D
        self.generate_2d_button = QPushButton("Generar Gráfico 2D")
        self.generate_2d_button.clicked.connect(self.generate_2d_plot)
        control_panel.addWidget(self.generate_2d_button)

        # Añadir botón para generar el gráfico 3D
        self.generate_3d_button = QPushButton("Generar Gráfico 3D")
        self.generate_3d_button.clicked.connect(self.generate_3d_plot)
        control_panel.addWidget(self.generate_3d_button)

# FUNCIONES DE LA APP VESPY

    def update_processing_tab(self):
        """Actualizar la pestaña según el modelo seleccionado."""
        model = self.model_selector.currentText()


    def save_inversion_model(self):
        """Guardar el modelo de inversión sin expandir los puntos."""
        # Verificar que `self.depths` y `self.resistivity` contengan datos válidos
        if self.depths is None or self.resistivity is None:
            self.eda_output.append("Error: No hay modelo de inversión para guardar.")
            return

        if self.depths.size == 0 or self.resistivity.size == 0:
            self.eda_output.append("Error: Los datos de profundidad o resistividad están vacíos.")
            return

        # Asignar la posición X de este modelo en función de los modelos previos
        x_position = len(self.saved_models) * self.spacing_spin.value()

        # Crear y guardar el modelo en `self.saved_models` con su profundidad y resistividad originales
        model_data = {
            "depths": self.depths,  
            "resistivity": self.resistivity, 
            "x_position": x_position
        }
        
        # Llama a las funciones saved models y eda output
        self.saved_models.append(model_data)
        self.eda_output.append(f"Modelo guardado en posición X = {x_position} m.")

    def load_inverted_models(self):
        """Cargar modelos invertidos desde archivos Excel o CSV."""
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Cargar Modelos Invertidos", "", "Excel Files (*.xlsx);;CSV Files (*.csv)", options=options)
        if not files:
            return

        for file in files:
            if file.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                self.eda_output.append(f"Formato de archivo no soportado: {file}")
                continue

            # Verificar que el archivo tenga las columnas necesarias
            if not {'Espesor (m)', 'Profundidad (m)', 'Resistividad (Ω*m)'}.issubset(df.columns):
                self.eda_output.append(f"Archivo inválido: {file}")
                continue

            # Convertir los datos del archivo en el formato adecuado
            thickness = df['Espesor (m)'].values
            depths = df['Profundidad (m)'].values
            resistivity = df['Resistividad (Ω*m)'].values


            # Guardar el modelo cargado usando save_model
            self.depths = depths
            self.resistivity = resistivity
            self.save_model()

            self.eda_output.append(f"Modelo cargado desde: {file}")



    def generate_2d_plot(self):
        """Generar el gráfico 2D interpolado de resistividad en función de la profundidad y distancia."""

        if len(self.saved_models) + len(self.loaded_models) < 2:
            self.eda_output.append("Se necesitan al menos dos modelos para generar el mapa 2D.")
            return

        # Recoger datos de profundidad y resistividad
        all_depths = []
        all_x_positions = []
        all_resistivities = []
        x_positions_set = set()

        for idx, model in enumerate(self.saved_models + self.loaded_models):
            x_position = model["x_position"]
            depths = list(model["depths"])  # Convertir RVector a lista
            resistivities = list(model["resistivity"])  # Convertir RVector a lista

            # Asegurarse de que cada modelo empiece en profundidad 0
            if depths[0] != 0:
                depths = [0] + depths
                resistivities = [resistivities[0]] + resistivities

            # Agregar puntos para cada capa según su espesor y resistividad
            for i in range(1, len(depths)):
                depth_range = range(int(depths[i-1]), int(depths[i]))
                resistivity_value = resistivities[i-1]
                for depth in depth_range:
                    all_x_positions.append(x_position)
                    all_depths.append(depth)
                    all_resistivities.append(resistivity_value)

            # Añadir la posición X al conjunto para etiquetar
            x_positions_set.add((x_position, f"sev-{idx + 1}"))

        # Obtener la resolución de interpolación seleccionada por el usuario
        resolution = self.resolution_spin.value()

        # Crear la cuadrícula para la interpolación
        grid_x = np.linspace(min(all_x_positions), max(all_x_positions), resolution)
        grid_y = np.linspace(min(all_depths), max(all_depths), resolution)
        grid_x, grid_y = np.meshgrid(grid_x, grid_y)

        # Interpolación de resistividad
        grid_z = griddata(
            points=(all_x_positions, all_depths),
            values=all_resistivities,
            xi=(grid_x, grid_y),
            method=self.interpolation_combo.currentText()
        )

        # Normalizar los valores para evitar negativos
        grid_z = np.where(grid_z < 0, 0, grid_z)  # Reemplazar valores negativos por 0

        # Limpiar la figura y agregar el nuevo gráfico
        self.figure_2d.clear()
        ax = self.figure_2d.add_subplot(111)

        # Generar contorno de niveles
        contour_levels = self.contour_levels_spin.value()
        colormap = self.colormap_combo.currentText()
        cmap = cm.get_cmap(colormap)
        norm = Normalize(vmin=np.nanmin(all_resistivities), vmax=np.nanmax(all_resistivities))
        contourf_plot = ax.contourf(grid_x, grid_y, grid_z, levels=contour_levels, cmap=cmap, norm=norm)

        # Añadir etiquetas verticales en la parte superior del gráfico con mejor fuente
        for x_position, label in x_positions_set:
            ax.text(x_position, min(all_depths) - (max(all_depths) * 0.05), label, rotation=90, verticalalignment='bottom', horizontalalignment='center', fontsize=12, fontweight='bold', color='black')

        # Configuración de la gráfica
        ax.set_xlabel("Distancia (m)")
        ax.set_ylabel("Profundidad (m)")
        ax.set_title(self.title_input.text() or "Mapa 2D de Resistividad")
        ax.invert_yaxis()  # Invertir el eje Y para que la profundidad crezca hacia abajo
        cbar = self.figure_2d.colorbar(contourf_plot, ax=ax)
        cbar.set_label("Resistividad (Ω*m)")

        # Dibujar el gráfico actualizado en el canvas
        self.canvas_2d.draw()


    def generate_3d_plot(self):
        """Generar el gráfico 3D interpolado de resistividad en función de la profundidad, distancia X y distancia Y."""

        if len(self.saved_models) + len(self.loaded_models) < 2:
            self.eda_output.append("Se necesitan al menos dos modelos para generar el mapa 3D.")
            return

        # Recoger datos de profundidad y resistividad
        all_depths = []
        all_x_positions = []
        all_y_positions = []
        all_resistivities = []

        for model in self.saved_models + self.loaded_models:
            x_position = model["x_position"]
            y_position = model["y_position"]
            depths = list(model["depths"])  # Convertir RVector a lista
            resistivities = list(model["resistivity"])  # Convertir RVector a lista

            # Asegurarse de que cada modelo empiece en profundidad 0
            if depths[0] != 0:
                depths = [0] + depths
                resistivities = [resistivities[0]] + resistivities

            # Agregar puntos para cada capa según su espesor y resistividad
            for i in range(1, len(depths)):
                depth_range = range(int(depths[i-1]), int(depths[i]))
                resistivity_value = resistivities[i-1]
                for depth in depth_range:
                    all_x_positions.append(x_position)
                    all_y_positions.append(y_position)
                    all_depths.append(depth)
                    all_resistivities.append(resistivity_value)

        # Obtener la resolución de interpolación seleccionada por el usuario
        resolution = self.resolution_spin.value()

        # Crear la cuadrícula para la interpolación
        grid_x = np.linspace(min(all_x_positions), max(all_x_positions), resolution)
        grid_y = np.linspace(min(all_y_positions), max(all_y_positions), resolution)
        grid_z = np.linspace(min(all_depths), max(all_depths), resolution)
        grid_x, grid_y, grid_z = np.meshgrid(grid_x, grid_y, grid_z, indexing='ij')

        # Interpolación de resistividad
        try:
            grid_r = griddata(
                points=(all_x_positions, all_y_positions, all_depths),
                values=all_resistivities,
                xi=(grid_x, grid_y, grid_z),
                method=self.interpolation_combo.currentText()
            )
        except scipy.spatial.qhull.QhullError:
            self.eda_output.append("Error de interpolación: los puntos de entrada no son suficientemente diversos para formar un simplex inicial válido.")
            return

        # Normalizar los valores para evitar negativos
        grid_r = np.where(grid_r < 0, 0, grid_r)  # Reemplazar valores negativos por 0

        # Limpiar la figura y agregar el nuevo gráfico
        self.figure_3d.clear()
        ax = self.figure_3d.add_subplot(111, projection='3d')

        # Generar el gráfico 3D
        for i in range(len(grid_z)):
            ax.plot_surface(grid_x[:, :, i], grid_y[:, :, i], grid_z[:, :, i], facecolors=cm.jet(grid_r[:, :, i] / np.nanmax(grid_r)), rstride=1, cstride=1, alpha=0.7, linewidth=0)

        # Configuración de la gráfica
        ax.set_xlabel("Distancia X (m)")
        ax.set_ylabel("Distancia Y (m)")
        ax.set_zlabel("Profundidad (m)")
        ax.set_title(self.title_input.text() or "Mapa 3D de Resistividad")
        ax.invert_zaxis()  # Invertir el eje Z para que la profundidad crezca hacia abajo

        # Dibujar el gráfico actualizado en el canvas
        self.canvas_3d.draw()
        
    def load_data(self):
        """Cargar datos desde un archivo Excel y mostrar la curva de resistividad."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Cargar archivo Excel", "", "Excel Files (*.xlsx *.xls)", options=options)
        
        if file_path:
            # Cargar los datos desde el archivo
            self.data = pd.read_excel(file_path)
            self.data.columns = self.data.columns.str.strip()  # Quita espacios en los nombres de columnas
            self.data = self.data.dropna()  # Eliminar filas con valores NaN
            
            # Extraer el nombre del archivo para las pestañas
            self.current_file = os.path.splitext(os.path.basename(file_path))[0]
            self.table_tabs.setTabText(0, f"{self.current_file}-datos")
            
            # Llenar la tabla de datos en la interfaz
            self.display_data_table()
            
            # Mostrar la curva automáticamente después de cargar los datos
            self.plot_data()

            self.analyze_data()
    
    def display_data_table(self):
        """Mostrar los datos cargados en la tabla de datos."""
        if self.data is not None:
            self.data_table.setRowCount(len(self.data))
            self.data_table.setColumnCount(len(self.data.columns))
            self.data_table.setHorizontalHeaderLabels(self.data.columns)

            for i in range(len(self.data)):
                for j in range(len(self.data.columns)):
                    self.data_table.setItem(i, j, QTableWidgetItem(str(self.data.iat[i, j])))


    def save_curve(self):
        """Guardar la curva suavizada en un archivo Excel."""
        if self.smoothed_data is not None:
            self.data['Suavizado (Ω*m)'] = self.smoothed_data
            file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Curva Suavizada", "", "Excel Files (*.xlsx *.xls)")
            if file_path:
                self.data.to_excel(file_path, index=False)



    def realizar_empalme(self):
        """Generar el empalme y almacenarlo internamente."""
        if self.data is not None:
            # Generar el empalme para 'pa (Ω*m)'
            empalme_data = self.data.groupby('AB/2')['pa (Ω*m)'].mean().reset_index()
            
            # Ajustar 'MN/2' para que coincida con el empalme de 'AB/2'
            empalme_data['MN/2'] = self.data.groupby('AB/2')['MN/2'].first().values
            
            self.empalme_data = empalme_data
            self.plot_data(empalme=True)

    def apply_filter(self):
        """Aplicar el filtro de suavizado seleccionado a los datos."""
        if self.data is not None:
            señal = self.data['pa (Ω*m)'].values
            n_ventana = self.window_size_spin.value()

            if self.filter_combo.currentText() == "Media Móvil":
                self.smoothed_data = np.convolve(señal, np.ones(n_ventana) / n_ventana, mode='same')
            elif self.filter_combo.currentText() == "Savitzky-Golay":
                self.smoothed_data = savgol_filter(señal, window_length=n_ventana * 2 + 1, polyorder=2)
            elif self.filter_combo.currentText() == "Exponencial":
                self.smoothed_data = pd.Series(señal).ewm(span=n_ventana, adjust=False).mean().values
            
            self.plot_data(smoothed=True)
            self.analyze_data()

    def save_filtered_data(self):
        """Guardar los datos filtrados en un archivo Excel."""
        if hasattr(self, 'smoothed_data') and self.smoothed_data is not None:
            # Crear un DataFrame con los datos filtrados
            filtered_df = self.data.copy()
            filtered_df['pa (Ω*m)'] = self.smoothed_data

            # Abrir un diálogo para seleccionar la ubicación y el nombre del archivo
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo Filtrado", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
            if file_path:
                # Guardar el DataFrame en un archivo Excel
                filtered_df.to_excel(file_path, index=False)
                self.eda_output.append(f"Archivo filtrado guardado en: {file_path}")
        else:
            self.eda_output.append("No hay datos filtrados disponibles para guardar.")


    def plot_data(self, empalme=False, smoothed=False):
        """Graficar los datos de resistividad."""
        if self.data is not None:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # Graficar la curva original de resistividad
            ab2 = self.data['AB/2'].values
            rhoa = self.data['pa (Ω*m)'].values
            ax.plot(ab2, rhoa, 'o-', label='Curva Original', color='blue')

            # Si hay datos de empalme, incluir el empalme
            if empalme and self.empalme_data is not None:
                empalme_ab2 = self.empalme_data['AB/2'].values
                empalme_rhoa = self.empalme_data['pa (Ω*m)'].values
                ax.plot(empalme_ab2, empalme_rhoa, 'o-', label='Curva de Empalme', color='green')
            
            # Si hay datos suavizados, incluir la curva suavizada
            if smoothed and self.smoothed_data is not None:
                ax.plot(ab2, self.smoothed_data, 'o-', label='Curva Suavizada', color='red')
            
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xlabel("AB/2 (m)")
            ax.set_ylabel("Resistividad aparente (Ω*m)")
            ax.legend()
            ax.set_title("Curva de Resistividad")
            self.canvas.draw()

    def analyze_data(self):
        """Realizar un análisis completo de los datos de resistividad."""
        if self.data is not None:
            resistivity = self.data['pa (Ω*m)'].values
            
            # Estadísticas descriptivas
            mean = np.mean(resistivity)
            std_dev = np.std(resistivity)
            median = np.median(resistivity)
            skewness = pd.Series(resistivity).skew()
            kurtosis = pd.Series(resistivity).kurt()

            # Histograma y CDF (acumulativo)
            self.analysis_figure.clear()
            ax1 = self.analysis_figure.add_subplot(221)
            sns.histplot(resistivity, bins=20, kde=False, color='blue', ax=ax1)
            ax1.set_title("Histograma de Resistividades")
            ax1.set_xlabel("Resistividad (Ω*m)")
            ax1.set_ylabel("Frecuencia")

            ax2 = self.analysis_figure.add_subplot(222)
            sns.histplot(resistivity, bins=20, kde=True, cumulative=True, color='green', ax=ax2)
            ax2.set_title("Histograma Acumulativo de Resistividades")
            ax2.set_xlabel("Resistividad (Ω*m)")
            ax2.set_ylabel("Frecuencia Acumulada")
            
            # Transformada de Fourier (FFT)
            n = len(resistivity)
            T = 1.0  # Supongamos una unidad de muestreo regular
            yf = fft(resistivity)
            xf = fftfreq(n, T)[:n//2]  # Solo las frecuencias positivas
            
            # Cálculo de la energía en cada frecuencia y frecuencia dominante
            magnitudes = 2.0/n * np.abs(yf[:n//2])
            dominant_freq = xf[np.argmax(magnitudes)]
            
            ax3 = self.analysis_figure.add_subplot(223)
            ax3.plot(xf, magnitudes, color='purple')
            ax3.set_title("Transformada de Fourier")
            ax3.set_xlabel("Frecuencia")
            ax3.set_ylabel("Magnitud")

            # Mostrar la frecuencia dominante y estadísticas en la terminal de salida
            self.eda_output.clear()
            self.eda_output.append("Análisis Estadístico Completo:\n")
            self.eda_output.append(f"Media: {mean:.2f} Ω*m")
            self.eda_output.append(f"Desviación Estándar: {std_dev:.2f} Ω*m")
            self.eda_output.append(f"Mediana: {median:.2f} Ω*m")
            self.eda_output.append(f"Skewness (Asimetría): {skewness:.2f}")
            self.eda_output.append(f"Kurtosis: {kurtosis:.2f}")
            self.eda_output.append("\nTransformada de Fourier:\n")
            self.eda_output.append(f"Frecuencia Dominante: {dominant_freq:.2f} Hz")
            self.eda_output.append(f"Magnitud de Frecuencia Dominante: {magnitudes.max():.2f}")
            self.analysis_canvas.draw()

    def invert_model(self):
        """Realizar la inversión de resistividad y mostrar resultados."""
        if self.data is not None:
            # Usar los datos de empalme si están disponibles
            data_to_use = self.empalme_data if hasattr(self, 'empalme_data') and self.empalme_data is not None else self.data

            # Usar los datos filtrados si están disponibles
            if hasattr(self, 'smoothed_data') and self.smoothed_data is not None:
                rhoa = self.smoothed_data
            else:
                rhoa = data_to_use['pa (Ω*m)'].values

            # Extraer vectores para la inversión
            ab2 = data_to_use['AB/2'].values
            mn2 = data_to_use['MN/2'].values if 'MN/2' in data_to_use.columns else None

            # Verificar que las longitudes de los vectores sean iguales
            if len(rhoa) != len(ab2) or (mn2 is not None and len(rhoa) != len(mn2)):
                raise ValueError("Las longitudes de los vectores rhoa, ab2 y mn2 (si está presente) deben ser iguales.")

            # Configurar los parámetros y ejecutar la inversión
            ves = VESManager()
            n_layers = self.layer_spin.value()
            lambda_val = self.lambda_spin.value()
            lambda_factor = self.lambda_factor_spin.value()
            error = np.ones_like(rhoa) * 0.03
            
            # Calcular profundidad máxima automáticamente como max(AB/2) / 3
            max_depth = np.max(ab2) / 3

            # Obtener el método seleccionado
            method = self.model_selector.currentText()

            if method == 'Levenberg-Marquardt':
                print("No disponible")
                return
            else:
                # Ejecutar la inversión con o sin mn2 usando la navaja de Occam
                if mn2 is not None:
                    model = ves.invert(rhoa, error, ab2=ab2, mn2=mn2, nLayers=n_layers, lam=lambda_val, lambdaFactor=lambda_factor)
                else:
                    model = ves.invert(rhoa, error, ab2=ab2, nLayers=n_layers, lam=lambda_val, lambdaFactor=lambda_factor)

            # Graficar datos observados y curva ajustada en el modelo de inversión
            self.inversion_figure.clear()
            ax1 = self.inversion_figure.add_subplot(121)
            ves.showData(rhoa, ab2=ab2, ax=ax1, label="Datos Observados", color="C0", marker="o")
            ves.showData(ves.inv.response, ab2=ab2, ax=ax1, label="Curva Invertida", color="C1")
            ax1.set_xscale("log")
            ax1.set_yscale("log")
            ax1.set_title("Ajuste del Modelo")
            ax1.set_ylabel("AB/2 (m)")
            ax1.set_xlabel("Resistividad aparente (Ω*m)")
            ax1.legend()

            # Extraer profundidades y resistividades calculadas por el modelo
            depths = np.cumsum(model[:n_layers - 1])  # Calcular profundidades acumuladas
            resistividades = model[n_layers - 1:]  # Resistividades de las capas

            # Convertir profundidades a espesores
            thickness = np.diff(np.concatenate(([0], depths)))  # Espesores de las capas

            # Graficar el modelo de capas
            ax2 = self.inversion_figure.add_subplot(122)
            ves.showModel(
                model=np.concatenate((thickness, resistividades)),  # Modelo combinado
                ax=ax2,
                plot="semilogy",
                zmax=max_depth  # Se limita la profundidad visualizada
            )
            ax2.set_title("Modelo de Resistividad 1D")
            self.inversion_canvas.draw()

            # Almacenar y actualizar la tabla de inversión
            self.depths = depths
            self.resistivity = resistividades
            self.update_model_table(thickness, depths, resistividades)
            self.table_tabs.setTabText(1, f"{self.current_file}-inversión")

            # Store the results for further processing
            self.thickness = thickness
            self.resistivities = resistividades

    def find_water(self):
        # Lithological classification based on aquifer characteristics
        def classify_lithology(thickness, resistivities):
            lithology = []
            for t, r in zip(thickness, resistivities):
                if r < 10 and t > 5:
                    lithology.append("Aquifer")
                elif r < 100 and t > 2:
                    lithology.append("Permeable Rock")
                else:
                    lithology.append("Impermeable Rock")
            return lithology

        # Adjust probabilities to consider impermeable rocks
        def adjust_probabilities(probabilities, lithology):
            adjusted_probabilities = []
            for prob, lith in zip(probabilities, lithology):
                if lith == "Impermeable Rock":
                    adjusted_probabilities.append([0.0])  # Exploitation probability is 0 for impermeable rocks
                else:
                    adjusted_probabilities.append(prob)
            return np.array(adjusted_probabilities)

        # Obtain lithological classification
        lithology = classify_lithology(self.thickness, self.resistivities)
        print("Lithological classification:", lithology)

        # Dummy probabilities for demonstration purposes
        probabilities = np.random.rand(len(self.thickness), 1)

        # Adjust probabilities
        adjusted_probabilities = adjust_probabilities(probabilities, lithology)

        # Visualize the model with classifications
        self.plot_classified_layers(self.thickness, self.resistivities, adjusted_probabilities, lithology)

    def plot_classified_layers(self, thickness, resistivities, probabilities, lithology):
        fig, ax = plt.subplots(figsize=(6, 8))
        cumulative_depth = 0
        for i in range(len(thickness)):
            probability = probabilities[i][0]  # Convert to scalar value
            color = plt.cm.Blues(probability)
            edge_color = 'black' if probability > 0.5 else 'white'  # Edge contrast
            ax.fill_betweenx([cumulative_depth, cumulative_depth + thickness[i]], 0, 1, color=color, edgecolor=edge_color)
            ax.text(0.5, cumulative_depth + thickness[i] / 2, f'{lithology[i]}\n{probability * 100:.1f}%', 
                    va='center', ha='center', color='white' if probability > 0.5 else 'black', fontsize=10, weight='bold')
            cumulative_depth += thickness[i]
        ax.set_yscale('log')
        ax.set_ylim(cumulative_depth, 0.1)  # Adjust lower limit to avoid log(0) issues
        ax.set_xlim(0, 1)
        ax.set_xticks([])
        ax.set_yticks(np.logspace(np.log10(0.1), np.log10(cumulative_depth), num=10))
        ax.set_ylabel('Depth (m)')
        ax.set_title('Layer Classification')
        plt.show()

        
    def update_model_table(self, thickness, depths, resistivity):
        """Actualizar la tabla de inversión con espesores, profundidades y resistividades."""
        self.model_table.setRowCount(len(resistivity))
        self.model_table.setColumnCount(3)
        self.model_table.setHorizontalHeaderLabels(["Espesor (m)", "Profundidad (m)", "Resistividad (Ω*m)"])
        
        for i in range(len(resistivity)):
            if i < len(thickness):
                self.model_table.setItem(i, 0, QTableWidgetItem(f"{thickness[i]:.2f}"))
                self.model_table.setItem(i, 1, QTableWidgetItem(f"{depths[i]:.2f}"))
            self.model_table.setItem(i, 2, QTableWidgetItem(f"{resistivity[i]:.2f}"))

    
    def plot_inversion_results(self, ves, model):
        """Actualizar la visualización de los resultados de inversión."""
        self.inversion_figure.clear()
        ax = self.inversion_figure.add_subplot(111)
        ves.showModel(model, ax=ax, plot="semilogy")
        ax.set_title("Modelo de Resistividad 1D")
        self.inversion_canvas.draw()

    def save_inversion_table(self):
        """Guardar la tabla del resultado de la inversión en un archivo."""
        if self.depths is None or self.resistivity is None:
            self.eda_output.append("Error: No hay datos de inversión para guardar.")
            return

        if self.depths.size == 0 or self.resistivity.size == 0:
            self.eda_output.append("Error: Los datos de profundidad o resistividad están vacíos.")
            return

        # Crear un DataFrame con los datos de inversión, excluyendo la última resistividad
        thickness = np.diff(np.concatenate(([0], self.depths)))  # Espesores de las capas

        # Imprimir las longitudes de las arrays para verificar
        print(f"Longitud de thickness: {len(thickness)}")
        print(f"Longitud de depths: {len(self.depths)}")
        print(f"Longitud de resistivity: {len(self.resistivity)}")

        df = pd.DataFrame({
            "Espesor (m)": thickness,
            "Profundidad (m)": self.depths,
            "Resistividad (Ω*m)": self.resistivity[:-1] 
        })
        # Guardar el DataFrame en un archivo
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, "Guardar Tabla de Inversión", "", "Excel Files (*.xlsx);;CSV Files (*.csv)", options=options)
        if not file:
            return

        if file.endswith('.xlsx'):
            df.to_excel(file, index=False)
        elif file.endswith('.csv'):
            df.to_csv(file, index=False)
        else:
            self.eda_output.append("Formato de archivo no soportado.")
            return

        self.eda_output.append(f"Tabla de inversión guardada en: {file}")
        self.eda_output.append("Nota: Por favor, copie y pegue la última resistividad en la tabla guardada antes de cargarla.")

    def save_model(self, x_position=None, y_position=None):
        """Guardar el modelo de inversión actual."""

        # Solicitar la posición X del usuario
        x_position, ok = QInputDialog.getDouble(self, "Posición X", "Ingrese la posición X para el modelo cargado:", 0, -10000, 10000, 2)
        if not ok:
            self.eda_output.append("Carga del modelo cancelada.")
            return

        # Solicitar la posición Y del usuario
        y_position, ok = QInputDialog.getDouble(self, "Posición Y", "Ingrese la posición Y para el modelo cargado:", 0, -10000, 10000, 2)
        if not ok:
            self.eda_output.append("Carga del modelo cancelada.")
            return

        if self.depths is None or self.resistivity is None:
            self.eda_output.append("Error: No hay modelo de inversión para guardar.")
            return

        if self.depths.size == 0 or self.resistivity.size == 0:
            self.eda_output.append("Error: Los datos de profundidad o resistividad están vacíos.")
            return

        # Crear y guardar el modelo en `self.saved_models` con su profundidad y resistividad originales
        model_data = {
            "depths": self.depths,  
            "resistivity": self.resistivity, 
            "x_position": x_position,
            "y_position": y_position  # Añadir coordenada Y
        }
        
        self.saved_models.append(model_data)
        self.eda_output.append(f"Modelo guardado en posición X = {x_position} m, Y = {y_position} m.")

def main():
    app = QApplication(sys.argv)
    
    welcome_window = WelcomeWindow()
    welcome_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()