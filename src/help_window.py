from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QScrollArea, QWidget, QFrame, QGridLayout, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon

class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🛟 Ayuda de VESPY")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)
        
        # Aplicar estilos modernos
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f8f9fa, stop: 1 #e9ecef);
                border-radius: 12px;
            }
            QLabel {
                color: #2c3e50;
                background: transparent;
            }
            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding: 20px;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #667eea, stop: 1 #764ba2);
                color: white;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            QLabel#subtitle {
                font-size: 16px;
                color: #6c757d;
                font-style: italic;
                text-align: center;
                margin-bottom: 20px;
            }
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #667eea, stop: 1 #764ba2);
                color: white;
                border: none;
                padding: 15px 25px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                margin: 5px;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5a67d8, stop: 1 #6b46c1);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #4c51bf, stop: 1 #553c9a);
            }
            QPushButton#close_button {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f56565, stop: 1 #e53e3e);
            }
            QPushButton#close_button:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e53e3e, stop: 1 #c53030);
            }
            QFrame {
                background: white;
                border-radius: 12px;
                border: 1px solid #dee2e6;
                padding: 20px;
                margin: 10px;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título principal
        title = QLabel("🛟 Centro de Ayuda VESPY")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Selecciona el tema sobre el que necesitas ayuda")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)
        
        # Frame contenedor para los botones
        content_frame = QFrame()
        content_layout = QGridLayout(content_frame)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Botones de ayuda con iconos y descripciones
        help_buttons = [
            ("🔄 Inversión", "Aprende sobre métodos de inversión y regularización", self.show_inversion_help),
            ("⚙️ Preprocesamiento", "Técnicas de empalme y suavizado de datos", self.show_preprocessing_help),
            ("📊 Análisis de Datos", "Herramientas de análisis estadístico", self.show_analysis_help),
            ("📈 Gráficos", "Generación y personalización de visualizaciones", self.show_plotting_help),
            ("❓ Guía de Uso", "Instrucciones paso a paso del software", self.show_usage_help)
        ]
        
        for i, (title_text, description, callback) in enumerate(help_buttons):
            row = i // 2
            col = i % 2
            
            button_container = QFrame()
            button_layout = QVBoxLayout(button_container)
            button_layout.setContentsMargins(10, 10, 10, 10)
            
            button = QPushButton(title_text)
            button.clicked.connect(callback)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #6c757d; font-size: 12px; margin-top: 5px;")
            desc_label.setAlignment(Qt.AlignCenter)
            
            button_layout.addWidget(button)
            button_layout.addWidget(desc_label)
            
            content_layout.addWidget(button_container, row, col)
        
        main_layout.addWidget(content_frame)
        main_layout.addStretch()
        
        # Botón de cerrar
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_button = QPushButton("✕ Cerrar")
        close_button.setObjectName("close_button")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
    
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

class HelpInversionWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔄 Ayuda - Inversión")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(700, 500)
        
        # Aplicar estilos modernos
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f8f9fa, stop: 1 #e9ecef);
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QWidget#scroll_content {
                background: white;
                border-radius: 12px;
                border: 1px solid #dee2e6;
            }
            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: white;
                padding: 20px;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #667eea, stop: 1 #764ba2);
                border-radius: 8px;
                margin-bottom: 20px;
            }
            QLabel#content {
                color: #2c3e50;
                font-size: 14px;
                line-height: 1.6;
                padding: 20px;
                background: transparent;
            }
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f56565, stop: 1 #e53e3e);
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                margin: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e53e3e, stop: 1 #c53030);
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)
        
        # Título
        title = QLabel("🔄 Inversión de Datos")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Crear área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Contenido scrollable
        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_content")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        # Texto explicativo
        inversion_text = QLabel("""
        <div style="padding: 20px; line-height: 1.8;">
            <h2 style="color: #667eea; margin-bottom: 15px;">🎯 ¿Qué es la Inversión?</h2>
            <p style="margin-bottom: 15px;">
                La <strong>inversión en VESPY</strong> se refiere al proceso de ajustar un modelo de subsuelo 
                a los datos de resistividad medidos. Este proceso permite estimar la distribución 
                de resistividades en función de la profundidad.
            </p>
            
            <h3 style="color: #764ba2; margin: 20px 0 10px 0;">⚖️ Inversión con la Navaja de Occam</h3>
            <p style="margin-bottom: 15px;">
                Este método busca el <strong>modelo más simple</strong> que explique los datos observados, 
                evitando sobreajustes. La simplicidad del modelo se controla mediante la regularización, 
                que penaliza la complejidad del modelo.
            </p>
            
            <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #28a745; margin: 0 0 10px 0;">✅ Ventajas:</h4>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>Produce modelos más estables y menos sensibles al ruido</li>
                    <li>Evita la sobreinterpretación de los datos</li>
                    <li>Proporciona resultados más confiables</li>
                </ul>
            </div>
            
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #856404; margin: 0 0 10px 0;">⚠️ Desventajas:</h4>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>Puede subestimar la complejidad real del subsuelo</li>
                    <li>Regularización excesiva puede omitir detalles importantes</li>
                </ul>
            </div>
            
            <h3 style="color: #764ba2; margin: 20px 0 10px 0;">🔧 Parámetros de Control</h3>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #495057; margin: 0 0 10px 0;">λ (Lambda)</h4>
                <p style="margin: 0;">
                    El parámetro <strong>lambda</strong> controla la regularización del modelo de inversión. 
                    Un valor más alto de lambda suaviza el modelo, mientras que un valor más bajo permite 
                    más variabilidad en el modelo.
                </p>
            </div>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #495057; margin: 0 0 10px 0;">Factor Lambda</h4>
                <p style="margin: 0;">
                    El <strong>factor lambda</strong> es un multiplicador que ajusta el valor de lambda 
                    durante el proceso de inversión. Esto permite un control más fino sobre la regularización 
                    del modelo.
                </p>
            </div>
            
            <h3 style="color: #764ba2; margin: 20px 0 10px 0;">📏 Gestión de Capas</h3>
            <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <p style="margin: 0 0 10px 0;">
                    El número de capas en el modelo se ajusta para equilibrar la resolución y la estabilidad:
                </p>
                <ul style="margin: 0; padding-left: 20px;">
                    <li><strong>Aumentar capas:</strong> Mejora la resolución pero puede introducir ruido</li>
                    <li><strong>Disminuir capas:</strong> Produce mayor estabilidad pero menor resolución</li>
                </ul>
            </div>
        </div>
        """)
        inversion_text.setObjectName("content")
        inversion_text.setWordWrap(True)
        scroll_layout.addWidget(inversion_text)
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Botón de cerrar
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_button = QPushButton("✕ Cerrar")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

class HelpPreprocessingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ Ayuda - Preprocesamiento")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(700, 500)
        
        # Aplicar estilos modernos
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f8f9fa, stop: 1 #e9ecef);
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QWidget#scroll_content {
                background: white;
                border-radius: 12px;
                border: 1px solid #dee2e6;
            }
            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: white;
                padding: 20px;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #f093fb, stop: 1 #f5576c);
                border-radius: 8px;
                margin-bottom: 20px;
            }
            QLabel#content {
                color: #2c3e50;
                font-size: 14px;
                line-height: 1.6;
                padding: 20px;
                background: transparent;
            }
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f56565, stop: 1 #e53e3e);
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                margin: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e53e3e, stop: 1 #c53030);
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)
        
        # Título
        title = QLabel("⚙️ Preprocesamiento de Datos")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Crear área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Contenido scrollable
        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_content")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        # Texto explicativo
        preprocessing_text = QLabel("""
        <div style="padding: 20px; line-height: 1.8;">
            <h2 style="color: #f093fb; margin-bottom: 15px;">🎯 ¿Qué es el Preprocesamiento?</h2>
            <p style="margin-bottom: 15px;">
                El <strong>preprocesamiento en VESPY</strong> incluye el empalme y el suavizado de los datos de resistividad. 
                Estos pasos son fundamentales para preparar los datos antes de realizar la inversión y obtener resultados más precisos.
            </p>
            
            <h3 style="color: #f5576c; margin: 25px 0 15px 0;">🔗 Empalme de Datos</h3>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <p style="margin: 0 0 15px 0;">
                    El <strong>empalme</strong> combina múltiples mediciones de resistividad en un solo conjunto de datos 
                    para mejorar la calidad y reducir el ruido. 
                </p>
                <p style="margin: 0;">
                    La idea principal es integrar mediciones de diferentes conjuntos de datos (por ejemplo, con diferentes 
                    valores de MN) ajustando los segmentos para que formen una curva unificada, optimizando la continuidad 
                    y asegurando transiciones graduales.
                </p>
            </div>
            
            <h3 style="color: #f5576c; margin: 25px 0 15px 0;">🌊 Suavizado de Datos</h3>
            <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <p style="margin: 0 0 15px 0;">
                    El <strong>suavizado</strong> aplica filtros a los datos de resistividad para eliminar el ruido 
                    y resaltar las tendencias principales. Esto mejora la calidad del modelo de inversión.
                </p>
            </div>
            
            <h3 style="color: #f5576c; margin: 25px 0 15px 0;">🔧 Tipos de Filtros</h3>
            
            <div style="background: #fff3e0; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #f57c00; margin: 0 0 10px 0;">📊 Filtro de Savitzky-Golay</h4>
                <p style="margin: 0;">
                    Ajusta una serie de polinomios a los datos en una ventana deslizante, 
                    permitiendo suavizar sin distorsionar significativamente las características importantes.
                </p>
            </div>
            
            <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #1976d2; margin: 0 0 10px 0;">📈 Media Móvil</h4>
                <p style="margin: 0;">
                    Calcula el promedio de los datos en una ventana deslizante, 
                    ayudando a reducir el ruido aleatorio y resaltar las tendencias a largo plazo.
                </p>
            </div>
            
            <div style="background: #f3e5f5; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #7b1fa2; margin: 0 0 10px 0;">⚡ Suavizado Exponencial</h4>
                <p style="margin: 0;">
                    Aplica un promedio ponderado a los datos, donde los datos más recientes tienen mayor peso, 
                    permitiendo una respuesta más rápida a los cambios en los datos.
                </p>
            </div>
            
            <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #4caf50;">
                <h4 style="color: #2e7d32; margin: 0 0 10px 0;">💡 Recomendaciones</h4>
                <ul style="margin: 0; padding-left: 20px; color: #2e7d32;">
                    <li>Realiza siempre el empalme antes del suavizado</li>
                    <li>Ajusta los parámetros de suavizado según el nivel de ruido</li>
                    <li>Visualiza los resultados antes y después del preprocesamiento</li>
                </ul>
            </div>
        </div>
        """)
        preprocessing_text.setObjectName("content")
        preprocessing_text.setWordWrap(True)
        scroll_layout.addWidget(preprocessing_text)
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Botón de cerrar
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_button = QPushButton("✕ Cerrar")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

class HelpAnalysisWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📊 Ayuda - Análisis de Datos")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(700, 500)
        
        # Estilos modernos
        self.setStyleSheet("""
            QDialog { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f8f9fa, stop: 1 #e9ecef); }
            QScrollArea { border: none; background: transparent; }
            QWidget#scroll_content { background: white; border-radius: 12px; border: 1px solid #dee2e6; }
            QLabel#title { font-size: 28px; font-weight: bold; color: white; padding: 20px; 
                          background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #4facfe, stop: 1 #00f2fe); 
                          border-radius: 8px; margin-bottom: 20px; }
            QLabel#content { color: #2c3e50; font-size: 14px; line-height: 1.6; padding: 20px; background: transparent; }
            QPushButton { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f56565, stop: 1 #e53e3e); 
                         color: white; border: none; padding: 12px 30px; font-size: 14px; font-weight: bold; 
                         border-radius: 8px; margin: 20px; }
            QPushButton:hover { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e53e3e, stop: 1 #c53030); }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)
        
        title = QLabel("📊 Análisis de Datos")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_content")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        analysis_text = QLabel("""
        <div style="padding: 20px; line-height: 1.8;">
            <h2 style="color: #4facfe; margin-bottom: 15px;">🎯 Análisis Estadístico</h2>
            <p>El <strong>análisis de datos en VESPY</strong> incluye herramientas avanzadas para generar estadísticas 
            descriptivas y visualizaciones que permiten entender mejor los datos de resistividad.</p>
            
            <h3 style="color: #00f2fe; margin: 25px 0 15px 0;">📈 Estadísticas Descriptivas</h3>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <p>VESPY calcula automáticamente:</p>
                <ul style="margin: 10px 0 0 20px;">
                    <li><strong>Media:</strong> Promedio de los valores de resistividad</li>
                    <li><strong>Mediana:</strong> Valor central de la distribución</li>
                    <li><strong>Desviación estándar:</strong> Medida de dispersión de los datos</li>
                    <li><strong>Percentiles:</strong> Valores que dividen la distribución en partes iguales</li>
                </ul>
                <p style="margin-top: 10px; font-style: italic; color: #6c757d;">
                    Utilizando <code>numpy</code> y <code>pandas</code> para máxima precisión y eficiencia.
                </p>
            </div>
            
            <h3 style="color: #00f2fe; margin: 25px 0 15px 0;">📊 Análisis de Frecuencia</h3>
            <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #28a745; margin: 0 0 10px 0;">📋 Histogramas</h4>
                <p>Representación gráfica de la distribución de datos, mostrando la frecuencia en intervalos específicos.</p>
                
                <h4 style="color: #28a745; margin: 15px 0 10px 0;">📈 Histogramas Acumulativos</h4>
                <p>Muestran la suma acumulada de frecuencias, útiles para entender la distribución acumulativa.</p>
            </div>
            
            <h3 style="color: #00f2fe; margin: 25px 0 15px 0;">🔬 Análisis Avanzado</h3>
            <div style="background: #fff3e0; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #f57c00; margin: 0 0 10px 0;">🌊 Transformada de Fourier</h4>
                <p>Herramienta matemática que descompone señales en componentes de frecuencia, útil para analizar 
                patrones periódicos en los datos de resistividad.</p>
                
                <h4 style="color: #f57c00; margin: 15px 0 10px 0;">📐 Derivadas Logarítmicas</h4>
                <p>Analizan la tasa de cambio relativa de los datos, identificando tendencias en datos que varían exponencialmente.</p>
            </div>
            
            <h3 style="color: #00f2fe; margin: 25px 0 15px 0;">🗺️ Visualización Espacial</h3>
            <div style="background: #f3e5f5; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <p>Generación de mapas de resistividad utilizando técnicas de interpolación avanzadas:</p>
                <ul style="margin: 10px 0 0 20px;">
                    <li><strong>Kriging:</strong> Método geoestadístico para interpolación óptima</li>
                    <li><strong>IDW:</strong> Interpolación inversa de la distancia ponderada</li>
                </ul>
                <p style="margin-top: 10px; font-style: italic; color: #6c757d;">
                    Implementado con <code>scipy</code>, <code>matplotlib</code> y <code>seaborn</code>.
                </p>
            </div>
        </div>
        """)
        analysis_text.setObjectName("content")
        analysis_text.setWordWrap(True)
        scroll_layout.addWidget(analysis_text)
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_button = QPushButton("✕ Cerrar")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

class HelpPlottingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📈 Ayuda - Gráficos")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(700, 500)
        
        # Estilos modernos
        self.setStyleSheet("""
            QDialog { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f8f9fa, stop: 1 #e9ecef); }
            QScrollArea { border: none; background: transparent; }
            QWidget#scroll_content { background: white; border-radius: 12px; border: 1px solid #dee2e6; }
            QLabel#title { font-size: 28px; font-weight: bold; color: white; padding: 20px; 
                          background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #a8edea, stop: 1 #fed6e3); 
                          border-radius: 8px; margin-bottom: 20px; }
            QLabel#content { color: #2c3e50; font-size: 14px; line-height: 1.6; padding: 20px; background: transparent; }
            QPushButton { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f56565, stop: 1 #e53e3e); 
                         color: white; border: none; padding: 12px 30px; font-size: 14px; font-weight: bold; 
                         border-radius: 8px; margin: 20px; }
            QPushButton:hover { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e53e3e, stop: 1 #c53030); }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)
        
        title = QLabel("📈 Generación de Gráficos")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_content")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        plotting_text = QLabel("""
        <div style="padding: 20px; line-height: 1.8;">
            <h2 style="color: #a8edea; margin-bottom: 15px;">🎨 Visualización de Datos</h2>
            <p><strong>VESPY</strong> permite generar varios tipos de gráficos para visualizar los datos de resistividad 
            y los resultados de la inversión de manera clara y profesional.</p>
            
            <h3 style="color: #fed6e3; margin: 25px 0 15px 0;">📊 Curva de Resistividad</h3>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <p>Este gráfico muestra la resistividad en función de la profundidad, permitiendo identificar 
                capas de diferentes resistividades en el subsuelo.</p>
                <p style="margin-top: 10px;"><strong>Escala Logarítmica:</strong> La visualización utiliza escala logarítmica 
                debido a la amplia gama de valores de resistividad en el subsuelo.</p>
            </div>
            
            <h3 style="color: #fed6e3; margin: 25px 0 15px 0;">🗺️ Gráficos 2D</h3>
            <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <p><strong>Resolución:</strong> Cantidad de puntos de datos utilizados para crear la visualización.</p>
                <p><strong>Niveles:</strong> Intervalos de valores representados en el gráfico.</p>
                <p style="margin-top: 10px; font-style: italic;">Una mayor resolución y más niveles proporcionan 
                visualizaciones más detalladas de las estructuras geológicas.</p>
            </div>
            
            <h3 style="color: #fed6e3; margin: 25px 0 15px 0;">🔧 Métodos de Interpolación</h3>
            <p style="margin-bottom: 15px;">Técnicas para estimar valores desconocidos entre puntos de datos conocidos:</p>
            
            <div style="background: #fff3e0; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #f57c00; margin: 0 0 10px 0;">📏 Linear</h4>
                <p>Utiliza líneas rectas entre dos puntos de datos conocidos. Método rápido y simple.</p>
            </div>
            
            <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #1976d2; margin: 0 0 10px 0;">🌊 Cubic</h4>
                <p>Utiliza polinomios cúbicos para estimar valores, proporcionando transiciones más suaves 
                entre puntos de datos.</p>
            </div>
            
            <div style="background: #f3e5f5; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #7b1fa2; margin: 0 0 10px 0;">📍 Nearest</h4>
                <p>Asigna el valor del punto de datos conocido más cercano, resultando en transiciones más abruptas 
                pero preservando valores exactos.</p>
            </div>
            
            <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #4caf50;">
                <h4 style="color: #2e7d32; margin: 0 0 10px 0;">💡 Consejos de Visualización</h4>
                <ul style="margin: 0; padding-left: 20px; color: #2e7d32;">
                    <li>Ajusta la resolución según el detalle requerido</li>
                    <li>Usa interpolación cubic para datos suaves</li>
                    <li>Considera la escala logarítmica para rangos amplios</li>
                    <li>Valida los resultados con datos conocidos</li>
                </ul>
            </div>
        </div>
        """)
        plotting_text.setObjectName("content")
        plotting_text.setWordWrap(True)
        scroll_layout.addWidget(plotting_text)
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_button = QPushButton("✕ Cerrar")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

class HelpUsageWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("❓ Ayuda - Guía de Uso")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(700, 500)
        
        # Estilos modernos
        self.setStyleSheet("""
            QDialog { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f8f9fa, stop: 1 #e9ecef); }
            QScrollArea { border: none; background: transparent; }
            QWidget#scroll_content { background: white; border-radius: 12px; border: 1px solid #dee2e6; }
            QLabel#title { font-size: 28px; font-weight: bold; color: white; padding: 20px; 
                          background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffecd2, stop: 1 #fcb69f); 
                          border-radius: 8px; margin-bottom: 20px; }
            QLabel#content { color: #2c3e50; font-size: 14px; line-height: 1.6; padding: 20px; background: transparent; }
            QPushButton { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f56565, stop: 1 #e53e3e); 
                         color: white; border: none; padding: 12px 30px; font-size: 14px; font-weight: bold; 
                         border-radius: 8px; margin: 20px; }
            QPushButton:hover { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e53e3e, stop: 1 #c53030); }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)
        
        title = QLabel("❓ Guía de Uso del Software")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_content")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        usage_text = QLabel("""
        <div style="padding: 20px; line-height: 1.8;">
            <h2 style="color: #ffecd2; margin-bottom: 15px;">🚀 Pasos para Usar VESPY</h2>
            <p>Sigue esta guía paso a paso para obtener los mejores resultados con VESPY:</p>
            
            <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2196f3;">
                <h3 style="color: #1976d2; margin: 0 0 15px 0;">1️⃣ Cargar Datos</h3>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>Haz clic en '<strong>Cargar Datos</strong>' en la barra de herramientas</li>
                    <li>Selecciona el archivo de datos de resistividad</li>
                    <li>Asegúrate de que el archivo esté en formato correcto (CSV o TXT)</li>
                    <li>Verifica que los datos estén organizados adecuadamente</li>
                </ul>
            </div>
            
            <div style="background: #f3e5f5; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #9c27b0;">
                <h3 style="color: #7b1fa2; margin: 0 0 15px 0;">2️⃣ Preprocesar Datos</h3>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>Utiliza las pestañas de preprocesamiento</li>
                    <li>Realiza el <strong>empalme</strong> para combinar múltiples mediciones</li>
                    <li>Aplica <strong>suavizado</strong> para eliminar ruido</li>
                    <li>Ajusta los parámetros según la calidad de tus datos</li>
                </ul>
            </div>
            
            <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #4caf50;">
                <h3 style="color: #2e7d32; margin: 0 0 15px 0;">3️⃣ Invertir Modelo</h3>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>Haz clic en '<strong>Invertir Modelo</strong>'</li>
                    <li>Selecciona el método de inversión (ej: Navaja de Occam)</li>
                    <li>Ajusta parámetros de regularización (lambda y factor lambda)</li>
                    <li>Revisa los resultados preliminares y ajusta si es necesario</li>
                </ul>
            </div>
            
            <div style="background: #fff3e0; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ff9800;">
                <h3 style="color: #f57c00; margin: 0 0 15px 0;">4️⃣ Generar Gráficos</h3>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>Utiliza las opciones de generación de gráficos</li>
                    <li>Crea gráficos de resistividad vs profundidad</li>
                    <li>Genera gráficos 2D interpolados</li>
                    <li>Ajusta resolución y niveles para mejor visualización</li>
                </ul>
            </div>
            
            <div style="background: #ffebee; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #f44336;">
                <h3 style="color: #d32f2f; margin: 0 0 15px 0;">5️⃣ Guardar Resultados</h3>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>Guarda los modelos invertidos y gráficos generados</li>
                    <li>Utiliza las opciones de guardado en la barra de herramientas</li>
                    <li>Elige formatos adecuados (PNG para gráficos, CSV para datos)</li>
                    <li>Organiza los archivos para fácil acceso posterior</li>
                </ul>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #495057; margin: 0 0 15px 0;">💡 Consejos Adicionales</h3>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>Siempre visualiza los datos antes y después del preprocesamiento</li>
                    <li>Experimenta con diferentes parámetros de inversión</li>
                    <li>Guarda copias de seguridad de tus datos originales</li>
                    <li>Consulta la documentación específica para cada herramienta</li>
                    <li>Utiliza el sistema de ayuda integrado para dudas específicas</li>
                </ul>
            </div>
        </div>
        """)
        usage_text.setObjectName("content")
        usage_text.setWordWrap(True)
        scroll_layout.addWidget(usage_text)
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_button = QPushButton("✕ Cerrar")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)