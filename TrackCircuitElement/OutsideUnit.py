from TrackCircuitElement.Unit import Unit
from TrackCircuitElement.ElectricModule import ImpedanceModule


class SVA(Unit):
    """
        室外空心线圈
    """

    def __init__(self, parent, bas_name):
        super().__init__(parent)
        self._bas_name = bas_name
        self._md_type = ImpedanceModule

    def init_module(self):
        pass


class CapC(Unit):
    """
        室外补偿电容
    """

    def __init__(self, parent, bas_name):
        super().__init__(parent)
        self._bas_name = bas_name

    @property
    def bas_name(self):
        return self._bas_name


class TB(Unit):
    """
        室外TB
    """

    def __init__(self, parent, bas_name):
        super().__init__(parent)
        self._bas_name = bas_name

    @property
    def freq(self):
        return


class UPowerOut(Unit):
    """
        室外电压源
    """

    def __init__(self, parent, bas_name):
        super().__init__(parent)
        self._bas_name = bas_name


class ROutside(Unit):
    """
        室外电阻
    """

    def __init__(self, parent, bas_name):
        super().__init__(parent)
        self._bas_name = bas_name


class BreakPoint(Unit):
    """
        钢轨断点
    """

    def __init__(self, parent, bas_name):
        super().__init__(parent)
        self._bas_name = bas_name
