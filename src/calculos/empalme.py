"""
Módulo de Empalme para VESPY
============================

Funciones para realizar empalme de curvas de resistividad.

Autor: Jose Maria Garcia Marquez
Email: josemariagarciamarquez2.72@gmail.com
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def realizar_empalme(data, ab2_col, rhoa_col):
    """
    Realizar empalme de curvas de resistividad aparente.
    Simple: agrupa por AB/2 y calcula la media.
    
    Args:
        data: DataFrame con los datos
        ab2_col: Nombre de la columna AB/2
        rhoa_col: Nombre de la columna de resistividad aparente
    
    Returns:
        DataFrame con datos empalmados (promediados por AB/2)
    """
    try:
        # Crear copia del DataFrame con solo las columnas necesarias
        df_work = data[[ab2_col, rhoa_col]].copy()
        
        # Convertir a numérico
        df_work[ab2_col] = pd.to_numeric(df_work[ab2_col], errors='coerce')
        df_work[rhoa_col] = pd.to_numeric(df_work[rhoa_col], errors='coerce')
        
        # Eliminar NaN
        df_work = df_work.dropna()
        
        if len(df_work) == 0:
            raise Exception("No hay datos válidos para empalmar")
        
        # Agrupar por AB/2 y promediar resistividad
        # Esto automáticamente une mediciones con el mismo espaciamiento
        result = df_work.groupby(ab2_col)[rhoa_col].mean().reset_index()
        
        # Ordenar por AB/2
        result = result.sort_values(by=ab2_col).reset_index(drop=True)
        
        return result
        
    except Exception as e:
        raise Exception(f"Error en empalme: {str(e)}")


def detectar_segmentos(ab2, rhoa, threshold=2.0):
    """
    Detectar segmentos en una curva de resistividad.
    
    Args:
        ab2: Array de espaciamientos AB/2
        rhoa: Array de resistividades aparentes
        threshold: Umbral para detección de rupturas (en desviaciones estándar)
    
    Returns:
        Lista de tuplas (inicio, fin) de cada segmento
    """
    if len(ab2) < 3:
        return [(0, len(ab2))]
    
    log_rhoa = np.log10(rhoa)
    d_log_rhoa = np.diff(log_rhoa)
    
    std = np.std(d_log_rhoa)
    mean = np.mean(d_log_rhoa)
    
    breakpoints = np.where(np.abs(d_log_rhoa - mean) > threshold * std)[0]
    
    if len(breakpoints) == 0:
        return [(0, len(ab2))]
    
    segments = []
    start = 0
    for bp in breakpoints:
        segments.append((start, bp + 1))
        start = bp + 1
    segments.append((start, len(ab2)))
    
    return segments
