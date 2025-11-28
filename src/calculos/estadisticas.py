"""
Módulo de Análisis Estadístico para VESPY
=========================================

Funciones para análisis estadístico de datos SEV.

Autor: Jose Maria Garcia Marquez
Email: josemariagarciamarquez2.72@gmail.com
"""

import numpy as np
import pandas as pd
from scipy import stats


def calcular_estadisticas(data, ab2_col, rhoa_col):
    """
    Calcular estadísticas descriptivas de los datos.
    
    Args:
        data: DataFrame con los datos
        ab2_col: Nombre de la columna AB/2
        rhoa_col: Nombre de la columna de resistividad
    
    Returns:
        dict con estadísticas
    """
    try:
        ab2 = pd.to_numeric(data[ab2_col], errors='coerce')
        rhoa = pd.to_numeric(data[rhoa_col], errors='coerce')
        
        valid = ~(ab2.isna() | rhoa.isna())
        ab2 = ab2[valid].values
        rhoa = rhoa[valid].values
        
        estadisticas = {
            'n_puntos': len(rhoa),
            'ab2_min': np.min(ab2),
            'ab2_max': np.max(ab2),
            'ab2_media': np.mean(ab2),
            'rhoa_min': np.min(rhoa),
            'rhoa_max': np.max(rhoa),
            'rhoa_media': np.mean(rhoa),
            'rhoa_mediana': np.median(rhoa),
            'rhoa_std': np.std(rhoa),
            'rhoa_cv': np.std(rhoa) / np.mean(rhoa) * 100,  # Coeficiente de variación
            'log_rhoa_media': np.mean(np.log10(rhoa)),
            'log_rhoa_std': np.std(np.log10(rhoa))
        }
        
        return estadisticas
        
    except Exception as e:
        raise Exception(f"Error calculando estadísticas: {str(e)}")


def detectar_anomalias(rhoa, threshold=3.0):
    """
    Detectar anomalías en la curva de resistividad.
    
    Args:
        rhoa: Array de resistividades
        threshold: Umbral en desviaciones estándar
    
    Returns:
        Array de índices con anomalías
    """
    log_rhoa = np.log10(rhoa)
    z_scores = np.abs(stats.zscore(log_rhoa))
    
    anomalies = np.where(z_scores > threshold)[0]
    
    return anomalies


def calcular_tendencia(ab2, rhoa):
    """
    Calcular tendencia de la curva (regresión lineal en escala log-log).
    
    Args:
        ab2: Array de espaciamientos
        rhoa: Array de resistividades
    
    Returns:
        dict con pendiente, intercepto y R²
    """
    log_ab2 = np.log10(ab2)
    log_rhoa = np.log10(rhoa)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_ab2, log_rhoa)
    
    return {
        'pendiente': slope,
        'intercepto': intercept,
        'r_cuadrado': r_value**2,
        'p_valor': p_value,
        'error_std': std_err
    }


def calcular_rango_investigacion(ab2):
    """
    Estimar rango de investigación en profundidad.
    
    Args:
        ab2: Array de espaciamientos AB/2
    
    Returns:
        dict con profundidades estimadas
    """
    # Regla empírica: profundidad ≈ AB/2 / 3
    prof_min = np.min(ab2) / 3
    prof_max = np.max(ab2) / 3
    
    return {
        'profundidad_min': prof_min,
        'profundidad_max': prof_max,
        'rango': prof_max - prof_min
    }
