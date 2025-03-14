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
from scipy.ndimage import gaussian_filter
from scipy.fft import fft, fftfreq
from scipy.interpolate import griddata
from scipy.signal import savgol_filter
import pygimli as pg
from pygimli.physics import VESManager
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, 
                             QTableWidget, QTableWidgetItem, QComboBox, QDoubleSpinBox, 
                             QSpinBox, QLabel, QGroupBox, QToolBar, QAction, QPushButton, 
                             QTabWidget, QTextEdit, QLineEdit, QInputDialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import Normalize
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
#from src.data_analysis import Analysis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_analysis import Analysis
from load import DataLoader
from welcome import WelcomeWindow
from plot_ves import PlotVes

class SEVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.setWindowTitle("VESPY")
        self.setGeometry(100, 100, 1600, 900)  # Ventana más grande
        self.data_loader = DataLoader(self)
        self.plot_ves = PlotVes()
        
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
        self.lambda_factor_spin.setRange(0.1, 100.0)
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
        #self.figure_2d = Figure(figsize=(10, 6))
        #self.canvas_2d = FigureCanvas(self.figure_2d)
        #self.tabs.addTab(self.canvas_2d, "Gráfico 2D")
        
        #visualization_layout.addWidget(self.tabs)

        ## Tab 5: Gráfico 3D
        #self.figure_3d = Figure(figsize=(10, 6))
        #self.canvas_3d = FigureCanvas(self.figure_3d)
        #self.tabs.addTab(self.canvas_3d, "Gráfico 3D")
        
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

        # Añadir botón para guardar la figura 2D
        self.save_2d_button = QPushButton("Guardar Figura 2D")
        self.save_2d_button.clicked.connect(self.save_2d_figure)
        control_panel.addWidget(self.save_2d_button)



# FUNCIONES DE LA APP VESPY

    def update_processing_tab(self):
        """Actualizar la pestaña según el modelo seleccionado."""
        model = self.model_selector.currentText()



    def load_inverted_models(self):
        self.data_loader.load_inverted_models()


    def generate_2d_plot(self):
        """Generar el gráfico 2D interpolado de resistividad en función de la profundidad y distancia."""
        interpolation_method = self.interpolation_combo.currentText()
        contour_levels = self.contour_levels_spin.value()
        colormap = self.colormap_combo.currentText()
        resolution = self.resolution_spin.value()
        title = self.title_input.text()
        
        canvas = self.plot_ves.generate_2d_plot(self.saved_models, self.loaded_models, self.eda_output, interpolation_method, contour_levels, colormap, resolution, title)
        if canvas:
            tab_title = f"{title}-2d"
            if self.current_2d_plot_title == tab_title:
                # Actualizar la figura existente
                index = self.tabs.indexOf(self.canvas_2d)
                self.tabs.removeTab(index)
            else:
                self.current_2d_plot_title = tab_title
            self.tabs.addTab(canvas, tab_title)
            self.canvas_2d = canvas

    def save_2d_figure(self):
        """Guardar la figura 2D generada."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Figura 2D", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)", options=options)
        if file_path:
            self.figure_2d.savefig(file_path)
            self.eda_output.append(f"Figura 2D guardada en: {file_path}")


    def analyze_and_recommend(self, data):
        """Realizar recomendaciones basadas en el análisis de los datos de resistividad."""
        analysis = Analysis(data, self.analysis_figure, self.eda_output)
        return analysis.analyze_and_recommend(data)

    def load_data(self):
        self.data_loader.load_data()

    
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
        analysis = Analysis(self.data, self.analysis_figure, self.eda_output)
        analysis.analyze_data()


    def invert_model(self):
        """Realizar la inversión de resistividad y mostrar resultados."""
        if self.data is not None:
            try:
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
                    self.eda_output.append("Método Levenberg-Marquardt no disponible.")
                    return
                else:
                    # Ejecutar la inversión con o sin mn2 usando la navaja de Occam
                    if mn2 is not None:
                        model = ves.invert(rhoa, error, ab2=ab2, mn2=mn2, nLayers=n_layers, lam=lambda_val, lambdaFactor=lambda_factor)
                    else:
                        model = ves.invert(rhoa, error, ab2=ab2, nLayers=n_layers, lam=lambda_val, lambdaFactor=lambda_factor)

                # Calcular el error cuadrático medio (RMSE) en términos de porcentaje
                rmse = np.sqrt(np.mean(((ves.inv.response - rhoa) / rhoa) ** 2)) * 100

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

                # Mostrar el RMSE en la terminal de salida
                self.eda_output.append(f"Error Cuadrático Medio (RMSE) de la Inversión: {rmse:.2f}%")

            except Exception as e:
                self.eda_output.append(f"Error durante la inversión: {str(e)}")

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

        # Solicitar el número de SEV del usuario
        sev_number, ok = QInputDialog.getInt(self, "Número de SEV", "Ingrese el número de SEV para el modelo cargado:", 0, 0, 10000, 1)
        if not ok:
            if self.saved_models:
                sev_number = self.saved_models[-1].get("sev_number", 0) + 1
            else:
                sev_number = 1

        # Solicitar la altura relativa del usuario
        relative_height, ok = QInputDialog.getDouble(self, "Altura Relativa", "Ingrese la altura relativa para el modelo cargado:", 0, -10000, 10000, 2)
        if not ok:
            relative_height = 0

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
            "y_position": y_position,
            "sev_number": sev_number,  # Añadir número de SEV
            "relative_height": relative_height  # Añadir altura relativa
        }

        self.saved_models.append(model_data)
        self.eda_output.append(f"Modelo guardado en posición X = {x_position} m, Y = {y_position} m, SEV = {sev_number}, Altura Relativa = {relative_height} m.")

def main():
    app = QApplication(sys.argv)
    
    welcome_window = WelcomeWindow()
    welcome_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()