from pathlib import Path
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QPalette
from PyQt5.QtWidgets import (QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, 
                             QTableWidget, QTableWidgetItem, QComboBox, QDoubleSpinBox, 
                             QSpinBox, QLabel, QGroupBox, QToolBar, QAction, QPushButton, 
                             QTabWidget, QTextEdit, QLineEdit, QInputDialog, QSplitter,
                             QFrame, QScrollArea, QProgressBar, QStatusBar, QAbstractScrollArea)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GUI:
    def init_gui(self, image_path):
        # Configurar el estilo general de la aplicación
        self.setStyleSheet(self.get_modern_style())
        
        # Configurar barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("VESPY - Listo para cargar datos")
        
        # Crear widget central con splitter para mejor control de dimensiones
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        # Layout principal con splitter horizontal
        main_layout = QHBoxLayout(self.main_widget)
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Crear la barra de herramientas mejorada
        self.create_modern_toolbar(image_path)
        
        # Panel izquierdo - Controles (mejorado)
        control_widget = self.create_control_panel()
        main_splitter.addWidget(control_widget)
        
        # Panel central - Visualización (mejorado)
        visualization_widget = self.create_visualization_panel()
        main_splitter.addWidget(visualization_widget)
        
        # Panel derecho - Tablas (mejorado)
        table_widget = self.create_table_panel()
        main_splitter.addWidget(table_widget)
        
        # Configurar proporciones del splitter
        main_splitter.setSizes([350, 800, 400])  # Izquierda, Centro, Derecha
        main_splitter.setStretchFactor(1, 1)  # El panel central se expande más

    def get_modern_style(self):
        """Devuelve un estilo moderno para la aplicación"""
        return """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QTabWidget::pane {
            border: 1px solid #c0c0c0;
            background-color: white;
            border-radius: 5px;
        }
        
        QTabWidget::tab-bar {
            alignment: left;
        }
        
        QTabBar::tab {
            background-color: #e1e1e1;
            border: 1px solid #c0c0c0;
            padding: 8px 15px;
            margin-right: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            min-width: 80px;
        }
        
        QTabBar::tab:hover {
            background-color: #d1d1d1;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            border-bottom-color: white;
            font-weight: bold;
        }
        
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #106ebe;
        }
        
        QPushButton:pressed {
            background-color: #005a9e;
        }
        
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
            background-color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 10px 0 10px;
            color: #0078d4;
        }
        
        QComboBox {
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 5px;
            background-color: white;
            min-height: 20px;
        }
        
        QComboBox:hover {
            border-color: #0078d4;
        }
        
        QSpinBox, QDoubleSpinBox, QLineEdit {
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 5px;
            background-color: white;
            min-height: 20px;
        }
        
        QSpinBox:hover, QDoubleSpinBox:hover, QLineEdit:hover {
            border-color: #0078d4;
        }
        
        QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {
            border-color: #0078d4;
            border-width: 2px;
        }
        
        QTextEdit {
            border: 1px solid #cccccc;
            border-radius: 4px;
            background-color: white;
            font-family: 'Consolas', monospace;
        }
        
        QTableWidget {
            gridline-color: #e0e0e0;
            background-color: white;
            alternate-background-color: #f9f9f9;
            selection-background-color: #0078d4;
            border: 1px solid #cccccc;
            border-radius: 4px;
        }
        
        QTableWidget::item {
            padding: 5px;
        }
        
        QToolBar {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f0f0f0, stop: 1 #e0e0e0);
            border: 1px solid #cccccc;
            spacing: 3px;
            padding: 2px;
        }
        
        QToolBar::separator {
            background-color: #cccccc;
            width: 1px;
            margin: 5px;
        }
        
        QStatusBar {
            background-color: #e0e0e0;
            border-top: 1px solid #cccccc;
            color: #333333;
        }
        
        QLabel {
            color: #333333;
        }
        
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        """

    def create_modern_toolbar(self, image_path):
        """Crear una barra de herramientas moderna y organizada"""
        toolbar = QToolBar("Herramientas")
        toolbar.setIconSize(QSize(32, 32))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)
        
        # Acción para cargar datos
        load_action = QAction(QIcon(str(image_path / "cargar.png")), "Cargar\nDatos", self)
        load_action.triggered.connect(self.load_data)
        load_action.setStatusTip("Cargar datos de sondeo eléctrico vertical")
        toolbar.addAction(load_action)
        
        toolbar.addSeparator()
        
        # Acción para invertir el modelo
        inversion_action = QAction(QIcon(str(image_path / "inversion.png")), "Invertir\nModelo", self)
        inversion_action.triggered.connect(self.invert_model)
        inversion_action.setStatusTip("Realizar inversión de resistividad")
        toolbar.addAction(inversion_action)
        
        # Acción para cargar modelos invertidos
        load_model_action = QAction(QIcon(str(image_path / "cargar_modelo.png")), "Cargar\nModelos", self)
        load_model_action.triggered.connect(self.load_inverted_models)
        load_model_action.setStatusTip("Cargar modelos de inversión guardados")
        toolbar.addAction(load_model_action)
        
        toolbar.addSeparator()
        
        # Acción para guardar tabla
        save_table_action = QAction(QIcon(str(image_path / "guardar_tabla.png")), "Guardar\nTabla", self)
        save_table_action.triggered.connect(self.save_inversion_table)
        save_table_action.setStatusTip("Guardar tabla de resultados de inversión")
        toolbar.addAction(save_table_action)
        
        # Acción para generar gráfico 2D
        generate_2d_action = QAction(QIcon(str(image_path / "generar_2d.png")), "Generar\n2D", self)
        generate_2d_action.triggered.connect(self.generate_2d_plot)
        generate_2d_action.setStatusTip("Generar gráfico 2D de resistividad")
        toolbar.addAction(generate_2d_action)
        
        # Acción para guardar figura 2D
        save_2d_action = QAction(QIcon(str(image_path / "guardar_2d.png")), "Guardar\n2D", self)
        save_2d_action.triggered.connect(self.save_2d_figure)
        save_2d_action.setStatusTip("Guardar figura 2D generada")
        toolbar.addAction(save_2d_action)
        
        toolbar.addSeparator()
        
        # Acción para clasificar agua
        water_action = QAction(QIcon(str(image_path / "agua.png")), "Clasificar\nAgua", self)
        water_action.triggered.connect(self.find_water)
        water_action.setStatusTip("Clasificar datos para identificar acuíferos")
        toolbar.addAction(water_action)

    def create_control_panel(self):
        """Crear el panel de controles mejorado"""
        control_widget = QWidget()
        control_widget.setMaximumWidth(350)
        control_widget.setMinimumWidth(300)
        
        # Layout principal del control widget (sin scroll area para evitar problemas)
        main_control_layout = QVBoxLayout(control_widget)
        
        # Título del panel
        title_label = QLabel("Panel de Control")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d4; margin: 10px;")
        main_control_layout.addWidget(title_label)
        
        # Pestañas de control mejoradas
        control_tabs = QTabWidget()
        
        # Pestaña Preprocesamiento mejorada
        preprocessing_tab = self.create_preprocessing_tab()
        control_tabs.addTab(preprocessing_tab, "📊 Preprocesamiento")
        
        # Pestaña Procesamiento mejorada
        processing_tab = self.create_processing_tab()
        control_tabs.addTab(processing_tab, "⚙️ Inversión")
        
        # Pestaña Gráfico 2D mejorada
        plot2d_tab = self.create_plot2d_tab()
        control_tabs.addTab(plot2d_tab, "📈 Gráfico 2D")
        
        main_control_layout.addWidget(control_tabs)
        
        return control_widget

    def create_preprocessing_tab(self):
        """Crear la pestaña de preprocesamiento mejorada"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Grupo de empalme
        empalme_group = QGroupBox("🔄 Promediado de Datos")
        empalme_layout = QVBoxLayout()
        
        info_label = QLabel("Combina mediciones con el mismo AB/2 pero diferente MN/2")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666666; font-size: 11px;")
        empalme_layout.addWidget(info_label)
        
        self.empalme_button = QPushButton("🔄 Promediar MN")
        self.empalme_button.clicked.connect(self.realizar_empalme)
        empalme_layout.addWidget(self.empalme_button)
        
        empalme_group.setLayout(empalme_layout)
        layout.addWidget(empalme_group)
        
        # Grupo de suavizado mejorado
        filter_group = QGroupBox("📈 Suavizado de Curvas")
        filter_layout = QVBoxLayout()
        
        filter_layout.addWidget(QLabel("Tipo de Filtro:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Media Móvil", "Savitzky-Golay", "Exponencial"])
        filter_layout.addWidget(self.filter_combo)
        
        filter_layout.addWidget(QLabel("Tamaño de Ventana:"))
        self.window_size_spin = QSpinBox()
        self.window_size_spin.setRange(1, 100)
        self.window_size_spin.setValue(5)
        filter_layout.addWidget(self.window_size_spin)
        
        self.apply_filter_button = QPushButton("📈 Aplicar Suavizado")
        self.apply_filter_button.clicked.connect(self.apply_filter)
        filter_layout.addWidget(self.apply_filter_button)
        
        self.save_filtered_button = QPushButton("💾 Guardar Curva Filtrada")
        self.save_filtered_button.clicked.connect(self.save_filtered_data)
        filter_layout.addWidget(self.save_filtered_button)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        layout.addStretch()
        return tab

    def create_processing_tab(self):
        """Crear la pestaña de procesamiento mejorada"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Selector de modelo mejorado
        model_group = QGroupBox("🔬 Modelo de Inversión")
        model_layout = QVBoxLayout()
        
        model_layout.addWidget(QLabel("Algoritmo:"))
        self.model_selector = QComboBox()
        self.model_selector.addItems(["Occam's razor", "Levenberg-Marquardt"])
        model_layout.addWidget(self.model_selector)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # Parámetros de inversión mejorados
        params_group = QGroupBox("⚙️ Parámetros de Inversión")
        params_layout = QVBoxLayout()
        
        params_layout.addWidget(QLabel("Número de Capas:"))
        self.layer_spin = QSpinBox()
        self.layer_spin.setRange(2, 50)
        self.layer_spin.setValue(5)
        params_layout.addWidget(self.layer_spin)
        
        params_layout.addWidget(QLabel("Parámetro Lambda:"))
        self.lambda_spin = QSpinBox()
        self.lambda_spin.setRange(1, 1000)
        self.lambda_spin.setValue(20)
        params_layout.addWidget(self.lambda_spin)
        
        params_layout.addWidget(QLabel("Factor Lambda:"))
        self.lambda_factor_spin = QDoubleSpinBox()
        self.lambda_factor_spin.setRange(0.1, 100.0)
        self.lambda_factor_spin.setSingleStep(0.1)
        self.lambda_factor_spin.setValue(0.8)
        params_layout.addWidget(self.lambda_factor_spin)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # Botones de acción
        action_group = QGroupBox("🚀 Acciones")
        action_layout = QVBoxLayout()
        
        self.invert_button = QPushButton("🔄 Invertir Modelo")
        self.invert_button.clicked.connect(self.invert_model)
        action_layout.addWidget(self.invert_button)
        
        self.water_button = QPushButton("💧 Clasificar Agua")
        self.water_button.clicked.connect(self.find_water)
        action_layout.addWidget(self.water_button)
        
        action_group.setLayout(action_layout)
        layout.addWidget(action_group)
        
        layout.addStretch()
        return tab

    def create_plot2d_tab(self):
        """Crear la pestaña de gráfico 2D mejorada"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Parámetros de interpolación
        interp_group = QGroupBox("🎨 Configuración de Visualización")
        interp_layout = QVBoxLayout()
        
        interp_layout.addWidget(QLabel("Método de Interpolación:"))
        self.interpolation_combo = QComboBox()
        self.interpolation_combo.addItems(["linear", "nearest", "cubic"])
        interp_layout.addWidget(self.interpolation_combo)
        
        interp_layout.addWidget(QLabel("Niveles de Contorno:"))
        self.contour_levels_spin = QSpinBox()
        self.contour_levels_spin.setRange(1, 100)
        self.contour_levels_spin.setValue(10)
        interp_layout.addWidget(self.contour_levels_spin)
        
        interp_layout.addWidget(QLabel("Mapa de Colores:"))
        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems(["jet", "rainbow", "viridis", "plasma", "inferno", "magma", "cividis"])
        interp_layout.addWidget(self.colormap_combo)
        
        interp_layout.addWidget(QLabel("Resolución:"))
        self.resolution_spin = QSpinBox()
        self.resolution_spin.setRange(10, 500)
        self.resolution_spin.setValue(100)
        interp_layout.addWidget(self.resolution_spin)
        
        interp_group.setLayout(interp_layout)
        layout.addWidget(interp_group)
        
        # Configuración de títulos
        title_group = QGroupBox("📝 Personalización")
        title_layout = QVBoxLayout()
        
        title_layout.addWidget(QLabel("Título del Gráfico:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Ingrese el título de la gráfica")
        title_layout.addWidget(self.title_input)
        
        title_group.setLayout(title_layout)
        layout.addWidget(title_group)
        
        # Botones de acción para 2D
        action2d_group = QGroupBox("🎯 Generar Gráfico")
        action2d_layout = QVBoxLayout()
        
        self.generate_2d_button = QPushButton("📊 Generar Gráfico 2D")
        self.generate_2d_button.clicked.connect(self.generate_2d_plot)
        action2d_layout.addWidget(self.generate_2d_button)
        
        self.save_2d_button = QPushButton("💾 Guardar Figura 2D")
        self.save_2d_button.clicked.connect(self.save_2d_figure)
        action2d_layout.addWidget(self.save_2d_button)
        
        action2d_group.setLayout(action2d_layout)
        layout.addWidget(action2d_group)
        
        layout.addStretch()
        return tab

    def create_visualization_panel(self):
        """Crear el panel de visualización mejorado"""
        visualization_widget = QWidget()
        layout = QVBoxLayout(visualization_widget)
        
        # Título del panel
        title_label = QLabel("Visualización de Datos")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d4; margin: 5px;")
        layout.addWidget(title_label)
        
        # Pestañas de gráficos mejoradas
        self.tabs = QTabWidget()
        
        # Tab 1: Gráfica principal
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.tabs.addTab(self.canvas, "📈 Curva y Empalme")
        
        # Tab 2: Análisis estadístico
        self.analysis_figure = Figure(figsize=(12, 8))
        self.analysis_canvas = FigureCanvas(self.analysis_figure)
        self.tabs.addTab(self.analysis_canvas, "📊 Análisis Estadístico")
        
        # Tab 3: Resultados de inversión
        self.inversion_figure = Figure(figsize=(10, 6))
        self.inversion_canvas = FigureCanvas(self.inversion_figure)
        self.tabs.addTab(self.inversion_canvas, "⚙️ Inversión")
        
        layout.addWidget(self.tabs)
        
        # Terminal mejorado
        terminal_label = QLabel("Terminal de Salida")
        terminal_label.setStyleSheet("font-weight: bold; color: #0078d4; margin-top: 10px;")
        layout.addWidget(terminal_label)
        
        self.eda_output = QTextEdit()
        self.eda_output.setReadOnly(True)
        self.eda_output.setFixedHeight(150)
        self.eda_output.setPlaceholderText("Los resultados y mensajes aparecerán aquí...")
        layout.addWidget(self.eda_output)
        
        return visualization_widget

    def create_table_panel(self):
        """Crear el panel de tablas mejorado"""
        table_widget = QWidget()
        table_widget.setMaximumWidth(400)
        table_widget.setMinimumWidth(300)
        
        layout = QVBoxLayout(table_widget)
        
        # Título del panel
        title_label = QLabel("Datos y Resultados")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d4; margin: 5px;")
        layout.addWidget(title_label)
        
        # Pestañas de tablas mejoradas
        self.table_tabs = QTabWidget()
        
        # Tabla de datos cargados
        self.data_table = QTableWidget()
        self.data_table.setAlternatingRowColors(True)
        self.table_tabs.addTab(self.data_table, "📋 Datos")
        
        # Tabla de modelo de inversión
        self.model_table = QTableWidget()
        self.model_table.setAlternatingRowColors(True)
        self.table_tabs.addTab(self.model_table, "🔬 Modelo")
        
        layout.addWidget(self.table_tabs)
        
        return table_widget