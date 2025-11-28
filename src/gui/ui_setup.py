"""
Configuración de la interfaz gráfica de VESPY
==============================================

Crea y configura todos los widgets de la UI.

Autor: VESPY Team
Fecha: 2025
"""

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QToolBar, QAction, QTabWidget, 
    QWidget, QLabel, QGroupBox, QComboBox, QSpinBox, QDoubleSpinBox,
    QPushButton, QTextEdit, QTableWidget, QSplitter
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def create_toolbar(parent):
    """
    Crear barra de herramientas con acciones principales.
    
    Args:
        parent: Widget padre (VESPYApp)
    
    Returns:
        QToolBar: Barra de herramientas configurada
    """
    toolbar = QToolBar("Herramientas")
    toolbar.setStyleSheet("background-color: #f0f0f0;")
    
    # Acción para cargar datos
    load_action = QAction("📂 Cargar Datos", parent)
    load_action.triggered.connect(parent.load_data)
    toolbar.addAction(load_action)

    # Acción para guardar la curva suavizada
    save_action = QAction("💾 Guardar Curva", parent)
    save_action.triggered.connect(parent.save_curve)
    toolbar.addAction(save_action)
    
    # Acción para cargar modelos invertidos
    load_model_action = QAction("📥 Cargar Modelos", parent)
    load_model_action.triggered.connect(parent.load_inverted_models)
    toolbar.addAction(load_model_action)

    # Acción para guardar la tabla del resultado de la inversión
    save_table_action = QAction("📊 Guardar Tabla", parent)
    save_table_action.triggered.connect(parent.save_inversion_table)
    toolbar.addAction(save_table_action)
    
    return toolbar


def create_preprocessing_tab(parent):
    """
    Crear pestaña de preprocesamiento.
    
    Args:
        parent: Widget padre (VESPYApp)
    
    Returns:
        QWidget: Pestaña de preprocesamiento
    """
    preprocessing_tab = QWidget()
    preprocessing_layout = QVBoxLayout(preprocessing_tab)
    preprocessing_layout.addWidget(QLabel("<b>Preprocesamiento</b>"))
    
    parent.empalme_button = QPushButton("🔗 Realizar Empalme")
    parent.empalme_button.clicked.connect(parent.realizar_empalme)
    preprocessing_layout.addWidget(parent.empalme_button)
    
    # Opciones de suavizado
    filter_group = QGroupBox("Suavizado")
    filter_layout = QVBoxLayout()
    
    parent.filter_combo = QComboBox()
    parent.filter_combo.addItems(["Media Móvil", "Savitzky-Golay", "Exponencial"])
    
    parent.window_size_spin = QSpinBox()
    parent.window_size_spin.setRange(1, 100)
    parent.window_size_spin.setValue(5)
    
    parent.apply_filter_button = QPushButton("✨ Aplicar Suavizado")
    parent.apply_filter_button.clicked.connect(parent.apply_filter)
    
    filter_layout.addWidget(QLabel("Tipo de Filtro"))
    filter_layout.addWidget(parent.filter_combo)
    filter_layout.addWidget(QLabel("Tamaño de Ventana"))
    filter_layout.addWidget(parent.window_size_spin)
    filter_layout.addWidget(parent.apply_filter_button)
    filter_group.setLayout(filter_layout)
    preprocessing_layout.addWidget(filter_group)
    preprocessing_layout.addStretch()
    
    return preprocessing_tab


