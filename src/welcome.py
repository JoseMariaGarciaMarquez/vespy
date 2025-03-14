import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import webbrowser

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bienvenida")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Imagen de Patreon
        image_label = QLabel(self)
        pixmap = QPixmap("images/patreon.png")
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        # Lista de patrocinadores
        sponsors_label = QLabel(self)
        sponsors_text = self.get_sponsors_text()
        sponsors_label.setText(sponsors_text)
        sponsors_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(sponsors_label)

        # Botón de Patreon
        patreon_button = QPushButton("Patrocíname", self)
        patreon_button.clicked.connect(self.open_patreon)
        layout.addWidget(patreon_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_sponsors_text(self):
        """Leer el archivo CSV y obtener los nombres de los patrocinadores."""
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'aditional-data', 'members.csv'))
        df = pd.read_csv(csv_path)
        sponsors = df[df['Free Member'] == 'No']['Name'].tolist()
        sponsors_text = "Este proyecto se ha hecho gracias a las aportaciones en Patreon de:\n" + "\n".join(sponsors)
        return sponsors_text

    def open_patreon(self):
        webbrowser.open("https://www.patreon.com/chemitas")

    def closeEvent(self, event):
        from vespy import SEVApp  # Importar SEVApp desde vespy en src
        self.main_window = SEVApp()
        self.main_window.show()
        event.accept()