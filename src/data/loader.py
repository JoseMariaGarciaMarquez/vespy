"""
Módulo de Carga de Datos para VESPY
===================================

Carga datos de SEV desde diferentes formatos:
- Excel (.xlsx, .xls)
- CSV (.csv)
- Texto (.txt)

Autor: VESPY Team
Fecha: 2025
"""

import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class DataLoader:
    """Cargador de datos SEV"""
    
    def __init__(self):
        self.data = None
        self.file_path = None
    
    def load_file(self, parent=None):
        """
        Cargar archivo de datos SEV
        
        Returns:
            pandas.DataFrame: Datos cargados o None si hay error
        """
        try:
            # Abrir diálogo de archivo
            file_path, _ = QFileDialog.getOpenFileName(
                parent,
                "Cargar Datos SEV",
                "",
                "Excel files (*.xlsx *.xls);;CSV files (*.csv);;Text files (*.txt);;All files (*.*)"
            )
            
            if not file_path:
                return None
            
            self.file_path = file_path
            
            # Cargar según extensión
            if file_path.lower().endswith(('.xlsx', '.xls')):
                self.data = self._load_excel(file_path)
            elif file_path.lower().endswith('.csv'):
                self.data = self._load_csv(file_path)
            elif file_path.lower().endswith('.txt'):
                self.data = self._load_txt(file_path)
            else:
                raise ValueError("Formato de archivo no soportado")
            
            # Validar datos
            self._validate_data()
            
            return self.data
            
        except Exception as e:
            if parent:
                QMessageBox.critical(parent, "Error", f"Error cargando archivo: {str(e)}")
            raise e
    
    def _load_excel(self, file_path):
        """Cargar archivo Excel"""
        try:
            # Intentar cargar primera hoja
            data = pd.read_excel(file_path, sheet_name=0)
            return data
        except Exception as e:
            raise ValueError(f"Error leyendo Excel: {str(e)}")
    
    def _load_csv(self, file_path):
        """Cargar archivo CSV"""
        try:
            # Intentar diferentes separadores
            separators = [',', ';', '\\t', ' ']
            
            for sep in separators:
                try:
                    data = pd.read_csv(file_path, sep=sep)
                    if len(data.columns) > 1:  # Si tiene más de 1 columna, probablemente es correcto
                        return data
                except:
                    continue
            
            # Si no funcionó ningún separador, usar coma por defecto
            data = pd.read_csv(file_path)
            return data
            
        except Exception as e:
            raise ValueError(f"Error leyendo CSV: {str(e)}")
    
    def _load_txt(self, file_path):
        """Cargar archivo de texto"""
        try:
            # Intentar como CSV con diferentes separadores
            separators = ['\\t', ' ', ',', ';']
            
            for sep in separators:
                try:
                    data = pd.read_csv(file_path, sep=sep, header=None)
                    if len(data.columns) >= 2:
                        # Asignar nombres de columna por defecto
                        data.columns = [f'Col_{i+1}' for i in range(len(data.columns))]
                        return data
                except:
                    continue
            
            raise ValueError("No se pudo determinar el formato del archivo de texto")
            
        except Exception as e:
            raise ValueError(f"Error leyendo archivo de texto: {str(e)}")
    
    def _validate_data(self):
        """Validar que los datos sean apropiados para SEV"""
        if self.data is None:
            raise ValueError("No se cargaron datos")
        
        if self.data.empty:
            raise ValueError("El archivo está vacío")
        
        if len(self.data.columns) < 2:
            raise ValueError("Se necesitan al menos 2 columnas (AB/2 y Resistividad)")
        
        # Intentar convertir primeras dos columnas a numérico
        try:
            pd.to_numeric(self.data.iloc[:, 0], errors='coerce')
            pd.to_numeric(self.data.iloc[:, 1], errors='coerce')
        except:
            raise ValueError("Las primeras dos columnas deben ser numéricas")
        
        # Asignar nombres estándar si no los tiene
        if self.data.columns[0] in [0, 'Col_1'] or str(self.data.columns[0]).startswith('Unnamed'):
            self.data.columns = ['AB2'] + [f'Col_{i+2}' for i in range(len(self.data.columns)-1)]
        
        return True
    
    def get_ab2_column(self):
        """Obtener nombre de la columna AB/2"""
        if self.data is None:
            return None
        
        # Buscar columna que contenga AB, distancia, etc.
        for col in self.data.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['ab', 'distancia', 'spacing', 'electrode']):
                return col
        
        # Si no encuentra, usar primera columna
        return self.data.columns[0]
    
    def get_resistivity_column(self):
        """Obtener nombre de la columna de resistividad"""
        if self.data is None:
            return None
        
        # Buscar columna que contenga resistividad, rho, etc.
        for col in self.data.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['rho', 'resistividad', 'resistivity', 'apparent']):
                return col
        
        # Si no encuentra, usar segunda columna
        if len(self.data.columns) > 1:
            return self.data.columns[1]
        
        return None

def load_sample_data():
    """Crear datos de muestra para testing"""
    import numpy as np
    
    # Datos sintéticos de SEV
    ab2 = np.logspace(0, 2, 20)  # 1 a 100 m
    rho = 100 * (1 + 0.5 * np.sin(np.log10(ab2) * 2))  # Resistividad sintética
    
    data = pd.DataFrame({
        'AB2': ab2,
        'Resistividad': rho
    })
    
    return data

if __name__ == "__main__":
    # Test del módulo
    loader = DataLoader()
    sample_data = load_sample_data()
    print("Datos de muestra:")
    print(sample_data.head())
    print(f"Columna AB/2: {loader.get_ab2_column()}")
    print(f"Columna Resistividad: {loader.get_resistivity_column()}")