def create_processing_tab(parent, pygimli_available):
    """
    Crear pestaña de procesamiento e inversión.
    
    Args:
        parent: Widget padre (VESPYApp)
        pygimli_available: Si PyGIMLi está disponible
    
    Returns:
        QWidget: Pestaña de procesamiento
    """
    processing_tab = QWidget()
    processing_layout = QVBoxLayout(processing_tab)

    # Selector de Modelo
    parent.model_selector = QComboBox()
    if pygimli_available:
        parent.model_selector.addItems(["PyGIMLi (Occam's razor)"])
    else:
        parent.model_selector.addItems(["Método Simple (sin PyGIMLi)"])
    processing_layout.addWidget(QLabel("Modelo de Inversión:"))
    processing_layout.addWidget(parent.model_selector)
    
    # Parámetros de Inversión
    params_group = QGroupBox("Parámetros de Inversión")
    params_layout = QVBoxLayout()
    
    # Número de capas
    parent.layer_label = QLabel("Número de Capas")
    parent.layer_spin = QSpinBox()
    parent.layer_spin.setRange(2, 10)
    parent.layer_spin.setValue(5)
    params_layout.addWidget(parent.layer_label)
    params_layout.addWidget(parent.layer_spin)
    
    parent.lambda_spin = QSpinBox()
    parent.lambda_spin.setRange(1, 1000)
    parent.lambda_spin.setValue(20)

    parent.lambda_factor_spin = QDoubleSpinBox()
    parent.lambda_factor_spin.setRange(0.1, 10.0)
    parent.lambda_factor_spin.setSingleStep(0.1)
    parent.lambda_factor_spin.setValue(0.8)

    params_layout.addWidget(QLabel("Lambda (λ)"))
    params_layout.addWidget(parent.lambda_spin)
    params_layout.addWidget(QLabel("Factor Lambda"))
    params_layout.addWidget(parent.lambda_factor_spin)
    
    params_group.setLayout(params_layout)
    processing_layout.addWidget(params_group)
    
    # Suavizado del modelo (opcional)
    smooth_group = QGroupBox("Suavizado del Modelo Invertido")
    smooth_layout = QVBoxLayout()
    
    parent.smooth_combo = QComboBox()
    parent.smooth_combo.addItems(["Orden 1 (Suave)", "Orden 2 (Muy Suave)"])
    
    parent.smooth_model_button = QPushButton("🌊 Suavizar Modelo")
    parent.smooth_model_button.clicked.connect(parent.smooth_current_model)
    parent.smooth_model_button.setEnabled(False)
    
    smooth_layout.addWidget(QLabel("Orden de Suavizado"))
    smooth_layout.addWidget(parent.smooth_combo)
    smooth_layout.addWidget(parent.smooth_model_button)
    smooth_group.setLayout(smooth_layout)
    processing_layout.addWidget(smooth_group)
    
    # Botones de inversión y guardado
    parent.invert_button = QPushButton("⚡ Invertir Modelo")
    parent.invert_button.clicked.connect(parent.invert_model)
    processing_layout.addWidget(parent.invert_button)
    
    parent.save_model_button = QPushButton("💾 Guardar Modelo")
    parent.save_model_button.clicked.connect(parent.save_model)
    processing_layout.addWidget(parent.save_model_button)
    
    processing_layout.addStretch()
    
    return processing_tab


def create_2d_controls(parent):
    """
    Crear controles para gráfico 2D.
    
    Args:
        parent: Widget padre (VESPYApp)
    
    Returns:
        QGroupBox: Grupo de controles 2D
    """
    plot2d_controls = QGroupBox("Controles de Gráfico 2D")
    plot2d_layout = QVBoxLayout()
    
    parent.interpolation_combo = QComboBox()
    parent.interpolation_combo.addItems(["linear", "nearest", "cubic"])
    
    parent.contour_levels_spin = QSpinBox()
    parent.contour_levels_spin.setRange(1, 100)
    parent.contour_levels_spin.setValue(10)
    
    parent.colormap_combo = QComboBox()
    parent.colormap_combo.addItems(["jet", "rainbow", "viridis", "plasma", "inferno", "magma", "cividis"])

    plot2d_layout.addWidget(QLabel("Método de Interpolación"))
    plot2d_layout.addWidget(parent.interpolation_combo)
    plot2d_layout.addWidget(QLabel("Niveles de Contorno"))
    plot2d_layout.addWidget(parent.contour_levels_spin)
    plot2d_layout.addWidget(QLabel("Mapa de Colores"))
    plot2d_layout.addWidget(parent.colormap_combo)
    plot2d_controls.setLayout(plot2d_layout)
    
    return plot2d_controls


