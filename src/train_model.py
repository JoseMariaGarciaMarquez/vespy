import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset
from classified_ves import ClassifiedVes

# Datos de ejemplo
thickness = np.random.rand(100, 10)
resistivities = np.random.rand(100, 10)
labels = np.random.randint(0, 2, (100, 10))

# Crear DataLoader
inputs = np.stack((thickness, resistivities), axis=1)  # Combinar thickness y resistivities en 2 canales
train_dataset = TensorDataset(torch.tensor(inputs, dtype=torch.float32), torch.tensor(labels, dtype=torch.float32))
train_loader = DataLoader(train_dataset, batch_size=10, shuffle=True)

# Crear instancia de ClassifiedVes y entrenar el modelo
classified_ves = ClassifiedVes()
classified_ves.train_model(train_loader, num_epochs=10)