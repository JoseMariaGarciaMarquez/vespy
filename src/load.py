import os
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QInputDialog
import odf 

class DataLoader:
    def __init__(self, parent):
        self.parent = parent

    def load_excel(self, file_path):
        """Cargar datos desde un archivo Excel."""
        return pd.read_excel(file_path)

    def load_csv(self, file_path):
        """Cargar datos desde un archivo CSV."""
        return pd.read_csv(file_path)

    def load_libreoffice(self, file_path):
        """Cargar datos desde un archivo LibreOffice (ODS)."""
        try:
            return pd.read_excel(file_path, engine='odf')
        except ImportError:
            self.parent.eda_output.append("Error: Falta la dependencia 'odfpy'. Use pip o conda para instalar 'odfpy'.")
            return None

    def load_data(self):
        """Cargar datos desde un archivo y mostrar la curva de resistividad."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self.parent, "Cargar archivo", "", "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;LibreOffice Files (*.ods)", options=options)
        
        if file_path:
            # Determinar el tipo de archivo y cargar los datos
            if file_path.endswith(('.xlsx', '.xls')):
                self.parent.data = self.load_excel(file_path)
            elif file_path.endswith('.csv'):
                self.parent.data = self.load_csv(file_path)
            elif file_path.endswith('.ods'):
                self.parent.data = self.load_libreoffice(file_path)
                if self.parent.data is None:
                    return
            else:
                self.parent.eda_output.append("Error: Formato de archivo no soportado.")
                return

            self.parent.data.columns = self.parent.data.columns.str.strip()  # Quita espacios en los nombres de columnas
            self.parent.data = self.parent.data.dropna()  # Eliminar filas con valores NaN
            
            # Convertir todas las columnas a formato numérico si es posible
            self.parent.data = self.parent.data.apply(pd.to_numeric, errors='coerce')

            # Verificar que los encabezados sean correctos
            required_columns = ['AB/2', 'MN/2', 'K', 'PN', 'PI', 'I (Ma)', '∆V (Mv)', 'pa (Ω*m)']
            missing_columns = [col for col in required_columns if col not in self.parent.data.columns]
            if missing_columns:
                self.assign_columns(missing_columns)
            
            # Extraer el nombre del archivo para las pestañas
            self.parent.current_file = os.path.splitext(os.path.basename(file_path))[0]
            self.parent.table_tabs.setTabText(0, f"{self.parent.current_file}-datos")
            
            # Llenar la tabla de datos en la interfaz
            self.parent.display_data_table()
            
            # Mostrar la curva automáticamente después de cargar los datos
            self.parent.plot_data()

            # Añadir el nombre del archivo a la lista de archivos cargados
            self.parent.loaded_files.append(self.parent.current_file)


    def load_inverted_models(self):
        """Cargar modelos invertidos desde archivos Excel, CSV o LibreOffice (ODS)."""
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self.parent, "Cargar Modelos Invertidos", "", "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;LibreOffice Files (*.ods)", options=options)
        if not files:
            return

        for file in files:
            if file.endswith('.xlsx') or file.endswith('.xls'):
                df = self.load_excel(file)
            elif file.endswith('.csv'):
                df = self.load_csv(file)
            elif file.endswith('.ods'):
                df = self.load_libreoffice(file)
                if df is None:
                    continue
            else:
                self.parent.eda_output.append(f"Formato de archivo no soportado: {file}")
                continue

            # Verificar que el archivo tenga las columnas necesarias
            if not {'Espesor (m)', 'Profundidad (m)', 'Resistividad (Ω*m)'}.issubset(df.columns):
                self.parent.eda_output.append(f"Archivo inválido: {file}")
                continue

            # Convertir los datos del archivo en el formato adecuado
            thickness = df['Espesor (m)'].values
            depths = df['Profundidad (m)'].values
            resistivity = df['Resistividad (Ω*m)'].values

            # Calcular las profundidades acumuladas
            cumulative_depths = np.cumsum(thickness)

            # Guardar el modelo cargado usando save_model
            self.parent.depths = cumulative_depths
            self.parent.resistivity = resistivity
            self.parent.save_model()

            # Extraer el nombre del archivo y añadirlo a la lista de archivos cargados
            file_name = os.path.splitext(os.path.basename(file))[0]
            self.parent.loaded_files.append(file_name)
            self.parent.eda_output.append(f"Modelo cargado desde: {file}")

    def assign_columns(self, missing_columns):
        """Asignar columnas faltantes a los encabezados requeridos."""
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Asignar Columnas")
        layout = QVBoxLayout()

        combo_boxes = {}
        for col in missing_columns:
            label = QLabel(f"Seleccione la columna para {col}:")
            combo_box = QComboBox()
            combo_box.addItems(self.parent.data.columns)
            layout.addWidget(label)
            layout.addWidget(combo_box)
            combo_boxes[col] = combo_box

        def on_accept():
            for col, combo_box in combo_boxes.items():
                selected_column = combo_box.currentText()
                self.parent.data[col] = self.parent.data[selected_column]
            dialog.accept()

        accept_button = QPushButton("Aceptar")
        accept_button.clicked.connect(on_accept)
        layout.addWidget(accept_button)

        dialog.setLayout(layout)
        dialog.exec_()