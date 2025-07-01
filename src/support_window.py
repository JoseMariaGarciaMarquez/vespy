import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QScrollArea, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
import webbrowser
from pathlib import Path

class SupportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Configurar la interfaz de usuario moderna"""
        self.setWindowTitle('💖 ¡Quiero aportar a VESPY!')
        self.setFixedSize(550, 700)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        # Aplicar estilo moderno
        self.setStyleSheet(self.get_modern_style())
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        self.create_header(main_layout)
        
        # Contenido principal con scroll
        self.create_content(main_layout)
        
        # Footer con botones de acción
        self.create_footer(main_layout)
        
        self.setLayout(main_layout)
        self.center_window()

    def get_modern_style(self):
        """Estilo moderno para la ventana de soporte"""
        return """
        QWidget {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #667eea, stop: 1 #764ba2);
            color: white;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        #headerFrame {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #4facfe, stop: 1 #00f2fe);
            border: none;
            padding: 20px;
        }
        
        #contentFrame {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #ffffff, stop: 1 #f8f9fa);
            border: none;
            border-radius: 15px;
            margin: 10px;
            padding: 20px;
        }
        
        #footerFrame {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #ff9a9e, stop: 1 #fecfef);
            border: none;
            padding: 15px;
        }
        
        #titleLabel {
            font-size: 24px;
            font-weight: bold;
            color: white;
            margin: 10px 0;
        }
        
        #subtitleLabel {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 10px;
        }
        
        #contentLabel {
            color: #343a40;
            font-size: 13px;
            line-height: 1.6;
            background: transparent;
        }
        
        QPushButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #667eea, stop: 1 #764ba2);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 13px;
            min-width: 120px;
            margin: 5px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #7c3aed, stop: 1 #8b5cf6);
            transform: translateY(-2px);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #5b21b6, stop: 1 #6d28d9);
        }
        
        QPushButton#patreonButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #ff424d, stop: 1 #ff6b35);
            font-size: 16px;
            padding: 15px 25px;
            min-width: 200px;
        }
        
        QPushButton#patreonButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #ff6b35, stop: 1 #f7931e);
        }
        
        QPushButton#youtubeButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #ff0000, stop: 1 #cc0000);
        }
        
        QPushButton#twitchButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #9146ff, stop: 1 #772ce8);
        }
        
        QScrollArea {
            border: none;
            background: transparent;
        }
        
        QFrame#separator {
            background-color: rgba(255, 255, 255, 0.3);
            max-height: 2px;
            margin: 10px 20px;
        }
        """

    def create_header(self, layout):
        """Crear el header de la ventana"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout(header_frame)
        
        # Emoji grande
        emoji_label = QLabel("�")
        emoji_label.setAlignment(Qt.AlignCenter)
        emoji_label.setStyleSheet("font-size: 48px; margin: 10px;")
        header_layout.addWidget(emoji_label)
        
        # Título
        title_label = QLabel("¡Apoya el desarrollo de VESPY!")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Tu contribución hace posible que esta herramienta siga mejorando")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setWordWrap(True)
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_frame)

    def create_content(self, layout):
        """Crear el contenido principal"""
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)
        
        # Crear área de scroll para el contenido
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Mensaje principal
        message = self.get_support_message()
        content_label = QLabel(message)
        content_label.setObjectName("contentLabel")
        content_label.setWordWrap(True)
        content_label.setTextFormat(Qt.RichText)
        content_label.setAlignment(Qt.AlignLeft)
        scroll_layout.addWidget(content_label)
        
        # Información del autor
        author_info = self.get_author_info()
        author_label = QLabel(author_info)
        author_label.setObjectName("contentLabel")
        author_label.setWordWrap(True)
        author_label.setTextFormat(Qt.RichText)
        author_label.setAlignment(Qt.AlignLeft)
        scroll_layout.addWidget(author_label)
        
        scroll_area.setWidget(scroll_widget)
        content_layout.addWidget(scroll_area)
        
        layout.addWidget(content_frame)

    def create_footer(self, layout):
        """Crear el footer con botones de acción"""
        footer_frame = QFrame()
        footer_frame.setObjectName("footerFrame")
        footer_layout = QVBoxLayout(footer_frame)
        
        # Botón principal de Patreon
        patreon_button = QPushButton('🌟 Únete a mi Patreon')
        patreon_button.setObjectName("patreonButton")
        patreon_button.setToolTip("Apoya el proyecto con una contribución mensual")
        patreon_button.clicked.connect(lambda: self.open_link("https://www.patreon.com/chemitas"))
        footer_layout.addWidget(patreon_button)
        
        # Separador
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.HLine)
        footer_layout.addWidget(separator)
        
        # Botones de redes sociales
        social_layout = QHBoxLayout()
        social_layout.setSpacing(10)
        
        youtube_button = QPushButton('📺 YouTube')
        youtube_button.setObjectName("youtubeButton")
        youtube_button.setToolTip("Visita mi canal de YouTube")
        youtube_button.clicked.connect(lambda: self.open_link("https://www.youtube.com/@jomaing"))
        social_layout.addWidget(youtube_button)
        
        twitch_button = QPushButton('🎮 Twitch')
        twitch_button.setObjectName("twitchButton")
        twitch_button.setToolTip("Sígueme en Twitch")
        twitch_button.clicked.connect(lambda: self.open_link("https://www.twitch.tv/chemitas96"))
        social_layout.addWidget(twitch_button)
        
        footer_layout.addLayout(social_layout)
        
        # Botón de cerrar
        close_button = QPushButton('❌ Cerrar')
        close_button.setToolTip("Cerrar esta ventana")
        close_button.clicked.connect(self.close)
        footer_layout.addWidget(close_button)
        
        layout.addWidget(footer_frame)

    def get_support_message(self):
        """Obtener el mensaje de soporte principal"""
        return """
        <div style="text-align: center; margin: 20px 0;">
            <h3 style="color: #667eea; margin-bottom: 15px;">🚀 ¿Cómo tu apoyo hace la diferencia?</h3>
        </div>
        
        <p><strong>VESPY es un proyecto de código abierto</strong> desarrollado con pasión para la comunidad geofísica. 
        Tu apoyo me permite:</p>
        
        <ul style="line-height: 1.8; margin: 15px 0;">
            <li>🔧 <strong>Mantener y mejorar VESPY</strong> con nuevas características</li>
            <li>📚 <strong>Crear tutoriales y documentación</strong> detallada</li>
            <li>🐛 <strong>Corregir errores</strong> y optimizar el rendimiento</li>
            <li>💡 <strong>Desarrollar nuevas herramientas</strong> para geofísica</li>
            <li>🎓 <strong>Compartir conocimientos</strong> en YouTube y Twitch</li>
        </ul>
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h4 style="margin: 0 0 10px 0;">💎 Niveles de Patrocinio:</h4>
            <p style="margin: 5px 0;"><strong>☕ Café Geofísico ($3/mes)</strong><br>
            • Acceso a actualizaciones exclusivas<br>
            • Agradecimiento en redes sociales</p>
            
            <p style="margin: 5px 0;"><strong>📡 Explorador de Ondas ($5/mes)</strong><br>
            • Todo lo anterior + acceso anticipado a tutoriales<br>
            • Participación en decisiones de futuros proyectos</p>
            
            <p style="margin: 5px 0;"><strong>🌍 Maestro de Fourier ($10/mes)</strong><br>
            • Todo lo anterior + sesiones Q&A mensuales<br>
            • Créditos especiales en los proyectos</p>
        </div>
        """

    def get_author_info(self):
        """Obtener información del autor"""
        return """
        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; 
                    border-left: 4px solid #667eea; margin: 20px 0;">
            <h4 style="color: #667eea; margin: 0 0 10px 0;">👨‍🔬 Sobre el Autor</h4>
            <p><strong>Soy un ingeniero geofísico apasionado</strong> por el análisis de datos, 
            la estadística, Python y el software de código abierto.</p>
            
            <p>Mi misión es <strong>democratizar las herramientas geofísicas</strong> y hacer que 
            sean accesibles para estudiantes, profesionales e investigadores en todo el mundo.</p>
            
            <p style="margin: 15px 0 5px 0;"><strong>🎯 Mis objetivos:</strong></p>
            <ul style="margin: 5px 0;">
                <li>Crear software geofísico de calidad profesional</li>
                <li>Educar a través de contenido en YouTube y Twitch</li>
                <li>Fomentar la comunidad de código abierto en geofísica</li>
                <li>Hacer la ciencia más accesible y divertida</li>
            </ul>
        </div>
        
        <p style="text-align: center; font-size: 16px; color: #667eea; margin: 20px 0;">
            <strong>¡Juntos podemos hacer que VESPY sea aún mejor! 🌟</strong>
        </p>
        """

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        from PyQt5.QtWidgets import QDesktopWidget
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_link(self, url):
        """Abrir enlace en el navegador"""
        webbrowser.open(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SupportWindow()
    window.show()
    sys.exit(app.exec_())