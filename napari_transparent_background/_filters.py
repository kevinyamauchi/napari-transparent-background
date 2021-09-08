from typing import List

from vispy.visuals.filters.base_filter import Filter

from typing import Optional


class FilterModel:
    """A model that manages connecting a filter to a layer"""
    def __init__(self, filter: 'vispy.visuals.filters.base_filter.Filter',
                 visuals: Optional['vispy.visuals.visuals.BaseVisual'] = None
                 ):
        self.filter = filter
        self.visuals = visuals
        self._filter_attached = False

    @property
    def filter_attached(self)->bool:
        """A flag set to true if a filter is attached to a visual"""
        return self._filter_attached

    def attach(self):
        if self.filter_attached is False:
            for vis in self.visuals:
                vis.attach(self.filter)
                vis.update()
            self._filter_attached = True

    def detach(self):
        if self.filter_attached:
            for vis in self.visuals:
                self.filter._detach(vis)
                vis.update()
            self._filter_attached = False

    def _on_toggle(self, state):
        if state > 0:
            self.attach()
        if state == 0:
            self.detach()


class TransparentBackground(Filter):
    FRAG_SHADER = """
        void apply_alpha() {
            float r_diff = gl_FragColor.r - $transparent_value.r;
            if (abs(r_diff) < 1e-10) {
                float g_diff = gl_FragColor.g - $transparent_value.g;
                if (abs(g_diff) < 1e-10) {
                    float b_diff = gl_FragColor.b - $transparent_value.b;
                    if (abs(b_diff) < 1e-10) {
                        discard;
                    }
                }
            }
        }
    """

    def __init__(self, alpha: float = 0, transparent_value: List[float] = [0, 0, 0]):
        super(TransparentBackground, self).__init__(fcode=self.FRAG_SHADER)

        self.alpha = alpha
        self.transparent_value = transparent_value

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, a):
        self._alpha = a
        self.fshader['alpha'] = float(a)

    @property
    def transparent_value(self) -> List[float]:
        return self._transparent_value[0:4]

    @transparent_value.setter
    def transparent_value(self, transparent_value: List[float]):
        if not isinstance(transparent_value, list):
            transparent_value = list(transparent_value)
        if len(transparent_value) == 3:
            transparent_value.append(0)
        elif len(transparent_value) > 4:
            raise ValueError('transparent_value should be a list of length 3 or 4')
        self._transparent_value = transparent_value
        self.fshader['transparent_value'] = transparent_value


class FragDepth(Filter):
    FRAG_SHADER = """
        void apply_frag_depth() {   
            
            gl_FragDepth = $frag_depth;
        }
    """

    def __init__(self, frag_depth: float = 0):
        super(FragDepth, self).__init__(fcode=self.FRAG_SHADER)

        self.frag_depth = frag_depth


    @property
    def frag_depth(self) -> float:
        return self._frag_depth

    @frag_depth.setter
    def frag_depth(self, frag_depth: float):
        if not isinstance(frag_depth, float):
            frag_depth = float(frag_depth)
        self._frag_depth = frag_depth
        self.fshader['frag_depth'] = frag_depth


AVAILABLE_FILTERS = {'transparent_background': TransparentBackground,
                     'frag_depth' : FragDepth}
