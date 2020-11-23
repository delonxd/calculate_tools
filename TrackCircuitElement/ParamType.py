# import math
import numpy as np


class Impedance:
    """
        存放对阻抗值进行操作的方法
    """

    @classmethod
    def resistance(cls, ele):
        if isinstance(ele, ResistanceType):
            return ele
        else:
            try:
                tmp = float(ele)
                ele = ResistanceType(value=tmp)
            finally:
                return ele

    @classmethod
    def inductance(cls, ele):
        if isinstance(ele, InductanceType):
            return ele
        else:
            try:
                tmp = float(ele)
                ele = InductanceType(value=tmp)
            finally:
                return ele

    @classmethod
    def capacitance(cls, ele):
        if isinstance(ele, CapacitanceType):
            return ele
        else:
            try:
                tmp = float(ele)
                ele = CapacitanceType(value=tmp)
            finally:
                return ele


    @classmethod
    def get_rlc_s(cls, value, freq):
        """
            获取RLC串联等效
        """

        rss = ResistanceType(value=0)
        idc = InductanceType(value=0)
        cpc = CapacitanceType(value=np.inf)

        if value is not None:
            real = value.real
            imag = value.imag
            rss.set_real(real=real)
            if imag > 0:
                idc.set_imag(imag=imag, freq=freq)
            elif imag < 0:
                cpc.set_imag(imag=imag, freq=freq)

        if rss.is_open() or idc.is_open() or cpc.is_open():
            r_open = ResistanceType(value=np.inf)
            return r_open, None, None

        if rss.is_short() and idc.is_short() and cpc.is_short():
            return rss, None, None

        if rss.is_short():
            rss = None
        if idc.is_short():
            idc = None
        if cpc.is_short():
            cpc = None

        return rss, idc, cpc

    @classmethod
    def get_rlc_p(cls, value, freq):
        """
            获取RLC并联等效
        """

        rss = ResistanceType(value=np.inf)
        idc = InductanceType(value=np.inf)
        cpc = CapacitanceType(value=0)

        if value is not None:
            if value == 0:
                rss.set_real(real=0)
                return rss, None, None
            y = 1 / value
            real = y.real
            imag = y.imag
            if not real == 0:
                rss.set_real(real=real)
            if not imag == 0:
                imag = -1/imag
                if imag > 0:
                    idc.set_imag(imag=imag, freq=freq)
                elif imag < 0:
                    cpc.set_imag(imag=imag, freq=freq)

        if rss.is_short() or idc.is_short() or cpc.is_short():
            r_short = ResistanceType(value=0)
            return r_short, None, None

        if rss.is_open() and idc.is_open() and cpc.is_open():
            return rss, None, None

        if rss.is_open():
            rss = None
        if idc.is_open():
            idc = None
        if cpc.is_open():
            cpc = None

        return rss, idc, cpc

    @classmethod
    def rlc_s_to_z(cls, freq, **kwargs):

        rss = ResistanceType(value=0)
        idc = InductanceType(value=0)
        cpc = CapacitanceType(value=np.inf)

        if 'rss' in kwargs:
            ele = kwargs['rss']
            ele = Impedance.resistance(ele)
            if ele is None:
                pass
            elif not isinstance(ele, ResistanceType):
                raise KeyboardInterrupt('电阻参数应为电阻类型')
            else:
                if ele.is_exist():
                    rss = ele

        if 'idc' in kwargs:
            ele = kwargs['idc']
            ele = Impedance.inductance(ele)
            if ele is None:
                pass
            if not isinstance(ele, InductanceType):
                raise KeyboardInterrupt('电感参数应为电感类型')
            else:
                if ele.is_exist():
                    idc = ele

        if 'cpc' in kwargs:
            ele = kwargs['cpc']
            ele = Impedance.capacitance(ele)
            if ele is None:
                pass
            if not isinstance(ele, CapacitanceType):
                raise KeyboardInterrupt('电容参数应为电容类型')
            else:
                if ele.is_exist():
                    cpc = ele

        if rss.is_open() or idc.is_open() or cpc.is_open():
            return np.inf

        value = rss.z(freq) + idc.z(freq) + cpc.z(freq)

        return value

    @classmethod
    def rlc_p_to_z(cls, freq, **kwargs):

        rss = ResistanceType(value=np.inf)
        idc = InductanceType(value=np.inf)
        cpc = CapacitanceType(value=0)

        if 'rss' in kwargs:
            ele = kwargs['rss']
            ele = Impedance.resistance(ele)
            if ele is None:
                pass
            elif not isinstance(ele, ResistanceType):
                raise KeyboardInterrupt('电阻参数应为电阻类型')
            else:
                if ele.is_exist():
                    rss = ele

        if 'idc' in kwargs:
            ele = kwargs['idc']
            ele = Impedance.inductance(ele)
            if ele is None:
                pass
            if not isinstance(ele, InductanceType):
                raise KeyboardInterrupt('电感参数应为电感类型')
            else:
                if ele.is_exist():
                    idc = ele

        if 'cpc' in kwargs:
            ele = kwargs['cpc']
            ele = Impedance.capacitance(ele)
            if ele is None:
                pass
            if not isinstance(ele, CapacitanceType):
                raise KeyboardInterrupt('电容参数应为电容类型')
            else:
                if ele.is_exist():
                    cpc = ele

        if rss.is_short() or idc.is_short() or cpc.is_short():
            return 0

        value = 1/rss.z(freq) + 1/idc.z(freq) + 1/cpc.z(freq)

        if value == 0:
            return np.inf
        return 1 / value

    @classmethod
    def parallel_z(cls, z1, z2):
        if z1 == 0 or z2 == 0:
            z_new = 0
        elif z1 == np.inf:
            z_new = z2
        elif z2 == np.inf:
            z_new = z1
        else:
            tmp = 1/z1 + 1/z2
            if tmp == 0:
                z_new = np.inf
            else:
                z_new = 1 / tmp
        return z_new


