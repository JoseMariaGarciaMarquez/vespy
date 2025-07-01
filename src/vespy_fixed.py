"""
VESPY - Visualización y Procesamiento de Datos de Sondeo Eléctrico Vertical (VES) en Python

Funcionalidades Principales:
- Ventana principal con título "VESPY" y tamaño 1600x900 píxeles.
- Barra de herramientas para cargar datos, invertir modelos, guardar tablas y generar gráficos.
- Panel de control con pestañas para preprocesamiento (empalme y suavizado) y procesamiento (inversión de resistividad).
- Visualización de gráficos: curva y empalme, análisis estadístico, resultados de inversión y gráfico 2D.
- Terminal de texto para mostrar estadísticas descriptivas y análisis.
- Tablas de datos cargados y modelo de inversión.

Métodos Principales:
- load_data: Carga datos desde un archivo.
- save_curve: Guarda la curva de resistividad suavizada.
- save_inversion_table: Guarda la tabla del modelo de inversión.
- realizar_empalme: Genera el empalme de los datos.
- apply_filter: Aplica un filtro de suavizado.
- plot_data: Grafica los datos de resistividad.
- analyze_data: Realiza un análisis estadístico completo.
- invert_model: Realiza la inversión de resistividad.
- generate_2d_plot: Genera un gráfico 2D interpolado.
- load_inverted_models: Carga modelos invertidos desde archivos.
- save_2d_figure: Guarda la figura 2D generada.
- find_water: Clasifica los datos para identificar posibles acuíferos.

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
"""
import sys
import os
import pandas as pd
from pathlib import Path
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, 
                             QTableWidget, QTableWidgetItem, QComboBox, QDoubleSpinBox, 
                             QSpinBox, QLabel, QGroupBox, QToolBar, QAction, QPushButton, 
                             QTabWidget, QTextEdit, QLineEdit, QInputDialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from data_analysis import Analysis
from load import DataLoader
from welcome import WelcomeWindow
from plot_ves import PlotVes
from invert_ves import InvertVes
from preprocessing import Preprocessing
from classified_ves import ClassifiedVes
from gui_ves import GUI
from help_window import HelpWindow, HelpInversionWindow, HelpPreprocessingWindow, HelpAnalysisWindow, HelpPlottingWindow, HelpUsageWindow
from loaded_data_files_window import LoadedDataFilesWindow
from loaded_inverted_models_window import LoadedInvertedModelsWindow
from support_window import SupportWindow

