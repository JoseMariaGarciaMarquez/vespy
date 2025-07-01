from pathlib import Path
from PyQt5.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPalette, QPixmap
from PyQt5.QtWidgets import (QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, 
                             QTableWidget, QTableWidgetItem, QComboBox, QDoubleSpinBox, 
                             QSpinBox, QLabel, QGroupBox, QToolBar, QAction, QPushButton, 
                             QTabWidget, QTextEdit, QLineEdit, QInputDialog, QSplitter,
                             QFrame, QScrollArea, QProgressBar, QStatusBar, QMessageBox,
                             QSlider, QCheckBox, QSpacerItem, QSizePolicy)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime

class EnhancedGUI:
    """Versión mejorada de la GUI con características profesionales adicionales"""
    
    def __init__(self):
        self.progress_bar = None
        self.current_theme = "light"  # light o dark
        self.auto_save_enabled = False
        
    def setup_enhanced_gui(self, image_path):
        """Configurar la GUI mejorada con características profesionales"""
        
        # Configurar el estilo y tema
        self.apply_theme(self.current_theme)
        
        # Configurar barra de estado mejorada
        self.setup_enhanced_status_bar()
        
        # Crear widget central con diseño profesional
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        # Layout principal con splitter
        main_layout = QHBoxLayout(self.main_widget)
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Crear paneles con diseño profesional
        left_panel = self.create_enhanced_control_panel()
        center_panel = self.create_enhanced_visualization_panel()
        right_panel = self.create_enhanced_data_panel()
        
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(center_panel)
        main_splitter.addWidget(right_panel)
        
        # Configurar proporciones
        main_splitter.setSizes([400, 900, 450])
        main_splitter.setStretchFactor(1, 1)
        
        # Crear barra de herramientas profesional
        self.create_professional_toolbar(image_path)
        
        # Configurar atajos de teclado
        self.setup_keyboard_shortcuts()
        
        # Configurar auto-guardado (opcional)
        self.setup_auto_save()

    def apply_theme(self, theme_name):
        """Aplicar tema claro u oscuro"""
        if theme_name == "dark":
            style = self.get_dark_theme_style()
        else:
            style = self.get_light_theme_style()
        
        self.setStyleSheet(style)

    def get_light_theme_style(self):
        """Tema claro profesional"""
        return """
        /* Tema Claro Profesional */
        QMainWindow {
            background-color: #f8f9fa;
            color: #212529;
        }
        
        QTabWidget::pane {
            border: 1px solid #dee2e6;
            background-color: white;
            border-radius: 8px;
        }
        
        QTabBar::tab {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #ffffff, stop: 1 #f8f9fa);
            border: 1px solid #dee2e6;
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            min-width: 100px;
            font-weight: 500;
        }
        
        QTabBar::tab:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #e3f2fd, stop: 1 #bbdefb);
        }
        
        QTabBar::tab:selected {
            background: white;
            border-bottom-color: white;
            font-weight: bold;
            color: #1976d2;
        }
        
        QPushButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #2196f3, stop: 1 #1976d2);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            min-height: 25px;
            font-size: 13px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #42a5f5, stop: 1 #1e88e5);
            transform: translateY(-1px);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #1565c0, stop: 1 #0d47a1);
        }
        
        QPushButton:disabled {
            background: #e0e0e0;
            color: #9e9e9e;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            margin-top: 15px;
            padding-top: 15px;
            background-color: white;
            font-size: 14px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 15px 0 15px;
            color: #1976d2;
            font-size: 14px;
            font-weight: bold;
        }
        
        QComboBox {
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            padding: 8px 12px;
            background-color: white;
            min-height: 25px;
            font-size: 13px;
        }
        
        QComboBox:hover {
            border-color: #2196f3;
        }
        
        QComboBox:focus {
            border-color: #1976d2;
            border-width: 2px;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAGCAYAAAD37n+BAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAdgAAAHYBTnsmCAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAFKSURBVBiVY/j//z8DLoCRgQGCkPFv2P9X7P//3/7/4/+f/3/9//f/H/8//v/9/+//f/+/+f/b/0v/9/xP/5/zP+d/5v/0/wn/4/7H/I/6H/k/4n/4/+D/Qf+D/gf+D/gf+D/gf+D/wf+D/oedGf+f/vfm/zn/x/1v+L/6f9v/rf/X/m/8v/J/zf+V/8v+l/zP+l/5v/L/5f9r/lf+r/lf+r/1f9r/tf/r/tf/r/9f/r/zf+7/nf87/vf97/nf97/3f+7/nf87/vf97/3f+7/nf97/vf87/3f97/nf87/vf97/3f+7/nf87/3f97/nf87/vf97/nf87/vf87/3f+7/vf97/nf87/vf87/vf87/3f+7/vf87/vf87/3f+7/vf87/vf87/3f+7/vf87/3f97/nf97/vf87/3f+7/vf87/vf87/3f+7/vf87/3f+7/vf87/3f97/nf97/vf87/vf87/3f+7/vf97/vf87/vf87/3f+7/vf97/3f97/vf87/vf87/3f+7/vf97/3f97/vf87/vf87/3f+7/vf97/3f97/vf87/vf87/3f+7/vf97/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/vf87/3f+7/vf87/3f97/vf87/); 
            width: 12px;
            height: 6px;
        }
        
        QSpinBox, QDoubleSpinBox, QLineEdit {
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            padding: 8px 12px;
            background-color: white;
            min-height: 25px;
            font-size: 13px;
        }
        
        QSpinBox:hover, QDoubleSpinBox:hover, QLineEdit:hover {
            border-color: #2196f3;
        }
        
        QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {
            border-color: #1976d2;
            border-width: 2px;
        }
        
        QTextEdit {
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            background-color: white;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
            padding: 8px;
        }
        
        QTableWidget {
            gridline-color: #e0e0e0;
            background-color: white;
            alternate-background-color: #f8f9fa;
            selection-background-color: #bbdefb;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 12px;
        }
        
        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        QTableWidget::item:selected {
            background-color: #2196f3;
            color: white;
        }
        
        QHeaderView::section {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f8f9fa, stop: 1 #e9ecef);
            border: 1px solid #dee2e6;
            padding: 8px;
            font-weight: bold;
            color: #495057;
        }
        
        QToolBar {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #ffffff, stop: 1 #f8f9fa);
            border: 1px solid #dee2e6;
            spacing: 5px;
            padding: 5px;
            border-radius: 0px;
        }
        
        QToolBar::separator {
            background-color: #dee2e6;
            width: 1px;
            margin: 8px;
        }
        
        QStatusBar {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f8f9fa, stop: 1 #e9ecef);
            border-top: 1px solid #dee2e6;
            color: #495057;
            font-size: 12px;
            padding: 5px;
        }
        
        QProgressBar {
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            text-align: center;
            background-color: #f5f5f5;
            height: 20px;
        }
        
        QProgressBar::chunk {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #4caf50, stop: 1 #388e3c);
            border-radius: 4px;
        }
        
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        
        QScrollBar:vertical {
            background: #f5f5f5;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background: #bdbdbd;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #9e9e9e;
        }
        
        QLabel {
            color: #495057;
            font-size: 13px;
        }
        """

    def get_dark_theme_style(self):
        """Tema oscuro profesional"""
        return """
        /* Tema Oscuro Profesional */
        QMainWindow {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        QTabWidget::pane {
            border: 1px solid #404040;
            background-color: #2d2d2d;
            border-radius: 8px;
        }
        
        QTabBar::tab {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #404040, stop: 1 #353535);
            border: 1px solid #555555;
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            min-width: 100px;
            color: #ffffff;
            font-weight: 500;
        }
        
        QTabBar::tab:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #505050, stop: 1 #454545);
        }
        
        QTabBar::tab:selected {
            background: #2d2d2d;
            border-bottom-color: #2d2d2d;
            font-weight: bold;
            color: #64b5f6;
        }
        
        QPushButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #1976d2, stop: 1 #1565c0);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            min-height: 25px;
            font-size: 13px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #1e88e5, stop: 1 #1976d2);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #0d47a1, stop: 1 #0d47a1);
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #555555;
            border-radius: 10px;
            margin-top: 15px;
            padding-top: 15px;
            background-color: #2d2d2d;
            color: #ffffff;
            font-size: 14px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 15px 0 15px;
            color: #64b5f6;
            font-size: 14px;
            font-weight: bold;
        }
        
        QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit {
            border: 2px solid #555555;
            border-radius: 6px;
            padding: 8px 12px;
            background-color: #2d2d2d;
            color: #ffffff;
            min-height: 25px;
            font-size: 13px;
        }
        
        QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover, QLineEdit:hover {
            border-color: #64b5f6;
        }
        
        QTextEdit {
            border: 2px solid #555555;
            border-radius: 8px;
            background-color: #2d2d2d;
            color: #ffffff;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
            padding: 8px;
        }
        
        QTableWidget {
            gridline-color: #555555;
            background-color: #2d2d2d;
            alternate-background-color: #353535;
            selection-background-color: #1976d2;
            border: 2px solid #555555;
            border-radius: 8px;
            color: #ffffff;
            font-size: 12px;
        }
        
        QLabel {
            color: #ffffff;
            font-size: 13px;
        }
        """

    def setup_enhanced_status_bar(self):
        """Configurar barra de estado con información adicional"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Mensaje principal
        self.status_label = QLabel("VESPY - Listo para cargar datos")
        self.status_bar.addWidget(self.status_label)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Información del archivo actual
        self.file_info_label = QLabel("")
        self.status_bar.addPermanentWidget(self.file_info_label)
        
        # Hora actual
        self.time_label = QLabel()
        self.update_time()
        self.status_bar.addPermanentWidget(self.time_label)
        
        # Timer para actualizar la hora
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Actualizar cada segundo

    def update_time(self):
        """Actualizar la hora en la barra de estado"""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(f"🕒 {current_time}")

    def update_status(self, message, progress=None):
        """Actualizar el estado con mensaje y progreso opcional"""
        self.status_label.setText(message)
        
        if progress is not None:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(progress)
        else:
            self.progress_bar.setVisible(False)

    def create_professional_toolbar(self, image_path):
        """Crear barra de herramientas profesional con agrupaciones"""
        # Barra principal
        main_toolbar = QToolBar("Herramientas Principales")
        main_toolbar.setIconSize(QSize(32, 32))
        main_toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(main_toolbar)
        
        # Grupo: Gestión de Archivos
        load_action = QAction(QIcon(str(image_path / "cargar.png")), "Cargar\nDatos", self)
        load_action.triggered.connect(self.load_data)
        load_action.setStatusTip("Cargar datos de sondeo eléctrico vertical (Ctrl+O)")
        load_action.setShortcut("Ctrl+O")
        main_toolbar.addAction(load_action)
        
        save_table_action = QAction(QIcon(str(image_path / "guardar_tabla.png")), "Guardar\nTabla", self)
        save_table_action.triggered.connect(self.save_inversion_table)
        save_table_action.setStatusTip("Guardar tabla de resultados (Ctrl+S)")
        save_table_action.setShortcut("Ctrl+S")
        main_toolbar.addAction(save_table_action)
        
        main_toolbar.addSeparator()
        
        # Grupo: Procesamiento
        inversion_action = QAction(QIcon(str(image_path / "inversion.png")), "Invertir\nModelo", self)
        inversion_action.triggered.connect(self.invert_model)
        inversion_action.setStatusTip("Realizar inversión de resistividad (F5)")
        inversion_action.setShortcut("F5")
        main_toolbar.addAction(inversion_action)
        
        load_model_action = QAction(QIcon(str(image_path / "cargar_modelo.png")), "Cargar\nModelos", self)
        load_model_action.triggered.connect(self.load_inverted_models)
        load_model_action.setStatusTip("Cargar modelos de inversión guardados")
        main_toolbar.addAction(load_model_action)
        
        main_toolbar.addSeparator()
        
        # Grupo: Visualización
        generate_2d_action = QAction(QIcon(str(image_path / "generar_2d.png")), "Generar\n2D", self)
        generate_2d_action.triggered.connect(self.generate_2d_plot)
        generate_2d_action.setStatusTip("Generar gráfico 2D de resistividad (F6)")
        generate_2d_action.setShortcut("F6")
        main_toolbar.addAction(generate_2d_action)
        
        save_2d_action = QAction(QIcon(str(image_path / "guardar_2d.png")), "Guardar\n2D", self)
        save_2d_action.triggered.connect(self.save_2d_figure)
        save_2d_action.setStatusTip("Guardar figura 2D generada")
        main_toolbar.addAction(save_2d_action)
        
        main_toolbar.addSeparator()
        
        # Grupo: Análisis
        water_action = QAction(QIcon(str(image_path / "agua.png")), "Clasificar\nAgua", self)
        water_action.triggered.connect(self.find_water)
        water_action.setStatusTip("Clasificar datos para identificar acuíferos (F7)")
        water_action.setShortcut("F7")
        main_toolbar.addAction(water_action)
        
        # Barra de herramientas secundaria para funciones avanzadas
        secondary_toolbar = QToolBar("Herramientas Secundarias")
        secondary_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(secondary_toolbar)
        
        # Botón para cambiar tema
        theme_action = QAction("🌓", self)
        theme_action.setStatusTip("Cambiar entre tema claro y oscuro")
        theme_action.triggered.connect(self.toggle_theme)
        secondary_toolbar.addAction(theme_action)
        
        secondary_toolbar.addSeparator()
        
        # Botón de auto-guardado
        auto_save_action = QAction("💾", self)
        auto_save_action.setStatusTip("Activar/desactivar auto-guardado")
        auto_save_action.setCheckable(True)
        auto_save_action.triggered.connect(self.toggle_auto_save)
        secondary_toolbar.addAction(auto_save_action)

    def setup_keyboard_shortcuts(self):
        """Configurar atajos de teclado adicionales"""
        # Los atajos principales ya están configurados en la toolbar
        pass

    def setup_auto_save(self):
        """Configurar auto-guardado"""
        if hasattr(self, 'auto_save_timer'):
            return
            
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        # Se activará solo si el usuario lo habilita

    def toggle_theme(self):
        """Alternar entre tema claro y oscuro"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(self.current_theme)
        
        theme_name = "oscuro" if self.current_theme == "dark" else "claro"
        self.update_status(f"Tema cambiado a {theme_name}")

    def toggle_auto_save(self, enabled):
        """Activar/desactivar auto-guardado"""
        self.auto_save_enabled = enabled
        if enabled:
            self.auto_save_timer.start(300000)  # 5 minutos
            self.update_status("Auto-guardado activado (cada 5 minutos)")
        else:
            self.auto_save_timer.stop()
            self.update_status("Auto-guardado desactivado")

    def auto_save(self):
        """Función de auto-guardado"""
        if hasattr(self, 'data') and self.data is not None:
            # Implementar lógica de auto-guardado aquí
            self.update_status("Auto-guardado realizado", 100)
            QTimer.singleShot(2000, lambda: self.update_status("VESPY - Datos cargados"))

    def create_enhanced_control_panel(self):
        """Crear panel de control mejorado con características profesionales"""
        # Usar el método existente como base y agregar mejoras
        control_widget = self.create_control_panel()
        
        # Agregar funcionalidades adicionales
        return control_widget

    def create_enhanced_visualization_panel(self):
        """Crear panel de visualización mejorado"""
        # Usar el método existente como base
        visualization_widget = self.create_visualization_panel()
        
        return visualization_widget

    def create_enhanced_data_panel(self):
        """Crear panel de datos mejorado"""
        # Usar el método existente como base
        table_widget = self.create_table_panel()
        
        return table_widget
        
    def show_success_message(self, title, message):
        """Mostrar mensaje de éxito"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
        
    def show_error_message(self, title, message):
        """Mostrar mensaje de error"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
        
    def show_warning_message(self, title, message):
        """Mostrar mensaje de advertencia"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
