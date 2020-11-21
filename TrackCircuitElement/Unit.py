class Unit:
    """
        轨面单元
    """

    def __init__(self, parent,  **kwargs):
        self.parent = parent
        self._rlt_pos = None
        self._md_type = None
        self.module = None

        # generated
        self.name = str()
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

    @property
    def md_type(self):
        return self._md_type

    def create_module(self):
        pass

    def load_kwargs(self, **kwargs):
        if 'rlt_pos' in kwargs:
            self._rlt_pos = kwargs['rlt_pos']
