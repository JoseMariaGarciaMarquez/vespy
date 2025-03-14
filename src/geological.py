import os
import gempy as gp
import gempy_viewer as gpv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class lithology:
    def __init__(self, data):
        self.data = data

    def lithology(self, lithology):
        """Plot lithology."""
        self.data = self.data.sort_values('Z')
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.fill_betweenx(self.data['Z'], self.data['X'], self.data['Y'], color=lithology, alpha=0.5)
        ax.set_xlabel('X')
        ax.set_ylabel('Z')
        ax.set_title('Lithology')
        plt.gca().invert_yaxis()
        plt.show()

    def lithology_3d(self, lithology):
        """Plot 3D lithology."""
        self.data = self.data.sort_values('Z')
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(self.data['X'], self.data['Y'], self.data['Z'], linewidth=0, antialiased=False, color=lithology)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Lithology')
        plt.show()

    def lithology_3d_viewer(self, lithology):
        """Plot 3D lithology with viewer."""
        self.data = self.data.sort_values('Z')
        geo_model = gp.create_model('geo_model')
        geo_model = gp.init_data(geo_model, [self.data['X'], self.data['Y'], self.data['Z']], lithology)
        gpv.plot_3d(geo_model, plotter_type='background', show_data=False)
        gpv.plot_3d(geo_model, show_data=False)