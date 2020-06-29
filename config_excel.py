import pandas as pd
import os
import time
import itertools


from Data2Excel import *


# 获取时间戳
localtime = time.localtime()
timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

filepath = 'C:\\Users\\李继隆\\Desktop\\干扰抑制电容设计'
# dir_path = 'C:\\Users\\李继隆\\Desktop\\干扰抑制电容设计\\结果导出'


# filename = '全TB被串单故障仿真.xlsx'
# filename = '全TB被串双故障仿真_副本.xlsx'
# filename = '全TB被串单故障仿真_副本.xlsx'
# filename = '双TB全换TB轨入电压_频率遍历.xlsx'
filename = '双TB加电容轨入电压_频率遍历.xlsx'
prefix = filename[:-5]

sheet_name = '数据输出'

path = os.path.join(filepath, filename)
df_input = pd.read_excel(path, sheet_name=sheet_name)
# df_input = pd.read_excel('邻线干扰参数输入_BPLN.xlsx')

df_input = df_input.where(df_input.notnull(), None)
num_len = len(list(df_input['序号']))

excel_data = []
data2excel = SheetDataGroup(sheet_names=[])

head_list = [
        '序号',
        '备注',

        '主串区段长度(m)', '被串区段长度(m)',

        '钢轨电阻(Ω/km)', '钢轨电感(H/km)',

        '耦合系数',
        '主串频率(Hz)', '被串频率(Hz)',
        '主串道床电阻(Ω·km)', '被串道床电阻(Ω·km)',
        '主串电容数(含TB)', '被串电容数(含TB)',
        '主串电容值(μF)', '被串电容值(μF)',

        # '主串抑制电容L1(μH)', '主串抑制电容C1(μF)', '主串抑制电容模式',
        # '被串抑制电容L2(μH)', '被串抑制电容C2(μF)', '被串抑制电容模式',

        '主串故障模式', '被串故障模式',
        # '主串故障位置', '被串故障位置',
        'TB模式',

        '主串分路电阻(Ω)', '被串分路电阻(Ω)',
        '主串电缆长度(km)', '被串电缆长度(km)',

        '分路间隔(m)',

        '主串电平级',
        '电源电压',

        # '是否全部更换TB',

        # '主串轨入电压(调整状态)',
        # '被串最大轨入电压(主备串同时分路状态)',

        # '被串最大干扰电流(A)', '被串最大干扰位置(m)',
        # '主串出口电流(A)', '主串入口电流(A)',
        # '被串轨入电压(调整状态)', '被串最大轨入电压(主被串同时分路状态)',
    ]

sheet_list = ['调整时被串轨入干扰电压(mV)', '分路时被串轨入最大干扰电压(mV)']
index_list = ['主串频率(Hz)', '被串频率(Hz)']

for temp_temp in range(num_len):

    df_input_row = df_input.iloc[temp_temp]
    # 数据表初始化
    data = dict()
    for key in head_list:
        data[key] = df_input_row[key]

    # fault_mode = eval(df_input_row['被串故障模式'])

    # mode_str = '全开路'
    # mode_str = '电感短路'
    # mode_str = '电感开路'
    # if not fault_mode[0] == mode_str:
    #     continue

    # fault_pst = eval(df_input_row['被串故障位置'])

    # fault_temp = fault_mode[0] + '_' + fault_mode[1]
    # sheet_temp = fault_mode[0]

    c_num = df_input_row['主串电容数(含TB)']
    length = df_input_row['主串区段长度(m)']
    str_temp = str(length) + 'm_' + str(c_num) + 'C'
    # if sheet_temp not in sheet_list:
    #     sheet_list.append(sheet_temp)
    if str_temp not in index_list:
        index_list.append(str_temp)

    # sheet_temp = sheet_list[0]

    # if fault_pst[0] == 1 and fault_pst[1] == 2:
    # if fault_pst[0] == 1:
    if c_num == 2:
        data2excel.add_new_row()
        data_row = [data[key] for key in head_list]
        excel_data.append(data_row)

        for sheet_temp in sheet_list:
            data_temp = df_input_row['主串频率(Hz)']
            data2excel.add_data(sheet_name=sheet_temp, data1=data_temp)

            data_temp = df_input_row['被串频率(Hz)']
            data2excel.add_data(sheet_name=sheet_temp, data1=data_temp)

        # data_temp = fault_mode
        # data_temp = fault_temp
        # data2excel.add_data(sheet_name=fault_temp, data1=data_temp)

    # i_trk_bei = round(df_input_row['被串最大干扰电流(A)'] * 1000, 2)
    v_rcv_bei = round(df_input_row['被串轨入电压(调整状态)'] * 1000, 2)
    v_rcv_shunt = round(df_input_row['被串最大轨入电压(主被串同时分路状态)'] * 1000, 2)

    # data2excel.add_data(sheet_name=sheet_temp, data1=i_trk_bei)
    data2excel.add_data(sheet_name=sheet_list[0], data1=v_rcv_bei)
    data2excel.add_data(sheet_name=sheet_list[1], data1=v_rcv_shunt)

C_7_1 = ['TB1', 'TB2', 'TB3', 'TB4', 'TB5', 'TB6', 'TB7']
C_7_2 = list(itertools.combinations([1, 2, 3, 4, 5, 6, 7], 2))


posi_header = ['主串频率(Hz)', '被串频率(Hz)']
# posi_header.extend(C_7_2)
posi_header.extend(C_7_1)
# posi_header = ['主串频率(Hz)', '被串频率(Hz)', '被串故障模式',
#                'TB1', 'TB2', 'TB3', 'TB4', 'TB5', 'TB6', 'TB7', ]

posi_header = index_list
data2excel.config_header()

for temp in sheet_list:
    data2excel[temp].data_list.insert(0, posi_header)
    data2excel[temp].config_header(header=False)

df_data = pd.DataFrame(excel_data, columns=head_list)

#################################################################################

# 保存到本地excel

filepath = '数据整理_' + prefix + '_' + timestamp + '.xlsx'

with pd.ExcelWriter(filepath) as writer:
    # if pd_read_flag:
    #     df_input.to_excel(writer, sheet_name="参数设置", index=False)
    df_data.to_excel(writer, sheet_name="数据输出", index=False)

    # names = [
    #     "故障位置遍历",
    # ]

    names = sheet_list
    # data2excel.write2excel(sheet_names=names, header=None, writer1=writer)
    # data2excel.write2excel(sheet_names=names, header=posi_header, writer1=writer)
    data2excel.write2excel(sheet_names=names, writer=writer)

    pass