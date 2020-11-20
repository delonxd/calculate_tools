class Joint:
    """
        绝缘节
    """

    def __init__(self, l_par=None, r_par=None):
        """structure"""
        self.l_par = l_par
        self.r_par = r_par

        """parameters"""
        self.length = None

        """generated"""
        self.name = str()
        self.element = set()

    @property
    def parent(self):
        if self.l_par:
            return self.l_par
        elif self.r_par:
            return self.r_par
        else:
            return None

    @property
    def bas_name(self):
        return

    @property
    def rlt_pos(self):
        return

    @property
    def abs_pos(self):
        return

    def set_l_par(self, l_par):
        self.l_par = l_par

    def set_r_par(self, r_par):
        self.r_par = r_par

    def load_kwargs(self, **kwargs):
        if 'length' in kwargs:
            self.length = kwargs['length']