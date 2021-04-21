from qtpy.QtWidgets import QWidget, QVBoxLayout, QCheckBox

from .filter_manager import ImageFilterManager

class QtFilterManager(QWidget):
    """Widget to control the filter settings"""
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.filter_manager = ImageFilterManager(self.viewer)

        self.layout = QVBoxLayout()
        self._initialize_checkboxes()

        self.setLayout(self.layout)

    def _initialize_checkboxes(self):
        self.checkboxes = []
        self.checkbox_layout = QVBoxLayout()
        for layer, filter in self.filter_manager.filter_map.items():
            checkbox = QCheckBox(layer)
            checkbox.stateChanged.connect(filter._on_toggle)
            self.checkbox_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)
        self.layout.addLayout(self.checkbox_layout)