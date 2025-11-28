"""
Utilidades de UI para VESPY
===========================

Funciones auxiliares para actualizar tablas y componentes de UI.

Autor: Jose Maria Garcia Marquez
Email: josemariagarciamarquez2.72@gmail.com
"""

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


def update_model_table(table_widget, thickness, depths, resistivity):
    """
    Actualizar tabla con modelo de inversión.
    
    Args:
        table_widget: QTableWidget a actualizar
        thickness: Array de espesores
        depths: Array de profundidades
        resistivity: Array de resistividades
    """
    table_widget.setRowCount(len(resistivity))
    table_widget.setColumnCount(3)
    table_widget.setHorizontalHeaderLabels(["Espesor (m)", "Profundidad (m)", "Resistividad (Ω*m)"])
    
    for i in range(len(resistivity)):
        if i < len(thickness):
            table_widget.setItem(i, 0, QTableWidgetItem(f"{thickness[i]:.2f}"))
            table_widget.setItem(i, 1, QTableWidgetItem(f"{depths[i]:.2f}"))
        else:
            table_widget.setItem(i, 0, QTableWidgetItem("∞"))
            table_widget.setItem(i, 1, QTableWidgetItem("∞"))
        table_widget.setItem(i, 2, QTableWidgetItem(f"{resistivity[i]:.2f}"))


def update_smooth_model_table(table_widget, thickness, depths, resistivity, max_rows=12):
    """
    Actualizar tabla con modelo suavizado (muestra representativa).
    
    Args:
        table_widget: QTableWidget a actualizar
        thickness: Array de espesores
        depths: Array de profundidades
        resistivity: Array de resistividades
        max_rows: Número máximo de filas a mostrar
    """
    # Mostrar solo una muestra de las capas para legibilidad
    step = max(1, len(resistivity) // max_rows)
    
    indices = list(range(0, len(resistivity), step))
    if indices[-1] != len(resistivity) - 1:
        indices.append(len(resistivity) - 1)  # Siempre incluir la última
    
    table_widget.setRowCount(len(indices))
    table_widget.setColumnCount(3)
    table_widget.setHorizontalHeaderLabels(["Espesor (m)", "Profundidad (m)", "Resistividad (Ω*m)"])
    
    for row, i in enumerate(indices):
        if i < len(thickness):
            table_widget.setItem(row, 0, QTableWidgetItem(f"{thickness[i]:.2f}"))
            table_widget.setItem(row, 1, QTableWidgetItem(f"{depths[i]:.2f}"))
        else:
            table_widget.setItem(row, 0, QTableWidgetItem("∞"))
            table_widget.setItem(row, 1, QTableWidgetItem("∞"))
        table_widget.setItem(row, 2, QTableWidgetItem(f"{resistivity[i]:.2f}"))


def update_data_table(table_widget, dataframe):
    """
    Actualizar tabla con datos del DataFrame.
    
    Args:
        table_widget: QTableWidget a actualizar
        dataframe: pandas DataFrame con los datos
    """
    table_widget.setRowCount(len(dataframe))
    table_widget.setColumnCount(len(dataframe.columns))
    table_widget.setHorizontalHeaderLabels(list(dataframe.columns))
    
    for i in range(len(dataframe)):
        for j, col in enumerate(dataframe.columns):
            value = dataframe.iloc[i, j]
            if isinstance(value, (int, float)):
                table_widget.setItem(i, j, QTableWidgetItem(f"{value:.2f}"))
            else:
                table_widget.setItem(i, j, QTableWidgetItem(str(value)))
