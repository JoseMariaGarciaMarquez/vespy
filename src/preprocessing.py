import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from PyQt5.QtWidgets import QFileDialog

class Preprocessing:
    def __init__(self, parent):
        self.parent = parent

    def realizar_empalme(self):
        """Generar el empalme y almacenarlo internamente."""
        if self.parent.data is not None:
            # Generar el empalme para 'pa (Ω*m)'
            empalme_data = self.parent.data.groupby('AB/2')['pa (Ω*m)'].mean().reset_index()
            
            # Ajustar 'MN/2' para que coincida con el empalme de 'AB/2'
            empalme_data['MN/2'] = self.parent.data.groupby('AB/2')['MN/2'].first().values
            
            self.parent.empalme_data = empalme_data
            self.parent.plot_data(empalme=True)

    def apply_filter(self):
        """Aplicar el filtro de suavizado seleccionado a los datos."""
        if self.parent.data is not None:
            señal = self.parent.data['pa (Ω*m)'].values
            n_ventana = self.parent.window_size_spin.value()

            if self.parent.filter_combo.currentText() == "Media Móvil":
                self.parent.smoothed_data = np.convolve(señal, np.ones(n_ventana) / n_ventana, mode='same')
            elif self.parent.filter_combo.currentText() == "Savitzky-Golay":
                self.parent.smoothed_data = savgol_filter(señal, window_length=n_ventana * 2 + 1, polyorder=2)
            elif self.parent.filter_combo.currentText() == "Exponencial":
                self.parent.smoothed_data = pd.Series(señal).ewm(span=n_ventana, adjust=False).mean().values
            
            self.parent.plot_data(smoothed=True)
            self.parent.analyze_data()

    def save_filtered_data(self):
        """Guardar los datos filtrados en un archivo Excel."""
        if hasattr(self.parent, 'smoothed_data') and self.parent.smoothed_data is not None:
            # Crear un DataFrame con los datos filtrados
            filtered_df = self.parent.data.copy()
            filtered_df['pa (Ω*m)'] = self.parent.smoothed_data

            # Abrir un diálogo para seleccionar la ubicación y el nombre del archivo
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self.parent, "Guardar Archivo Filtrado", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
            if file_path:
                # Guardar el DataFrame en un archivo Excel
                filtered_df.to_excel(file_path, index=False)
                self.parent.eda_output.append(f"Archivo filtrado guardado en: {file_path}")
        else:
            self.parent.eda_output.append("No hay datos filtrados disponibles para guardar.")