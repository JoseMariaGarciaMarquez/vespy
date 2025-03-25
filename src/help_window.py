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
            "<p><b>Inversión de Datos con la Navaja de Occam:</b> Este método busca el modelo más simple "
            "que explique los datos observados, evitando sobreajustes. La simplicidad del modelo se controla "
            "mediante la regularización, que penaliza la complejidad del modelo.</p>"
            "<p><b>Ventajas:</b> La inversión con la navaja de Occam produce modelos más estables y menos "
            "sensibles al ruido en los datos. Además, evita la sobreinterpretación de los datos.</p>"
            "<p><b>Desventajas:</b> Puede subestimar la complejidad real del subsuelo si la regularización "
            "es demasiado fuerte, omitiendo detalles importantes.</p>"
            "<p><b>Lambda:</b> El parámetro lambda controla la regularización del modelo de inversión. "
            "Un valor más alto de lambda suaviza el modelo, mientras que un valor más bajo permite "
            "más variabilidad en el modelo.</p>"
            "<p><b>Factor Lambda:</b> El factor lambda es un multiplicador que ajusta el valor de lambda "
            "durante el proceso de inversión. Esto permite un control más fino sobre la regularización "
            "del modelo.</p>"
            "<p><b>Criterio para Aumentar o Disminuir Capas:</b> El número de capas en el modelo se ajusta "
            "para equilibrar la resolución y la estabilidad. Aumentar el número de capas puede mejorar la "
            "resolución del modelo, pero también puede introducir ruido. Disminuir el número de capas "
            "puede producir un modelo más estable, pero con menor resolución.</p>"
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
            "para mejorar la calidad de los datos y reducir el ruido. La idea principal del empalme es integrar mediciones "
            "de diferentes conjuntos de datos (por ejemplo, con diferentes valores de MN) ajustando los segmentos para que formen una curva unificada. "
            "Esto optimiza la continuidad, asegurando que la transición entre las mediciones sea gradual y que el modelo pueda interpretarse sin interrupciones aparentes.</p>"
            "<p><b>Suavizado:</b> El suavizado aplica un filtro a los datos de resistividad para eliminar el ruido "
            "y resaltar las tendencias principales en los datos. Existen diferentes tipos de filtros de suavizado:</p>"
            "<ul>"
            "<li><b>Filtro de Savitzky-Golay:</b> Este filtro ajusta una serie de polinomios a los datos en una ventana deslizante, "
            "lo que permite suavizar los datos sin distorsionar significativamente las características importantes.</li>"
            "<li><b>Media Móvil:</b> Este filtro calcula el promedio de los datos en una ventana deslizante, "
            "lo que ayuda a reducir el ruido aleatorio y resaltar las tendencias a largo plazo.</li>"
            "<li><b>Suavizado Exponencial:</b> Este filtro aplica un promedio ponderado a los datos, "
            "donde los datos más recientes tienen un mayor peso, permitiendo una respuesta más rápida a los cambios en los datos.</li>"
            "</ul>"
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
        
        analysis_text = QLabel(
                    "<p>El análisis de datos en VESPY incluye la generación de estadísticas descriptivas y gráficos "
                    "para visualizar y entender mejor los datos de resistividad.</p>"
                    "<p><b>Estadísticas Descriptivas:</b> VESPY calcula estadísticas como la media, la mediana, "
                    "la desviación estándar y los percentiles para resumir los datos de resistividad. Estos cálculos "
                    "se realizan utilizando métodos de la biblioteca <code>numpy</code> y <code>pandas</code>, "
                    "asegurando precisión y eficiencia.</p>"
                    "<p><b>Gráficos:</b> VESPY genera gráficos de resistividad en función de la profundidad, "
                    "así como gráficos 2D interpolados para visualizar la distribución espacial de la resistividad. "
                    "Para esto, se utilizan las bibliotecas <code>matplotlib</code> y <code>seaborn</code>, "
                    "que permiten crear visualizaciones claras y detalladas.</p>"
                    "<p>Además, se aplican técnicas de interpolación para generar mapas de resistividad, "
                    "utilizando algoritmos como el de Kriging o la interpolación inversa de la distancia ponderada (IDW), "
                    "implementados en la biblioteca <code>scipy</code>.</p>"
                    "<p><b>Histogramas:</b> Un histograma es una representación gráfica de la distribución de un conjunto de datos. "
                    "Muestra la frecuencia de los datos en intervalos específicos, permitiendo identificar patrones y tendencias.</p>"
                    "<p><b>Histogramas Acumulativos:</b> Un histograma acumulativo muestra la suma acumulada de las frecuencias "
                    "de los datos hasta un punto específico, ayudando a entender la distribución acumulativa de los datos.</p>"
                    "<p><b>Transformada de Fourier:</b> La transformada de Fourier es una herramienta matemática que descompone una señal "
                    "en sus componentes de frecuencia. Es útil para analizar la frecuencia y la amplitud de las señales en los datos de resistividad.</p>"
                    "<p><b>Derivadas Logarítmicas:</b> Las derivadas logarítmicas se utilizan para analizar la tasa de cambio relativa de los datos. "
                    "Son útiles para identificar tendencias y patrones en datos que varían exponencialmente.</p>"

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
            "lo que permite identificar capas de diferentes resistividades en el subsuelo. La visualización de la resistividad aparente "
            "se realiza en una escala logarítmica debido a la amplia gama de valores que puede tomar la resistividad en el subsuelo. "
            "La resistividad aparente es una medida de la resistividad del subsuelo obtenida a partir de mediciones en la superficie, "
            "y puede variar significativamente dependiendo de las propiedades del subsuelo y la configuración del equipo de medición.</p>"
            "<p><b>Gráficos 2D:</b> En los gráficos 2D, la resolución se refiere a la cantidad de puntos de datos utilizados para crear la visualización, "
            "y los niveles se refieren a los intervalos de valores representados en el gráfico. Una mayor resolución y más niveles pueden proporcionar "
            "una visualización más detallada. Estos gráficos se utilizan para representar la distribución espacial de la resistividad en el subsuelo, "
            "permitiendo una mejor interpretación de las estructuras geológicas.</p>"
            "<p><b>Métodos de Interpolación:</b> La interpolación es una técnica para estimar valores desconocidos entre puntos de datos conocidos. "
            "Los métodos de interpolación incluyen:</p>"
            "<ul>"
            "<li><b>Linear:</b> La interpolación lineal estima valores desconocidos utilizando una línea recta entre dos puntos de datos conocidos.</li>"
            "<li><b>Cubic:</b> La interpolación cúbica utiliza polinomios cúbicos para estimar valores, proporcionando una transición más suave entre puntos de datos.</li>"
            "<li><b>Nearest:</b> La interpolación por el vecino más cercano asigna el valor del punto de datos conocido más cercano al punto desconocido, "
            "resultando en una transición más abrupta.</li>"
            "</ul>"
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
            "<p>Para usar VESPY, sigue estos pasos detallados:</p>"
            "<ol>"
            "<li><b>Cargar Datos:</b> Haz clic en 'Cargar Datos' en la barra de herramientas y selecciona el archivo de datos de resistividad. "
            "Asegúrate de que el archivo esté en el formato correcto (por ejemplo, CSV o TXT) y que los datos estén organizados adecuadamente.</li>"
            "<li><b>Preprocesar Datos:</b> Utiliza las pestañas de preprocesamiento para realizar el empalme y el suavizado de los datos. "
            "El empalme combina múltiples mediciones para mejorar la calidad de los datos, mientras que el suavizado aplica filtros para eliminar el ruido. "
            "Puedes ajustar los parámetros de los filtros según sea necesario para obtener los mejores resultados.</li>"
            "<li><b>Invertir Modelo:</b> Haz clic en 'Invertir Modelo' para ajustar un modelo de resistividad a los datos medidos. "
            "Selecciona el método de inversión adecuado (por ejemplo, la navaja de Occam) y ajusta los parámetros de regularización como el lambda y el factor lambda. "
            "Revisa los resultados preliminares y ajusta los parámetros si es necesario para mejorar la precisión del modelo.</li>"
            "<li><b>Generar Gráficos:</b> Utiliza las opciones de generación de gráficos para visualizar los resultados de la inversión y los datos de resistividad. "
            "Puedes crear gráficos de resistividad en función de la profundidad, gráficos 2D interpolados y otros tipos de visualizaciones. "
            "Ajusta la resolución y los niveles de los gráficos para obtener una representación clara y detallada de los datos.</li>"
            "<li><b>Guardar Resultados:</b> Guarda los modelos invertidos y los gráficos generados utilizando las opciones de guardado en la barra de herramientas. "
            "Asegúrate de guardar los archivos en un formato adecuado (por ejemplo, PNG para gráficos y CSV para datos) y organiza los archivos de manera que sean fáciles de acceder y revisar posteriormente.</li>"
            "</ol>"
            "<p>Para obtener más información sobre cada paso, consulta la documentación detallada de VESPY o accede a las ventanas de ayuda específicas desde la ventana principal de ayuda.</p>"
        )
        usage_text.setWordWrap(True)
        layout.addWidget(usage_text)
        
        # Botón de Cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)