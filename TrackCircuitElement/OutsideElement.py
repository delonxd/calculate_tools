class SVA:
    """
        室外空心线圈
    """

    def __init__(self, parent):
        self.parent = parent
        self.rlt_pos = None
        self.device = None


class CapC:
    """
        室外补偿电容
    """

    def __init__(self, parent):
        self.parent = parent
        self.rlt_pos = None
        self.device = None


class TB:
    """
        室外TB
    """

    def __init__(self, parent):
        self.parent = parent
        self.rlt_pos = None
        self.device = None

    @property
    def freq(self):
        return


class UPowerOut:
    """

    """

    def __init__(self, parent):
        self.parent = parent
        self.rlt_pos = None
        self.device = None


class ROutside:
    """

    """

    def __init__(self, parent):
        self.parent = parent
        self.rlt_pos = None
        self.device = None