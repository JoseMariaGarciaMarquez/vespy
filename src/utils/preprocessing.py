"""
Módulo de Preprocesamiento para VESPY
=====================================

Funciones de preprocesamiento:
- Empalme de datos (merge/stitch)
- Suavizado (smoothing)
- Filtrado de outliers
- Interpolación

Autor: VESPY Team
Fecha: 2025
"""

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton,
    QLabel, QSpinBox, QDoubleSpinBox, QComboBox, QTableWidget,
    QTableWidgetItem, QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PreprocessingDialog(QDialog):
    """Diálogo para preprocesamiento de datos"""
    
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.original_data = data.copy()
        self.processed_data = data.copy()
        self.init_ui()
    
    def init_ui(self):
        """Inicializar interfaz"""
        self.setWindowTitle("Preprocesamiento de Datos")
        self.setGeometry(100, 100, 900, 600)
        
        layout = QVBoxLayout(self)
        
        # Panel de controles
        controls_layout = QHBoxLayout()
        
        # Grupo de suavizado
        smooth_group = QGroupBox("Suavizado")
        smooth_layout = QVBoxLayout(smooth_group)
        
        self.smooth_check = QCheckBox("Aplicar suavizado")
        smooth_layout.addWidget(self.smooth_check)
        
        smooth_layout.addWidget(QLabel("Ventana:"))
        self.window_spin = QSpinBox()
        self.window_spin.setRange(3, 15)
        self.window_spin.setValue(5)
        self.window_spin.setSingleStep(2)  # Solo impares
        smooth_layout.addWidget(self.window_spin)
        
        smooth_layout.addWidget(QLabel("Orden polinomial:"))
        self.order_spin = QSpinBox()
        self.order_spin.setRange(1, 5)
        self.order_spin.setValue(2)
        smooth_layout.addWidget(self.order_spin)
        
        controls_layout.addWidget(smooth_group)
        
        # Grupo de empalme
        merge_group = QGroupBox("Empalme")
        merge_layout = QVBoxLayout(merge_group)
        
        self.merge_check = QCheckBox("Aplicar empalme automático")
        merge_layout.addWidget(self.merge_check)
        
        merge_layout.addWidget(QLabel("Umbral de cambio (%):"))
        self.threshold_spin = QDoubleSpinBox()
        self.threshold_spin.setRange(10, 100)
        self.threshold_spin.setValue(30)
        self.threshold_spin.setSuffix(" %")
        merge_layout.addWidget(self.threshold_spin)
        
        controls_layout.addWidget(merge_group)
        
        # Grupo de filtrado
        filter_group = QGroupBox("Filtrado")
        filter_layout = QVBoxLayout(filter_group)
        
        self.outlier_check = QCheckBox("Eliminar outliers")
        filter_layout.addWidget(self.outlier_check)
        
        filter_layout.addWidget(QLabel("Desviaciones estándar:"))
        self.std_spin = QDoubleSpinBox()
        self.std_spin.setRange(1, 5)
        self.std_spin.setValue(3)
        filter_layout.addWidget(self.std_spin)
        
        controls_layout.addWidget(filter_group)
        
        layout.addLayout(controls_layout)
        
        # Gráfico de comparación
        plot_group = QGroupBox("Vista Previa")
        plot_layout = QVBoxLayout(plot_group)
        
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        plot_layout.addWidget(self.canvas)
        
        layout.addWidget(plot_group)
        
        # Botones
        button_layout = QHBoxLayout()
        
        preview_btn = QPushButton("🔍 Vista Previa")
        preview_btn.clicked.connect(self.preview_processing)
        button_layout.addWidget(preview_btn)
        
        apply_btn = QPushButton("✅ Aplicar")
        apply_btn.clicked.connect(self.accept)
        button_layout.addWidget(apply_btn)
        
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Mostrar datos iniciales
        self.plot_data()
    
    def preview_processing(self):
        """Vista previa del procesamiento"""
        try:
            self.processed_data = self.original_data.copy()
            
            # Aplicar empalme si está activado
            if self.merge_check.isChecked():
                self.processed_data = apply_stitching(
                    self.processed_data, 
                    threshold=self.threshold_spin.value()
                )
            
            # Aplicar filtrado de outliers
            if self.outlier_check.isChecked():
                self.processed_data = remove_outliers(
                    self.processed_data,
                    std_dev=self.std_spin.value()
                )
            
            # Aplicar suavizado
            if self.smooth_check.isChecked():
                self.processed_data = smooth_data(
                    self.processed_data,
                    window=self.window_spin.value(),
                    order=self.order_spin.value()
                )
            
            self.plot_data()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en procesamiento: {str(e)}")
    
    def plot_data(self):
        """Graficar datos originales y procesados"""
        self.ax.clear()
        
        try:
            # Obtener columnas
            ab2_col = self.original_data.columns[0]
            rho_col = self.original_data.columns[1]
            
            ab2_orig = pd.to_numeric(self.original_data[ab2_col], errors='coerce')
            rho_orig = pd.to_numeric(self.original_data[rho_col], errors='coerce')
            
            ab2_proc = pd.to_numeric(self.processed_data[ab2_col], errors='coerce')
            rho_proc = pd.to_numeric(self.processed_data[rho_col], errors='coerce')
            
            # Eliminar NaN
            valid_orig = ~(ab2_orig.isna() | rho_orig.isna())
            valid_proc = ~(ab2_proc.isna() | rho_proc.isna())
            
            # Graficar
            self.ax.loglog(ab2_orig[valid_orig], rho_orig[valid_orig], 
                          'o', alpha=0.5, label='Original', markersize=6)
            self.ax.loglog(ab2_proc[valid_proc], rho_proc[valid_proc], 
                          's-', label='Procesado', markersize=5, linewidth=2)
            
            self.ax.set_xlabel('AB/2 (m)')
            self.ax.set_ylabel('Resistividad (Ω·m)')
            self.ax.legend()
            self.ax.grid(True, alpha=0.3)
            self.canvas.draw()
            
        except Exception as e:
            self.ax.text(0.5, 0.5, f'Error: {str(e)}',
                        transform=self.ax.transAxes, ha='center')
            self.canvas.draw()
    
    def get_processed_data(self):
        """Obtener datos procesados"""
        return self.processed_data

