"""
Módulo de Suavizado para VESPY
==============================

Funciones para suavizado de curvas de resistividad.

Autor: Jose Maria Garcia Marquez
Email: josemariagarciamarquez2.72@gmail.com
"""

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter


def apply_smoothing(data, ab2_col, rhoa_col, method='moving_average', window_size=3, poly_order=2):
    """
    Aplicar suavizado a la curva de resistividad.
    
    Args:
        data: DataFrame con los datos
        ab2_col: Nombre de la columna AB/2
        rhoa_col: Nombre de la columna de resistividad
        method: Método de suavizado ('moving_average', 'savgol', 'exponential')
        window_size: Tamaño de ventana para suavizado
        poly_order: Orden polinomial (para Savitzky-Golay)
    
    Returns:
        DataFrame con datos suavizados
    """
    try:
        # Extraer datos
        ab2 = pd.to_numeric(data[ab2_col], errors='coerce')
        rhoa = pd.to_numeric(data[rhoa_col], errors='coerce')
        
        # Eliminar NaN
        valid = ~(ab2.isna() | rhoa.isna())
        ab2 = ab2[valid].values
        rhoa = rhoa[valid].values
        
        # Ordenar por AB/2
        sort_idx = np.argsort(ab2)
        ab2 = ab2[sort_idx]
        rhoa = rhoa[sort_idx]
        
        # Aplicar suavizado
        if method == 'moving_average':
            smoothed = moving_average(rhoa, window_size)
        elif method == 'savgol':
            if len(rhoa) < window_size:
                window_size = len(rhoa) if len(rhoa) % 2 == 1 else len(rhoa) - 1
            if window_size < poly_order + 2:
                poly_order = window_size - 2 if window_size > 2 else 1
            smoothed = savgol_filter(rhoa, window_size, poly_order)
        elif method == 'exponential':
            smoothed = exponential_smoothing(rhoa, alpha=2.0/(window_size + 1))
        else:
            smoothed = rhoa
        
        result = pd.DataFrame({
            ab2_col: ab2,
            rhoa_col: smoothed
        })
        
        return result
        
    except Exception as e:
        raise Exception(f"Error en suavizado: {str(e)}")


def moving_average(data, window_size):
    """
    Suavizado por media móvil.
    
    Args:
        data: Array de datos
        window_size: Tamaño de ventana
    
    Returns:
        Array suavizado
    """
    if window_size < 1:
        return data
    
    result = np.zeros_like(data)
    half_window = window_size // 2
    
    for i in range(len(data)):
        start = max(0, i - half_window)
        end = min(len(data), i + half_window + 1)
        result[i] = np.mean(data[start:end])
    
    return result


def exponential_smoothing(data, alpha=0.3):
    """
    Suavizado exponencial.
    
    Args:
        data: Array de datos
        alpha: Factor de suavizado (0-1)
    
    Returns:
        Array suavizado
    """
    result = np.zeros_like(data)
    result[0] = data[0]
    
    for i in range(1, len(data)):
        result[i] = alpha * data[i] + (1 - alpha) * result[i-1]
    
    return result


def remove_outliers(ab2, rhoa, threshold=3.0):
    """
    Eliminar outliers de la curva de resistividad.
    
    Args:
        ab2: Array de espaciamientos
        rhoa: Array de resistividades
        threshold: Umbral en desviaciones estándar
    
    Returns:
        Tupla (ab2_clean, rhoa_clean)
    """
    log_rhoa = np.log10(rhoa)
    
    mean = np.mean(log_rhoa)
    std = np.std(log_rhoa)
    
    # Identificar outliers
    z_scores = np.abs((log_rhoa - mean) / std)
    mask = z_scores < threshold
    
    return ab2[mask], rhoa[mask]
