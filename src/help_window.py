from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayuda de VESPY")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("<h1>Ayuda de VESPY</h1>")
        layout.addWidget(title)
        
        # Botones para abrir las ventanas de ayuda específicas
        inversion_button = QPushButton("Inversión")
        inversion_button.clicked.connect(self.show_inversion_help)
        layout.addWidget(inversion_button)
        
        preprocessing_button = QPushButton("Preprocesamiento")
        preprocessing_button.clicked.connect(self.show_preprocessing_help)
        layout.addWidget(preprocessing_button)
        
        analysis_button = QPushButton("Análisis de Datos")
        analysis_button.clicked.connect(self.show_analysis_help)
        layout.addWidget(analysis_button)
        
        plotting_button = QPushButton("Generación de Gráficos")
        plotting_button.clicked.connect(self.show_plotting_help)
        layout.addWidget(plotting_button)
        
        usage_button = QPushButton("Cómo Usar el Software")
        usage_button.clicked.connect(self.show_usage_help)
        layout.addWidget(usage_button)
        
        # Botón de Cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
    
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
        self.setWindowTitle("Ayuda de VESPY - Inversión")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("<h1>Inversión</h1>")
        layout.addWidget(title)
        
        # Texto de Inversión
        inversion_text = QLabel(
            "<p>La inversión en VESPY se refiere al proceso de ajustar un modelo de subsuelo "
            "a los datos de resistividad medidos. Este proceso permite estimar la distribución "
            "de resistividades en función de la profundidad.</p>"
            "<p><b>Lambda:</b> El parámetro lambda controla la regularización del modelo de inversión. "
            "Un valor más alto de lambda suaviza el modelo, mientras que un valor más bajo permite "
            "más variabilidad en el modelo.</p>"
            "<p><b>Factor Lambda:</b> El factor lambda es un multiplicador que ajusta el valor de lambda "
            "durante el proceso de inversión. Esto permite un control más fino sobre la regularización "
            "del modelo.</p>"
        )
        inversion_text.setWordWrap(True)
        layout.addWidget(inversion_text)
        
        # Botón de Cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)

class HelpPreprocessingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayuda de VESPY - Preprocesamiento")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("<h1>Preprocesamiento</h1>")
        layout.addWidget(title)
        
        # Texto de Preprocesamiento
        preprocessing_text = QLabel(
            "<p>El preprocesamiento en VESPY incluye el empalme y el suavizado de los datos de resistividad. "
            "Estos pasos son importantes para preparar los datos antes de realizar la inversión.</p>"
            "<p><b>Empalme:</b> El empalme combina múltiples mediciones de resistividad en un solo conjunto de datos "
            "para mejorar la calidad de los datos y reducir el ruido.</p>"
            "<p><b>Suavizado:</b> El suavizado aplica un filtro a los datos de resistividad para eliminar el ruido "
            "y resaltar las tendencias principales en los datos.</p>"
        )
        preprocessing_text.setWordWrap(True)
        layout.addWidget(preprocessing_text)
        
        # Botón de Cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)

class HelpAnalysisWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayuda de VESPY - Análisis de Datos")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("<h1>Análisis de Datos</h1>")
        layout.addWidget(title)
        
        # Texto de Análisis de Datos
        analysis_text = QLabel(
            "<p>El análisis de datos en VESPY incluye la generación de estadísticas descriptivas y gráficos "
            "para visualizar y entender mejor los datos de resistividad.</p>"
            "<p><b>Estadísticas Descriptivas:</b> VESPY calcula estadísticas como la media, la mediana, "
            "la desviación estándar y los percentiles para resumir los datos de resistividad.</p>"
            "<p><b>Gráficos:</b> VESPY genera gráficos de resistividad en función de la profundidad, "
            "así como gráficos 2D interpolados para visualizar la distribución espacial de la resistividad.</p>"
        )
        analysis_text.setWordWrap(True)
        layout.addWidget(analysis_text)
        
        # Botón de Cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)

class HelpPlottingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayuda de VESPY - Generación de Gráficos")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("<h1>Generación de Gráficos</h1>")
        layout.addWidget(title)
        
        # Texto de Generación de Gráficos
        plotting_text = QLabel(
            "<p>VESPY permite generar varios tipos de gráficos para visualizar los datos de resistividad y los resultados "
            "de la inversión.</p>"
            "<p><b>Curva de Resistividad:</b> Este gráfico muestra la resistividad en función de la profundidad, "
            "lo que permite identificar capas de diferentes resistividades en el subsuelo.</p>"
            "<p><b>Gráfico 2D Interpolado:</b> Este gráfico muestra la distribución espacial de la resistividad "
            "en una sección transversal del subsuelo, utilizando interpolación para estimar los valores entre los puntos medidos.</p>"
        )
        plotting_text.setWordWrap(True)
        layout.addWidget(plotting_text)
        
        # Botón de Cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)

class HelpUsageWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayuda de VESPY - Cómo Usar el Software")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("<h1>Cómo Usar el Software</h1>")
        layout.addWidget(title)
        
        # Texto de Cómo Usar el Software
        usage_text = QLabel(
            "<p>Para usar VESPY, sigue estos pasos:</p>"
            "<ol>"
            "<li><b>Cargar Datos:</b> Haz clic en 'Cargar Datos' en la barra de herramientas y selecciona el archivo de datos de resistividad.</li>"
            "<li><b>Preprocesar Datos:</b> Utiliza las pestañas de preprocesamiento para realizar el empalme y el suavizado de los datos.</li>"
            "<li><b>Invertir Modelo:</b> Haz clic en 'Invertir Modelo' para ajustar un modelo de resistividad a los datos medidos.</li>"
            "<li><b>Generar Gráficos:</b> Utiliza las opciones de generación de gráficos para visualizar los resultados de la inversión y los datos de resistividad.</li>"
            "<li><b>Guardar Resultados:</b> Guarda los modelos invertidos y los gráficos generados utilizando las opciones de guardado en la barra de herramientas.</li>"
            "</ol>"
        )
        usage_text.setWordWrap(True)
        layout.addWidget(usage_text)
        
        # Botón de Cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)