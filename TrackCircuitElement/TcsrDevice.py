
class TcsrDevice:
    """

    """

    def __init__(self, parent):
        self.parent = parent
        # parameter library
        self.parameter = None
        self.dev_list = list()

    @property
    def snd_lvl(self):
        return

    @property
    def rcv_lvl(self):
        return

    @property
    def mode(self):
        return

    @property
    def cable_len(self):
        return

    def add_device(self):
        pass


class ZPW2000A_QJ_Normal(TcsrDevice):
    """
        创建ZPW2000A区间标准配置
    """

    def __init__(self, parent):
        super().__init__(parent)
        pass