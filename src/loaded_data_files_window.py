from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QListWidget, QMessageBox, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class LoadedDataFilesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📁 Archivos de Datos Cargados")
        self.setGeometry(100, 100, 600, 500)
        self.setMinimumSize(500, 400)
        
        self.parent = parent
        
        # Aplicar estilos modernos
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f8f9fa, stop: 1 #e9ecef);
                border-radius: 12px;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: white;
                padding: 15px;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #667eea, stop: 1 #764ba2);
                border-radius: 8px;
                margin-bottom: 15px;
            }
            QLabel#info {
                color: #6c757d;
                font-size: 14px;
                font-style: italic;
                padding: 10px;
                background: transparent;
            }
            QListWidget {
                background: white;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                selection-background-color: #667eea;
                selection-color: white;
                alternate-background-color: #f8f9fa;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e9ecef;
                border-radius: 4px;
                margin: 2px 0;
            }
            QListWidget::item:hover {
                background: #e3f2fd;
                color: #1976d2;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #667eea, stop: 1 #764ba2);
                color: white;
                font-weight: bold;
            }
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #667eea, stop: 1 #764ba2);
                color: white;
                border: none;
                padding: 12px 20px;
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
            QPushButton#delete_button {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f56565, stop: 1 #e53e3e);
            }
            QPushButton#delete_button:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e53e3e, stop: 1 #c53030);
            }
            QPushButton#close_button {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #6c757d, stop: 1 #495057);
            }
            QPushButton#close_button:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5a6268, stop: 1 #343a40);
            }
            QFrame {
                background: white;
                border-radius: 12px;
                border: 1px solid #dee2e6;
                padding: 15px;
                margin: 10px;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("📁 Archivos de Datos Cargados (SEVs)")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Información
        info_label = QLabel("Gestiona los archivos de datos de SEV cargados en memoria")
        info_label.setObjectName("info")
        info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(info_label)
        
        # Frame contenedor
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Lista de archivos cargados
        list_label = QLabel("📄 Lista de archivos:")
        list_label.setStyleSheet("color: #495057; font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        content_layout.addWidget(list_label)
        
        self.file_list = QListWidget()
        self.file_list.setAlternatingRowColors(True)
        self.update_file_list()
        content_layout.addWidget(self.file_list)
        
        main_layout.addWidget(content_frame)
        
        # Botones de acción
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(20, 10, 20, 10)
        
        # Botón de cargar archivo
        load_button = QPushButton("📥 Cargar Seleccionado")
        load_button.clicked.connect(self.load_selected_file)
        load_button.setToolTip("Cargar el archivo seleccionado en la interfaz principal")
        button_layout.addWidget(load_button)
        
        # Botón de eliminar archivo
        delete_button = QPushButton("🗑️ Eliminar Seleccionado")
        delete_button.setObjectName("delete_button")
        delete_button.clicked.connect(self.delete_selected_file)
        delete_button.setToolTip("Eliminar el archivo seleccionado de la memoria")
        button_layout.addWidget(delete_button)
        
        # Botón de cerrar
        close_button = QPushButton("✕ Cerrar")
        close_button.setObjectName("close_button")
        close_button.clicked.connect(self.close)
        close_button.setToolTip("Cerrar esta ventana")
        button_layout.addWidget(close_button)
        
        main_layout.addWidget(button_frame)
        self.setLayout(main_layout)
    
    def update_file_list(self):
        """Actualizar la lista de archivos cargados."""
        self.file_list.clear()
        for file in self.parent.loaded_data_files:
            self.file_list.addItem(file)
    
    def load_selected_file(self):
        """Cargar el archivo seleccionado de la lista."""
        selected_item = self.file_list.currentItem()
        if selected_item:
            file_name = selected_item.text()
            self.parent.load_data_from_memory(file_name)
            self.parent.eda_output.append(f"Archivo '{file_name}' cargado.")
        else:
            QMessageBox.warning(self, 'Cargar Archivo', "Por favor, selecciona un archivo para cargar.")
    
    def delete_selected_file(self):
        """Eliminar el archivo seleccionado de la lista."""
        selected_item = self.file_list.currentItem()
        if selected_item:
            file_name = selected_item.text()
            reply = QMessageBox.question(self, 'Eliminar Archivo',
                                         f"¿Estás seguro de que deseas eliminar el archivo '{file_name}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.parent.loaded_data_files[file_name]
                self.update_file_list()
                self.parent.eda_output.append(f"Archivo '{file_name}' eliminado.")
        else:
            QMessageBox.warning(self, 'Eliminar Archivo', "Por favor, selecciona un archivo para eliminar.")