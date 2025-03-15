from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox

class LoadedDataFilesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Archivos de Datos Cargados")
        self.setGeometry(100, 100, 400, 300)
        
        self.parent = parent
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("<h1>Archivos de Datos Cargados</h1>")
        layout.addWidget(title)
        
        # Lista de archivos cargados
        self.file_list = QListWidget()
        self.update_file_list()
        layout.addWidget(self.file_list)
        
        # Botón de cargar archivo
        load_button = QPushButton("Cargar Archivo Seleccionado")
        load_button.clicked.connect(self.load_selected_file)
        layout.addWidget(load_button)
        
        # Botón de eliminar archivo
        delete_button = QPushButton("Eliminar Archivo Seleccionado")
        delete_button.clicked.connect(self.delete_selected_file)
        layout.addWidget(delete_button)
        
        # Botón de cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
    
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