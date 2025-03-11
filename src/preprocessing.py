import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Preprocessing:
    def __init__(self, data):
        self.data = data

    def empalmes(self, method='drop'):
        """Eliminar empalmes en los datos."""
        if method == 'drop':
            self.data = self.data.drop_duplicates()
        elif method == 'mean':
            empalme_data = self.data.groupby('AB/2')['pa (Ω*m)'].mean().reset_index()
            empalme_data['MN/2'] = self.data.groupby('AB/2')['MN/2'].first().values
            self.empalme_data = empalme_data
            self.plot_data(empalme=True)
        elif method == 'median':
            empalme_data = self.data.groupby('AB/2')['pa (Ω*m)'].median().reset_index()
            empalme_data['MN/2'] = self.data.groupby('AB/2')['MN/2'].first().values
            self.empalme_data = empalme_data
            self.plot_data(empalme=True)
        elif method == 'upper':
            empalme_data = self.data.copy()
            empalme_data['pa (Ω*m)'] = empalme_data.groupby('AB/2')['pa (Ω*m)'].transform(lambda x: x.diff().fillna(0).cumsum() + x.iloc[0])
            empalme_data = empalme_data.drop_duplicates(subset=['AB/2'], keep='last').reset_index(drop=True)
            empalme_data['MN/2'] = self.data.groupby('AB/2')['MN/2'].first().values
            self.empalme_data = empalme_data
            self.plot_data(empalme=True)
        return self.data