class ShortCircuit:
    pass


class OpenCircuit:
    pass


class ResistanceType:
    """
        电阻类
    """

    def __init__(self, value=None):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val is None:
            self._value = OpenCircuit
        elif not isinstance(val, (int, float)):
            raise KeyboardInterrupt('电阻值必须是实数')
        elif val > 0:
            if val == np.inf:
                self._value = OpenCircuit
            else:
                self._value = val
        elif val == 0:
            self._value = ShortCircuit
        else:
            raise KeyboardInterrupt('电阻值必须大于等于0')

    def is_exist(self):
        if self._value is None:
            return False
        else:
            return True

    def is_short(self):
        if self.value == ShortCircuit:
            return True
        else:
            return False

    def is_open(self):
        if self.value == OpenCircuit:
            return True
        else:
            return False

    def z(self, freq):
        """
            阻抗值
        """

        if self.value == ShortCircuit:
            return 0
        elif self.value == OpenCircuit:
            return np.inf
        else:
            real = self.value
            imag = 0
            z = complex(real, imag)
            return z

    def set_real(self, real):
        """
            设置阻抗值
        """

        if real >= 0:
            self.value = real
        else:
            raise KeyboardInterrupt('电阻阻抗实部必须大于等于0')

    def to_imp_type(self, freq):
        obj = ImpedanceType(freq, self.z(freq))
        return obj


class InductanceType:
    """
        电感类
    """

    def __init__(self, value=None):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val is None:
            self._value = OpenCircuit
        elif not isinstance(val, (int, float)):
            raise KeyboardInterrupt('电感值必须是实数')
        elif val > 0:
            if val == np.inf:
                self._value = OpenCircuit
            else:
                self._value = val
        elif val == 0:
            self._value = ShortCircuit
        else:
            raise KeyboardInterrupt('电感值必须大于等于0')

    def is_exist(self):
        if self._value is None:
            return False
        else:
            return True

    def is_short(self):
        if self.value == ShortCircuit:
            return True
        else:
            return False

    def is_open(self):
        if self.value == OpenCircuit:
            return True
        else:
            return False

    def z(self, freq):
        """
            阻抗值
        """

        if self.value == ShortCircuit:
            return 0
        elif self.value == OpenCircuit:
            return np.inf
        else:
            real = 0
            imag = 2 * np.pi * freq * self.value
            z = complex(real, imag)
            return z

    def set_imag(self, imag, freq):
        """
            设置阻抗值
        """

        if imag > 0:
            omega = 2 * np.pi * freq
            self.value = imag / omega
        else:
            raise KeyboardInterrupt('电感阻抗虚部必须大于等于0')

    def to_imp_type(self, freq):
        obj = ImpedanceType(freq, self.z(freq))
        return obj