def setup_ui(parent, pygimli_available):
    """
    Configurar toda la interfaz gráfica.
    
    Args:
        parent: Widget padre (VESPYApp)
        pygimli_available: Si PyGIMLi está disponible
    """
    # Layout principal
    main_layout = QVBoxLayout()
    
    # Barra de herramientas
    toolbar = create_toolbar(parent)
    parent.addToolBar(toolbar)
    
    # Splitter principal (horizontal)
    splitter = QSplitter(Qt.Horizontal)
    
    # Panel izquierdo: Gráficos
    left_widget = QWidget()
    left_layout = QVBoxLayout(left_widget)
    
    # Pestañas de gráficos
    parent.tabs = QTabWidget()
    
    # Pestaña de datos originales
    data_tab = QWidget()
    data_layout = QVBoxLayout(data_tab)
    parent.figure = Figure(figsize=(8, 6))
    parent.canvas = FigureCanvas(parent.figure)
    data_layout.addWidget(parent.canvas)
    parent.tabs.addTab(data_tab, "📊 Datos")
    
    # Pestaña de análisis estadístico
    analysis_tab = QWidget()
    analysis_layout = QVBoxLayout(analysis_tab)
    parent.analysis_figure = Figure(figsize=(12, 8))
    parent.analysis_canvas = FigureCanvas(parent.analysis_figure)
    analysis_layout.addWidget(parent.analysis_canvas)
    
    parent.analyze_button = QPushButton("📈 Analizar Datos")
    parent.analyze_button.clicked.connect(parent.analyze_data)
    analysis_layout.addWidget(parent.analyze_button)
    parent.tabs.addTab(analysis_tab, "📈 Análisis")
    
    # Pestaña de inversión
    inversion_tab = QWidget()
    inversion_layout = QVBoxLayout(inversion_tab)
    parent.inversion_figure = Figure(figsize=(12, 6))
    parent.inversion_canvas = FigureCanvas(parent.inversion_figure)
    inversion_layout.addWidget(parent.inversion_canvas)
    parent.tabs.addTab(inversion_tab, "⚡ Inversión")
    
    # Pestaña de gráfico 2D
    plot2d_tab = QWidget()
    plot2d_layout = QVBoxLayout(plot2d_tab)
    parent.plot2d_figure = Figure(figsize=(12, 8))
    parent.plot2d_canvas = FigureCanvas(parent.plot2d_figure)
    plot2d_layout.addWidget(parent.plot2d_canvas)
    parent.tabs.addTab(plot2d_tab, "🗺️ Gráfico 2D")
    
    left_layout.addWidget(parent.tabs)
    
    # Panel derecho: Controles y tabla
    right_widget = QWidget()
    right_layout = QVBoxLayout(right_widget)
    
    # Panel de control con pestañas
    control_tabs = QTabWidget()
    control_tabs.setStyleSheet("background-color: #e8e8e8;")
    
    # Crear pestañas
    preprocessing_tab = create_preprocessing_tab(parent)
    processing_tab = create_processing_tab(parent, pygimli_available)
    
    control_tabs.addTab(preprocessing_tab, "Preprocesamiento")
    control_tabs.addTab(processing_tab, "Procesamiento")
    
    right_layout.addWidget(control_tabs)
    
    # Controles 2D
    plot2d_controls = create_2d_controls(parent)
    right_layout.addWidget(plot2d_controls)
    
    # Botón para generar el gráfico 2D
    parent.generate_2d_button = QPushButton("🗺️ Generar Gráfico 2D")
    parent.generate_2d_button.clicked.connect(parent.generate_2d_plot)
    right_layout.addWidget(parent.generate_2d_button)
    
    # Pestañas de tablas
    parent.table_tabs = QTabWidget()
    
    # Tabla de datos
    parent.data_table = QTableWidget()
    parent.table_tabs.addTab(parent.data_table, "Datos")
    
    # Tabla de modelo discreto
    parent.model_table = QTableWidget()
    parent.table_tabs.addTab(parent.model_table, "Modelo Discreto")
    
    # Tabla de modelo suavizado
    parent.smooth_model_table = QTableWidget()
    parent.table_tabs.addTab(parent.smooth_model_table, "Modelo Suavizado")
    
    right_layout.addWidget(parent.table_tabs)
    
    # Terminal de salida
    parent.eda_output = QTextEdit()
    parent.eda_output.setReadOnly(True)
    parent.eda_output.setMaximumHeight(200)
    parent.eda_output.setStyleSheet("background-color: #2b2b2b; color: #00ff00; font-family: 'Courier New';")
    right_layout.addWidget(QLabel("📟 Terminal de Salida"))
    right_layout.addWidget(parent.eda_output)
    
    # Configurar splitter
    splitter.addWidget(left_widget)
    splitter.addWidget(right_widget)
    splitter.setSizes([700, 300])
    
    main_layout.addWidget(splitter)
    
    # Widget central
    central_widget = QWidget()
    central_widget.setLayout(main_layout)
    parent.setCentralWidget(central_widget)