def smooth_data(data, window=5, order=2):
    """
    Suavizar datos usando filtro Savitzky-Golay
    
    Args:
        data: DataFrame con datos
        window: Tamaño de ventana (debe ser impar)
        order: Orden del polinomio
    
    Returns:
        DataFrame con datos suavizados
    """
    result = data.copy()
    
    try:
        # Asegurar ventana impar
        if window % 2 == 0:
            window += 1
        
        # Suavizar segunda columna (resistividad)
        rho_col = result.columns[1]
        rho = pd.to_numeric(result[rho_col], errors='coerce')
        
        # Eliminar NaN temporalmente
        valid = ~rho.isna()
        rho_valid = rho[valid].values
        
        if len(rho_valid) > window:
            # Aplicar filtro
            rho_smooth = savgol_filter(rho_valid, window, order)
            
            # Reemplazar valores
            result.loc[valid, rho_col] = rho_smooth
        
        return result
        
    except Exception as e:
        print(f"Error en suavizado: {e}")
        return data

def apply_stitching(data, threshold=30):
    """
    Aplicar empalme automático para detectar y corregir saltos
    
    Args:
        data: DataFrame con datos
        threshold: Umbral de cambio en porcentaje
    
    Returns:
        DataFrame con datos empalmados
    """
    result = data.copy()
    
    try:
        rho_col = result.columns[1]
        rho = pd.to_numeric(result[rho_col], errors='coerce')
        
        # Detectar saltos grandes
        changes = rho.pct_change().abs() * 100
        jumps = changes > threshold
        
        if jumps.any():
            # Corregir saltos aplicando factor de corrección
            for idx in jumps[jumps].index:
                if idx > 0:
                    correction_factor = rho.iloc[idx-1] / rho.iloc[idx]
                    # Aplicar corrección a partir del salto
                    result.loc[idx:, rho_col] *= correction_factor
        
        return result
        
    except Exception as e:
        print(f"Error en empalme: {e}")
        return data

def remove_outliers(data, std_dev=3):
    """
    Eliminar outliers usando desviación estándar
    
    Args:
        data: DataFrame con datos
        std_dev: Número de desviaciones estándar
    
    Returns:
        DataFrame sin outliers
    """
    result = data.copy()
    
    try:
        rho_col = result.columns[1]
        rho = pd.to_numeric(result[rho_col], errors='coerce')
        
        # Calcular en escala logarítmica
        log_rho = np.log10(rho[~rho.isna()])
        mean = log_rho.mean()
        std = log_rho.std()
        
        # Identificar outliers
        lower_bound = 10 ** (mean - std_dev * std)
        upper_bound = 10 ** (mean + std_dev * std)
        
        # Filtrar
        mask = (rho >= lower_bound) & (rho <= upper_bound)
        result = result[mask].reset_index(drop=True)
        
        return result
        
    except Exception as e:
        print(f"Error eliminando outliers: {e}")
        return data

def interpolate_missing(data, method='linear'):
    """
    Interpolar datos faltantes
    
    Args:
        data: DataFrame con datos
        method: Método de interpolación ('linear', 'cubic', 'quadratic')
    
    Returns:
        DataFrame con datos interpolados
    """
    result = data.copy()
    
    try:
        ab2_col = result.columns[0]
        rho_col = result.columns[1]
        
        ab2 = pd.to_numeric(result[ab2_col], errors='coerce')
        rho = pd.to_numeric(result[rho_col], errors='coerce')
        
        # Identificar datos válidos
        valid = ~(ab2.isna() | rho.isna())
        
        if valid.sum() > 2:  # Necesita al menos 3 puntos
            # Crear interpolador
            f = interp1d(ab2[valid], rho[valid], kind=method, 
                        fill_value='extrapolate')
            
            # Interpolar valores faltantes
            rho_interp = f(ab2)
            result[rho_col] = rho_interp
        
        return result
        
    except Exception as e:
        print(f"Error en interpolación: {e}")
        return data

if __name__ == "__main__":
    # Test
    import sys
    from PyQt5.QtWidgets import QApplication
    
    # Crear datos de prueba
    ab2 = np.logspace(0, 2, 20)
    rho = 100 * (1 + 0.5 * np.sin(np.log10(ab2) * 2))
    rho += np.random.normal(0, 5, len(rho))  # Ruido
    
    data = pd.DataFrame({'AB2': ab2, 'Resistividad': rho})
    
    app = QApplication(sys.argv)
    dialog = PreprocessingDialog(data)
    dialog.show()
    sys.exit(app.exec_())