class CapacitanceType:
    """
        电容类
    """
    def __init__(self, value=None):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val is None:
            self._value = OpenCircuit
        elif not isinstance(val, (int, float)):
            raise KeyboardInterrupt('电容值必须是实数')
        elif val > 0:
            if val == np.inf:
                self._value = ShortCircuit
            else:
                self._value = val
        elif val == 0:
            self._value = OpenCircuit
        else:
            raise KeyboardInterrupt('电容值必须大于等于0')

    def is_exist(self):
        if self._value is None:
            return False
        else:
            return True

    def is_short(self):
        if self.value == ShortCircuit:
            return True
        else:
            return False

    def is_open(self):
        if self.value == OpenCircuit:
            return True
        else:
            return False

    def z(self, freq):
        """
            阻抗值
        """

        if self.value == ShortCircuit:
            return 0
        elif self.value == OpenCircuit:
            return np.inf
        else:
            real = 0
            imag = -1 / (2 * np.pi * freq * self.value)
            z = complex(real, imag)
            return z

    def set_imag(self, imag, freq):
        """
            设置阻抗值
        """

        if imag < 0:
            omega = 2 * np.pi * freq
            self.value = - 1 / (imag * omega)
        else:
            raise KeyboardInterrupt('电容阻抗虚部必须小0')

    def to_imp_type(self, freq):
        obj = ImpedanceType(freq, self.z(freq))
        return obj


class ImpedanceType:
    """
        单一频率阻抗类
    """

    def __init__(self, freq, value=None):
        self.freq = freq
        # self._z = None
        # self.z_complex = value
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val is None:
            self._value = OpenCircuit
        else:
            real = val.real
            imag = val.imag

            if real >= 0:
                if real == 0 and imag == 0:
                    self._value = ShortCircuit
                elif real == np.inf:
                    self._value = OpenCircuit
                elif imag == np.inf or imag == -np.inf:
                    self._value = OpenCircuit
                else:
                    self._value = val
            else:
                raise KeyboardInterrupt('阻抗实部必须大于等于0')

    @property
    def z(self):
        """
            阻抗值
        """

        if self.value == ShortCircuit:
            return 0
        elif self.value == OpenCircuit:
            return np.inf
        else:
            return self.value

    @z.setter
    def z(self, value):
        self.value = value

    @property
    def omega(self):
        omega = 2 * np.pi * self.freq
        return omega

    @property
    def z_complex(self):
        """
            阻抗复数形式
        """

        return self.z

    @z_complex.setter
    def z_complex(self, value: complex):
        self.z = value

    @property
    def z_polar(self):
        """
            阻抗极坐标形式
        """

        r, angle = None, None
        if self.z is not None:
            z = self.z
            r = abs(z)
            angle = np.degrees(np.arctan2(z.imag, z.real))
        return r, angle

    @z_polar.setter
    def z_polar(self, value):
        r, angle = value
        if r >= 0:
            # if -90 <= angle <= 90:
            imag = r * np.sin(np.radians(angle))
            real = r * np.cos(np.radians(angle))
            self.value = complex(real, imag)
            # else:
            #     raise KeyboardInterrupt('辐角需要在正负90度之间')
        else:
            raise KeyboardInterrupt('模值不能为负数')

    @property
    def rlc_s(self):
        """
            RLC串联等效形式
        """

        return Impedance.get_rlc_s(value=self.z, freq=self.freq)

    @rlc_s.setter
    def rlc_s(self, rlc):
        rss, idc, cpc = rlc
        Impedance.rlc_s_to_z(freq=self.freq, rss=rss, idc=idc, cpc=cpc)

    @property
    def rlc_p(self):
        """
            RLC并联等效形式
        """

        return Impedance.get_rlc_p(value=self.z, freq=self.freq)

    @rlc_p.setter
    def rlc_p(self, rlc):
        rss, idc, cpc = rlc
        Impedance.rlc_p_to_z(freq=self.freq, rss=rss, idc=idc, cpc=cpc)

    def copy(self):
        obj = ImpedanceType(self.freq, self.z)
        return obj

    def __add__(self, other):
        if isinstance(other, ImpedanceType):
            if other.freq == self.freq:
                z_new = self.value + other.value
            else:
                raise KeyboardInterrupt('频率不同不能运算')
        else:
            z_new = self.value + other
        obj = ImpedanceType(self.freq, z_new)
        return obj

    def __radd__(self, other):
        obj = self.__add__(other)
        return obj

    def __sub__(self, other):
        obj = -other
        return self.__add__(obj)

    def __rsub__(self, other):
        obj = -self
        return obj.__add__(other)

    def __neg__(self):
        z_new = -self.z
        obj = ImpedanceType(self.freq, z_new)
        return obj

    def __mul__(self, other):
        if isinstance(other, ImpedanceType):
            if other.freq == self.freq:
                z_new = self.value * other.value
            else:
                raise KeyboardInterrupt('频率不同不能运算')
        else:
            z_new = self.value * other
        obj = ImpedanceType(self.freq, z_new)
        return obj

    def __rmul__(self, other):
        obj = self.__mul__(other)
        return obj

    def __truediv__(self, other):
        if isinstance(other, ImpedanceType):
            if other.freq == self.freq:
                z_new = self.value / other.value
            else:
                raise KeyboardInterrupt('频率不同不能运算')
        else:
            z_new = self.value / other
        obj = ImpedanceType(self.freq, z_new)
        return obj

    def __rtruediv__(self, other):
        z_new = other / self.value
        obj = ImpedanceType(self.freq, z_new)
        return obj

    def __floordiv__(self, other):
        if isinstance(other, ImpedanceType):
            if other.freq == self.freq:
                z_new = Impedance.parallel_z(self.z, other.z)
            else:
                raise KeyboardInterrupt('频率不同不能运算')
        else:
            raise KeyboardInterrupt('并联错误')
        obj = ImpedanceType(self.freq, z_new)
        return obj

    def get_branch(self, other):
        """
            获取并联支路
        """

        if isinstance(other, ImpedanceType):
            if other.freq == self.freq:
                z_new = self._value / (other._value - self._value) * other._value
            else:
                raise KeyboardInterrupt('频率不同不能运算')
        else:
            raise KeyboardInterrupt('并联错误')
        obj = ImpedanceType(self.freq)
        obj.z = z_new
        return obj

    def to_mult_freq(self, freqs: list):
        obj_m = MultiFreqImpType()
        for freq in freqs:
            obj = ImpedanceType(freq, self.z)
            obj_m.config_impedance(obj)
        return obj_m

    def __repr__(self):
        return str(self.value)


