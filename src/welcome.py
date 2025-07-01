import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QWidget, QFrame, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer
import webbrowser
from pathlib import Path

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        
        # Auto-cerrar después de 5 segundos si el usuario no hace nada
        self.auto_close_timer = QTimer()
        self.auto_close_timer.timeout.connect(self.auto_close)
        self.auto_close_timer.start(8000)  # 8 segundos

    def setupUI(self):
        """Configurar la interfaz de usuario moderna"""
        self.setWindowTitle("VESPY - Bienvenida")
        self.setFixedSize(500, 600)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        # Aplicar estilo moderno
        self.setStyleSheet(self.get_modern_style())
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 20, 30, 20)
        
        # Header con logo y título
        self.create_header(main_layout)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #cccccc;")
        main_layout.addWidget(separator)
        
        # Sección de agradecimientos
        self.create_sponsors_section(main_layout)
        
        # Separador
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setStyleSheet("color: #cccccc;")
        main_layout.addWidget(separator2)
        
        # Botones de acción
        self.create_action_buttons(main_layout)
        
        # Footer
        self.create_footer(main_layout)
        
        # Centrar la ventana
        self.center_window()

    def get_modern_style(self):
        """Estilo moderno para la ventana de bienvenida"""
        return """
        QMainWindow {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f8f9fa, stop: 1 #e9ecef);
        }
        
        QWidget {
            background-color: transparent;
        }
        
        QLabel {
            color: #343a40;
        }
        
        QPushButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #28a745, stop: 1 #1e7e34);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            min-width: 120px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #34ce57, stop: 1 #28a745);
            transform: translateY(-2px);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #1e7e34, stop: 1 #155724);
        }
        
        QPushButton#continueButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #007bff, stop: 1 #0056b3);
        }
        
        QPushButton#continueButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #0084ff, stop: 1 #007bff);
        }
        
        QFrame {
            background-color: transparent;
        }
        
        #titleLabel {
            font-size: 28px;
            font-weight: bold;
            color: #007bff;
            margin: 10px 0;
        }
        
        #subtitleLabel {
            font-size: 16px;
            color: #6c757d;
            margin-bottom: 10px;
        }
        
        #sponsorsLabel {
            font-size: 12px;
            color: #495057;
            background-color: rgba(255, 255, 255, 0.8);
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        
        #footerLabel {
            font-size: 11px;
            color: #6c757d;
            margin-top: 10px;
        }
        """

    def create_header(self, layout):
        """Crear el header con logo y título"""
        header_layout = QVBoxLayout()
        
        # Logo de VESPY
        logo_label = QLabel()
        try:
            # Intentar cargar el logo principal
            image_path = Path(__file__).parent.parent / 'images' / 'logo.png'
            if image_path.exists():
                pixmap = QPixmap(str(image_path))
                pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(pixmap)
        except:
            # Si no se puede cargar el logo, mostrar emoji
            logo_label.setText("🌍")
            logo_label.setStyleSheet("font-size: 48px;")
        
        logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(logo_label)
        
        # Título principal
        title_label = QLabel("VESPY")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Visualización y Procesamiento de Datos de Sondeo Eléctrico Vertical")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setWordWrap(True)
        header_layout.addWidget(subtitle_label)
        
        layout.addLayout(header_layout)

    def create_sponsors_section(self, layout):
        """Crear la sección de agradecimientos"""
        # Título de agradecimientos
        thanks_label = QLabel("💝 Agradecimientos Especiales")
        thanks_label.setAlignment(Qt.AlignCenter)
        thanks_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #28a745; margin: 10px 0;")
        layout.addWidget(thanks_label)
        
        # Lista de patrocinadores
        sponsors_label = QLabel()
        sponsors_label.setObjectName("sponsorsLabel")
        sponsors_text = self.get_sponsors_text()
        sponsors_label.setText(sponsors_text)
        sponsors_label.setAlignment(Qt.AlignCenter)
        sponsors_label.setWordWrap(True)
        layout.addWidget(sponsors_label)

    def create_action_buttons(self, layout):
        """Crear los botones de acción"""
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Botón de Patreon
        patreon_button = QPushButton("💖 Patrocíname en Patreon")
        patreon_button.setToolTip("Apoya el desarrollo de VESPY")
        patreon_button.clicked.connect(self.open_patreon)
        buttons_layout.addWidget(patreon_button)
        
        # Botón para continuar
        continue_button = QPushButton("🚀 Continuar a VESPY")
        continue_button.setObjectName("continueButton")
        continue_button.setToolTip("Abrir la aplicación principal")
        continue_button.clicked.connect(self.continue_to_app)
        buttons_layout.addWidget(continue_button)
        
        layout.addLayout(buttons_layout)

    def create_footer(self, layout):
        """Crear el footer informativo"""
        footer_layout = QVBoxLayout()
        
        # Espacio flexible
        footer_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Información adicional
        info_label = QLabel("Esta ventana se cerrará automáticamente en unos segundos...")
        info_label.setObjectName("footerLabel")
        info_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(info_label)
        
        # Copyright
        copyright_label = QLabel("© 2024 VESPY - Herramienta de Análisis Geofísico")
        copyright_label.setObjectName("footerLabel")
        copyright_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(copyright_label)
        
        layout.addLayout(footer_layout)

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        from PyQt5.QtWidgets import QDesktopWidget
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_sponsors_text(self):
        """Leer el archivo CSV y obtener los nombres de los patrocinadores."""
        try:
            csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'aditional-data', 'members.csv'))
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                sponsors = df[df['Free Member'] == 'No']['Name'].tolist()
                if sponsors:
                    sponsors_text = "Este proyecto se ha hecho gracias a las aportaciones en Patreon de:\n\n"
                    sponsors_text += "🌟 " + "\n🌟 ".join(sponsors)
                    sponsors_text += "\n\n¡Gracias por hacer posible VESPY!"
                else:
                    sponsors_text = "¡Sé el primero en apoyar VESPY en Patreon!\n\nTu apoyo nos ayuda a mantener y mejorar esta herramienta."
            else:
                sponsors_text = "¡Apoya el desarrollo de VESPY en Patreon!\n\nTu contribución nos ayuda a seguir mejorando esta herramienta para la comunidad geofísica."
        except Exception as e:
            sponsors_text = "¡Apoya el desarrollo de VESPY en Patreon!\n\nTu contribución nos ayuda a seguir mejorando esta herramienta."
        
        return sponsors_text

    def open_patreon(self):
        """Abrir la página de Patreon"""
        self.auto_close_timer.stop()
        webbrowser.open("https://www.patreon.com/chemitas")
        # Opcional: cerrar la ventana después de abrir Patreon
        QTimer.singleShot(1000, self.continue_to_app)

    def continue_to_app(self):
        """Continuar a la aplicación principal"""
        self.auto_close_timer.stop()
        self.close()

    def auto_close(self):
        """Cerrar automáticamente la ventana"""
        self.continue_to_app()

    def closeEvent(self, event):
        """Manejar el evento de cierre"""
        self.auto_close_timer.stop()
        from vespy import SEVApp  # Importar SEVApp desde vespy en src
        self.main_window = SEVApp()
        self.main_window.show()
        event.accept()