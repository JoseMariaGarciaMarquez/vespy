"""
Diálogos personalizados para VESPY
==================================

Diálogos para guardar modelos, seleccionar parámetros, etc.

Autor: Jose Maria Garcia Marquez
Email: josemariagarciamarquez2.72@gmail.com
"""

from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QLabel,
    QDoubleSpinBox, QSpinBox, QVBoxLayout, QComboBox,
    QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt


class SaveModelDialog(QDialog):
    """Diálogo para guardar modelo con posición X y número SEV."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guardar Modelo")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        # Posición X
        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(0, 100000)
        self.x_spin.setDecimals(2)
        self.x_spin.setValue(0)
        self.x_spin.setSuffix(" m")
        layout.addRow("Posición X:", self.x_spin)
        
        # Número de SEV
        self.sev_spin = QSpinBox()
        self.sev_spin.setRange(1, 9999)
        self.sev_spin.setValue(1)
        layout.addRow("Número de SEV:", self.sev_spin)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def get_values(self):
        """Obtener valores ingresados."""
        return {
            'x_position': self.x_spin.value(),
            'sev_number': self.sev_spin.value()
        }


class ColumnMappingDialog(QDialog):
    """Diálogo para mapear columnas de datos."""
    
    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mapeo de Columnas")
        self.setModal(True)
        self.columns = columns
        
        main_layout = QVBoxLayout(self)
        
        # Instrucciones
        instructions = QLabel(
            "Seleccione qué columna de su archivo corresponde a cada variable:"
        )
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)
        
        # Formulario
        form_layout = QFormLayout()
        
        # ComboBox para AB/2
        self.ab2_combo = QComboBox()
        self.ab2_combo.addItem("-- No seleccionado --")
        self.ab2_combo.addItems(columns)
        form_layout.addRow("AB/2 (espaciamiento):", self.ab2_combo)
        
        # ComboBox para MN/2
        self.mn2_combo = QComboBox()
        self.mn2_combo.addItem("-- No seleccionado --")
        self.mn2_combo.addItems(columns)
        form_layout.addRow("MN/2 (opcional):", self.mn2_combo)
        
        # ComboBox para Resistividad Aparente
        self.rhoa_combo = QComboBox()
        self.rhoa_combo.addItem("-- No seleccionado --")
        self.rhoa_combo.addItems(columns)
        form_layout.addRow("Resistividad aparente (pa/ρa):", self.rhoa_combo)
        
        main_layout.addLayout(form_layout)
        
        # Auto-detectar
        self._auto_detect()
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)
    
    def _auto_detect(self):
        """Auto-detectar columnas basándose en nombres comunes."""
        for i, col in enumerate(self.columns):
            col_lower = str(col).lower().strip()
            
            # Detectar AB/2
            if 'ab/2' in col_lower or 'ab2' in col_lower or col_lower == 'ab':
                self.ab2_combo.setCurrentIndex(i + 1)
            
            # Detectar MN/2
            if 'mn/2' in col_lower or 'mn2' in col_lower or col_lower == 'mn':
                self.mn2_combo.setCurrentIndex(i + 1)
            
            # Detectar resistividad
            if any(x in col_lower for x in ['pa', 'rhoa', 'ρa', 'resistividad', 'ohm', 'ω']):
                self.rhoa_combo.setCurrentIndex(i + 1)
    
    def get_mapping(self):
        """Obtener mapeo de columnas (formato: {columna_original: columna_destino})."""
        mapping = {}
        
        if self.ab2_combo.currentIndex() > 0:
            original_col = self.columns[self.ab2_combo.currentIndex() - 1]
            mapping[original_col] = 'AB/2'
        
        if self.mn2_combo.currentIndex() > 0:
            original_col = self.columns[self.mn2_combo.currentIndex() - 1]
            mapping[original_col] = 'MN/2'
        
        if self.rhoa_combo.currentIndex() > 0:
            original_col = self.columns[self.rhoa_combo.currentIndex() - 1]
            mapping[original_col] = 'pa (Ω*m)'
        
        return mapping
    
    def validate(self):
        """Validar que al menos AB/2 y resistividad estén seleccionados."""
        if self.ab2_combo.currentIndex() == 0:
            return False, "Debe seleccionar la columna AB/2"
        if self.rhoa_combo.currentIndex() == 0:
            return False, "Debe seleccionar la columna de resistividad aparente"
        return True, ""
    
    def accept(self):
        """Override accept para validar antes de cerrar."""
        valid, msg = self.validate()
        if valid:
            super().accept()
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", msg)


class InversionParametersDialog(QDialog):
    """Diálogo para configurar parámetros de inversión."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Parámetros de Inversión")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        # Número de capas
        self.layers_spin = QSpinBox()
        self.layers_spin.setRange(2, 20)
        self.layers_spin.setValue(5)
        layout.addRow("Número de Capas:", self.layers_spin)
        
        # Lambda
        self.lambda_spin = QSpinBox()
        self.lambda_spin.setRange(1, 1000)
        self.lambda_spin.setValue(20)
        layout.addRow("Lambda (λ):", self.lambda_spin)
        
        # Factor Lambda
        self.lambda_factor_spin = QDoubleSpinBox()
        self.lambda_factor_spin.setRange(0.1, 1.0)
        self.lambda_factor_spin.setSingleStep(0.1)
        self.lambda_factor_spin.setValue(0.8)
        layout.addRow("Factor Lambda:", self.lambda_factor_spin)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def get_parameters(self):
        """Obtener parámetros configurados."""
        return {
            'n_layers': self.layers_spin.value(),
            'lambda': self.lambda_spin.value(),
            'lambda_factor': self.lambda_factor_spin.value()
        }
