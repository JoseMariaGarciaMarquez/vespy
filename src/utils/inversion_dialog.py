"""
Diálogo de Configuración de Inversión
====================================

Interfaz para configurar y ejecutar inversión de datos SEV

Autor: VESPY Team
Fecha: 2025
"""

import pandas as pd
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton,
    QLabel, QSpinBox, QDoubleSpinBox, QComboBox, QProgressBar,
    QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class InversionWorker(QThread):
    """Worker thread para ejecutar inversión sin bloquear GUI"""
    
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, data, num_layers, method, lam, lam_factor):
        super().__init__()
        self.data = data
        self.num_layers = num_layers
        self.method = method
        self.lam = lam
        self.lam_factor = lam_factor
    
    def run(self):
        """Ejecutar inversión en thread separado"""
        try:
            from inversion.inversion import VESInverter
            
            self.progress.emit(20)
            inverter = VESInverter()
            
            self.progress.emit(40)
            result = inverter.invert(
                self.data, 
                num_layers=self.num_layers,
                lam=self.lam,
                lam_factor=self.lam_factor
            )
            
            self.progress.emit(100)
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))

class InversionDialog(QDialog):
    """Diálogo para configurar y ejecutar inversión"""
    
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.result = None
        self.worker = None
        self.init_ui()
    
    def init_ui(self):
        """Inicializar interfaz"""
        self.setWindowTitle("Configuración de Inversión")
        self.setGeometry(150, 150, 500, 400)
        
        layout = QVBoxLayout(self)
        
        # Grupo de parámetros
        params_group = QGroupBox("Parámetros de Inversión")
        params_layout = QVBoxLayout(params_group)
        
        # Número de capas
        layers_layout = QHBoxLayout()
        layers_layout.addWidget(QLabel("Número de capas:"))
        self.layers_spin = QSpinBox()
        self.layers_spin.setRange(2, 10)
        self.layers_spin.setValue(3)
        layers_layout.addWidget(self.layers_spin)
        params_layout.addLayout(layers_layout)
        
        # Método
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("Método:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Optimización Simple", "PyGIMLi (si disponible)"])
        method_layout.addWidget(self.method_combo)
        params_layout.addLayout(method_layout)
        
        # Tolerancia RMS
        rms_layout = QHBoxLayout()
        rms_layout.addWidget(QLabel("RMS objetivo:"))
        self.rms_spin = QDoubleSpinBox()
        self.rms_spin.setRange(0.01, 10.0)
        self.rms_spin.setValue(1.0)
        self.rms_spin.setSuffix(" %")
        rms_layout.addWidget(self.rms_spin)
        params_layout.addLayout(rms_layout)
        
        # Máximo de iteraciones
        iter_layout = QHBoxLayout()
        iter_layout.addWidget(QLabel("Máx. iteraciones:"))
        self.iter_spin = QSpinBox()
        self.iter_spin.setRange(10, 1000)
        self.iter_spin.setValue(100)
        iter_layout.addWidget(self.iter_spin)
        params_layout.addLayout(iter_layout)
        
        # Lambda (regularización)
        lambda_layout = QHBoxLayout()
        lambda_layout.addWidget(QLabel("Lambda (λ):"))
        self.lambda_spin = QDoubleSpinBox()
        self.lambda_spin.setRange(0.1, 100.0)
        self.lambda_spin.setValue(20.0)
        self.lambda_spin.setDecimals(1)
        self.lambda_spin.setToolTip("Parámetro de regularización PyGIMLi (mayor = modelo más suave)")
        lambda_layout.addWidget(self.lambda_spin)
        params_layout.addLayout(lambda_layout)
        
        # Factor Lambda
        lam_factor_layout = QHBoxLayout()
        lam_factor_layout.addWidget(QLabel("Factor Lambda:"))
        self.lam_factor_spin = QDoubleSpinBox()
        self.lam_factor_spin.setRange(0.1, 1.0)
        self.lam_factor_spin.setValue(0.8)
        self.lam_factor_spin.setSingleStep(0.05)
        self.lam_factor_spin.setDecimals(2)
        self.lam_factor_spin.setToolTip("Factor de decaimiento de lambda por iteración")
        lam_factor_layout.addWidget(self.lam_factor_spin)
        params_layout.addLayout(lam_factor_layout)
        
        layout.addWidget(params_group)
        
        # Información de datos
        info_group = QGroupBox("Información de Datos")
        info_layout = QVBoxLayout(info_group)
        
        info_text = f"""
        Puntos de datos: {len(self.data)}
        Rango AB/2: {self.data.iloc[:, 0].min():.1f} - {self.data.iloc[:, 0].max():.1f} m
        Rango resistividad: {self.data.iloc[:, 1].min():.1f} - {self.data.iloc[:, 1].max():.1f} Ω·m
        """
        info_label = QLabel(info_text)
        info_layout.addWidget(info_label)
        
        layout.addWidget(info_group)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Log de salida
        log_group = QGroupBox("Salida")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_group)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.run_btn = QPushButton("▶️ Ejecutar Inversión")
        self.run_btn.clicked.connect(self.run_inversion)
        button_layout.addWidget(self.run_btn)
        
        self.accept_btn = QPushButton("✅ Aceptar")
        self.accept_btn.clicked.connect(self.accept)
        self.accept_btn.setEnabled(False)
        button_layout.addWidget(self.accept_btn)
        
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def run_inversion(self):
        """Ejecutar inversión"""
        try:
            self.log_text.clear()
            self.log("Iniciando inversión...")
            self.log(f"Parámetros: λ={self.lambda_spin.value()}, factor={self.lam_factor_spin.value()}")
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.run_btn.setEnabled(False)
            
            # Crear y ejecutar worker
            self.worker = InversionWorker(
                self.data, 
                self.layers_spin.value(),
                self.method_combo.currentText(),
                self.lambda_spin.value(),
                self.lam_factor_spin.value()
            )
            self.worker.finished.connect(self.on_inversion_finished)
            self.worker.error.connect(self.on_inversion_error)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.start()
            
        except Exception as e:
            self.on_inversion_error(str(e))
    
    def on_inversion_finished(self, result):
        """Callback cuando la inversión termina"""
        self.result = result
        self.log(f"\\n✅ Inversión completada")
        self.log(f"Método: {result.get('method', 'N/A')}")
        self.log(f"RMS Error: {result.get('rms_error', 0):.4f}")
        self.log(f"\\nResistividades (Ω·m):")
        for i, rho in enumerate(result.get('resistivities', [])):
            self.log(f"  Capa {i+1}: {rho:.2f}")
        self.log(f"\\nEspesores (m):")
        for i, thick in enumerate(result.get('thicknesses', [])[:-1]):
            self.log(f"  Capa {i+1}: {thick:.2f}")
        self.log(f"  Capa {len(result.get('thicknesses', []))}: ∞")
        
        self.progress_bar.setVisible(False)
        self.run_btn.setEnabled(True)
        self.accept_btn.setEnabled(True)
        
        QMessageBox.information(self, "Éxito", 
            f"Inversión completada\\nRMS: {result.get('rms_error', 0):.4f}")
    
    def on_inversion_error(self, error_msg):
        """Callback cuando hay error"""
        self.log(f"\\n❌ Error: {error_msg}")
        self.progress_bar.setVisible(False)
        self.run_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Error en inversión:\\n{error_msg}")
    
    def log(self, message):
        """Agregar mensaje al log"""
        self.log_text.append(message)
    
    def get_result(self):
        """Obtener resultado de inversión"""
        return self.result

if __name__ == "__main__":
    import sys
    import numpy as np
    from PyQt5.QtWidgets import QApplication
    
    # Crear datos de prueba
    ab2 = np.logspace(0, 2, 20)
    rho = 100 * (1 + 0.5 * np.sin(np.log10(ab2) * 2))
    data = pd.DataFrame({'AB2': ab2, 'Resistividad': rho})
    
    app = QApplication(sys.argv)
    dialog = InversionDialog(data)
    dialog.show()
    sys.exit(app.exec_())