class ParaDescribe:
    """
        多频率阻抗类 -> 参数描述符
    """

    def __init__(self, prop):
        self.prop = prop

    def __get__(self, instance, owner):
        para_dict = dict()
        for freq in instance.freq_dict.keys():
            exec('para_dict[freq] = instance.freq_dict[freq].' + self.prop)
        return para_dict

    def __set__(self, instance, value):
        for freq in value.keys():
            instance.freq_dict[freq] = ImpedanceType(freq)
            exec('instance.freq_dict[freq].' + self.prop + ' = value[freq]')


# 多频率阻抗
class MultiFreqImpType:
    """
        多频率阻抗类
    """

    def __init__(self):
        self.freq_dict = {}

    z = ParaDescribe('z_complex')
    z_complex = ParaDescribe('z_complex')
    z_polar = ParaDescribe('z_polar')
    rlc_s = ParaDescribe('rlc_s')
    rlc_p = ParaDescribe('rlc_p')

    @property
    def freq(self):
        f = set(self.freq_dict.keys())
        return f

    def value(self, freq):
        return self[freq].z_complex

    def values(self):
        return self.freq_dict.values()

    def keys(self):
        return self.freq_dict.keys()

    def items(self):
        return self.freq_dict.items()

    def copy(self):
        return self.select_freqs(self.keys())

    def __repr__(self):
        return str(self.z)

    def __len__(self):
        return len(self.freq_dict)

    def __getitem__(self, key):
        return self.freq_dict[key]

    def config_impedance(self, value):
        if isinstance(value, ImpedanceType):
            self.freq_dict[value.freq] = value.copy()
        else:
            raise KeyboardInterrupt('类型异常: 参数需要为阻抗类型')

    def get_property(self, key):
        value = None
        try:
            value = self.freq_dict[key]
        except KeyError:
            pass
        return value

    def set_property(self, key, value_t):
        obj = ImpedanceType(key, value_t)
        self.config_impedance(obj)

    def pop_property(self, key):
        self.freq_dict.pop(key)

    def select_freqs(self, freqs):
        obj = MultiFreqImpType()
        for freq in freqs:
            obj.config_impedance(self[freq])
        return obj

    def convert_to_multi_freq(self, other):
        obj_m = MultiFreqImpType()
        if isinstance(other, MultiFreqImpType):
            obj_m = other.select_freqs(self.keys())
        else:
            for freq in self.keys():
                obj = ImpedanceType(freq, other)
                obj_m.config_impedance(obj)
        return obj_m

    def __add__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = MultiFreqImpType()
        for key in self.keys():
            obj.config_impedance(self[key] + other[key])
        return obj

    def __radd__(self, other):
        obj = self.__add__(other)
        return obj

    def __sub__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = self.__add__(-other)
        return obj

    def __rsub__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = other.__add__(-self)
        return obj

    def __neg__(self):
        obj = MultiFreqImpType()
        for key in self.keys():
            obj.config_impedance(-self[key])
        return obj

    def __mul__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = MultiFreqImpType()
        for key in self.keys():
            obj.config_impedance(self[key] * other[key])
        return obj

    def __rmul__(self, other):
        obj = self.__mul__(other)
        return obj

    def __truediv__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = MultiFreqImpType()
        for key in self.keys():
            obj.config_impedance(self[key] / other[key])
        return obj

    def __rtruediv__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = MultiFreqImpType()
        for key in self.keys():
            obj.config_impedance(other[key] / self[key])
        return obj

    def __floordiv__(self, other):
        other = self.convert_to_multi_freq(other)
        obj = MultiFreqImpType()
        for key in self.keys():
            obj.config_impedance(other[key] // self[key])
        return obj

    def get_branch(self, other):
        other = self.convert_to_multi_freq(other)
        obj = MultiFreqImpType()
        for key in self.keys():
            # obj.config_impedance(other[key] // self[key])
            obj.config_impedance(self[key].get_branch(other[key]))
        return obj


if __name__ == '__main__':
    pass
    # a = ImpedanceMultiFreq()
    # a.rlc_s = {
    #     # 1700: [1.539, 502e-6, None],
    #     1700: [1.539, 502.818e-6, None],
    #     2000: [1.595, 500e-6, None],
    #     2300: [1.652, 498e-6, None],
    #     2600: [1.712, 496e-6, None]}
    #
    # b = ImpedanceMultiFreq()
    # b.rlc_s = {
    #     # 1700: [221, 44.2e-3, None],
    #     1700: [221.835, 44.169e-3, None],
    #     2000: [253, 40.9e-3, None],
    #     2300: [277, 38.3e-3, None],
    #     2600: [298, 36.1e-3, None]}
    # c = ImpedanceWithFreq(1700)
    # c.z = 20
    #
    # d = c.copy()
    # d.freq = 1700

    # a = MultiFreqImpType()
    # # l1 = 0.38594e-3
    #
    # a.rlc_s = {
    #     1700: [None, None, 25e-6],
    #     2000: [None, None, 25e-6],
    #     2300: [None, None, 25e-6],
    #     2600: [None, None, 25e-6]}
    #
    # b = MultiFreqImpType()
    # c1 = 100e-6
    # b.rlc_s = {
    #     1700: [None, None, c1],
    #     2000: [None, None, c1],
    #     2300: [None, None, c1],
    #     2600: [None, None, c1]}
    #
    # # c = a + b
    #
    # c = a[2300].get_branch(b[2300])
    #
    # d = MultiFreqImpType()
    # l1 = 6.384447614514039e-05
    # d.rlc_s = {
    #     1700: [None, l1, None],
    #     2000: [None, l1, None],
    #     2300: [None, l1, None],
    #     2600: [None, l1, None]}
    #
    # e = b // d

    xxx = 10

    # yy = CapacitanceType()
    # yy.value = 0
    # yy.set_z(0, 1700)
    # a = Impedance.get_rlc_s(1 -1j/2/np.pi, 1)
    # b = Impedance.get_rlc_p(1 -1j/2/np.pi, 1)
    # c = Impedance.get_rlc_s(0, 1)
    # d = Impedance.get_rlc_p(0, 1)
    # e = Impedance.get_rlc_s(np.inf, 1)
    # f = Impedance.get_rlc_p(np.inf, 1)
    j = Impedance.get_rlc_s(1, 1)
    h = Impedance.get_rlc_p(1, 1)
    a = ResistanceType(12)
    b = InductanceType(10e-3)
    c = CapacitanceType(25*10e-6)

    xx = Impedance.rlc_p_to_z(freq=1/2/np.pi, idc=1, cpc=1)
    yy = Impedance.rlc_s_to_z(freq=1/2/np.pi, rss=-np.inf, idc=1, cpc=1)
    d = CapacitanceType(np.inf)
    aa = a.to_imp_type(1700)
    bb = b.to_imp_type(1700)
    cc = c.to_imp_type(1700)
    pass
