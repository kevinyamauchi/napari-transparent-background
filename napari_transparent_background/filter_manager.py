from ._filters import AVAILABLE_FILTERS, FilterModel


class ImageFilterManager:
    def __init__(self, viewer: 'napari.viewer.Viewer'):
        self.viewer = viewer
        self._initialize_filter_map()

    def _initialize_filter_map(self):
        # todo filter for image layers
        valid_layers = [l for l in self.viewer.layers if type(l).__name__ == 'Image']

        self.filter_map = {layer.name: self._initialize_filter_model(layer.name) for layer in valid_layers}

    def _initialize_filter_model(self, layer_name, filter='transparent_background'):
        layer = self.viewer.layers[layer_name]
        transparent_color = layer.colormap.map(0)[0, :4].tolist()
        new_filter = AVAILABLE_FILTERS[filter](alpha=0, transparent_value=transparent_color)
        visuals = self._get_visual(layer_name)
        filter_model = FilterModel(filter=new_filter, visuals=visuals)
        return filter_model

    def add_layer(self, layer_name, filter=None):
        new_layer = {layer_name: filter}
        self.filter_map.update(new_layer)

    def remove_layer(self, layer_name: str):
        self.detach_filter(layer_name)
        self.filter.pop(layer_name)

    def attach_filter(self, layer_name:str, filter:str):
        visuals = self._get_visual(layer_name)
        new_filter = AVAILABLE_FILTERS[filter]()
        filter_model = FilterModel(new_filter)
        filter_model.attach(visuals)

        self.filter_map.update({layer_name: filter_model})

    def _get_visual(self, layer_name: str)-> 'vispy.visuals.visuals.BaseVisual':
        layer = self.viewer.layers[layer_name]
        visual_model = self.viewer.window.qt_viewer.layer_to_visual[layer]
        visual_2d = visual_model._layer_node.get_node(2)
        visual_3d = visual_model._layer_node.get_node(3)
        return visual_2d, visual_3d

    def detach_filter(self, layer_name: str):
        layer_filter = self.filter_map[layer_name]
        if layer_filter is not None:
            layer_filter.detach()
            self.filter_map.update({layer_name: None})
