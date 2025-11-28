"""
Módulo de Gestión de Modelos para VESPY
=======================================

Funciones para guardar y cargar modelos invertidos.

Autor: Jose Maria Garcia Marquez
Email: josemariagarciamarquez2.72@gmail.com
"""

import pickle
import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox


def save_model_to_file(model_data, parent=None):
    """
    Guardar modelo invertido a archivo pickle.
    
    Args:
        model_data: Dict con datos del modelo
        parent: Widget padre para diálogos
    
    Returns:
        bool: True si se guardó exitosamente
    """
    try:
        file_path, _ = QFileDialog.getSaveFileName(
            parent,
            "Guardar Modelo",
            "",
            "Pickle Files (*.pkl);;All Files (*)"
        )
        
        if file_path:
            if not file_path.endswith('.pkl'):
                file_path += '.pkl'
            
            with open(file_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            return True, file_path
        
        return False, None
        
    except Exception as e:
        return False, str(e)


def load_models_from_file(parent=None):
    """
    Cargar modelos invertidos desde archivo pickle.
    
    Args:
        parent: Widget padre para diálogos
    
    Returns:
        list: Lista de modelos cargados o None si hay error
    """
    try:
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Cargar Modelos",
            "",
            "Pickle Files (*.pkl);;All Files (*)"
        )
        
        if file_path:
            with open(file_path, 'rb') as f:
                models = pickle.load(f)
            
            # Asegurar que sea una lista
            if not isinstance(models, list):
                models = [models]
            
            return True, models
        
        return False, None
        
    except Exception as e:
        return False, str(e)


def save_inversion_table_to_csv(thickness, depths, resistivity, filename=None, parent=None):
    """
    Guardar tabla de inversión a CSV.
    
    Args:
        thickness: Array de espesores
        depths: Array de profundidades
        resistivity: Array de resistividades
        filename: Nombre del archivo (opcional)
        parent: Widget padre para diálogos
    
    Returns:
        bool: True si se guardó exitosamente
    """
    import pandas as pd
    
    try:
        if filename is None:
            file_path, _ = QFileDialog.getSaveFileName(
                parent,
                "Guardar Tabla",
                "",
                "CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)"
            )
            if not file_path:
                return False, None
        else:
            file_path = filename
        
        # Crear DataFrame
        data = []
        for i in range(len(resistivity)):
            row = {}
            if i < len(thickness):
                row['Espesor (m)'] = f"{thickness[i]:.2f}"
                row['Profundidad (m)'] = f"{depths[i]:.2f}"
            else:
                row['Espesor (m)'] = "∞"
                row['Profundidad (m)'] = "∞"
            row['Resistividad (Ω*m)'] = f"{resistivity[i]:.2f}"
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # Guardar según extensión
        if file_path.endswith('.csv'):
            df.to_csv(file_path, index=False)
        elif file_path.endswith('.xlsx'):
            df.to_excel(file_path, index=False)
        else:
            file_path += '.csv'
            df.to_csv(file_path, index=False)
        
        return True, file_path
        
    except Exception as e:
        return False, str(e)


def save_curve_to_csv(ab2, rhoa, filename=None, parent=None):
    """
    Guardar curva de resistividad a CSV.
    
    Args:
        ab2: Array de espaciamientos AB/2
        rhoa: Array de resistividades aparentes
        filename: Nombre del archivo (opcional)
        parent: Widget padre para diálogos
    
    Returns:
        bool: True si se guardó exitosamente
    """
    import pandas as pd
    
    try:
        if filename is None:
            file_path, _ = QFileDialog.getSaveFileName(
                parent,
                "Guardar Curva",
                "",
                "CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)"
            )
            if not file_path:
                return False, None
        else:
            file_path = filename
        
        # Crear DataFrame
        df = pd.DataFrame({
            'AB/2 (m)': ab2,
            'Resistividad Aparente (Ω*m)': rhoa
        })
        
        # Guardar según extensión
        if file_path.endswith('.csv'):
            df.to_csv(file_path, index=False)
        elif file_path.endswith('.xlsx'):
            df.to_excel(file_path, index=False)
        else:
            file_path += '.csv'
            df.to_csv(file_path, index=False)
        
        return True, file_path
        
    except Exception as e:
        return False, str(e)
