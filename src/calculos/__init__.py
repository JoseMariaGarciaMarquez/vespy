"""
Paquete de cálculos para VESPY
==============================

Contiene funciones de cálculo y procesamiento de datos SEV.
"""

from .empalme import realizar_empalme, detectar_segmentos
from .suavizado import apply_smoothing, moving_average, exponential_smoothing, remove_outliers
from .estadisticas import calcular_estadisticas, detectar_anomalias, calcular_tendencia, calcular_rango_investigacion

__all__ = [
    'realizar_empalme',
    'detectar_segmentos',
    'apply_smoothing',
    'moving_average',
    'exponential_smoothing',
    'remove_outliers',
    'calcular_estadisticas',
    'detectar_anomalias',
    'calcular_tendencia',
    'calcular_rango_investigacion'
]
