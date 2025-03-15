from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox, QInputDialog

class LoadedInvertedModelsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modelos Invertidos Cargados")
        self.setGeometry(100, 100, 400, 300)
        
        self.parent = parent
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("<h1>Modelos Invertidos Cargados</h1>")
        layout.addWidget(title)
        
        # Lista de archivos cargados
        self.file_list = QListWidget()
        self.update_file_list()
        layout.addWidget(self.file_list)
        
        # Botón de ver/editar modelo
        edit_button = QPushButton("Ver/Editar Modelo Seleccionado")
        edit_button.clicked.connect(self.edit_selected_model)
        layout.addWidget(edit_button)
        
        # Botón de eliminar archivo
        delete_button = QPushButton("Eliminar Modelo Seleccionado")
        delete_button.clicked.connect(self.delete_selected_file)
        layout.addWidget(delete_button)
        
        # Botón de cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
    
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