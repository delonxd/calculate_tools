class Unit:
    """
        轨面单元
    """

    def __init__(self, parent,  **kwargs):
        self.parent = parent
        self._rlt_pos = None
        self.load_kwargs(**kwargs)

    @property
    def rlt_pos(self):
        return self._rlt_pos

    @property
    def abs_pos(self):
        return

    @property
    def bas_name(self):
        return

    def load_kwargs(self, **kwargs):
        if 'rlt_pos' in kwargs:
            self._rlt_pos = kwargs['rlt_pos']
