from pathlib import Path
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, 
                             QTableWidget, QTableWidgetItem, QComboBox, QDoubleSpinBox, 
                             QSpinBox, QLabel, QGroupBox, QToolBar, QAction, QPushButton, 
                             QTabWidget, QTextEdit, QLineEdit, QInputDialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GUI:
    def init_gui(self, image_path):
        # Crear widget central
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        # Layout principal: HBox dividido en paneles de control, visualización y tablas
        main_layout = QHBoxLayout(self.main_widget)
        
        # Barra de herramientas con botones de acciones principales
        toolbar = QToolBar("Herramientas")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Acción para cargar datos con icono "cargar.png"
        load_action = QAction(QIcon(str(image_path / "cargar.png")), "Cargar Datos", self)
        load_action.triggered.connect(self.load_data)
        toolbar.addAction(load_action)

        # Acción para invertir el modelo con icono "inversion.png"
        inversion_action = QAction(QIcon(str(image_path / "inversion.png")), "Invertir Modelo", self)
        inversion_action.triggered.connect(self.invert_model)
        toolbar.addAction(inversion_action)
        
        # Acción para cargar modelos invertidos con icono "cargar_modelo.png"
        load_model_action = QAction(QIcon(str(image_path / "cargar_modelo.png")), "Cargar Modelos Invertidos", self)
        load_model_action.triggered.connect(self.load_inverted_models)
        toolbar.addAction(load_model_action)

        # Acción para guardar la tabla del resultado de la inversión con icono "guardar_tabla.png"
        save_table_action = QAction(QIcon(str(image_path / "guardar_tabla.png")), "Guardar Tabla de Inversión", self)
        save_table_action.triggered.connect(self.save_inversion_table)
        toolbar.addAction(save_table_action)

        # Acción para generar el gráfico 2D con icono "generar_2d.png"
        generate_2d_action = QAction(QIcon(str(image_path / "generar_2d.png")), "Generar Gráfico 2D", self)
        generate_2d_action.triggered.connect(self.generate_2d_plot)
        toolbar.addAction(generate_2d_action)

        # Acción para guardar la figura 2D con icono "guardar_2d.png"
        save_2d_action = QAction(QIcon(str(image_path / "guardar_2d.png")), "Guardar Figura 2D", self)
        save_2d_action.triggered.connect(self.save_2d_figure)
        toolbar.addAction(save_2d_action)

        # Acción para clasificar los datos con icono "agua.png"
        water_action = QAction(QIcon(str(image_path / "agua.png")), "Clasificar Agua", self)
        water_action.triggered.connect(self.find_water)
        toolbar.addAction(water_action)

        # Panel izquierdo - Controles y Procesamiento
        control_panel = QVBoxLayout()
        
        # Controles de preprocesamiento y procesamiento en pestañas de control
        control_tabs = QTabWidget()
        control_tabs.setStyleSheet("background-color: #e8e8e8;")
        
        # Pestaña Preprocesamiento
        preprocessing_tab = QWidget()
        preprocessing_layout = QVBoxLayout(preprocessing_tab)
        preprocessing_layout.addWidget(QLabel("Preprocesamiento"))
        
        self.empalme_button = QPushButton("Promediar MN")
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
        self.save_filtered_button = QPushButton("Guardar Curva Filtrada")
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
        self.water_button = QPushButton("Clasificar Agua")
        self.water_button.clicked.connect(self.find_water)
        processing_layout.addWidget(self.water_button)

        control_tabs.addTab(processing_tab, "Procesamiento")
        
        # Añadir control_tabs al panel izquierdo
        control_panel.addWidget(control_tabs)
        
        # Controles para el gráfico 2D
        plot2d_controls = QGroupBox("Controles de Gráfico 2D")
        plot2d_layout = QVBoxLayout()

        # Definir los controles para el gráfico 2D
        self.interpolation_combo = QComboBox()
        self.interpolation_combo.addItems(["linear", "nearest", "cubic"])
        self.contour_levels_spin = QSpinBox()
        self.contour_levels_spin.setRange(1, 100)
        self.contour_levels_spin.setValue(10)
        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems(["jet","rainbow","viridis", "plasma", "inferno", "magma", "cividis"])
        self.resolution_spin = QSpinBox()
        self.resolution_spin.setRange(10, 500)
        self.resolution_spin.setValue(100)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Ingrese el título de la gráfica")

        plot2d_layout.addWidget(QLabel("Método de Interpolación"))
        plot2d_layout.addWidget(self.interpolation_combo)
        plot2d_layout.addWidget(QLabel("Niveles de Contorno"))
        plot2d_layout.addWidget(self.contour_levels_spin)
        plot2d_layout.addWidget(QLabel("Mapa de Colores"))
        plot2d_layout.addWidget(self.colormap_combo)
        plot2d_layout.addWidget(QLabel("Resolución de Interpolación"))
        plot2d_layout.addWidget(self.resolution_spin)
        plot2d_layout.addWidget(QLabel("Título de la Gráfica"))
        plot2d_layout.addWidget(self.title_input)

        # Botón para generar gráfico 2D
        self.generate_2d_button = QPushButton("Generar Gráfico 2D")
        self.generate_2d_button.clicked.connect(self.generate_2d_plot)
        plot2d_layout.addWidget(self.generate_2d_button)

        # Botón para guardar figura 2D
        self.save_2d_button = QPushButton("Guardar Figura 2D")
        self.save_2d_button.clicked.connect(self.save_2d_figure)
        plot2d_layout.addWidget(self.save_2d_button)

        plot2d_controls.setLayout(plot2d_layout)
        control_panel.addWidget(plot2d_controls)

        # Añadir control_panel al layout principal
        main_layout.addLayout(control_panel, 1)
        
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
        
        visualization_layout.addWidget(self.tabs)

        # Terminal de texto para mostrar estadísticas descriptivas y análisis
        self.eda_output = QTextEdit()
        self.eda_output.setReadOnly(True)
        self.eda_output.setFixedHeight(150)
        visualization_layout.addWidget(self.eda_output)
        
        # Añadir visualización al layout principal
        main_layout.addLayout(visualization_layout, 3)
        
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
        
        # Añadir tablas al layout principal
        main_layout.addLayout(table_layout, 1)