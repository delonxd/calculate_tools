from TrackCircuitElement.Parameter import TADXfmrParam
from TrackCircuitElement.ParamType import MultiFreqImpType
import pickle


if __name__ == '__main__':
    param = dict()

    param1 = TADXfmrParam('TAD_发送端_区间')
    param[param1.name] = param1

    param1.z1 = MultiFreqImpType()
    param1.z1.rlc_s = {
        1700: (3.9146, 581.14e-6, None),
        2000: (3.9695, 684.89e-6, None),
        2300: (3.8636, 769.06e-6, None),
        2600: (3.7937, 959.15e-6, None),
    }

    param1.z2 = MultiFreqImpType()
    param1.z2.rlc_s = {
        1700: (3.0451e3, 551.191e-3, None),
        2000: (3.1163e3, 580.653e-3, None),
        2300: (3.1775e3, 605.011e-3, None),
        2600: (3.2591e3, 635.065e-3, None),
    }

    param1.z3 = MultiFreqImpType()
    param1.z3.rlc_s = {
        1700: (250e-3, 4.2e-3, None),
        2000: (250e-3, 4.2e-3, None),
        2300: (250e-3, 4.2e-3, None),
        2600: (250e-3, 4.2e-3, None),
    }

    param1.zc = MultiFreqImpType()
    param1.zc.rlc_s = {
        1700: (None, None, 4.7e-3),
        2000: (None, None, 4.7e-3),
        2300: (None, None, 4.7e-3),
        2600: (None, None, 4.7e-3),
    }

    param1.n = {
        1700: 8.9202,
        2000: 8.8912,
        2300: 8.8508,
        2600: 8.8688,
    }


    # with open('../parameter_pkl/Parameter_TAD.pkl', 'wb') as pk_f:
    #     pickle.dump(param1, pk_f)
    pass