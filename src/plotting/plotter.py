"""
Módulo de Visualización para VESPY
==================================

Maneja todos los gráficos de SEV:
- Curva de resistividad aparente
- Resultado de inversión
- Gráficos comparativos

Autor: VESPY Team
Fecha: 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class VESPlotter:
    """Graficador de datos SEV"""
    
    def __init__(self, ax: Axes):
        """
        Inicializar graficador
        
        Args:
            ax: Axes de matplotlib donde graficar
        """
        self.ax = ax
        self.colors = {
            'data': '#2E86AB',      # Azul para datos
            'model': '#A23B72',     # Rosa para modelo
            'inversion': '#F18F01', # Naranja para inversión
            'grid': '#CCCCCC'       # Gris para grid
        }
    
    def plot_data(self, data: pd.DataFrame):
        """
        Graficar datos de resistividad aparente
        
        Args:
            data: DataFrame con datos SEV
        """
        try:
            print("\\n" + "="*50)
            print("📊 INICIANDO GRÁFICO DE RESISTIVIDADES APARENTES")
            print("="*50)
            
            # Limpiar gráfico
            self.ax.clear()
            
            # Obtener columnas
            ab2_col, rho_col = self._get_columns(data)
            
            print(f"\\n🎯 Columnas seleccionadas:")
            print(f"   AB/2: '{ab2_col}'")
            print(f"   Resistividad: '{rho_col}'")
            
            # Extraer datos
            ab2 = pd.to_numeric(data[ab2_col], errors='coerce')
            rho = pd.to_numeric(data[rho_col], errors='coerce')
            
            print(f"\\n📈 Estadísticas de datos:")
            print(f"   AB/2 - Min: {ab2.min():.2f}, Max: {ab2.max():.2f}")
            print(f"   Rho - Min: {rho.min():.2f}, Max: {rho.max():.2f}")
            
            # Eliminar NaN
            valid_data = ~(ab2.isna() | rho.isna())
            ab2_clean = ab2[valid_data].values
            rho_clean = rho[valid_data].values
            
            print(f"\\n✅ Puntos válidos: {len(ab2_clean)} de {len(ab2)}")
            
            if len(ab2_clean) == 0:
                raise ValueError("No hay datos válidos para graficar")
            
            # Graficar
            print(f"\\n🎨 Graficando {len(ab2_clean)} puntos...")
            self.ax.loglog(ab2_clean, rho_clean, 'o-', 
                          color=self.colors['data'], 
                          markersize=8, 
                          linewidth=2, 
                          label='Resistividad Aparente',
                          markeredgecolor='white',
                          markeredgewidth=1)
            
            # Configurar gráfico
            self._setup_plot(f"{ab2_col} (m)", f"{rho_col} (Ω·m)")
            
            print("✅ Gráfico completado exitosamente")
            print("="*50 + "\\n")
            
        except Exception as e:
            # En caso de error, mostrar gráfico vacío con mensaje
            print(f"\\n❌ ERROR EN GRÁFICO: {str(e)}")
            print("="*50 + "\\n")
            self.ax.clear()
            self.ax.text(0.5, 0.5, f'Error graficando:\\n{str(e)}', 
                        transform=self.ax.transAxes, 
                        ha='center', va='center',
                        fontsize=10, color='red')
            self._setup_plot()
    
    def plot_inversion(self, data: pd.DataFrame, inversion_result: dict):
        """
        Graficar datos originales y resultado de inversión
        
        Args:
            data: DataFrame con datos originales
            inversion_result: Diccionario con resultado de inversión
        """
        try:
            # Graficar datos originales
            self.plot_data(data)
            
            # Agregar curva de inversión si existe
            if 'ab2_model' in inversion_result and 'rho_model' in inversion_result:
                ab2_model = inversion_result['ab2_model']
                rho_model = inversion_result['rho_model']
                
                self.ax.loglog(ab2_model, rho_model, '-', 
                              color=self.colors['inversion'], 
                              linewidth=2, 
                              label='Modelo invertido')
            
            # Actualizar leyenda
            self.ax.legend()
            
        except Exception as e:
            self.plot_data(data)  # Fallback a solo datos
    
    def plot_model_layers(self, layers: dict):
        """
        Graficar capas del modelo como barras
        
        Args:
            layers: Diccionario con espesores y resistividades
        """
        # Esta función se puede implementar más tarde
        # para mostrar el modelo de capas como un gráfico de barras
        pass
    
    def _get_columns(self, data: pd.DataFrame):
        """Obtener nombres de columnas AB/2 y resistividad"""
        ab2_col = None
        rho_col = None
        
        print(f"🔍 Columnas disponibles: {list(data.columns)}")
        
        # Buscar columna AB/2
        for col in data.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['ab', 'distancia', 'spacing', 'electrode', 'ab/2', 'ab2']):
                ab2_col = col
                print(f"✅ Columna AB/2 encontrada: {col}")
                break
        
        # Buscar columna resistividad
        for col in data.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['rho', 'resistividad', 'resistivity', 'apparent', 'ohm', 'ω']):
                rho_col = col
                print(f"✅ Columna Resistividad encontrada: {col}")
                break
        
        # Si no encuentra, usar primeras dos columnas
        if ab2_col is None:
            ab2_col = data.columns[0]
            print(f"⚠️ Usando primera columna como AB/2: {ab2_col}")
        if rho_col is None and len(data.columns) > 1:
            rho_col = data.columns[1]
            print(f"⚠️ Usando segunda columna como Resistividad: {rho_col}")
        
        # Mostrar valores para debug
        print(f"📊 Primeros valores AB/2: {data[ab2_col].head().tolist()}")
        print(f"📊 Primeros valores Rho: {data[rho_col].head().tolist()}")
        
        return ab2_col, rho_col
    
    def _setup_plot(self, ab2_label="AB/2 (m)", rho_label="Resistividad Aparente (Ω·m)"):
        """Configurar aspecto del gráfico"""
        self.ax.set_xlabel(ab2_label, fontsize=12)
        self.ax.set_ylabel(rho_label, fontsize=12)
        self.ax.set_title('Curva de Sondeo Eléctrico Vertical', fontsize=14, fontweight='bold')
        
        # Grid
        self.ax.grid(True, alpha=0.3, color=self.colors['grid'])
        
        # Escala logarítmica
        self.ax.set_xscale('log')
        self.ax.set_yscale('log')
        
        # Mejorar aspecto
        self.ax.tick_params(labelsize=10)
        
        # Leyenda si hay múltiples series
        if len(self.ax.get_lines()) > 1:
            self.ax.legend(fontsize=10)

class VESModelPlotter:
    """Graficador específico para modelos de capas"""
    
    def __init__(self, ax: Axes):
        self.ax = ax
    
    def plot_layer_model(self, thicknesses, resistivities):
        """
        Graficar modelo de capas
        
        Args:
            thicknesses: Lista de espesores de capas (m)
            resistivities: Lista de resistividades (Ω·m)
        """
        self.ax.clear()
        
        # Calcular profundidades
        depths = [0]
        for thickness in thicknesses[:-1]:  # Última capa es infinita
            depths.append(depths[-1] + thickness)
        depths.append(depths[-1] + max(thicknesses[:-1]))  # Profundidad final para visualización
        
        # Crear gráfico de escalera
        for i, (depth_top, depth_bottom, rho) in enumerate(zip(depths[:-1], depths[1:], resistivities)):
            self.ax.barh(y=(depth_top + depth_bottom) / 2, 
                        width=rho, 
                        height=depth_bottom - depth_top,
                        alpha=0.7,
                        edgecolor='black',
                        label=f'Capa {i+1}: {rho:.1f} Ω·m')
        
        self.ax.set_xlabel('Resistividad (Ω·m)')
        self.ax.set_ylabel('Profundidad (m)')
        self.ax.set_title('Modelo de Capas')
        self.ax.invert_yaxis()  # Profundidad aumenta hacia abajo
        self.ax.legend()

def create_sample_plot():
    """Crear gráfico de muestra para testing"""
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Datos sintéticos
    ab2 = np.logspace(0, 2, 20)
    rho = 100 * (1 + 0.5 * np.sin(np.log10(ab2) * 2))
    
    data = pd.DataFrame({'AB2': ab2, 'Resistividad': rho})
    
    # Graficar
    plotter = VESPlotter(ax)
    plotter.plot_data(data)
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    # Test del módulo
    fig = create_sample_plot()
    plt.show()