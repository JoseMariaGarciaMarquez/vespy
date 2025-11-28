"""
VESPY - Visualización y Procesamiento de Datos de Sondeos Eléctricos Verticales (VES) en Python

Funcionalidades Principales:
- Ventana principal con título "VESPY" y tamaño 1600x900 píxeles.
- Barra de herramientas para cargar datos, guardar curvas suavizadas y cargar modelos invertidos.
- Panel de control con pestañas para preprocesamiento (empalme y suavizado) y procesamiento (inversión de resistividad).
- Visualización de gráficos: curva y empalme, análisis estadístico, resultados de inversión y gráfico 2D.
- Terminal de texto para mostrar estadísticas descriptivas y análisis.
- Tablas de datos cargados y modelo de inversión.

Autor: Jose Maria Garcia Marquez
Email: josemariagarciamarquez2.72@gmail.com
Versión: 3.0
"""
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.fft import fft, fftfreq
from scipy.interpolate import griddata
from scipy.signal import savgol_filter

# Intentar importar PyGIMLi (opcional)
try:
    import pygimli as pg
    from pygimli.physics import VESManager
    PYGIMLI_AVAILABLE = True
except ImportError:
    PYGIMLI_AVAILABLE = False
    print("⚠️ PyGIMLi no disponible. Instalar con: conda install -c gimli pygimli")

from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, 
    QTableWidget, QTableWidgetItem, QComboBox, QDoubleSpinBox, 
    QSpinBox, QLabel, QGroupBox, QToolBar, QAction, QPushButton, 
    QTabWidget, QTextEdit, QApplication, QInputDialog, QMessageBox,
    QDialog, QDialogButtonBox, QFormLayout, QCheckBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import Normalize
from matplotlib import cm

# Módulos propios
from calculos.empalme import realizar_empalme
from calculos.suavizado import apply_smoothing
from calculos.estadisticas import calcular_estadisticas
from inversion.inversion import (
    prepare_inversion_data, 
    extract_inversion_arrays, 
    invert_pygimli_discrete, 
    invert_simple_discrete,
    invert_smooth_model
)


