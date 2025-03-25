import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
import webbrowser

class SupportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('¡Quiero aportar!')

        layout = QVBoxLayout()

        message = (
            "<h2>📢 ¡Únete a mi comunidad en Patreon!</h2>"
            "<p><b>Soy ingeniero geofísico apasionado por el análisis de datos, la estadística, Python y el open source.</b> "
            "Si disfrutas de mi contenido en YouTube y Twitch o te interesa la geofísica y el software de procesamiento de datos, "
            "tu apoyo puede marcar la diferencia.</p>"
            "<p>Con tu contribución, me ayudas a seguir creando contenido, desarrollando proyectos de código abierto y compartiendo conocimientos. "
            "Además, recibirás recompensas exclusivas:</p>"
            "<ul>"
            "<li><b>☕ Invítame un café ($3/mes)</b><br>"
            "🔹 Acceso a actualizaciones exclusivas de mis proyectos.<br>"
            "🔹 Mención de agradecimiento en mis redes sociales.<br>"
            "🔹 Acceso a un canal de chat privado.</li>"
            "<li><b>📡 Principiante de Frecuencias ($5/mes)</b><br>"
            "🔹 Todo lo del nivel anterior.<br>"
            "🔹 Acceso anticipado a artículos y tutoriales.<br>"
            "🔹 Participación en encuestas para decidir futuros proyectos.</li>"
            "<li><b>🌍 Creyente de Fourier ($10/mes)</b><br>"
            "🔹 Todo lo de los niveles anteriores.<br>"
            "🔹 Sesiones mensuales de preguntas y respuestas en vivo.<br>"
            "🔹 Mención especial en los créditos de mis proyectos.</li>"
            "</ul>"
            "<p><b>¡Gracias por tu apoyo! 🙌</b></p>"
        )

        label = QLabel(message, self)
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        label.setTextFormat(Qt.RichText)
        layout.addWidget(label)

        button_patreon = QPushButton('Ir a Patreon', self)
        button_patreon.clicked.connect(lambda: self.open_link("https://www.patreon.com/tu_pagina"))
        layout.addWidget(button_patreon)

        button_youtube = QPushButton('YouTube', self)
        button_youtube.clicked.connect(lambda: self.open_link("https://www.youtube.com/@jomaing"))
        layout.addWidget(button_youtube)

        button_twitch = QPushButton('Twitch', self)
        button_twitch.clicked.connect(lambda: self.open_link("https://www.twitch.tv/chemitas96"))
        layout.addWidget(button_twitch)

        self.setLayout(layout)
        self.resize(400, 600)

    def open_link(self, url):
        webbrowser.open(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SupportWindow()
    window.show()
    sys.exit(app.exec_())