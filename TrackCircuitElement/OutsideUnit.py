from TrackCircuitElement.Unit import Unit


class SVA(Unit):
    """
        室外空心线圈
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.device = None


class CapC(Unit):
    """
        室外补偿电容
    """

    def __init__(self, parent, bas_name):
        super().__init__(parent)
        self.device = None
        self._bas_name = bas_name

    @property
    def bas_name(self):
        return self._bas_name


class TB(Unit):
    """
        室外TB
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.device = None

    @property
    def freq(self):
        return


class UPowerOut(Unit):
    """
        室外电压源
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.device = None


class ROutside(Unit):
    """
        室外电阻
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.device = None
