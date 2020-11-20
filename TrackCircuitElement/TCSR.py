class TCSR:
    """

    """

    def __init__(self, parent):
        # structure
        self.parent = parent

        # parameters
        self._bas_name = None
        self.snd_lvl = None
        self.rcv_lvl = None
        self._mode = None
        self.cable_len = None
        self.device = None

        # generated
        self.name = str()
        self.element = set()

    @property
    def bas_name(self):
        return

    @property
    def mode(self):
        return self._mode

    @property
    def _rlt_pos(self):
        return

    @property
    def abs_pos(self):
        return

    def load_kwargs(self, **kwargs):

        if 'bas_name' in kwargs:
            self._bas_name = kwargs['bas_name']

        if 'snd_lvl' in kwargs:
            self.snd_lvl = kwargs['snd_lvl']

        if 'rcv_lvl' in kwargs:
            self.rcv_lvl = kwargs['rcv_lvl']

        if 'mode' in kwargs:
            self._mode = kwargs['mode']

        if 'cable_len' in kwargs:
            self.cable_len = kwargs['cable_len']


class TCSR_Mde_Flg:
    """

    """

    def __init__(self, parent):
        self.parent = parent


class Snd_Mde(TCSR_Mde_Flg):
    """

    """


class Rcv_Mde(TCSR_Mde_Flg):
    """

    """