class SEVApp(QMainWindow, GUI):
    def __init__(self):
        super().__init__()
        self.plot_ves = PlotVes()
        self.invert_ves = InvertVes()
        self.preprocessing = Preprocessing(self)
        self.classified_ves = ClassifiedVes()
        self.current_2d_plot_title = None
        
        # Configuración de la ventana principal
        self.setWindowTitle("VESPY")
        self.setGeometry(100, 100, 1600, 900)  # Ventana más grande
        self.data_loader = DataLoader(self)
        
        # Obtener ruta de la carpeta de imágenes
        image_path = Path(__file__).parent.parent / 'images'
        self.setWindowIcon(QIcon(str(image_path / "logo.png")))

        # Inicializar GUI
        self.init_gui(image_path)

        # Variables para almacenar datos y resultados
        self.data = None
        self.smoothed_data = None
        self.empalme_data = None
        self.saved_models = []  # Lista para almacenar modelos de capas invertidos
        self.loaded_models = []  # Lista para almacenar modelos cargados
        self.depths = None
        self.resistivity = None
        self.model_path = "modelos"
        self.loaded_data_files = {}  # Diccionario para almacenar los datos cargados en memoria
        self.loaded_inverted_models = {}  # Diccionario para almacenar los modelos invertidos cargados en memoria
        
        # Parámetros para el gráfico 2D
        self.distances = None
        self.grid_x = None
        self.grid_y = None
        self.grid_z = None

        # Añadir el menú de ayuda y archivos cargados
        self.init_menus()

    def init_menus(self):
        menubar = self.menuBar()
        
        # Menú de ayuda
        help_menu = menubar.addMenu("Ayuda")
        
        # Submenú de Inversión
        inversion_help_action = QAction("Inversión", self)
        inversion_help_action.triggered.connect(self.show_inversion_help)
        help_menu.addAction(inversion_help_action)
        
        # Submenú de Preprocesamiento
        preprocessing_help_action = QAction("Preprocesamiento", self)
        preprocessing_help_action.triggered.connect(self.show_preprocessing_help)
        help_menu.addAction(preprocessing_help_action)
        
        # Submenú de Análisis de Datos
        analysis_help_action = QAction("Análisis de Datos", self)
        analysis_help_action.triggered.connect(self.show_analysis_help)
        help_menu.addAction(analysis_help_action)
        
        # Submenú de Generación de Gráficos
        plotting_help_action = QAction("Generación de Gráficos", self)
        plotting_help_action.triggered.connect(self.show_plotting_help)
        help_menu.addAction(plotting_help_action)
        
        # Submenú de Cómo Usar el Software
        usage_help_action = QAction("Cómo Usar el Software", self)
        usage_help_action.triggered.connect(self.show_usage_help)
        help_menu.addAction(usage_help_action)
        
        # Menú de archivos de datos cargados
        loaded_data_files_action = QAction("Archivos de Datos Cargados", self)
        loaded_data_files_action.triggered.connect(self.show_loaded_data_files)
        menubar.addAction(loaded_data_files_action)
        
        # Menú de modelos invertidos cargados
        loaded_inverted_models_action = QAction("Modelos Invertidos Cargados", self)
        loaded_inverted_models_action.triggered.connect(self.show_loaded_inverted_models)
        menubar.addAction(loaded_inverted_models_action)

        # Menú de soporte
        support_action = QAction("¡Quiero aportar!", self)
        support_action.triggered.connect(self.show_support_window)
        menubar.addAction(support_action)

    def show_support_window(self):
        self.support_window = SupportWindow()
        self.support_window.show()

    def show_inversion_help(self):
        self.inversion_help_window = HelpInversionWindow(self)
        self.inversion_help_window.show()

    def show_preprocessing_help(self):
        self.preprocessing_help_window = HelpPreprocessingWindow(self)
        self.preprocessing_help_window.show()

    def show_analysis_help(self):
        self.analysis_help_window = HelpAnalysisWindow(self)
        self.analysis_help_window.show()

    def show_plotting_help(self):
        self.plotting_help_window = HelpPlottingWindow(self)
        self.plotting_help_window.show()

    def show_usage_help(self):
        self.usage_help_window = HelpUsageWindow(self)
        self.usage_help_window.show()

    def show_loaded_data_files(self):
        self.loaded_data_files_window = LoadedDataFilesWindow(self)
        self.loaded_data_files_window.show()

    def show_loaded_inverted_models(self):
        self.loaded_inverted_models_window = LoadedInvertedModelsWindow(self)
        self.loaded_inverted_models_window.show()

    def load_data_from_file(self, file_path):
        """Cargar datos desde un archivo específico y mostrar la curva de resistividad."""
        if file_path.endswith(('.xlsx', '.xls')):
            self.data = self.data_loader.load_excel(file_path)
        elif file_path.endswith('.csv'):
            self.data = self.data_loader.load_csv(file_path)
        elif file_path.endswith('.ods'):
            self.data = self.data_loader.load_libreoffice(file_path)
            if self.data is None:
                return
        else:
            self.eda_output.append("Error: Formato de archivo no soportado.")
            return

        self.data.columns = self.data.columns.str.strip()  # Quita espacios en los nombres de columnas
        self.data = self.data.dropna()  # Eliminar filas con valores NaN
        
        # Convertir todas las columnas a formato numérico si es posible
        self.data = self.data.apply(pd.to_numeric, errors='coerce')

        # Verificar que los encabezados sean correctos
        required_columns = ['AB/2', 'MN/2', 'K', 'PN', 'PI', 'I (Ma)', '∆V (Mv)', 'pa (Ω*m)']
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        if missing_columns:
            self.data_loader.assign_columns(missing_columns)
        
        # Extraer el nombre del archivo para las pestañas
        self.current_file = os.path.splitext(os.path.basename(file_path))[0]
        self.table_tabs.setTabText(0, f"{self.current_file}-datos")
        
        # Llenar la tabla de datos en la interfaz
        self.display_data_table()
        
        # Mostrar la curva automáticamente después de cargar los datos
        self.plot_data()

        # Guardar los datos en memoria
        self.loaded_data_files[self.current_file] = self.data

    def load_data_from_memory(self, file_name):
        """Cargar datos desde la memoria y mostrar la curva de resistividad."""
        if file_name in self.loaded_data_files:
            self.data = self.loaded_data_files[file_name]
            self.current_file = file_name
            self.table_tabs.setTabText(0, f"{self.current_file}-datos")
            
            # Llenar la tabla de datos en la interfaz
            self.display_data_table()
            
            # Mostrar la curva automáticamente después de cargar los datos
            self.plot_data()
        else:
            self.eda_output.append(f"Error: El archivo '{file_name}' no se encuentra en memoria.")

    def load_inverted_model_from_memory(self, file_name):
        """Cargar un modelo invertido desde la memoria y mostrar los datos."""
        if file_name in self.loaded_inverted_models:
            model = self.loaded_inverted_models[file_name]
            self.depths = model['depths']
            self.resistivity = model['resistivity']
            self.current_file = file_name
            self.table_tabs.setTabText(1, f"{self.current_file}-inversión")
            
            # Llenar la tabla de inversión en la interfaz
            self.update_model_table(self.depths, self.resistivity)
            
            # Mostrar la curva automáticamente después de cargar los datos
            self.plot_data()
        else:
            self.eda_output.append(f"Error: El modelo invertido '{file_name}' no se encuentra en memoria.")
        
