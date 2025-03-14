import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.interpolate import griddata
from PyQt5.QtWidgets import QFileDialog

class PlotVes:
    def __init__(self):
        self.current_figure = None

    def generate_2d_plot(self, saved_models, loaded_models, eda_output, interpolation_method='linear', contour_levels=10, colormap='viridis', resolution=100, title='Mapa 2D de Resistividad'):
        """Generar el gráfico 2D interpolado de resistividad en función de la profundidad y distancia."""
        if len(saved_models) + len(loaded_models) < 2:
            eda_output.append("Se necesitan al menos dos modelos para generar el mapa 2D.")
            return

        all_depths, all_x_positions, all_resistivities, x_positions_set, sev_labels = self.collect_data(saved_models, loaded_models)

        grid_x, grid_y, grid_z = self.create_grid(all_depths, all_x_positions, all_resistivities, x_positions_set, interpolation_method, resolution)

        canvas = self.create_figure(grid_x, grid_y, grid_z, contour_levels, colormap, title, sev_labels)
        self.current_figure = canvas.figure

        return canvas

    def collect_data(self, saved_models, loaded_models):
        """Recoger datos de profundidad y resistividad."""
        all_depths = []
        all_x_positions = []
        all_resistivities = []
        x_positions_set = set()
        sev_labels = []

        for model in saved_models + loaded_models:
            x_position = model["x_position"]
            sev_number = model.get("sev_number", "N/A")
            relative_height = model.get("relative_height", 0)
            depths = list(model["depths"])  # Convertir RVector a lista
            resistivities = list(model["resistivity"])  # Convertir RVector a lista

            # Ajustar las profundidades según la altura relativa
            adjusted_depths = [depth + relative_height for depth in depths]

            all_depths.extend(adjusted_depths)
            all_x_positions.extend([x_position] * len(adjusted_depths))
            all_resistivities.extend(resistivities)
            x_positions_set.add(x_position)
            sev_labels.append((x_position, f"SEV-{sev_number}"))

        return all_depths, all_x_positions, all_resistivities, x_positions_set, sev_labels

    def create_grid(self, all_depths, all_x_positions, all_resistivities, x_positions_set, interpolation_method, resolution):
        """Crear la cuadrícula para la interpolación."""
        x_positions = sorted(x_positions_set)
        grid_x, grid_y = np.meshgrid(np.linspace(min(x_positions), max(x_positions), resolution), np.linspace(min(all_depths), max(all_depths), resolution))
        grid_z = griddata((all_x_positions, all_depths), all_resistivities, (grid_x, grid_y), method=interpolation_method)
        return grid_x, grid_y, grid_z

    def create_figure(self, grid_x, grid_y, grid_z, contour_levels, colormap, title, sev_labels):
        """Crear la figura y el lienzo."""
        fig = Figure(figsize=(10, 6))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        # Crear el gráfico de contorno
        contour = ax.contourf(grid_x, grid_y, grid_z, levels=np.linspace(np.nanmin(grid_z), np.nanmax(grid_z), contour_levels), cmap=colormap)
        fig.colorbar(contour, ax=ax, label='Resistividad (Ω*m)')

        ax.set_xlabel('Distancia (m)')
        ax.set_ylabel('Profundidad (m)')
        ax.set_title(title)
        ax.invert_yaxis()  # Invertir el eje Y para que las profundidades vayan hacia abajo

        # Agregar etiquetas de SEV
        for x_position, label in sev_labels:
            ax.text(x_position, grid_y.min() - 0.05 * (grid_y.max() - grid_y.min()), label, ha='center', va='bottom', fontsize=10, color='white', rotation=90, bbox=dict(facecolor='black', alpha=0.7))

        return canvas

    def save_2d_figure(self, parent):
        """Guardar la figura 2D generada."""
        if self.current_figure is None:
            parent.eda_output.append("No hay figura 2D generada para guardar.")
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(parent, "Guardar Figura 2D", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)", options=options)
        if file_path:
            self.current_figure.savefig(file_path)
            parent.eda_output.append(f"Figura 2D guardada en: {file_path}")

    def plot_data(self, data, empalme_data=None, smoothed_data=None, canvas=None, figure=None):
        """Graficar los datos de resistividad."""
        if data is not None:
            figure.clear()
            ax = figure.add_subplot(111)
            
            # Graficar la curva original de resistividad
            ab2 = data['AB/2'].values
            rhoa = data['pa (Ω*m)'].values
            ax.plot(ab2, rhoa, 'o-', label='Curva Original', color='blue')

            # Si hay datos de empalme, incluir el empalme
            if empalme_data is not None:
                empalme_ab2 = empalme_data['AB/2'].values
                empalme_rhoa = empalme_data['pa (Ω*m)'].values
                ax.plot(empalme_ab2, empalme_rhoa, 'o-', label='Curva de Empalme', color='green')
            
            # Si hay datos suavizados, incluir la curva suavizada
            if smoothed_data is not None:
                ax.plot(ab2, smoothed_data, 'o-', label='Curva Suavizada', color='red')
            
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xlabel("AB/2 (m)")
            ax.set_ylabel("Resistividad aparente (Ω*m)")
            ax.legend()
            ax.set_title("Curva de Resistividad")
            canvas.draw()