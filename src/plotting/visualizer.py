"""
Módulo de Visualización de Datos para VESPY
===========================================

Funciones para graficar datos de resistividad y análisis.

Autor: Jose Maria Garcia Marquez
Email: josemariagarciamarquez2.72@gmail.com
"""

import numpy as np
import pandas as pd
import seaborn as sns
from scipy.fft import fft, fftfreq


def plot_resistivity_curve(ax, data, empalme_data=None, smoothed_data=None):
    """
    Graficar curva de resistividad aparente.
    
    Args:
        ax: Axes de matplotlib
        data: DataFrame con columnas 'AB/2' y 'pa (Ω*m)'
        empalme_data: DataFrame con datos empalmados (opcional)
        smoothed_data: Array con datos suavizados (opcional)
    """
    ax.clear()
    
    ab2 = data['AB/2'].values
    rhoa = data['pa (Ω*m)'].values
    
    # Curva original
    ax.plot(ab2, rhoa, 'o-', label='Curva Original', 
           color='blue', markersize=5, linewidth=2)
    
    # Empalme
    if empalme_data is not None:
        empalme_ab2 = empalme_data['AB/2'].values
        empalme_rhoa = empalme_data['pa (Ω*m)'].values
        ax.plot(empalme_ab2, empalme_rhoa, 's-', label='Empalme', 
               color='green', markersize=6, linewidth=2)
    
    # Suavizado
    if smoothed_data is not None:
        ax.plot(ab2, smoothed_data, '^-', label='Suavizado', 
               color='red', markersize=5, linewidth=2)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("AB/2 (m)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Resistividad aparente (Ω·m)", fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.set_title("Curva de Resistividad Aparente", fontsize=14, fontweight='bold')
    ax.grid(True, which='both', ls='--', alpha=0.3)


def plot_statistical_analysis(figure, resistivity):
    """
    Crear gráficos de análisis estadístico.
    
    Args:
        figure: Figure de matplotlib
        resistivity: Array de resistividades
    
    Returns:
        dict con estadísticas calculadas
    """
    figure.clear()
    
    # Calcular estadísticas
    mean = np.mean(resistivity)
    std_dev = np.std(resistivity)
    median = np.median(resistivity)
    skewness = pd.Series(resistivity).skew()
    kurtosis = pd.Series(resistivity).kurt()
    
    # Histograma
    ax1 = figure.add_subplot(221)
    sns.histplot(resistivity, bins=20, kde=False, color='blue', ax=ax1)
    ax1.set_title("Histograma de Resistividades", fontweight='bold')
    ax1.set_xlabel("Resistividad (Ω·m)")
    ax1.set_ylabel("Frecuencia")
    
    # Histograma acumulativo
    ax2 = figure.add_subplot(222)
    sns.histplot(resistivity, bins=20, kde=True, cumulative=True, 
                color='green', ax=ax2)
    ax2.set_title("Distribución Acumulativa", fontweight='bold')
    ax2.set_xlabel("Resistividad (Ω·m)")
    ax2.set_ylabel("Frecuencia Acumulada")
    
    # FFT
    n = len(resistivity)
    yf = fft(resistivity)
    xf = fftfreq(n, 1.0)[:n//2]
    magnitudes = 2.0/n * np.abs(yf[:n//2])
    dominant_freq = xf[np.argmax(magnitudes)] if len(magnitudes) > 0 else 0
    
    ax3 = figure.add_subplot(223)
    ax3.plot(xf, magnitudes, color='purple', linewidth=2)
    ax3.set_title("Transformada de Fourier", fontweight='bold')
    ax3.set_xlabel("Frecuencia")
    ax3.set_ylabel("Magnitud")
    ax3.grid(True, alpha=0.3)
    
    # Boxplot
    ax4 = figure.add_subplot(224)
    ax4.boxplot(resistivity, vert=True)
    ax4.set_title("Diagrama de Caja", fontweight='bold')
    ax4.set_ylabel("Resistividad (Ω·m)")
    
    figure.tight_layout()
    
    # Retornar estadísticas
    return {
        'mean': mean,
        'std_dev': std_dev,
        'median': median,
        'skewness': skewness,
        'kurtosis': kurtosis,
        'dominant_freq': dominant_freq
    }
