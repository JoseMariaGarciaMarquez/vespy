"""
GUI Principal de VESPY
=====================

Interfaz gráfica simple con layout horizontal:
- Controles (izquierda)
- Gráfico (centro) 
- Tabla (derecha)

Autor: VESPY Team
Fecha: 2025
"""

import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, 
    QPushButton, QTableWidget, QTableWidgetItem, QLabel,
    QMessageBox, QHeaderView, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VESPYMainGUI(QMainWindow):
    """GUI principal de VESPY - Simple y funcional"""
    
    def __init__(self):
        super().__init__()
        self.data = None
        self.smoothed_data = None
        self.inversion_result = None
        self.init_ui()
        self.create_menu()
    
    def init_ui(self):
        """Inicializar interfaz de usuario"""
        self.setWindowTitle("VESPY - Sondeo Eléctrico Vertical")
        self.setGeometry(100, 100, 1400, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout(central_widget)
        
        # Crear los tres paneles
        self.create_controls_panel(main_layout)
        self.create_plot_panel(main_layout)
        self.create_table_panel(main_layout)
    
    def create_controls_panel(self, main_layout):
        """Panel de controles (izquierda)"""
        controls_group = QGroupBox("🎛️ Controles")
        controls_layout = QVBoxLayout(controls_group)
        
        # Botón cargar datos
        self.load_btn = QPushButton("📂 Cargar Datos")
        self.load_btn.clicked.connect(self.load_data)
        controls_layout.addWidget(self.load_btn)
        
        # Botón preprocesamiento
        self.preprocess_btn = QPushButton("🔧 Preprocesamiento")
        self.preprocess_btn.clicked.connect(self.open_preprocessing)
        self.preprocess_btn.setEnabled(False)
        controls_layout.addWidget(self.preprocess_btn)
        
        # Botón inversión
        self.invert_btn = QPushButton("⚡ Realizar Inversión")
        self.invert_btn.clicked.connect(self.open_inversion_dialog)
        self.invert_btn.setEnabled(False)
        controls_layout.addWidget(self.invert_btn)
        
        # Botón exportar
        self.export_btn = QPushButton("💾 Exportar Resultados")
        self.export_btn.clicked.connect(self.export_results)
        self.export_btn.setEnabled(False)
        controls_layout.addWidget(self.export_btn)
        
        # Botón limpiar
        self.clear_btn = QPushButton("🗑️ Limpiar Todo")
        self.clear_btn.clicked.connect(self.clear_all)
        controls_layout.addWidget(self.clear_btn)
        
        # Información
        info_group = QGroupBox("📋 Información")
        info_layout = QVBoxLayout(info_group)
        
        self.info_label = QLabel("Sin datos cargados")
        info_layout.addWidget(self.info_label)
        
        controls_layout.addWidget(info_group)
        controls_layout.addStretch()
        
        # Agregar al layout principal (proporción 1)
        main_layout.addWidget(controls_group, 1)
    
    def create_plot_panel(self, main_layout):
        """Panel de gráfico con pestañas (centro)"""
        from PyQt5.QtWidgets import QTabWidget
        
        # Crear widget de pestañas
        self.plot_tabs = QTabWidget()
        
        # Pestaña 1: Curva de Resistividad Aparente
        self.curve_widget = QWidget()
        curve_layout = QVBoxLayout(self.curve_widget)
        
        self.figure_curve = Figure(figsize=(8, 6))
        self.canvas_curve = FigureCanvas(self.figure_curve)
        self.ax_curve = self.figure_curve.add_subplot(111)
        curve_layout.addWidget(self.canvas_curve)
        
        self.plot_tabs.addTab(self.curve_widget, "📈 Curva SEV")
        
        # Pestaña 2: Modelo Invertido
        self.model_widget = QWidget()
        model_layout = QVBoxLayout(self.model_widget)
        
        self.figure_model = Figure(figsize=(8, 6))
        self.canvas_model = FigureCanvas(self.figure_model)
        self.ax_model = self.figure_model.add_subplot(111)
        model_layout.addWidget(self.canvas_model)
        
        self.plot_tabs.addTab(self.model_widget, "🏔️ Modelo de Capas")
        
        # Pestaña 3: Plot 2D (para futuro)
        self.plot2d_widget = QWidget()
        plot2d_layout = QVBoxLayout(self.plot2d_widget)
        
        self.figure_2d = Figure(figsize=(8, 6))
        self.canvas_2d = FigureCanvas(self.figure_2d)
        self.ax_2d = self.figure_2d.add_subplot(111)
        plot2d_layout.addWidget(self.canvas_2d)
        
        self.plot_tabs.addTab(self.plot2d_widget, "🗺️ Plot 2D")
        
        # Configurar gráficos iniciales
        self.setup_plot()
        
        # Agregar al layout principal (proporción 2 - más espacio)
        main_layout.addWidget(self.plot_tabs, 2)
    
    def create_table_panel(self, main_layout):
        """Panel de tabla (derecha)"""
        table_group = QGroupBox("📊 Datos")
        table_layout = QVBoxLayout(table_group)
        
        # Tabla de datos
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        table_layout.addWidget(self.table)
        
        # Agregar al layout principal (proporción 1)
        main_layout.addWidget(table_group, 1)
    
    def setup_plot(self):
        """Configurar los gráficos iniciales"""
        # Gráfico de curva SEV
        self.ax_curve.set_xlabel('AB/2 (m)')
        self.ax_curve.set_ylabel('Resistividad Aparente (Ω·m)')
        self.ax_curve.set_xscale('log')
        self.ax_curve.set_yscale('log')
        self.ax_curve.grid(True, alpha=0.3)
        self.ax_curve.set_title('Curva de Resistividad Aparente')
        self.canvas_curve.draw()
        
        # Gráfico de modelo de capas
        self.ax_model.set_xlabel('Resistividad (Ω·m)')
        self.ax_model.set_ylabel('Profundidad (m)')
        self.ax_model.set_title('Modelo de Capas Invertido')
        self.ax_model.grid(True, alpha=0.3)
        self.canvas_model.draw()
        
        # Gráfico 2D
        self.ax_2d.set_xlabel('Distancia (m)')
        self.ax_2d.set_ylabel('Profundidad (m)')
        self.ax_2d.set_title('Pseudosección 2D')
        self.ax_2d.text(0.5, 0.5, 'Cargue múltiples SEV para visualización 2D',
                       transform=self.ax_2d.transAxes, ha='center', va='center',
                       fontsize=10, style='italic', color='gray')
        self.canvas_2d.draw()
    
    def load_data(self):
        """Cargar datos - llama al módulo de datos"""
        try:
            # Importar módulo de carga
            from data.loader import DataLoader
            
            loader = DataLoader()
            self.data = loader.load_file()
            
            if self.data is not None:
                self.update_table()
                self.update_plot()
                self.update_info()
                self.invert_btn.setEnabled(True)
                self.preprocess_btn.setEnabled(True)
                QMessageBox.information(self, "Éxito", f"Datos cargados: {len(self.data)} puntos")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error cargando datos: {str(e)}")
    
    def run_inversion(self):
        """Realizar inversión - llama al módulo de inversión"""
        try:
            if self.data is None:
                return
            
            # Importar módulo de inversión
            from inversion.inversion import VESInverter
            
            inverter = VESInverter()
            result = inverter.invert(self.data)
            
            if result is not None:
                # Actualizar gráfico con resultado
                self.update_plot_with_inversion(result)
                QMessageBox.information(self, "Éxito", "Inversión completada")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en inversión: {str(e)}")
    
    def update_table(self):
        """Actualizar tabla con datos cargados"""
        if self.data is None:
            return
        
        # Configurar tabla
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(len(self.data.columns))
        self.table.setHorizontalHeaderLabels(self.data.columns.tolist())
        
        # Llenar datos
        for i, row in self.data.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(i, j, item)
        
        # Ajustar columnas
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.resizeColumnsToContents()
    
    def update_plot(self):
        """Actualizar gráfico con datos"""
        if self.data is None:
            return
        
        try:
            # Importar módulo de plotting
            from plotting.plotter import VESPlotter
            
            plotter = VESPlotter(self.ax_curve)
            plotter.plot_data(self.data)
            self.canvas_curve.draw()
            
            # Cambiar a la pestaña de curva
            self.plot_tabs.setCurrentIndex(0)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error graficando: {str(e)}")
    
    def update_plot_with_inversion(self, inversion_result):
        """Actualizar gráficos con resultado de inversión"""
        try:
            from plotting.plotter import VESPlotter, VESModelPlotter
            
            # Actualizar curva con modelo invertido
            plotter = VESPlotter(self.ax_curve)
            plotter.plot_inversion(self.data, inversion_result)
            self.canvas_curve.draw()
            
            # Graficar modelo de capas
            if 'resistivities' in inversion_result and 'thicknesses' in inversion_result:
                model_plotter = VESModelPlotter(self.ax_model)
                model_plotter.plot_layer_model(
                    inversion_result['thicknesses'],
                    inversion_result['resistivities']
                )
                self.canvas_model.draw()
                
                # Cambiar a la pestaña de modelo
                self.plot_tabs.setCurrentIndex(1)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error graficando inversión: {str(e)}")
    
    def update_info(self):
        """Actualizar información de datos"""
        if self.data is None:
            self.info_label.setText("Sin datos cargados")
        else:
            info_text = f"Puntos: {len(self.data)}\\nColumnas: {len(self.data.columns)}"
            # Agregar rango de AB/2 si existe
            try:
                ab2_col = self.data.columns[0]  # Asume primera columna es AB/2
                ab2_min = self.data[ab2_col].min()
                ab2_max = self.data[ab2_col].max()
                info_text += f"\\nRango AB/2: {ab2_min:.1f} - {ab2_max:.1f} m"
            except:
                pass
            
            self.info_label.setText(info_text)
    
    def create_menu(self):
        """Crear menú principal"""
        menubar = self.menuBar()
        
        # Menú Archivo
        file_menu = menubar.addMenu("📁 Archivo")
        
        load_action = file_menu.addAction("📂 Cargar Datos")
        load_action.triggered.connect(self.load_data)
        load_action.setShortcut("Ctrl+O")
        
        file_menu.addSeparator()
        
        save_table_action = file_menu.addAction("💾 Guardar Tabla")
        save_table_action.triggered.connect(self.save_table)
        
        save_plot_action = file_menu.addAction("🖼️ Guardar Gráfico")
        save_plot_action.triggered.connect(self.save_plot)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("❌ Salir")
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut("Ctrl+Q")
        
        # Menú Preprocesamiento
        preprocess_menu = menubar.addMenu("🔧 Preprocesamiento")
        
        empalme_action = preprocess_menu.addAction("🔗 Empalme de Datos")
        empalme_action.triggered.connect(self.open_preprocessing)
        
        smooth_action = preprocess_menu.addAction("📉 Suavizado")
        smooth_action.triggered.connect(self.apply_smoothing)
        
        # Menú Inversión
        inversion_menu = menubar.addMenu("⚡ Inversión")
        
        invert_action = inversion_menu.addAction("⚙️ Configurar Inversión")
        invert_action.triggered.connect(self.open_inversion_dialog)
        
        quick_invert_action = inversion_menu.addAction("🚀 Inversión Rápida")
        quick_invert_action.triggered.connect(self.run_quick_inversion)
        
        # Menú Análisis
        analysis_menu = menubar.addMenu("📊 Análisis")
        
        stats_action = analysis_menu.addAction("📈 Estadísticas")
        stats_action.triggered.connect(self.show_statistics)
        
        # Menú Ayuda
        help_menu = menubar.addMenu("❓ Ayuda")
        
        about_action = help_menu.addAction("ℹ️ Acerca de VESPY")
        about_action.triggered.connect(self.show_about)
        
        help_action = help_menu.addAction("📖 Documentación")
        help_action.triggered.connect(self.show_help)
    
    def open_preprocessing(self):
        """Abrir ventana de preprocesamiento"""
        if self.data is None:
            QMessageBox.warning(self, "Advertencia", "Primero debe cargar datos")
            return
        
        try:
            from utils.preprocessing import PreprocessingDialog
            dialog = PreprocessingDialog(self.data, self)
            if dialog.exec_():
                # Actualizar datos procesados
                self.smoothed_data = dialog.get_processed_data()
                if self.smoothed_data is not None:
                    self.data = self.smoothed_data
                    self.update_table()
                    self.update_plot()
                    QMessageBox.information(self, "Éxito", "Datos procesados correctamente")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en preprocesamiento: {str(e)}")
    
    def open_inversion_dialog(self):
        """Abrir diálogo de configuración de inversión"""
        if self.data is None:
            QMessageBox.warning(self, "Advertencia", "Primero debe cargar datos")
            return
        
        try:
            from utils.inversion_dialog import InversionDialog
            dialog = InversionDialog(self.data, self)
            if dialog.exec_():
                result = dialog.get_result()
                if result is not None:
                    self.inversion_result = result
                    self.update_plot_with_inversion(result)
                    self.export_btn.setEnabled(True)
                    QMessageBox.information(self, "Éxito", 
                        f"Inversión completada\nRMS: {result.get('rms_error', 0):.3f}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en inversión: {str(e)}")
    
    def run_quick_inversion(self):
        """Ejecutar inversión rápida con parámetros por defecto"""
        if self.data is None:
            QMessageBox.warning(self, "Advertencia", "Primero debe cargar datos")
            return
        
        try:
            from inversion.inversion import VESInverter
            inverter = VESInverter()
            self.inversion_result = inverter.invert(self.data, num_layers=3)
            self.update_plot_with_inversion(self.inversion_result)
            self.export_btn.setEnabled(True)
            QMessageBox.information(self, "Éxito", "Inversión rápida completada")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en inversión: {str(e)}")
    
    def apply_smoothing(self):
        """Aplicar suavizado a los datos"""
        if self.data is None:
            QMessageBox.warning(self, "Advertencia", "Primero debe cargar datos")
            return
        
        try:
            from utils.preprocessing import smooth_data
            self.smoothed_data = smooth_data(self.data)
            self.data = self.smoothed_data
            self.update_table()
            self.update_plot()
            QMessageBox.information(self, "Éxito", "Datos suavizados")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error suavizando: {str(e)}")
    
    def show_statistics(self):
        """Mostrar estadísticas de los datos"""
        if self.data is None:
            QMessageBox.warning(self, "Advertencia", "Primero debe cargar datos")
            return
        
        try:
            stats = self.data.describe().to_string()
            QMessageBox.information(self, "Estadísticas", stats)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error calculando estadísticas: {str(e)}")
    
    def save_table(self):
        """Guardar tabla de datos"""
        if self.data is None:
            QMessageBox.warning(self, "Advertencia", "No hay datos para guardar")
            return
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Guardar Tabla", "", 
                "Excel files (*.xlsx);;CSV files (*.csv)"
            )
            if file_path:
                if file_path.endswith('.xlsx'):
                    self.data.to_excel(file_path, index=False)
                else:
                    self.data.to_csv(file_path, index=False)
                QMessageBox.information(self, "Éxito", f"Tabla guardada en {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error guardando tabla: {str(e)}")
    
    def save_plot(self):
        """Guardar gráfico actual"""
        try:
            from PyQt5.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Guardar Gráfico", "",
                "PNG files (*.png);;PDF files (*.pdf);;SVG files (*.svg)"
            )
            if file_path:
                # Guardar el gráfico de la pestaña activa
                current_tab = self.plot_tabs.currentIndex()
                if current_tab == 0:
                    self.figure_curve.savefig(file_path, dpi=300, bbox_inches='tight')
                elif current_tab == 1:
                    self.figure_model.savefig(file_path, dpi=300, bbox_inches='tight')
                elif current_tab == 2:
                    self.figure_2d.savefig(file_path, dpi=300, bbox_inches='tight')
                
                QMessageBox.information(self, "Éxito", f"Gráfico guardado en {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error guardando gráfico: {str(e)}")
    
    def export_results(self):
        """Exportar todos los resultados"""
        if self.inversion_result is None:
            QMessageBox.warning(self, "Advertencia", "No hay resultados de inversión")
            return
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            import pandas as pd
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Resultados", "",
                "Excel files (*.xlsx)"
            )
            
            if file_path:
                # Crear DataFrame con resultados
                result_df = pd.DataFrame({
                    'Resistividades': self.inversion_result['resistivities'],
                    'Espesores': self.inversion_result['thicknesses']
                })
                result_df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Éxito", f"Resultados exportados a {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exportando: {str(e)}")
    
    def show_about(self):
        """Mostrar información de VESPY"""
        about_text = """
        <h2>VESPY v3.0</h2>
        <p><b>Vertical Electrical Sounding in Python</b></p>
        <p>Software para análisis e inversión de datos de Sondeo Eléctrico Vertical (SEV)</p>
        <p>Contacto: josemaria.garcia.marquez@gmail.com</p>
        <p>© 2025 VESPY Team</p>
        """
        QMessageBox.about(self, "Acerca de VESPY", about_text)
    
    def show_help(self):
        """Mostrar ayuda"""
        help_text = """
        <h3>Ayuda de VESPY</h3>
        <p><b>Carga de datos:</b> Archivo → Cargar Datos (Ctrl+O)</p>
        <p><b>Preprocesamiento:</b> Preprocesamiento → Empalme/Suavizado</p>
        <p><b>Inversión:</b> Inversión → Configurar Inversión</p>
        <p><b>Guardar:</b> Archivo → Guardar Tabla/Gráfico</p>
        """
        QMessageBox.information(self, "Ayuda", help_text)
    
    def clear_all(self):
        """Limpiar todos los datos"""
        self.data = None
        self.smoothed_data = None
        self.inversion_result = None
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        
        self.ax_curve.clear()
        self.ax_model.clear()
        self.ax_2d.clear()
        self.setup_plot()
        
        # Volver a la primera pestaña
        self.plot_tabs.setCurrentIndex(0)
        
        self.update_info()
        self.invert_btn.setEnabled(False)
        self.preprocess_btn.setEnabled(False)
        self.export_btn.setEnabled(False)

def main():
    """Función principal para testing"""
    app = QApplication(sys.argv)
    window = VESPYMainGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()