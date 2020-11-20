from TrackCircuitElement.ElectricModule import ImpedanceModule

class ZPW2000A_SVA(ImpedanceModule):
    """
        SVA模块
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self.parameter = None

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'z' in kwargs:
            self.r1.load_kw(z=kwargs['z'])

class ZPW2000A_CapC(ImpedanceModule):
    """
        补偿电容模块
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self.parameter = None

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'z' in kwargs:
            self.r1.load_kw(z=kwargs['z'])