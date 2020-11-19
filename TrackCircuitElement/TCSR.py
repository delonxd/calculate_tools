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

        # generated
        self.name = str()
        self.element = set()

    @property
    def bas_name(self):
        return

    @property
    def mode(self):
        return

    @property
    def _rlt_pos(self):
        return

    @property
    def abs_pos(self):
        return

    def load_params(self, **kw):

        if 'bas_name' in kw:
            self._bas_name = kw['bas_name']

        if 'snd_lvl' in kw:
            self.snd_lvl = kw['snd_lvl']

        if 'rcv_lvl' in kw:
            self.rcv_lvl = kw['rcv_lvl']

        if 'mode' in kw:
            self._mode = kw['mode']

        if 'cable_len' in kw:
            self.cable_len = kw['cable_len']



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