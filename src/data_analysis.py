import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy.fft import fft, fftfreq
import pandas as pd

class Analysis:
    def __init__(self, data, analysis_figure, eda_output):
        self.data = data
        self.analysis_figure = analysis_figure
        self.eda_output = eda_output

    def analyze_data(self):
        """Realizar un análisis completo de los datos de resistividad."""
        if self.data is not None:
            resistivity = self.data['pa (Ω*m)'].values
            ab2 = self.data['AB/2'].values
            
            # Estadísticas descriptivas
            mean = np.mean(resistivity)
            std_dev = np.std(resistivity)
            median = np.median(resistivity)
            skewness = pd.Series(resistivity).skew()
            kurtosis = pd.Series(resistivity).kurt()

            # Histograma y CDF (acumulativo)
            self.analysis_figure.clear()
            ax1 = self.analysis_figure.add_subplot(221)
            sns.histplot(resistivity, bins=20, kde=False, color='blue', ax=ax1)
            ax1.set_title("Histograma de Resistividades")
            ax1.set_xlabel("Resistividad aparente (Ω*m)")
            ax1.set_ylabel("Frecuencia")
            ax1.grid(True)

            ax2 = self.analysis_figure.add_subplot(222)
            sns.histplot(resistivity, bins=20, kde=True, cumulative=True, color='green', ax=ax2)
            ax2.set_title("Histograma Acumulativo de Resistividades")
            ax2.set_xlabel("Resistividad aparente (Ω*m)")
            ax2.set_ylabel("Frecuencia Acumulada")
            ax2.grid(True)
            
            # Transformada de Fourier (FFT) con suavizado previo
            sigma = 2
            resistivity_smooth = gaussian_filter(resistivity, sigma=sigma)
            n = len(resistivity_smooth)
            T = 1.0  # Supongamos una unidad de muestreo regular
            yf = fft(resistivity_smooth)
            xf = fftfreq(n, T)[:n//2]  # Solo las frecuencias positivas
            
            # Cálculo de la energía en cada frecuencia y frecuencia dominante
            magnitudes = 2.0/n * np.abs(yf[:n//2])
            top_freq_indices = np.argsort(magnitudes)[-3:][::-1]
            dominant_freqs = xf[top_freq_indices]

            ax3 = self.analysis_figure.add_subplot(223)
            ax3.plot(xf, magnitudes, color='purple')
            ax3.set_title("Transformada de Fourier")
            ax3.set_xlabel("Frecuencia (Hz)")
            ax3.set_ylabel("Magnitud")
            ax3.grid(True)

            # Calcular la derivada logarítmica para los datos originales
            log_ab2 = np.log(ab2)
            log_rhoa = np.log(resistivity)
            dlog_ab2 = np.diff(log_ab2)
            dlog_rhoa = np.diff(log_rhoa)
            with np.errstate(divide='ignore', invalid='ignore'):
                deriv_log = np.divide(dlog_rhoa, dlog_ab2, out=np.zeros_like(dlog_rhoa), where=dlog_ab2 != 0)

            # Calcular la derivada logarítmica para los datos suavizados
            log_rhoa_smooth = np.log(resistivity_smooth)
            dlog_rhoa_smooth = np.diff(log_rhoa_smooth)
            with np.errstate(divide='ignore', invalid='ignore'):
                deriv_log_smooth = np.divide(dlog_rhoa_smooth, dlog_ab2, out=np.zeros_like(dlog_rhoa_smooth), where=dlog_ab2 != 0)

            # Gráfico de la derivada logarítmica con dos ejes
            ax4 = self.analysis_figure.add_subplot(224)
            ax4.plot(ab2[1:], deriv_log, color='red', label='Derivada Logarítmica (Datos Originales)')
            ax4.plot(ab2[1:], deriv_log_smooth, color='blue', label='Derivada Logarítmica (Datos Suavizados)')
            ax4.set_xlabel("AB/2 (m)")
            ax4.set_ylabel("dlog(ρa)/dlog(AB/2)")
            ax4.set_xscale('log')
            ax4.grid(True)
            ax4.legend(loc='upper left')

            # Crear un segundo eje para la resistividad aparente
            ax4_resistivity = ax4.twinx()
            ax4_resistivity.plot(ab2, resistivity, 'o-', label='Resistividad Aparente (Datos Originales)', color='green')
            if hasattr(self, 'empalme_data') and self.empalme_data is not None:
                empalme_ab2 = self.empalme_data['AB/2'].values
                empalme_rhoa = self.empalme_data['pa (Ω*m)'].values
                ax4_resistivity.plot(empalme_ab2, empalme_rhoa, 'o-', label='Resistividad Aparente (Empalme)', color='orange')
            ax4_resistivity.set_ylabel("Resistividad aparente (Ω*m)")
            ax4_resistivity.set_yscale('log')
            ax4_resistivity.legend(loc='upper right')

            # Mostrar la frecuencia dominante y estadísticas en la terminal de salida
            self.eda_output.clear()
            self.eda_output.append("Análisis Estadístico Completo:\n")
            self.eda_output.append(f"Media: {mean:.2f} Ω*m")
            self.eda_output.append(f"Desviación Estándar: {std_dev:.2f} Ω*m")
            self.eda_output.append(f"Mediana: {median:.2f} Ω*m")
            self.eda_output.append(f"Skewness (Asimetría): {skewness:.2f}")
            self.eda_output.append(f"Kurtosis: {kurtosis:.2f}")
            self.eda_output.append("\nTransformada de Fourier:\n")
            for i, freq in enumerate(dominant_freqs):
                self.eda_output.append(f"Frecuencia Dominante {i+1}: {freq:.2f} Hz")
            self.eda_output.append(f"Magnitud de Frecuencia Dominante: {magnitudes.max():.2f}")
            self.analysis_figure.canvas.draw()

    def analyze_and_recommend(self, data):
        ab2 = data['AB/2'].values
        rhoa = data['pa (Ω*m)'].values

        # Calcular la derivada logarítmica
        log_ab2 = np.log(ab2)
        log_rhoa = np.log(rhoa)
        dlog_ab2 = np.diff(log_ab2)
        dlog_rhoa = np.diff(log_rhoa)
        with np.errstate(divide='ignore', invalid='ignore'):
            deriv_log = np.divide(dlog_rhoa, dlog_ab2, out=np.zeros_like(dlog_rhoa), where=dlog_ab2 != 0)

        # Contar picos y valles en la derivada logarítmica
        peaks_and_valleys = np.sum((np.diff(np.sign(np.diff(deriv_log))) != 0).astype(int))

        # Calcular la desviación estándar de rhoa
        std_rhoa = np.std(rhoa)
        mean_rhoa = np.mean(rhoa)
        std_ratio = std_rhoa / mean_rhoa

        # Suavizar la curva para la FFT
        sigma = 0.5
        rhoa_smooth = gaussian_filter(rhoa, sigma=sigma)
        n = len(rhoa_smooth)
        T = 1.0  # Supongamos una unidad de muestreo regular
        yf = fft(rhoa_smooth)
        xf = fftfreq(n, T)[:n//2]
        magnitudes = 2.0/n * np.abs(yf[:n//2])

        # Detectar múltiples frecuencias dominantes
        top_freq_indices = np.argsort(magnitudes)[-3:][::-1]
        dominant_freqs = xf[top_freq_indices]

        # Manejo de frecuencia dominante muy baja
        dominant_freqs_str = [f"{freq:.2f} Hz" if freq >= 0.01 else "Muy baja — Posible tendencia de fondo" for freq in dominant_freqs]

        # Evaluación de calidad de ajuste en la derivada logarítmica
        dispersion = np.std(deriv_log) / np.mean(np.abs(deriv_log))
        if dispersion > 1.5:  # Ajustar el umbral para detectar ruido
            quality_flag = "Datos ruidosos — Revisar o filtrar"
        else:
            quality_flag = "Datos de buena calidad"

        # Recomendaciones basadas en los criterios
        n_layers = max(3, min(8, peaks_and_valleys // 3))  # Ajustar el cálculo del número de capas
        lambda_val = max(1, min(200, 10 + std_ratio * 500))
        lambda_factor = max(0.8, min(2, 1 + std_ratio * 5))

        # Calcular el error estimado
        error_est = std_rhoa / np.sqrt(len(rhoa))

        recommendations = {
            "Número de capas": n_layers,
            "Valor de lambda": lambda_val,
            "Factor lambda": lambda_factor,
            "Frecuencia dominante": dominant_freqs_str,
            "Calidad de datos": quality_flag,
            "Error estimado": f"{error_est:.2f} Ω*m"
        }

        return recommendations