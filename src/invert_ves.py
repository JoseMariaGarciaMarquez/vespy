import numpy as np
import pandas as pd
from pygimli.physics import VESManager
from PyQt5.QtWidgets import QFileDialog

class InvertVes:
    def __init__(self):
        pass

    def invert_model(self, data, empalme_data, smoothed_data, layer_spin, lambda_spin, lambda_factor_spin, model_selector, eda_output, inversion_figure, inversion_canvas, current_file):
        """Realizar la inversión de resistividad y mostrar resultados."""
        if data is not None:
            try:
                data_to_use, rhoa, ab2, mn2 = self.prepare_data(data, empalme_data, smoothed_data)
                self.check_data_lengths(rhoa, ab2, mn2)

                ves, n_layers, lambda_val, lambda_factor, error, max_depth = self.setup_inversion(layer_spin, lambda_spin, lambda_factor_spin, ab2)

                method = model_selector.currentText()
                model = self.run_inversion(ves, method, rhoa, error, ab2, mn2, n_layers, lambda_val, lambda_factor, eda_output)

                depths, resistividades, thickness, rmse = self.process_results(ves, model, n_layers, rhoa, ab2, max_depth, inversion_figure, inversion_canvas)

                return depths, resistividades, thickness, rmse

            except Exception as e:
                eda_output.append(f"Error durante la inversión: {str(e)}")
                return None, None, None, None

    def prepare_data(self, data, empalme_data, smoothed_data):
        """Preparar los datos para la inversión."""
        data_to_use = empalme_data if empalme_data is not None else data
        rhoa = smoothed_data if smoothed_data is not None else data_to_use['pa (Ω*m)'].values
        ab2 = data_to_use['AB/2'].values
        mn2 = data_to_use['MN/2'].values if 'MN/2' in data_to_use.columns else None
        return data_to_use, rhoa, ab2, mn2

    def check_data_lengths(self, rhoa, ab2, mn2):
        """Verificar que las longitudes de los vectores sean iguales."""
        if len(rhoa) != len(ab2) or (mn2 is not None and len(rhoa) != len(mn2)):
            raise ValueError("Las longitudes de los vectores rhoa, ab2 y mn2 (si está presente) deben ser iguales.")

    def setup_inversion(self, layer_spin, lambda_spin, lambda_factor_spin, ab2):
        """Configurar los parámetros y ejecutar la inversión."""
        ves = VESManager()
        n_layers = layer_spin.value()
        lambda_val = lambda_spin.value()
        lambda_factor = lambda_factor_spin.value()
        error = np.ones_like(ab2) * 0.03
        max_depth = np.max(ab2) / 3
        return ves, n_layers, lambda_val, lambda_factor, error, max_depth

    def run_inversion(self, ves, method, rhoa, error, ab2, mn2, n_layers, lambda_val, lambda_factor, eda_output):
        """Ejecutar la inversión con el método seleccionado."""
        if method == 'Levenberg-Marquardt':
            eda_output.append("Método Levenberg-Marquardt no disponible.")
            raise ValueError("Método Levenberg-Marquardt no disponible.")
        else:
            if mn2 is not None:
                model = ves.invert(rhoa, error, ab2=ab2, mn2=mn2, nLayers=n_layers, lam=lambda_val, lambdaFactor=lambda_factor)
            else:
                model = ves.invert(rhoa, error, ab2=ab2, nLayers=n_layers, lam=lambda_val, lambdaFactor=lambda_factor)
        return model

    def process_results(self, ves, model, n_layers, rhoa, ab2, max_depth, inversion_figure, inversion_canvas):
        """Procesar los resultados de la inversión."""
        rmse = np.sqrt(np.mean(((ves.inv.response - rhoa) / rhoa) ** 2)) * 100

        inversion_figure.clear()
        ax1 = inversion_figure.add_subplot(121)
        ves.showData(rhoa, ab2=ab2, ax=ax1, label="Datos Observados", color="C0", marker="o")
        ves.showData(ves.inv.response, ab2=ab2, ax=ax1, label="Curva Invertida", color="C1")
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        ax1.set_title("Ajuste del Modelo")
        ax1.set_ylabel("AB/2 (m)")
        ax1.set_xlabel("Resistividad aparente (Ω*m)")
        ax1.legend()

        depths = np.cumsum(model[:n_layers - 1])
        resistividades = model[n_layers - 1:]
        thickness = np.diff(np.concatenate(([0], depths)))

        ax2 = inversion_figure.add_subplot(122)
        ves.showModel(
            model=np.concatenate((thickness, resistividades)),
            ax=ax2,
            plot="semilogy",
            zmax=max_depth
        )
        ax2.set_title("Modelo de Resistividad 1D")
        inversion_canvas.draw()

        return depths, resistividades, thickness, rmse

    def save_inversion_table(self, parent):
        """Guardar la tabla del resultado de la inversión en un archivo."""
        if parent.depths is None or parent.resistivity is None:
            parent.eda_output.append("Error: No hay datos de inversión para guardar.")
            return

        if parent.depths.size == 0 or parent.resistivity.size == 0:
            parent.eda_output.append("Error: Los datos de profundidad o resistividad están vacíos.")
            return

        # Crear un DataFrame con los datos de inversión
        thickness = np.diff(np.concatenate(([0], parent.depths)))  # Espesores de las capas

        # Calcular el promedio de los espesores
        avg_thickness = np.mean(thickness)

        # Calcular la última profundidad
        last_depth = parent.depths[-1] + avg_thickness

        # Agregar el último espesor y resistividad al DataFrame
        thickness = np.append(thickness, avg_thickness)
        depths = np.append(parent.depths, last_depth)
        resistivities = parent.resistivity

        df = pd.DataFrame({
            "Espesor (m)": thickness,
            "Profundidad (m)": depths,
            "Resistividad (Ω*m)": resistivities
        })

        # Guardar el DataFrame en un archivo
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(parent, "Guardar Tabla de Inversión", "", "Excel Files (*.xlsx);;CSV Files (*.csv)", options=options)
        if not file:
            return

        if file.endswith('.xlsx'):
            df.to_excel(file, index=False)
        elif file.endswith('.csv'):
            df.to_csv(file, index=False)
        else:
            parent.eda_output.append("Formato de archivo no soportado.")
            return

        parent.eda_output.append(f"Tabla de inversión guardada en: {file}")