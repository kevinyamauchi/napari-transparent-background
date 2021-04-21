import napari
import numpy as np


data = np.zeros((128, 128), dtype=np.float32)
data[100:110, 100:110] = 1

data_2 = np.random.random((128, 128))

with napari.gui_qt():
    viewer = napari.view_image(data_2, colormap='gray', opacity=1)
    viewer.add_image(data, colormap='viridis', opacity=0.5)