class ColumnMappingDialog(QDialog):
    """Diálogo para mapear columnas del archivo a las columnas esperadas."""
    
    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mapeo de Columnas")
        self.setModal(True)
        self.columns = columns
        self.mapping = {}
        
        layout = QVBoxLayout(self)
        
        # Instrucciones
        instructions = QLabel(
            "Seleccione qué columna de su archivo corresponde a cada variable:"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Formulario de mapeo
        form_layout = QFormLayout()
        
        # ComboBox para AB/2
        self.ab2_combo = QComboBox()
        self.ab2_combo.addItems(["-- No seleccionado --"] + columns)
        form_layout.addRow("AB/2 (espaciamiento):", self.ab2_combo)
        
        # ComboBox para MN/2
        self.mn2_combo = QComboBox()
        self.mn2_combo.addItems(["-- No seleccionado --"] + columns)
        form_layout.addRow("MN/2 (opcional):", self.mn2_combo)
        
        # ComboBox para resistividad aparente
        self.rhoa_combo = QComboBox()
        self.rhoa_combo.addItems(["-- No seleccionado --"] + columns)
        form_layout.addRow("Resistividad aparente (pa/ρa):", self.rhoa_combo)
        
        layout.addLayout(form_layout)
        
        # Intentar detección automática
        self._auto_detect()
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def _auto_detect(self):
        """Intentar detectar automáticamente las columnas correctas."""
        for i, col in enumerate(self.columns):
            col_lower = col.lower().strip()
            
            # Detectar AB/2
            if 'ab/2' in col_lower or 'ab2' in col_lower or col_lower == 'ab':
                self.ab2_combo.setCurrentIndex(i + 1)
            
            # Detectar MN/2
            if 'mn/2' in col_lower or 'mn2' in col_lower or col_lower == 'mn':
                self.mn2_combo.setCurrentIndex(i + 1)
            
            # Detectar resistividad
            if any(x in col_lower for x in ['pa', 'rhoa', 'ρa', 'resistividad', 'ohm', 'ω']):
                self.rhoa_combo.setCurrentIndex(i + 1)
    
    def get_mapping(self):
        """Obtener el mapeo de columnas."""
        mapping = {}
        
        if self.ab2_combo.currentIndex() > 0:
            mapping[self.columns[self.ab2_combo.currentIndex() - 1]] = 'AB/2'
        
        if self.mn2_combo.currentIndex() > 0:
            mapping[self.columns[self.mn2_combo.currentIndex() - 1]] = 'MN/2'
        
        if self.rhoa_combo.currentIndex() > 0:
            mapping[self.columns[self.rhoa_combo.currentIndex() - 1]] = 'pa (Ω*m)'
        
        return mapping
    
    def validate(self):
        """Validar que al menos AB/2 y resistividad estén seleccionados."""
        if self.ab2_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Error", "Debe seleccionar la columna AB/2")
            return False
        if self.rhoa_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Error", "Debe seleccionar la columna de resistividad aparente")
            return False
        return True
    
    def accept(self):
        """Override accept para validar antes de cerrar."""
        if self.validate():
            super().accept()


class SEVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.setWindowTitle("VESPY - Vertical Electrical Sounding in Python")
        self.setGeometry(100, 100, 1600, 900)
        
        # Establecer ícono de la ventana
        from pathlib import Path
        icon_path = Path(__file__).parent.parent / 'images' / 'logo.png'
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # Crear widget central
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        # Layout principal: HBox dividido en paneles de control, visualización y tablas
        main_layout = QHBoxLayout(self.main_widget)
        
        # Panel izquierdo - Controles y Procesamiento
        control_panel = QVBoxLayout()
        
        # Barra de herramientas con botones de acciones principales
        toolbar = QToolBar("Herramientas")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)
        
        # Acción para cargar datos
        load_action = QAction("📂 Cargar Datos", self)
        load_action.triggered.connect(self.load_data)
        toolbar.addAction(load_action)

        # Acción para guardar la curva suavizada
        save_action = QAction("💾 Guardar Curva", self)
        save_action.triggered.connect(self.save_curve)
        toolbar.addAction(save_action)
        
        # Acción para cargar modelos invertidos
        load_model_action = QAction("📥 Cargar Modelos", self)
        load_model_action.triggered.connect(self.load_inverted_models)
        toolbar.addAction(load_model_action)

        # Acción para guardar la tabla del resultado de la inversión
        save_table_action = QAction("📊 Guardar Tabla", self)
        save_table_action.triggered.connect(self.save_inversion_table)
        toolbar.addAction(save_table_action)
        
        # Controles de preprocesamiento y procesamiento en pestañas de control
        control_tabs = QTabWidget()
        control_tabs.setStyleSheet("background-color: #e8e8e8;")
        
        # Pestaña Preprocesamiento
        preprocessing_tab = QWidget()
        preprocessing_layout = QVBoxLayout(preprocessing_tab)
        preprocessing_layout.addWidget(QLabel("<b>Preprocesamiento</b>"))
        
        self.empalme_button = QPushButton("🔗 Realizar Empalme")
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
        
        self.apply_filter_button = QPushButton("✨ Aplicar Suavizado")
        self.apply_filter_button.clicked.connect(self.apply_filter)
        
        filter_layout.addWidget(QLabel("Tipo de Filtro"))
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(QLabel("Tamaño de Ventana"))
        filter_layout.addWidget(self.window_size_spin)
        filter_layout.addWidget(self.apply_filter_button)
        filter_group.setLayout(filter_layout)
        preprocessing_layout.addWidget(filter_group)
        preprocessing_layout.addStretch()
        control_tabs.addTab(preprocessing_tab, "Preprocesamiento")
        
        # Pestaña de Procesamiento e Inversión
        processing_tab = QWidget()
        processing_layout = QVBoxLayout(processing_tab)

        # Selector de Modelo
        self.model_selector = QComboBox()
        if PYGIMLI_AVAILABLE:
            self.model_selector.addItems(["PyGIMLi (Occam's razor)"])
        else:
            self.model_selector.addItems(["Método Simple (sin PyGIMLi)"])
        processing_layout.addWidget(QLabel("Modelo de Inversión:"))
        processing_layout.addWidget(self.model_selector)
        
        # Parámetros de Inversión
        params_group = QGroupBox("Parámetros de Inversión")
        params_layout = QVBoxLayout()
        
        self.layer_spin = QSpinBox()
        self.layer_spin.setRange(2, 10)
        self.layer_spin.setValue(5)
        
        self.lambda_spin = QSpinBox()
        self.lambda_spin.setRange(1, 1000)
        self.lambda_spin.setValue(20)

        self.lambda_factor_spin = QDoubleSpinBox()
        self.lambda_factor_spin.setRange(0.1, 10.0)
        self.lambda_factor_spin.setSingleStep(0.1)
        self.lambda_factor_spin.setValue(0.8)

        params_layout.addWidget(QLabel("Número de Capas"))
        params_layout.addWidget(self.layer_spin)
        params_layout.addWidget(QLabel("Lambda (λ)"))
        params_layout.addWidget(self.lambda_spin)
        params_layout.addWidget(QLabel("Factor Lambda"))
        params_layout.addWidget(self.lambda_factor_spin)
        
        params_group.setLayout(params_layout)
        processing_layout.addWidget(params_group)

        # Botón de Inversión
        self.invert_button = QPushButton("⚡ Invertir Modelo")
        self.invert_button.clicked.connect(self.invert_model)
        processing_layout.addWidget(self.invert_button)

        # Grupo de Suavizado de Modelo
        smooth_group = QGroupBox("Suavizado de Modelo Invertido")
        smooth_layout = QVBoxLayout()
        
        self.smooth_order_combo = QComboBox()
        self.smooth_order_combo.addItems(["Primera Derivada (suave)", "Segunda Derivada (muy suave)"])
        
        self.smooth_layers_spin = QSpinBox()
        self.smooth_layers_spin.setRange(10, 100)
        self.smooth_layers_spin.setValue(30)
        self.smooth_layers_spin.setToolTip("Número de capas para el modelo suavizado")
        
        # Checkbox para escala logarítmica en profundidad
        self.log_depth_checkbox = QCheckBox("Escala logarítmica en profundidad")
        self.log_depth_checkbox.setChecked(True)  # Por defecto activado
        self.log_depth_checkbox.setToolTip("Ver profundidad en escala log (mejor para capas superficiales)")
        self.log_depth_checkbox.stateChanged.connect(self.update_inversion_plot_scale)
        
        self.smooth_button = QPushButton("🌊 Suavizar Modelo")
        self.smooth_button.clicked.connect(self.smooth_inverted_model)
        self.smooth_button.setEnabled(False)  # Se activa después de invertir
        
        smooth_layout.addWidget(QLabel("Orden de Suavizado:"))
        smooth_layout.addWidget(self.smooth_order_combo)
        smooth_layout.addWidget(QLabel("Capas suavizadas:"))
        smooth_layout.addWidget(self.smooth_layers_spin)
        smooth_layout.addWidget(self.log_depth_checkbox)
        smooth_layout.addWidget(self.smooth_button)
        
        smooth_group.setLayout(smooth_layout)
        processing_layout.addWidget(smooth_group)

        # Botón para guardar el modelo
        self.save_model_button = QPushButton("💾 Guardar Modelo")
        self.save_model_button.clicked.connect(lambda: self.save_model())
        processing_layout.addWidget(self.save_model_button)
        processing_layout.addStretch()

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
        
        # Tab 2: Análisis estadístico completo
        self.analysis_figure = Figure(figsize=(12, 8))
        self.analysis_canvas = FigureCanvas(self.analysis_figure)
        self.tabs.addTab(self.analysis_canvas, "Análisis Estadístico")

        # Tab 3: Resultados de Inversión
        self.inversion_figure = Figure(figsize=(10, 6))
        self.inversion_canvas = FigureCanvas(self.inversion_figure)
        self.tabs.addTab(self.inversion_canvas, "Inversión")
        
        # Tab 4: Gráfico 2D
        self.figure_2d = Figure(figsize=(10, 6))
        self.canvas_2d = FigureCanvas(self.figure_2d)
        self.tabs.addTab(self.canvas_2d, "Gráfico 2D")
        
        visualization_layout.addWidget(self.tabs)
        
        # Terminal de texto para mostrar estadísticas
        self.eda_output = QTextEdit()
        self.eda_output.setReadOnly(True)
        self.eda_output.setFixedHeight(150)
        self.eda_output.setStyleSheet("background-color: #2b2b2b; color: #00ff00; font-family: 'Courier New';")
        visualization_layout.addWidget(self.eda_output)
        
        # Área de tablas de datos e inversión
        table_layout = QVBoxLayout()
        self.table_tabs = QTabWidget()
        
        # Tabla de datos cargados
        self.data_table = QTableWidget()
        self.table_tabs.addTab(self.data_table, "Datos Cargados")
        
        # Tabla de modelo de inversión discreto
        self.model_table = QTableWidget()
        self.table_tabs.addTab(self.model_table, "Modelo Discreto")
        
        # Tabla de modelo suavizado
        self.smooth_model_table = QTableWidget()
        self.table_tabs.addTab(self.smooth_model_table, "Modelo Suavizado")
        
        table_layout.addWidget(self.table_tabs)
        
        # Configuración del layout principal (proporciones 18:57:25)
        main_layout.addLayout(control_panel, 18)
        main_layout.addLayout(visualization_layout, 57)
        main_layout.addLayout(table_layout, 25)

        # Variables para almacenar datos y resultados
        self.data = None
        self.smoothed_data = None
        self.smoothed_data_df = None  # DataFrame completo del suavizado
        self.empalme_data = None
        self.saved_models = []
        self.loaded_models = []
        self.depths = None
        self.resistivity = None
        self.model_path = "modelos"
        self.current_file = "datos"
        self._last_inversion_data = None  # Para almacenar datos de inversión para suavizado posterior
        
        # Parámetros para el gráfico 2D
        self.distances = None
        self.grid_x = None
        self.grid_y = None
        self.grid_z = None

        # Controles para el gráfico 2D
        plot2d_controls = QGroupBox("Controles de Gráfico 2D")
        plot2d_layout = QVBoxLayout()
        
        self.interpolation_combo = QComboBox()
        self.interpolation_combo.addItems(["linear", "nearest", "cubic"])
        
        self.contour_levels_spin = QSpinBox()
        self.contour_levels_spin.setRange(1, 100)
        self.contour_levels_spin.setValue(10)
        
        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems(["jet", "rainbow", "viridis", "plasma", "inferno", "magma", "cividis"])

        plot2d_layout.addWidget(QLabel("Método de Interpolación"))
        plot2d_layout.addWidget(self.interpolation_combo)
        plot2d_layout.addWidget(QLabel("Niveles de Contorno"))
        plot2d_layout.addWidget(self.contour_levels_spin)
        plot2d_layout.addWidget(QLabel("Mapa de Colores"))
        plot2d_layout.addWidget(self.colormap_combo)
        plot2d_controls.setLayout(plot2d_layout)
        control_panel.addWidget(plot2d_controls)

        # Botón para generar el gráfico 2D
        self.generate_2d_button = QPushButton("🗺️ Generar Gráfico 2D")
        self.generate_2d_button.clicked.connect(self.generate_2d_plot)
        control_panel.addWidget(self.generate_2d_button)

        # Mensaje de bienvenida
        self.eda_output.append("=" * 60)
        self.eda_output.append("🌊 VESPY - Vertical Electrical Sounding in Python")
        self.eda_output.append("📧 josemaria.garcia.marquez@gmail.com")
        self.eda_output.append("=" * 60)
        if PYGIMLI_AVAILABLE:
            self.eda_output.append("✅ PyGIMLi disponible - Inversión avanzada activada")
        else:
            self.eda_output.append("⚠️ PyGIMLi no disponible - Usando métodos alternativos")
        self.eda_output.append("📂 Cargue sus datos para comenzar...")
        self.eda_output.append("=" * 60)

    # ============================================================================
    # FUNCIONES DE CARGA Y GUARDADO DE DATOS
    # ============================================================================

    def load_data(self):
        """Cargar datos desde un archivo Excel y mostrar la curva de resistividad."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Cargar archivo", "", 
            "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;Text Files (*.txt)", 
            options=options
        )
        
        if file_path:
            try:
                # Cargar según extensión
                if file_path.endswith(('.xlsx', '.xls')):
                    self.data = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    self.data = pd.read_csv(file_path)
                elif file_path.endswith('.txt'):
                    self.data = pd.read_csv(file_path, sep='\t')
                
                # Limpiar nombres de columnas (quitar espacios)
                self.data.columns = self.data.columns.str.strip()
                self.data = self.data.dropna()
                
                # Mostrar diálogo de mapeo de columnas
                dialog = ColumnMappingDialog(list(self.data.columns), self)
                if dialog.exec_() == QDialog.Accepted:
                    mapping = dialog.get_mapping()
                    
                    if mapping:
                        # Aplicar el mapeo
                        self.data.rename(columns=mapping, inplace=True)
                        self.eda_output.append("📋 Columnas mapeadas:")
                        for old, new in mapping.items():
                            self.eda_output.append(f"  {old} → {new}")
                    
                    # Verificar que tenemos las columnas necesarias
                    if 'AB/2' not in self.data.columns or 'pa (Ω*m)' not in self.data.columns:
                        QMessageBox.critical(self, "Error", "No se encontraron las columnas necesarias después del mapeo.")
                        return
                    
                    # Extraer el nombre del archivo
                    self.current_file = os.path.splitext(os.path.basename(file_path))[0]
                    self.table_tabs.setTabText(0, f"{self.current_file}-datos")
                    
                    # Llenar la tabla y graficar
                    self.display_data_table()
                    self.plot_data()
                    self.analyze_data()
                    
                    self.eda_output.append(f"✅ Datos cargados: {self.current_file}")
                    self.eda_output.append(f"📊 Puntos: {len(self.data)}")
                else:
                    self.eda_output.append("❌ Carga de datos cancelada")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar datos:\n{str(e)}")
                self.eda_output.append(f"❌ Error: {str(e)}")
    
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
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Guardar Curva Suavizada", "", 
                "Excel Files (*.xlsx);;CSV Files (*.csv)"
            )
            if file_path:
                if file_path.endswith('.xlsx'):
                    self.data.to_excel(file_path, index=False)
                elif file_path.endswith('.csv'):
                    self.data.to_csv(file_path, index=False)
                self.eda_output.append(f"💾 Curva guardada: {os.path.basename(file_path)}")
        else:
            QMessageBox.warning(self, "Advertencia", "No hay datos suavizados para guardar.")

    def save_inversion_table(self):
        """Guardar la tabla del resultado de la inversión en un archivo."""
        if self.depths is None or self.resistivity is None:
            QMessageBox.warning(self, "Advertencia", "No hay datos de inversión para guardar.")
            return

        if hasattr(self.depths, 'size'):
            if self.depths.size == 0 or self.resistivity.size == 0:
                QMessageBox.warning(self, "Advertencia", "Los datos están vacíos.")
                return

        # Crear DataFrame
        thickness = np.diff(np.concatenate(([0], self.depths)))

        df = pd.DataFrame({
            "Espesor (m)": thickness,
            "Profundidad (m)": self.depths,
            "Resistividad (Ω*m)": self.resistivity[:-1] if len(self.resistivity) > len(thickness) else self.resistivity
        })
        
        # Guardar
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Tabla de Inversión", "", 
            "Excel Files (*.xlsx);;CSV Files (*.csv)"
        )
        if file_path:
            if file_path.endswith('.xlsx'):
                df.to_excel(file_path, index=False)
            elif file_path.endswith('.csv'):
                df.to_csv(file_path, index=False)
            self.eda_output.append(f"📊 Tabla guardada: {os.path.basename(file_path)}")

    def load_inverted_models(self):
        """Cargar modelos invertidos desde archivos."""
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, "Cargar Modelos Invertidos", "", 
            "Excel Files (*.xlsx);;CSV Files (*.csv)", 
            options=options
        )
        if not files:
            return

        for file in files:
            try:
                if file.endswith('.xlsx'):
                    df = pd.read_excel(file)
                elif file.endswith('.csv'):
                    df = pd.read_csv(file)

                if not {'Espesor (m)', 'Profundidad (m)', 'Resistividad (Ω*m)'}.issubset(df.columns):
                    self.eda_output.append(f"❌ Archivo inválido: {os.path.basename(file)}")
                    continue

                depths = df['Profundidad (m)'].values
                resistivity = df['Resistividad (Ω*m)'].values

                # Sugerir posición basada en modelos existentes
                suggested_x = 0.0 if len(self.saved_models) == 0 else float(self.saved_models[-1]["x_position"]) + 20.0
                
                x_position, ok = QInputDialog.getDouble(
                    self, 
                    "Posición X del Modelo", 
                    f"Ingrese la posición X para:\n{os.path.basename(file)}\n\n"
                    f"Modelos actuales: {len(self.saved_models)}\n"
                    f"Sugerencia: {suggested_x} m",
                    suggested_x,  # value
                    -10000.0,     # min
                    10000.0,      # max
                    1             # decimals
                )
                if not ok:
                    self.eda_output.append(f"⏭️ Modelo omitido: {os.path.basename(file)}")
                    continue

                # Guardar directamente en saved_models
                model_data = {
                    "depths": depths,
                    "resistivity": resistivity,
                    "x_position": float(x_position)
                }
                self.saved_models.append(model_data)

                self.eda_output.append(f"✅ Modelo cargado: {os.path.basename(file)}")
                self.eda_output.append(f"   Posición X: {x_position} m")
            
            except Exception as e:
                self.eda_output.append(f"❌ Error en {os.path.basename(file)}: {str(e)}")

    def save_model(self, x_position=None):
        """Guardar el modelo de inversión actual con su posición X y número de SEV."""
        
        # Verificar que hay modelo discreto
        if self.depths is None or self.resistivity is None:
            QMessageBox.warning(self, "Advertencia", "No hay modelo discreto para guardar.")
            return

        if hasattr(self.depths, 'size'):
            if self.depths.size == 0 or self.resistivity.size == 0:
                QMessageBox.warning(self, "Advertencia", "Datos vacíos.")
                return
        
        # Preguntar qué tipo de modelo guardar
        from PyQt5.QtWidgets import QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Guardar Modelo")
        layout = QVBoxLayout(dialog)
        
        # Tipo de modelo
        layout.addWidget(QLabel("Seleccione el tipo de modelo a guardar:"))
        model_type_combo = QComboBox()
        model_type_combo.addItems(["Modelo Discreto", "Modelo Suavizado"])
        
        # Deshabilitar suavizado si no existe
        if not hasattr(self, 'smooth_resistivity'):
            model_type_combo.setItemData(1, 0, Qt.UserRole - 1)  # Deshabilitar
            model_type_combo.setCurrentIndex(0)
        
        layout.addWidget(model_type_combo)
        
        # Número de SEV
        layout.addWidget(QLabel("\nNúmero de SEV:"))
        sev_spin = QSpinBox()
        sev_spin.setRange(1, 1000)
        sev_spin.setValue(len(self.saved_models) + 1)  # Sugerir siguiente número
        layout.addWidget(sev_spin)
        
        # Posición X
        layout.addWidget(QLabel("\nPosición X (distancia en metros):"))
        suggested_x = 0.0 if len(self.saved_models) == 0 else float(self.saved_models[-1]["x_position"]) + 20.0
        x_spin = QDoubleSpinBox()
        x_spin.setRange(-10000.0, 10000.0)
        x_spin.setValue(suggested_x)
        x_spin.setDecimals(1)
        layout.addWidget(x_spin)
        
        # Elevación Z (altura inicial del punto de medición)
        layout.addWidget(QLabel("\nElevación Z (altura sobre nivel de referencia en metros):"))
        suggested_z = 0.0 if len(self.saved_models) == 0 else float(self.saved_models[-1].get("z_elevation", 0.0))
        z_spin = QDoubleSpinBox()
        z_spin.setRange(-1000.0, 10000.0)
        z_spin.setValue(suggested_z)
        z_spin.setDecimals(1)
        z_spin.setSuffix(" m")
        layout.addWidget(z_spin)
        
        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        # Mostrar diálogo
        if dialog.exec_() != QDialog.Accepted:
            self.eda_output.append("❌ Guardado de modelo cancelado")
            return
        
        # Obtener valores
        model_type = model_type_combo.currentText()
        sev_number = sev_spin.value()
        x_position = x_spin.value()
        z_elevation = z_spin.value()
        
        # Seleccionar datos según tipo
        if "Suavizado" in model_type and hasattr(self, 'smooth_resistivity'):
            depths_to_save = self.smooth_depths
            resistivity_to_save = self.smooth_resistivity
            model_label = "Suavizado"
        else:
            depths_to_save = self.depths
            resistivity_to_save = self.resistivity
            model_label = "Discreto"

        # Crear y guardar el modelo
        model_data = {
            "depths": depths_to_save,  
            "resistivity": resistivity_to_save, 
            "x_position": float(x_position),
            "z_elevation": float(z_elevation),
            "sev_number": int(sev_number),
            "model_type": model_label
        }
        
        self.saved_models.append(model_data)
        self.eda_output.append(f"💾 Modelo {model_label} guardado")
        self.eda_output.append(f"   SEV: {sev_number}")
        self.eda_output.append(f"   Posición X: {x_position:.1f} m")
        self.eda_output.append(f"   Elevación Z: {z_elevation:.1f} m")
        self.eda_output.append(f"   Total de modelos: {len(self.saved_models)}")

    # ============================================================================
    # FUNCIONES DE PREPROCESAMIENTO
    # ============================================================================

    def realizar_empalme(self):
        """Generar el empalme y almacenarlo internamente usando módulo de cálculos."""
        if self.data is not None:
            try:
                # Usar módulo de empalme
                self.empalme_data = realizar_empalme(self.data, 'AB/2', 'pa (Ω*m)')
                self.plot_data(empalme=True)
                self.eda_output.append("🔗 Empalme realizado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error en empalme:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Advertencia", "Cargue datos primero.")

    def apply_filter(self):
        """Aplicar el filtro de suavizado seleccionado usando módulo de cálculos."""
        if self.data is None:
            QMessageBox.warning(self, "Advertencia", "Cargue datos primero.")
            return
            
        try:
            n_ventana = self.window_size_spin.value()
            
            # Mapear nombres de filtros
            filter_map = {
                "Media Móvil": "moving_average",
                "Savitzky-Golay": "savgol",
                "Exponencial": "exponential"
            }
            
            method = filter_map.get(self.filter_combo.currentText(), "moving_average")
            
            # Determinar qué datos suavizar (priorizar empalme)
            if self.empalme_data is not None:
                data_to_smooth = self.empalme_data
                self.eda_output.append(f"✨ Aplicando filtro a datos EMPALMADOS")
            else:
                data_to_smooth = self.data
                self.eda_output.append(f"✨ Aplicando filtro a datos ORIGINALES")
            
            # Usar módulo de suavizado (devuelve DataFrame con 'AB/2' y 'pa (Ω*m)')
            result = apply_smoothing(data_to_smooth, 'AB/2', 'pa (Ω*m)', method=method, window_size=n_ventana)
            
            # Guardar resultado completo como DataFrame
            self.smoothed_data_df = result
            # Guardar solo los valores para compatibilidad
            self.smoothed_data = result['pa (Ω*m)'].values
            
            self.plot_data(smoothed=True)
            self.eda_output.append(f"  Método: {self.filter_combo.currentText()}")
            self.eda_output.append(f"  Ventana: {n_ventana}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al aplicar filtro:\n{str(e)}")

    # ============================================================================
    # FUNCIONES DE VISUALIZACIÓN
    # ============================================================================

    def plot_data(self, empalme=False, smoothed=False):
        """Graficar los datos de resistividad."""
        if self.data is not None:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # Datos originales siempre en azul
            ab2 = self.data['AB/2'].values
            rhoa = self.data['pa (Ω*m)'].values
            ax.plot(ab2, rhoa, 'o-', label='Datos Originales', color='blue', markersize=5)

            # Empalme en verde (si existe)
            if empalme and self.empalme_data is not None:
                empalme_ab2 = self.empalme_data['AB/2'].values
                empalme_rhoa = self.empalme_data['pa (Ω*m)'].values
                ax.plot(empalme_ab2, empalme_rhoa, 's-', label='Datos Empalmados', color='green', markersize=6)
            
            # Suavizado en rojo (usa AB/2 del DataFrame suavizado)
            if smoothed and hasattr(self, 'smoothed_data_df') and self.smoothed_data_df is not None:
                smooth_ab2 = self.smoothed_data_df['AB/2'].values
                smooth_rhoa = self.smoothed_data_df['pa (Ω*m)'].values
                ax.plot(smooth_ab2, smooth_rhoa, '^-', label='Datos Suavizados', color='red', markersize=5)
            
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xlabel("AB/2 (m)", fontsize=12)
            ax.set_ylabel("Resistividad aparente (Ω*m)", fontsize=12)
            ax.legend(fontsize=10)
            ax.set_title("Curva de Resistividad Aparente", fontsize=14, fontweight='bold')
            ax.grid(True, which='both', ls='--', alpha=0.3)
            self.canvas.draw()

    def analyze_data(self):
        """Realizar análisis estadístico completo."""
        if self.data is not None:
            try:
                resistivity = self.data['pa (Ω*m)'].values
                
                mean = np.mean(resistivity)
                std_dev = np.std(resistivity)
                median = np.median(resistivity)
                skewness = pd.Series(resistivity).skew()
                kurtosis = pd.Series(resistivity).kurt()

                self.analysis_figure.clear()
                
                # Histograma
                ax1 = self.analysis_figure.add_subplot(221)
                sns.histplot(resistivity, bins=20, kde=False, color='blue', ax=ax1)
                ax1.set_title("Histograma de Resistividades", fontweight='bold')
                ax1.set_xlabel("Resistividad (Ω*m)")
                ax1.set_ylabel("Frecuencia")

                # Histograma acumulativo
                ax2 = self.analysis_figure.add_subplot(222)
                sns.histplot(resistivity, bins=20, kde=True, cumulative=True, color='green', ax=ax2)
                ax2.set_title("Distribución Acumulativa", fontweight='bold')
                ax2.set_xlabel("Resistividad (Ω*m)")
                ax2.set_ylabel("Frecuencia Acumulada")
                
                # FFT
                n = len(resistivity)
                yf = fft(resistivity)
                xf = fftfreq(n, 1.0)[:n//2]
                magnitudes = 2.0/n * np.abs(yf[:n//2])
                dominant_freq = xf[np.argmax(magnitudes)]
                
                ax3 = self.analysis_figure.add_subplot(223)
                ax3.plot(xf, magnitudes, color='purple', linewidth=2)
                ax3.set_title("Transformada de Fourier", fontweight='bold')
                ax3.set_xlabel("Frecuencia")
                ax3.set_ylabel("Magnitud")
                ax3.grid(True, alpha=0.3)

                # Boxplot
                ax4 = self.analysis_figure.add_subplot(224)
                ax4.boxplot(resistivity, vert=True)
                ax4.set_title("Diagrama de Caja", fontweight='bold')
                ax4.set_ylabel("Resistividad (Ω*m)")

                self.analysis_figure.tight_layout()
                self.analysis_canvas.draw()

                # Estadísticas en terminal
                self.eda_output.append("\n📊 Análisis Estadístico:")
                self.eda_output.append(f"  Media: {mean:.2f} Ω*m")
                self.eda_output.append(f"  Desv. Estándar: {std_dev:.2f} Ω*m")
                self.eda_output.append(f"  Mediana: {median:.2f} Ω*m")
                self.eda_output.append(f"  Asimetría: {skewness:.2f}")
                self.eda_output.append(f"  Curtosis: {kurtosis:.2f}")
                self.eda_output.append(f"  Frecuencia Dominante: {dominant_freq:.2f} Hz")
                
            except Exception as e:
                self.eda_output.append(f"❌ Error en análisis: {str(e)}")

    # ============================================================================
    # FUNCIONES DE INVERSIÓN
    # ============================================================================

    def update_inversion_plot_scale(self):
        """Actualizar escala del gráfico de inversión cuando cambia el checkbox."""
        # Solo actualizar si hay ejes en la figura de inversión
        if len(self.inversion_figure.axes) >= 2:
            ax2 = self.inversion_figure.axes[1]  # Panel derecho (modelo)
            
            # Obtener límites actuales
            ylim = ax2.get_ylim()
            max_depth = max(ylim)
            
            if self.log_depth_checkbox.isChecked():
                ax2.set_yscale('log')
                min_depth = 0.1
                ax2.set_ylim([max_depth, min_depth])
                # Mejorar formato de etiquetas en escala log
                from matplotlib.ticker import LogLocator, FuncFormatter
                ax2.yaxis.set_major_locator(LogLocator(base=10, numticks=6))
                ax2.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1, numticks=10))
                ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.1f}' if y >= 1 else f'{y:.2f}'))
                ax2.tick_params(axis='y', labelsize=9)
            else:
                ax2.set_yscale('linear')
                ax2.set_ylim([max_depth, 0])
                ax2.tick_params(axis='y', labelsize=10)
                # Restaurar formato por defecto
                ax2.yaxis.set_major_locator(plt.AutoLocator())
                ax2.yaxis.set_major_formatter(plt.ScalarFormatter())
            
            # Ajustar espaciado
            self.inversion_figure.tight_layout(pad=2.0, w_pad=3.0)
            self.inversion_canvas.draw()

    def invert_model(self):
        """Realizar la inversión de resistividad."""
        if self.data is None:
            QMessageBox.warning(self, "Advertencia", "Cargue datos primero.")
            return
        
        try:
            # Determinar qué datos usar: PRIORIDAD → Suavizado > Empalme > Originales
            if hasattr(self, 'smoothed_data_df') and self.smoothed_data_df is not None:
                # Usar datos suavizados (ya procesados con empalme)
                data_to_use = self.smoothed_data_df
                self.eda_output.append("\n📊 Usando datos SUAVIZADOS para inversión")
            elif self.empalme_data is not None:
                # Usar datos del empalme
                data_to_use = self.empalme_data
                self.eda_output.append("\n📊 Usando datos EMPALMADOS para inversión")
            else:
                # Usar datos originales
                data_to_use = self.data
                self.eda_output.append("\n📊 Usando datos ORIGINALES para inversión")
            
            ab2 = data_to_use['AB/2'].values
            mn2 = data_to_use['MN/2'].values if 'MN/2' in data_to_use.columns else np.ones_like(ab2)
            rhoa = data_to_use['pa (Ω*m)'].values

            n_layers = self.layer_spin.value()
            lambda_val = self.lambda_spin.value()
            lambda_factor = self.lambda_factor_spin.value()
            
            self.eda_output.append("⚡ Iniciando inversión...")
            self.eda_output.append(f"  Capas: {n_layers}")
            self.eda_output.append(f"  Lambda: {lambda_val}")
            self.eda_output.append(f"  Factor: {lambda_factor}")

            if PYGIMLI_AVAILABLE:
                self._invert_with_pygimli(ab2, mn2, rhoa, n_layers, lambda_val, lambda_factor)
            else:
                self._invert_simple(ab2, rhoa, n_layers)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en inversión:\n{str(e)}")
            self.eda_output.append(f"❌ Error: {str(e)}")

    def _invert_with_pygimli(self, ab2, mn2, rhoa, n_layers, lambda_val, lambda_factor):
        """Inversión con PyGIMLi - usando módulo de inversión."""
        # Usar función modularizada
        result = invert_pygimli_discrete(ab2, mn2, rhoa, n_layers, lambda_val, lambda_factor)
        
        if not result['success']:
            raise Exception(result.get('error', 'Error desconocido en inversión'))
        
        # Extraer resultados
        ves = result['ves_manager']
        thickness = result['thickness']
        depths = result['depths']
        resistivities = result['resistivities']
        max_depth = result['max_depth']
        chi2 = result['chi2']

        # Graficar
        self.inversion_figure.clear()
        
        ax1 = self.inversion_figure.add_subplot(121)
        ves.showData(rhoa, ab2=ab2, ax=ax1, label="Observados", color="C0", marker="o")
        ves.showData(result['response'], ab2=ab2, ax=ax1, label="Ajustados", color="C1")
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        ax1.set_title("Ajuste del Modelo", fontweight='bold')
        ax1.set_ylabel("AB/2 (m)")
        ax1.set_xlabel("Resistividad aparente (Ω*m)")
        ax1.legend()
        ax1.grid(True, which='both', ls='--', alpha=0.3)

        ax2 = self.inversion_figure.add_subplot(122)
        
        # Graficar modelo discreto manualmente con formato estándar
        depths_plot = [0]
        res_plot = [resistivities[0]]
        
        for i in range(len(depths)):
            depths_plot.append(depths[i])
            res_plot.append(resistivities[i])
            if i < len(resistivities) - 1:
                depths_plot.append(depths[i])
                res_plot.append(resistivities[i+1])
        
        # Extender última capa hasta max_depth
        depths_plot.append(max_depth)
        res_plot.append(resistivities[-1])
        
        ax2.plot(res_plot, depths_plot, 's-', color='#2E86AB', linewidth=2.5, 
                label='Modelo Discreto', markersize=7, alpha=0.8)
        ax2.set_xlabel("Resistividad (Ω*m)", fontsize=11)
        ax2.set_ylabel("Profundidad (m)", fontsize=11)
        ax2.set_title("Modelo de Capas 1D", fontweight='bold')
        ax2.invert_yaxis()
        ax2.set_xscale('log')
        
        # Aplicar escala logarítmica en Y si está activado el checkbox
        if self.log_depth_checkbox.isChecked():
            ax2.set_yscale('log')
            # Evitar profundidad 0 en escala log
            min_depth = 0.1 if depths_plot[0] == 0 else depths_plot[0]
            ax2.set_ylim([max_depth, min_depth])
            # Mejorar formato de etiquetas en escala log
            from matplotlib.ticker import LogLocator, FuncFormatter
            ax2.yaxis.set_major_locator(LogLocator(base=10, numticks=6))
            ax2.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1, numticks=10))
            ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.1f}' if y >= 1 else f'{y:.2f}'))
            ax2.tick_params(axis='y', labelsize=9)
        else:
            ax2.set_yscale('linear')
            ax2.set_ylim([max_depth, 0])
            ax2.tick_params(axis='y', labelsize=10)
        
        ax2.legend(loc='best', fontsize=9)
        ax2.grid(True, which='both', ls='--', alpha=0.3)
        
        # Ajustar espaciado para evitar solapamiento
        self.inversion_figure.tight_layout(pad=2.0, w_pad=3.0)
        self.inversion_canvas.draw()

        self.depths = depths
        self.resistivity = resistivities
        self.update_model_table(thickness, depths, resistivities)
        self.table_tabs.setTabText(1, f"{self.current_file}-inversión")
        
        self.eda_output.append(f"✅ Inversión completada (PyGIMLi)")
        self.eda_output.append(f"  Chi²: {chi2:.4f}")
        self.eda_output.append(f"  RMS: {np.sqrt(chi2):.4f}")
        
        # Activar botón de suavizado
        self.smooth_button.setEnabled(True)
        
        # Guardar datos necesarios para suavizado posterior (incluye modelo discreto)
        self._last_inversion_data = {
            'ab2': ab2,
            'mn2': mn2,
            'rhoa': rhoa,
            'max_depth': max_depth,
            'discrete_thickness': thickness,
            'discrete_depths': depths,
            'discrete_resistivities': resistivities,
            'discrete_response': result['response']
        }

    def _invert_simple(self, ab2, rhoa, n_layers):
        """Inversión simple sin PyGIMLi - usando módulo de inversión."""
        # Usar función modularizada
        result = invert_simple_discrete(ab2, rhoa, n_layers)
        
        if not result['success']:
            raise Exception(result.get('error', 'Error desconocido en inversión'))
        
        thickness = result['thickness']
        resistivities = result['resistivities']
        depths = result['depths']
        
        # Graficar
        self.inversion_figure.clear()
        
        ax1 = self.inversion_figure.add_subplot(121)
        ax1.loglog(ab2, rhoa, 'o-', label='Observados', markersize=6)
        ax1.set_xlabel("AB/2 (m)")
        ax1.set_ylabel("Resistividad aparente (Ω*m)")
        ax1.set_title("Datos Observados", fontweight='bold')
        ax1.legend()
        ax1.grid(True, which='both', ls='--', alpha=0.3)
        
        ax2 = self.inversion_figure.add_subplot(122)
        for i, (d, r) in enumerate(zip(np.concatenate(([0], depths)), resistivities)):
            if i < len(depths):
                ax2.barh(i, r, height=0.8, left=0, color=f'C{i}', alpha=0.7)
        ax2.set_ylabel("Capa")
        ax2.set_xlabel("Resistividad (Ω*m)")
        ax2.set_title("Modelo de Capas", fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        self.inversion_figure.tight_layout()
        self.inversion_canvas.draw()
        
        self.depths = depths
        self.resistivity = resistivities
        self.update_model_table(thickness, depths, resistivities)
        self.table_tabs.setTabText(1, f"{self.current_file}-inversión")
        
        self.eda_output.append("✅ Inversión completada (método simple)")
        self.eda_output.append("⚠️ Instale PyGIMLi para mejores resultados")
        
        # No activar suavizado para método simple (requiere PyGIMLi)
        self.smooth_button.setEnabled(False)

    def smooth_inverted_model(self):
        """Suavizar el modelo invertido usando 1ra o 2da derivada."""
        if not hasattr(self, '_last_inversion_data'):
            QMessageBox.warning(self, "Advertencia", "Primero debe invertir un modelo.")
            return
        
        if not PYGIMLI_AVAILABLE:
            QMessageBox.warning(self, "Advertencia", "El suavizado requiere PyGIMLi.")
            return
        
        try:
            # Obtener parámetros
            smooth_order = 1 if "Primera" in self.smooth_order_combo.currentText() else 2
            n_layers = self.smooth_layers_spin.value()
            lambda_val = self.lambda_spin.value()
            
            # Recuperar datos de inversión
            ab2 = self._last_inversion_data['ab2']
            mn2 = self._last_inversion_data['mn2']
            rhoa = self._last_inversion_data['rhoa']
            max_depth = self._last_inversion_data['max_depth']
            
            self.eda_output.append(f"\n🌊 Suavizando modelo...")
            self.eda_output.append(f"  Orden: {smooth_order}")
            self.eda_output.append(f"  Capas: {n_layers}")
            self.eda_output.append(f"  Profundidad máxima: {max_depth:.2f} m")
            
            # Llamar función de suavizado
            result = invert_smooth_model(ab2, mn2, rhoa, max_depth, lambda_val, smooth_order, n_layers)
            
            if not result['success']:
                QMessageBox.critical(self, "Error", f"Error en suavizado:\n{result['error']}")
                return
            
            # Extraer resultados del suavizado
            thicknesses = result['thicknesses']
            depths = result['depths']
            resistivities = result['resistivities']
            smooth_response = result['response']
            
            # NO BORRAR la figura - mantener el gráfico del modelo discreto
            # Solo actualizamos el panel derecho para comparación
            
            # Obtener los ejes existentes o crear nuevos
            if len(self.inversion_figure.axes) >= 2:
                ax1 = self.inversion_figure.axes[0]
                ax2 = self.inversion_figure.axes[1]
                ax2.clear()  # Solo limpiar el panel derecho
            else:
                # Si no hay ejes, crear ambos
                self.inversion_figure.clear()
                ax1 = self.inversion_figure.add_subplot(121)
                ax2 = self.inversion_figure.add_subplot(122)
                
                # Recrear gráfico de ajuste del modelo discreto
                if 'discrete_response' in self._last_inversion_data:
                    discrete_response = self._last_inversion_data['discrete_response']
                    ax1.loglog(ab2, rhoa, 'o', label='Observados', color='C0', markersize=6)
                    ax1.loglog(ab2, discrete_response, '-', label='Modelo Discreto', color='C1', linewidth=2)
                    ax1.set_xlabel("AB/2 (m)")
                    ax1.set_ylabel("Resistividad aparente (Ω*m)")
                    ax1.set_title("Ajuste del Modelo", fontweight='bold')
                    ax1.legend()
                    ax1.grid(True, which='both', ls='--', alpha=0.3)
            
            # Panel derecho: Comparación de modelos (discreto vs suavizado)
            # NO crear subplot nuevo, usar ax2 existente ya limpiado
            
            # Graficar modelo DISCRETO original (escalones)
            if 'discrete_depths' in self._last_inversion_data:
                disc_depths = self._last_inversion_data['discrete_depths']
                disc_res = self._last_inversion_data['discrete_resistivities']
                
                # Crear escalones para modelo discreto
                depths_plot = [0]
                res_plot = [disc_res[0]]
                
                for i in range(len(disc_depths)):
                    depths_plot.append(disc_depths[i])
                    res_plot.append(disc_res[i])
                    if i < len(disc_res) - 1:
                        depths_plot.append(disc_depths[i])
                        res_plot.append(disc_res[i+1])
                
                # Extender última capa hasta max_depth
                depths_plot.append(max_depth)
                res_plot.append(disc_res[-1])
                
                ax2.plot(res_plot, depths_plot, 's-', color='#2E86AB', linewidth=2.5, 
                        label='Modelo Discreto', markersize=7, alpha=0.8)
            
            # Graficar modelo SUAVIZADO (continuo)
            smooth_depths_plot = [0]
            smooth_res_plot = [resistivities[0]]
            
            for i in range(len(depths)):
                smooth_depths_plot.append(depths[i])
                smooth_res_plot.append(resistivities[i])
                if i < len(resistivities) - 1:
                    smooth_depths_plot.append(depths[i])
                    smooth_res_plot.append(resistivities[i+1])
            
            # Extender hasta max_depth
            smooth_depths_plot.append(max_depth)
            smooth_res_plot.append(resistivities[-1])
            
            ax2.plot(smooth_res_plot, smooth_depths_plot, '-', color='#F18F01', 
                    linewidth=3, label='Modelo Suavizado', alpha=0.9)
            
            ax2.set_xlabel("Resistividad (Ω*m)", fontsize=11)
            ax2.set_ylabel("Profundidad (m)", fontsize=11)
            ax2.set_title("Comparación: Discreto vs Suavizado", fontweight='bold')
            ax2.invert_yaxis()
            ax2.set_xscale('log')
            
            # Aplicar escala logarítmica en Y si está activado el checkbox
            if self.log_depth_checkbox.isChecked():
                ax2.set_yscale('log')
                min_depth = 0.1
                ax2.set_ylim([max_depth, min_depth])
                # Mejorar formato de etiquetas en escala log
                from matplotlib.ticker import LogLocator, FuncFormatter
                ax2.yaxis.set_major_locator(LogLocator(base=10, numticks=6))
                ax2.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1, numticks=10))
                ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.1f}' if y >= 1 else f'{y:.2f}'))
                # Rotar etiquetas si es necesario
                ax2.tick_params(axis='y', labelsize=9)
            else:
                ax2.set_yscale('linear')
                ax2.set_ylim([max_depth, 0])
                ax2.tick_params(axis='y', labelsize=10)
            
            ax2.legend(loc='best', fontsize=9)
            ax2.grid(True, which='both', ls='--', alpha=0.3)
            
            # Ajustar espaciado para evitar solapamiento
            self.inversion_figure.tight_layout(pad=2.0, w_pad=3.0)
            self.inversion_canvas.draw()
            
            # Actualizar tabla del modelo suavizado (en su propia pestaña)
            self.update_smooth_model_table(thicknesses, depths[1:], resistivities)
            self.table_tabs.setTabText(2, f"{self.current_file}-suavizado")
            
            # Guardar para exportación
            self.smooth_depths = depths[1:]
            self.smooth_resistivity = resistivities
            self.smooth_thickness = thicknesses
            
            # Mostrar métricas
            self.eda_output.append(f"✅ Suavizado completado")
            self.eda_output.append(f"  Chi²: {result['chi2']:.4f}")
            self.eda_output.append(f"  RRMS: {result['rrms']:.2f}%")
            self.eda_output.append(f"  Profundidad alcanzada: {result['max_depth_achieved']:.2f} m")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en suavizado:\n{str(e)}")
            self.eda_output.append(f"❌ Error: {str(e)}")

    def update_model_table(self, thickness, depths, resistivity):
        """Actualizar tabla de inversión discreta."""
        self.model_table.setRowCount(len(resistivity))
        self.model_table.setColumnCount(3)
        self.model_table.setHorizontalHeaderLabels(["Espesor (m)", "Profundidad (m)", "Resistividad (Ω*m)"])
        
        for i in range(len(resistivity)):
            if i < len(thickness):
                self.model_table.setItem(i, 0, QTableWidgetItem(f"{thickness[i]:.2f}"))
                self.model_table.setItem(i, 1, QTableWidgetItem(f"{depths[i]:.2f}"))
            else:
                self.model_table.setItem(i, 0, QTableWidgetItem("∞"))
                self.model_table.setItem(i, 1, QTableWidgetItem("∞"))
            self.model_table.setItem(i, 2, QTableWidgetItem(f"{resistivity[i]:.2f}"))
    
    def update_smooth_model_table(self, thickness, depths, resistivity):
        """Actualizar tabla de inversión suavizada."""
        self.smooth_model_table.setRowCount(len(resistivity))
        self.smooth_model_table.setColumnCount(3)
        self.smooth_model_table.setHorizontalHeaderLabels(["Espesor (m)", "Profundidad (m)", "Resistividad (Ω*m)"])
        
        for i in range(len(resistivity)):
            if i < len(thickness):
                self.smooth_model_table.setItem(i, 0, QTableWidgetItem(f"{thickness[i]:.2f}"))
                self.smooth_model_table.setItem(i, 1, QTableWidgetItem(f"{depths[i]:.2f}"))
            else:
                self.smooth_model_table.setItem(i, 0, QTableWidgetItem("∞"))
                self.smooth_model_table.setItem(i, 1, QTableWidgetItem("∞"))
            self.smooth_model_table.setItem(i, 2, QTableWidgetItem(f"{resistivity[i]:.2f}"))

    # ============================================================================
    # GRÁFICO 2D
    # ============================================================================

    def generate_2d_plot(self):
        """Generar gráfico 2D interpolado con múltiples modelos."""
        total_models = len(self.saved_models)
        
        if total_models < 2:
            QMessageBox.warning(
                self, "Advertencia", 
                f"Se necesitan al menos 2 modelos para generar el gráfico 2D.\n"
                f"Modelos actuales: {total_models}\n\n"
                f"Ejecute inversiones y guárdelas con diferentes posiciones X."
            )
            return
        
        # Preguntar título al usuario
        title, ok = QInputDialog.getText(
            self,
            "Título del Gráfico 2D",
            "Ingrese el título para el gráfico 2D:",
            text=f"Perfil 2D de Resistividad - {total_models} SEV"
        )
        
        if not ok or not title:
            title = f"Perfil 2D de Resistividad ({total_models} modelos)"

        try:
            self.eda_output.append(f"\n🗺️ Generando gráfico 2D con {total_models} modelos...")
            
            all_depths = []
            all_x_positions = []
            all_resistivities = []

            # Procesar cada modelo guardado
            for idx, model in enumerate(self.saved_models):
                x_position = model["x_position"]
                z_elevation = model.get("z_elevation", 0.0)  # Elevación del punto
                depths = np.array(model["depths"]) if hasattr(model["depths"], '__iter__') else model["depths"]
                resistivities = np.array(model["resistivity"]) if hasattr(model["resistivity"], '__iter__') else model["resistivity"]
                
                # Asegurar que son listas
                if not isinstance(depths, (list, np.ndarray)):
                    depths = [depths]
                if not isinstance(resistivities, (list, np.ndarray)):
                    resistivities = [resistivities]
                
                depths = list(depths)
                resistivities = list(resistivities)
                
                self.eda_output.append(f"  Modelo {idx+1}: X={x_position}m, Z={z_elevation}m, {len(depths)} capas")

                # Asegurar que comienza en profundidad 0 (relativa al punto)
                if len(depths) > 0 and depths[0] != 0:
                    depths = [0] + depths
                    resistivities = [resistivities[0]] + resistivities

                # Expandir cada capa por su espesor
                # Las profundidades son relativas, pero las convertimos a elevación absoluta
                for i in range(1, len(depths)):
                    depth_start = int(depths[i-1])
                    depth_end = int(depths[i])
                    resistivity_value = resistivities[i-1]
                    
                    # Generar puntos cada metro de profundidad
                    for depth in range(depth_start, depth_end):
                        all_x_positions.append(x_position)
                        # Convertir profundidad relativa a elevación absoluta
                        # z_elevation - depth = elevación absoluta
                        all_depths.append(z_elevation - depth)
                        all_resistivities.append(resistivity_value)

            if len(all_x_positions) == 0:
                raise ValueError("No se generaron puntos de datos para interpolación")

            # Crear grilla de interpolación
            x_min, x_max = min(all_x_positions), max(all_x_positions)
            y_min, y_max = min(all_depths), max(all_depths)
            
            grid_x = np.linspace(x_min, x_max, 100)
            grid_y = np.linspace(y_min, y_max, 100)
            grid_x, grid_y = np.meshgrid(grid_x, grid_y)

            # Interpolación
            interpolation_method = self.interpolation_combo.currentText()
            self.eda_output.append(f"  Interpolación: {interpolation_method}")
            
            grid_z = griddata(
                points=(all_x_positions, all_depths),
                values=all_resistivities,
                xi=(grid_x, grid_y),
                method=interpolation_method
            )

            # Eliminar valores negativos
            grid_z = np.where(grid_z < 0, 0, grid_z)

            # Graficar
            self.figure_2d.clear()
            ax = self.figure_2d.add_subplot(111)

            contour_levels = self.contour_levels_spin.value()
            colormap = self.colormap_combo.currentText()
            cmap = cm.get_cmap(colormap)
            
            # Normalización logarítmica para mejor visualización
            vmin = np.nanmin(all_resistivities)
            vmax = np.nanmax(all_resistivities)
            norm = Normalize(vmin=vmin, vmax=vmax)
            
            contourf_plot = ax.contourf(
                grid_x, grid_y, grid_z, 
                levels=contour_levels, 
                cmap=cmap, 
                norm=norm
            )

            # Marcar las posiciones de los modelos con líneas y labels de SEV
            for model in self.saved_models:
                x_pos = model["x_position"]
                z_elev = model.get("z_elevation", 0.0)
                sev_num = model.get("sev_number", "?")
                
                # Línea vertical desde la superficie (z_elevation) hacia abajo
                ax.axvline(x=x_pos, color='white', linestyle='--', alpha=0.7, linewidth=1.5)
                
                # Label de SEV rotado 90 grados en la elevación del punto
                ax.text(
                    x_pos, z_elev + (y_max - y_min) * 0.02,  # Ligeramente arriba de la elevación
                    f'SEV {sev_num}',
                    rotation=90,
                    verticalalignment='bottom',
                    horizontalalignment='center',
                    fontsize=10,
                    fontweight='bold',
                    color='white',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7)
                )

            ax.set_xlabel("Distancia (m)", fontsize=12, fontweight='bold')
            ax.set_ylabel("Elevación (m)", fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=14, fontweight='bold')
            # No invertir Y-axis porque ahora es elevación (positivo arriba)
            
            cbar = self.figure_2d.colorbar(contourf_plot, ax=ax)
            cbar.set_label("Resistividad (Ω*m)", fontsize=11)

            self.figure_2d.tight_layout()
            self.canvas_2d.draw()
            
            self.eda_output.append(f"✅ Gráfico 2D generado exitosamente")
            self.eda_output.append(f"   Rango X: {x_min:.1f} - {x_max:.1f} m")
            self.eda_output.append(f"   Profundidad máx: {y_max:.1f} m")
            self.eda_output.append(f"   Resistividad: {vmin:.1f} - {vmax:.1f} Ω*m")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en gráfico 2D:\n{str(e)}")
            self.eda_output.append(f"❌ Error en gráfico 2D: {str(e)}")
            import traceback
            self.eda_output.append(traceback.format_exc())


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("VESPY")
    app.setStyle("Fusion")
    
    main_window = SEVApp()
    main_window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
