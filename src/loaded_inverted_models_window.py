from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QListWidget, QMessageBox, QInputDialog, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class LoadedInvertedModelsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔄 Modelos Invertidos Cargados")
        self.setGeometry(100, 100, 650, 550)
        self.setMinimumSize(550, 450)
        
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
                    stop: 0 #f093fb, stop: 1 #f5576c);
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
                selection-background-color: #f093fb;
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
                background: #fce4ec;
                color: #c2185b;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f093fb, stop: 1 #f5576c);
                color: white;
                font-weight: bold;
            }
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f093fb, stop: 1 #f5576c);
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
                    stop: 0 #e781fc, stop: 1 #e91e63);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #d15cfd, stop: 1 #c2185b);
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
        title = QLabel("🔄 Modelos Invertidos Cargados")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Información
        info_label = QLabel("Gestiona los modelos de inversión cargados en memoria")
        info_label.setObjectName("info")
        info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(info_label)
        
        # Frame contenedor
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Lista de archivos cargados
        list_label = QLabel("📋 Lista de modelos:")
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
        
        # Botón de ver/editar modelo
        edit_button = QPushButton("👁️ Ver/Editar Modelo")
        edit_button.clicked.connect(self.edit_selected_model)
        edit_button.setToolTip("Ver y editar el modelo seleccionado")
        button_layout.addWidget(edit_button)
        
        # Botón de eliminar archivo
        delete_button = QPushButton("🗑️ Eliminar Modelo")
        delete_button.setObjectName("delete_button")
        delete_button.clicked.connect(self.delete_selected_file)
        delete_button.setToolTip("Eliminar el modelo seleccionado de la memoria")
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
        """Actualizar la lista de modelos invertidos cargados."""
        self.file_list.clear()
        for file in self.parent.loaded_inverted_models:
            self.file_list.addItem(file)
    
    def edit_selected_model(self):
        """Ver/Editar el modelo seleccionado de la lista."""
        selected_item = self.file_list.currentItem()
        if selected_item:
            file_name = selected_item.text()
            model = self.parent.loaded_inverted_models[file_name]
            
            # Asegurarse de que las claves existen en el diccionario
            model.setdefault('x_position', 0.0)
            model.setdefault('y_position', 0.0)
            model.setdefault('sev_number', 0)
            model.setdefault('relative_height', 0.0)
            
            # Editar posición X
            x_position, ok = QInputDialog.getDouble(self, "Editar Posición X", "Ingrese la nueva posición X:", model['x_position'])
            if ok:
                model['x_position'] = x_position
            
            # Editar posición Y
            y_position, ok = QInputDialog.getDouble(self, "Editar Posición Y", "Ingrese la nueva posición Y:", model['y_position'])
            if ok:
                model['y_position'] = y_position
            
            # Editar número de SEV
            sev_number, ok = QInputDialog.getInt(self, "Editar Número de SEV", "Ingrese el nuevo número de SEV:", model['sev_number'])
            if ok:
                model['sev_number'] = sev_number
            
            # Editar altura relativa
            relative_height, ok = QInputDialog.getDouble(self, "Editar Altura Relativa", "Ingrese la nueva altura relativa:", model['relative_height'])
            if ok:
                model['relative_height'] = relative_height
            
            self.parent.loaded_inverted_models[file_name] = model
            self.parent.eda_output.append(f"Modelo invertido '{file_name}' actualizado.")
        else:
            QMessageBox.warning(self, 'Editar Modelo', "Por favor, selecciona un modelo para editar.")
    
    def delete_selected_file(self):
        """Eliminar el modelo seleccionado de la lista."""
        selected_item = self.file_list.currentItem()
        if selected_item:
            file_name = selected_item.text()
            reply = QMessageBox.question(self, 'Eliminar Modelo',
                                         f"¿Estás seguro de que deseas eliminar el modelo '{file_name}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.parent.loaded_inverted_models[file_name]
                self.update_file_list()
                self.parent.eda_output.append(f"Modelo invertido '{file_name}' eliminado.")
        else:
            QMessageBox.warning(self, 'Eliminar Modelo', "Por favor, selecciona un modelo para eliminar.")