# FUNCIONES DE LA APP VESPY------------------------------------------------------------------------------

    def load_inverted_models(self):
        self.data_loader.load_inverted_models()

    def realizar_empalme(self):
        """Generar el empalme y almacenarlo internamente."""
        self.preprocessing.realizar_empalme()

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
        self.plot_ves.save_2d_figure(self)

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
            self.data['Suavizado (Ω*m)'] = self.smoothed_data
            file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Curva Suavizada", "", "Excel Files (*.xlsx *.xls)")
            if file_path:
                self.data.to_excel(file_path, index=False)

    def apply_filter(self):
        """Aplicar el filtro de suavizado seleccionado a los datos."""
        self.preprocessing.apply_filter()

    def save_filtered_data(self):
        """Guardar los datos filtrados en un archivo Excel."""
        self.preprocessing.save_filtered_data()

    def plot_data(self, empalme=False, smoothed=False):
        """Graficar los datos de resistividad."""
        self.plot_ves.plot_data(self.data, self.empalme_data if empalme else None, self.smoothed_data if smoothed else None, self.canvas, self.figure)

    def analyze_data(self):
        """Realizar un análisis completo de los datos de resistividad."""
        analysis = Analysis(self.data, self.analysis_figure, self.eda_output)
        analysis.analyze_data()

    def invert_model(self):
        """Realizar la inversión de resistividad y mostrar resultados."""
        depths, resistividades, thickness, rmse = self.invert_ves.invert_model(
            self.data, self.empalme_data, self.smoothed_data, self.layer_spin, self.lambda_spin, self.lambda_factor_spin,
            self.model_selector, self.eda_output, self.inversion_figure, self.inversion_canvas, self.current_file
        )

        if depths is not None and resistividades is not None:
            # Almacenar y actualizar la tabla de inversión
            self.depths = depths
            self.resistivity = resistividades
            self.update_model_table(thickness, depths, resistividades)
            self.table_tabs.setTabText(1, f"{self.current_file}-inversión")

            # Store the results for further processing
            self.thickness = thickness
            self.resistividades = resistividades

            # Mostrar el RMSE en la terminal de salida
            self.eda_output.append(f"Error Cuadrático Medio (RMSE) de la Inversión: {rmse:.2f}%")

    def find_water(self):
        """Clasificar los datos para identificar posibles acuíferos."""
        self.classified_ves.find_water(self.thickness, self.resistividades, self.eda_output)

    def update_model_table(self, thickness, depths, resistivity):
        """Actualizar la tabla de inversión con espesores, profundidades y resistividades."""
        self.model_table.setRowCount(len(resistivity))
        self.model_table.setColumnCount(3)
        self.model_table.setHorizontalHeaderLabels(["Espesor (m)", "Profundidad (m)", "Resistividad (Ω*m)"])
        
        for i in range(len(resistivity)):
            if i < len(thickness):
                self.model_table.setItem(i, 0, QTableWidgetItem(f"{thickness[i]:.2f}"))
                self.model_table.setItem(i, 1, QTableWidgetItem(f"{depths[i]:.2f}"))
            self.model_table.setItem(i, 2, QTableWidgetItem(f"{resistivity[i]:.2f}"))

    def save_inversion_table(self):
        """Guardar la tabla del resultado de la inversión en un archivo."""
        self.invert_ves.save_inversion_table(self)


def main():
    app = QApplication(sys.argv)
    
    welcome_window = WelcomeWindow()
    welcome_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
