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
        self._type = None

        """generated"""
        self.name = str()
        self.units = set()

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
        from TrackCircuitElement.Section import Section

        if isinstance(self.parent, Section):
            if self == self.parent.l_joint:
                return '左侧绝缘节'
            elif self == self.parent.r_joint:
                return '右侧绝缘节'
            else:
                return
        return

    @property
    def rlt_pos(self):
        from TrackCircuitElement.Section import Section

        if isinstance(self.parent, Section):
            if self == self.parent.l_joint:
                return 0
            elif self == self.parent.r_joint:
                return self.parent.length
            else:
                return
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


class Joint_Type:
    """
        绝缘节类型
    """

    def __init__(self, parent: Joint):
        self.parent = parent


class Mechanical_JTyp(Joint_Type):
    """
        机械绝缘节
    """

    def set_unit(self):
        unit = BreakPoint
        self.parent.units.clear()
        self.parent.addunit(unit)


class Electric_2000A_JTyp(Joint_Type):
    """
        2000A电气绝缘节
    """

    def set_unit(self):
        unit = None
        self.parent.units.clear()
        self.parent.addunit(unit)


class Belarus_Electric__JTyp(Joint_Type):
    """
        白俄电气绝缘节
    """

    def set_unit(self):
        unit = None
        self.parent.units.clear()
        self.parent.addunit(unit)
