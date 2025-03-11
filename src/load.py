import numpy as np
import pandas as pd
import pyexcel as p

class Load:
    def __init__(self, path):
        self.path = path

    def load_data(self):
        """Cargar datos desde un archivo y devolver los nombres de las columnas."""
        try:
            if self.path.endswith('.csv'):
                data = pd.read_csv(self.path)
            elif self.path.endswith('.xlsx') or self.path.endswith('.xls'):
                data = pd.read_excel(self.path)
            elif self.path.endswith('.ods'):
                data = p.get_sheet(file_name=self.path).to_array()
                data = pd.DataFrame(data[1:], columns=data[0])
            else:
                raise ValueError("Formato de archivo no soportado.")
            
            return data.columns.tolist()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None