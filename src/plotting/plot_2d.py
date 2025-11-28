"""
Módulo de Visualización 2D para VESPY
=====================================

Generación de perfiles 2D de resistividad.

Autor: Jose Maria Garcia Marquez
Email: josemariagarciamarquez2.72@gmail.com
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


def generate_2d_plot(models, title="Perfil de Resistividad 2D"):
    """
    Generar gráfico 2D de resistividad a partir de modelos invertidos.
    
    Args:
        models: Lista de diccionarios con modelos invertidos
                Cada modelo debe tener: 'x_position', 'depths', 'resistivity', 
                'sev_number', 'has_smooth', 'depths_smooth', 'resistivity_smooth'
        title: Título del gráfico
    
    Returns:
        Figure y Axes de matplotlib
    """
    if not models or len(models) == 0:
        raise ValueError("No hay modelos para graficar")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Extraer datos para interpolación
    x_coords = []
    z_coords = []
    resistivities = []
    
    for model in models:
        x = model['x_position']
        
        # Usar modelo suavizado si está disponible
        if model.get('has_smooth', False):
            depths = model['depths_smooth']
            rho = model['resistivity_smooth']
        else:
            depths = model['depths']
            rho = model['resistivity']
        
        # Agregar puntos para interpolación
        for i in range(len(rho)):
            if i < len(depths) - 1:
                # Centro de la capa
                z_center = (depths[i] + depths[i+1]) / 2
            else:
                # Última capa
                z_center = depths[i] + (depths[i] - depths[i-1]) / 2
            
            x_coords.append(x)
            z_coords.append(z_center)
            resistivities.append(rho[i])
    
    x_coords = np.array(x_coords)
    z_coords = np.array(z_coords)
    resistivities = np.array(resistivities)
    
    # Crear grilla para interpolación
    x_min, x_max = x_coords.min(), x_coords.max()
    z_min, z_max = 0, z_coords.max()
    
    # Expandir límites un poco
    x_range = x_max - x_min
    x_min -= x_range * 0.1
    x_max += x_range * 0.1
    z_max *= 1.1
    
    grid_x, grid_z = np.meshgrid(
        np.linspace(x_min, x_max, 200),
        np.linspace(z_min, z_max, 100)
    )
    
    # Interpolar
    grid_rho = griddata(
        (x_coords, z_coords),
        resistivities,
        (grid_x, grid_z),
        method='linear',
        fill_value=np.nan
    )
    
    # Graficar
    levels = np.logspace(np.log10(resistivities.min()), np.log10(resistivities.max()), 20)
    
    contourf = ax.contourf(grid_x, grid_z, grid_rho, 
                           levels=levels, cmap='jet', 
                           norm=plt.matplotlib.colors.LogNorm())
    
    # Agregar etiquetas de SEV
    for model in models:
        x = model['x_position']
        sev_num = model.get('sev_number', '?')
        ax.text(x, z_min - z_max*0.05, f'SEV-{sev_num}', 
               rotation=90, ha='center', va='top',
               fontsize=10, fontweight='bold',
               color='white',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
    
    # Colorbar
    cbar = plt.colorbar(contourf, ax=ax, label='Resistividad (Ω·m)')
    
    # Configuración
    ax.set_xlabel('Posición (m)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Profundidad (m)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    return fig, ax


def plot_single_sev(ax, ab2, rhoa, response=None, title="Curva de Resistividad Aparente"):
    """
    Graficar curva de resistividad aparente de un SEV.
    
    Args:
        ax: Axes de matplotlib
        ab2: Array de espaciamientos AB/2
        rhoa: Array de resistividades aparentes observadas
        response: Array de resistividades calculadas (opcional)
        title: Título del gráfico
    """
    ax.clear()
    
    # Datos observados
    ax.loglog(ab2, rhoa, 'o-', color='C0', label='Observados', 
             markersize=8, linewidth=2)
    
    # Datos calculados (si existen)
    if response is not None:
        ax.loglog(ab2, response, 's-', color='C1', label='Calculados',
                 markersize=6, linewidth=2, alpha=0.8)
    
    ax.set_xlabel("AB/2 (m)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Resistividad aparente (Ω·m)", fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, which='both', ls='--', alpha=0.3)


def plot_inversion_model(ax, depths, resistivities, title="Modelo de Capas 1D"):
    """
    Graficar modelo de resistividad por capas.
    
    Args:
        ax: Axes de matplotlib
        depths: Array de profundidades de capas
        resistivities: Array de resistividades por capa
        title: Título del gráfico
    """
    ax.clear()
    
    # Crear escalera de resistividad vs profundidad
    for i, rho in enumerate(resistivities):
        if i < len(depths) - 1:
            z_top = depths[i]
            z_bottom = depths[i + 1]
        else:
            z_top = depths[i]
            z_bottom = depths[i] * 1.5  # Extender última capa
        
        ax.barh(i, rho, height=0.8, left=0, 
               color=f'C{i % 10}', alpha=0.7, edgecolor='black')
    
    ax.set_ylabel("Capa", fontsize=12, fontweight='bold')
    ax.set_xlabel("Resistividad (Ω·m)", fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.grid(True, alpha=0.3)
