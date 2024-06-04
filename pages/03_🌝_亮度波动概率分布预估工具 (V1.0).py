import numpy as np
import pandas as pd
import streamlit as st
import time
import math
from numba import njit

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具可以计算影响因子为5~15个的亮度波动概率分布</h4>", unsafe_allow_html=True)

# # # 工具名称、版本号
st.write("# 亮度波动概率计算工具 #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V1.0</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2024/03/20</h5>", unsafe_allow_html=True)
# # # 设置步骤1
col1, col2 = st.columns([2, 1])
bz1_1, bz1_2 = st.columns([1, 20])
with col1:
    st.write("<h6>步骤1：上传各影响因子透过率及概率分布TXT文件</h6>", unsafe_allow_html=True)

# 初始化l值
l = 0

with bz1_2:
    # 创建文件上传按钮
    fp_trans = st.file_uploader("请上传TXT文件，请确保最后一组影响因子为BLU亮度分布！", type=['txt'], help="请选择TXT文件进行上传", key='fp_trans')
    if fp_trans is not None:
        trans = pd.read_csv(fp_trans, header=None, sep="\t", skip_blank_lines=True)  # 使用pandas来读取txt，sep="t"为逗号分隔符
        trans1 = round(trans, 6)  # 用于计算行数的dataframe series
        trans2 = trans1.values  # Dataframe转换为ndarray

        # 获取影响因子个数
        l = int(trans.iloc[0, :].dropna().shape[0] / 2)
        # 获取每个影响因子的step数
        m = np.zeros((l, 1))
        for i in range(l):
            m[i] = int(trans1.iloc[:, i * 2].dropna().shape[0])

# # # 设置步骤2
col3, col4 = st.columns([2, 1])
bz2_1, bz2_2, bz2_3 = st.columns([1, 3, 15])
with col3:
    st.write("<h6>步骤2：设置透过率和BLU亮度精度</h6>", unsafe_allow_html=True)
with bz2_2:
    # 创建前p组数据的透过率矩阵，透过率分布按照min和max，精度0.01
    vac_trans = st.number_input(label='透过率精度', value=0.01, format='%f', key='trans_vac')
    vac_lum = st.number_input(label='BLU亮度精度', value=200, key='blu_vac')
    # vac_trans = 0.01  #输入panel透过率step精度
    # vac_lum = 200  #输入BLU亮度step精度
    p = int(math.floor((l - 1) / 2) + 1)  #输入前几个因子进行乘积
    # print(p)

    # 遍历前p个因子中最小值进行乘积得到前p列的trans最小值min1，同理获得前p列的trans最大值max1
    min1 = 1
    max1 = 1
    for i in range(p):
        min_trans1 = min(trans2[0:int(m[i, 0]), i * 2])
        max_trans1 = max(trans2[0:int(m[i, 0]), i * 2])
        min1 *= min_trans1
        max1 *= max_trans1
    min1 = math.floor(min1 * 100) / 100
    max1 = math.ceil(max1 * 100) / 100

    stp1 = int(math.ceil((max1 - min1) / vac_trans) + 1)
    # print(min1, max1, stp1)

    trans_step = np.zeros((stp1, 2))

    for i in range(stp1):
        trans_step[i, 0] = min1 + i * vac_trans
    start1 = np.zeros((stp1, 1))
    end1 = np.zeros((stp1, 1))
    for i in range(stp1):
        start1[i] = trans_step[i, 0] - vac_trans / 2
        end1[i] = trans_step[i, 0] + vac_trans / 2

    # 遍历所有trans因子中最小值进行乘积得到trans最小值min2，同理获得trans最大值max2
    min2 = 1
    max2 = 1
    for i in range(l - 1):
        min_trans2 = min(trans2[0:int(m[i, 0]), i * 2])
        max_trans2 = max(trans2[0:int(m[i, 0]), i * 2])
        min2 *= min_trans2
        max2 *= max_trans2
    min2 = math.floor(min2 * 100) / 100
    max2 = math.ceil(max2 * 100) / 100

    stp2 = int(math.ceil((max2 - min2) / vac_trans) + 1)
    # print(min2, max2, stp2)

    Final_trans_step = np.zeros((stp2, 2))
    for i in range(stp2):
        Final_trans_step[i, 0] = min2 + i * vac_trans

    start2 = np.zeros((stp2, 1))
    end2 = np.zeros((stp2, 1))
    for i in range(stp2):
        start2[i] = Final_trans_step[i, 0] - vac_trans / 2
        end2[i] = Final_trans_step[i, 0] + vac_trans / 2

    # 遍历所有lum因子中最小值进行乘积得到lum最小值min3，同理获得lum最大值max3
    min3 = 1
    max3 = 1
    for i in range(l):
        min_trans3 = min(trans2[0:int(m[i, 0]), i * 2])
        max_trans3 = max(trans2[0:int(m[i, 0]), i * 2])
        min3 *= min_trans3
        max3 *= max_trans3
    min3 = math.floor(min3 / 100) * 100
    max3 = math.ceil(max3 / 100) * 100
    stp3 = int(math.ceil((max3 - min3) / vac_lum) + 1)
    # print(min3, max3, stp3)

    Final_lum_step = np.zeros((stp3, 2))
    for i in range(stp3):
        Final_lum_step[i, 0] = min3 + i * vac_lum

    start3 = np.zeros((stp3, 1))
    end3 = np.zeros((stp3, 1))
    for i in range(stp3):
        start3[i] = Final_lum_step[i, 0] - vac_lum / 2
        end3[i] = Final_lum_step[i, 0] + vac_lum / 2

# 获取代码执行前时间戳
start_time = time.time()

@njit # (nopython=True)

def main_code(trans2, l, m, start1, end1, start2, end2, start3, end3, trans_step, Final_trans_step, Final_lum_step):
    if l == 5:
        # seq1 = trans2[0:int(m[0, 0]), 0]
        # val1 = trans2[0:int(m[0, 0]), 1]
        # seq2 = trans2[0:int(m[1, 0]), 2]
        # val2 = trans2[0:int(m[1, 0]), 3]
        # seq3 = trans2[0:int(m[2, 0]), 4]
        # val3 = trans2[0:int(m[2, 0]), 5]
        # seq4 = trans2[0:int(m[3, 0]), 6]
        # val4 = trans2[0:int(m[3, 0]), 7]
        # seq5 = trans2[0:int(m[4, 0]), 8]
        # val5 = trans2[0:int(m[4, 0]), 9]
        # seq6 = trans2[0:int(m[5, 0]), 10]

        seq1 = trans2[0:m[0, 0], 0]
        val1 = trans2[0:m[0, 0], 1]
        seq2 = trans2[0:m[1, 0], 2]
        val2 = trans2[0:m[1, 0], 3]
        seq3 = trans2[0:m[2, 0], 4]
        val3 = trans2[0:m[2, 0], 5]
        seq4 = trans2[0:m[3, 0], 6]
        val4 = trans2[0:m[3, 0], 7]
        seq5 = trans2[0:m[4, 0], 8]
        val5 = trans2[0:m[4, 0], 9]

        # 创建dict文件
        dict1 = dict(zip(seq1, val1))
        dict2 = dict(zip(seq2, val2))
        dict3 = dict(zip(seq3, val3))
        dict4 = dict(zip(seq4, val4))
        dict5 = dict(zip(seq5, val5))

        # 将前4个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                        for key4, value4 in dict4.items():
                            T1 = key1 * key2 * key3 * key4
                            V1 = value1 * value2 * value3 * value4
                            for i in range(stp1):
                                if start2[i] <= T1 <= end2[i]:
                                # 如果key在该区间内，则将该区间的value累加
                                    Final_trans_step[i, 1] += V1

        dict_trans = dict(zip(Final_trans_step[:, 0], Final_trans_step[:, 1]))

        for key_trans, value_trans in dict_trans.items():
            for key_blu, value_blu in dict5.items():
                T3 = key_trans * key_blu
                V3 = value_trans * value_blu
                for i in range(stp3):
                    if start3[i] <= T3 <= end3[i]:
                    # 如果key在该区间内，则将该区间的value累加
                        Final_lum_step[i, 1] += V3
    elif l == 6:
        # seq1 = trans2[0:int(m[0, 0]), 0]
        # val1 = trans2[0:int(m[0, 0]), 1]
        # seq2 = trans2[0:int(m[1, 0]), 2]
        # val2 = trans2[0:int(m[1, 0]), 3]
        # seq3 = trans2[0:int(m[2, 0]), 4]
        # val3 = trans2[0:int(m[2, 0]), 5]
        # seq4 = trans2[0:int(m[3, 0]), 6]
        # val4 = trans2[0:int(m[3, 0]), 7]
        # seq5 = trans2[0:int(m[4, 0]), 8]
        # val5 = trans2[0:int(m[4, 0]), 9]
        # seq6 = trans2[0:int(m[5, 0]), 10]
        # val6 = trans2[0:int(m[5, 0]), 11]

        seq1 = trans2[0:m[0, 0], 0]
        val1 = trans2[0:m[0, 0], 1]
        seq2 = trans2[0:m[1, 0], 2]
        val2 = trans2[0:m[1, 0], 3]
        seq3 = trans2[0:m[2, 0], 4]
        val3 = trans2[0:m[2, 0], 5]
        seq4 = trans2[0:m[3, 0], 6]
        val4 = trans2[0:m[3, 0], 7]
        seq5 = trans2[0:m[4, 0], 8]
        val5 = trans2[0:m[4, 0], 9]
        seq6 = trans2[0:m[5, 0], 10]
        val6 = trans2[0:m[5, 0], 11]

        # 创建dict文件
        dict1 = dict(zip(seq1, val1))
        dict2 = dict(zip(seq2, val2))
        dict3 = dict(zip(seq3, val3))
        dict4 = dict(zip(seq4, val4))
        dict5 = dict(zip(seq5, val5))
        dict6 = dict(zip(seq6, val6))

        # 将前5个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            T1 = key1 * key2 * key3 * key4 * key5
                            V1 = value1 * value2 * value3 * value4 * value5
                            for i in range(stp1):
                                if start2[i] <= T1 <= end2[i]:
                                # 如果key在该区间内，则将该区间的value累加
                                    Final_trans_step[i, 1] += V1

        dict_trans = dict(zip(Final_trans_step[:, 0], Final_trans_step[:, 1]))

        for key_trans, value_trans in dict_trans.items():
            for key_blu, value_blu in dict6.items():
                T3 = key_trans * key_blu
                V3 = value_trans * value_blu
                for i in range(stp3):
                    if start3[i] <= T3 <= end3[i]:
                    # 如果key在该区间内，则将该区间的value累加
                        Final_lum_step[i, 1] += V3

    elif l == 7:
        # seq1 = trans2[0:int(m[0, 0]), 0]
        # val1 = trans2[0:int(m[0, 0]), 1]
        # seq2 = trans2[0:int(m[1, 0]), 2]
        # val2 = trans2[0:int(m[1, 0]), 3]
        # seq3 = trans2[0:int(m[2, 0]), 4]
        # val3 = trans2[0:int(m[2, 0]), 5]
        # seq4 = trans2[0:int(m[3, 0]), 6]
        # val4 = trans2[0:int(m[3, 0]), 7]
        # seq5 = trans2[0:int(m[4, 0]), 8]
        # val5 = trans2[0:int(m[4, 0]), 9]
        # seq6 = trans2[0:int(m[5, 0]), 10]
        # val6 = trans2[0:int(m[5, 0]), 11]
        # seq7 = trans2[0:int(m[6, 0]), 12]
        # val7 = trans2[0:int(m[6, 0]), 13]

        seq1 = trans2[0:m[0, 0], 0]
        val1 = trans2[0:m[0, 0], 1]
        seq2 = trans2[0:m[1, 0], 2]
        val2 = trans2[0:m[1, 0], 3]
        seq3 = trans2[0:m[2, 0], 4]
        val3 = trans2[0:m[2, 0], 5]
        seq4 = trans2[0:m[3, 0], 6]
        val4 = trans2[0:m[3, 0], 7]
        seq5 = trans2[0:m[4, 0], 8]
        val5 = trans2[0:m[4, 0], 9]
        seq6 = trans2[0:m[5, 0], 10]
        val6 = trans2[0:m[5, 0], 11]
        seq7 = trans2[0:m[6, 0], 12]
        val7 = trans2[0:m[6, 0], 13]

        # 创建dict文件
        dict1 = dict(zip(seq1, val1))
        dict2 = dict(zip(seq2, val2))
        dict3 = dict(zip(seq3, val3))
        dict4 = dict(zip(seq4, val4))
        dict5 = dict(zip(seq5, val5))
        dict6 = dict(zip(seq6, val6))
        dict7 = dict(zip(seq7, val7))

        # 将前6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                T1 = key1 * key2 * key3 * key4 * key5 * key6
                                V1 = value1 * value2 * value3 * value4 * value5 * value6
                                for i in range(stp1):
                                    if start2[i] <= T1 <= end2[i]:
                                    # 如果key在该区间内，则将该区间的value累加
                                        Final_trans_step[i, 1] += V1

        dict_trans = dict(zip(Final_trans_step[:, 0], Final_trans_step[:, 1]))

        for key_trans, value_trans in dict_trans.items():
            for key_blu, value_blu in dict7.items():
                T3 = key_trans * key_blu
                V3 = value_trans * value_blu
                for i in range(stp3):
                    if start3[i] <= T3 <= end3[i]:
                    # 如果key在该区间内，则将该区间的value累加
                        Final_lum_step[i, 1] += V3

    elif l == 8:
        # seq1 = trans2[0:int(m[0, 0]), 0]
        # val1 = trans2[0:int(m[0, 0]), 1]
        # seq2 = trans2[0:int(m[1, 0]), 2]
        # val2 = trans2[0:int(m[1, 0]), 3]
        # seq3 = trans2[0:int(m[2, 0]), 4]
        # val3 = trans2[0:int(m[2, 0]), 5]
        # seq4 = trans2[0:int(m[3, 0]), 6]
        # val4 = trans2[0:int(m[3, 0]), 7]
        # seq5 = trans2[0:int(m[4, 0]), 8]
        # val5 = trans2[0:int(m[4, 0]), 9]
        # seq6 = trans2[0:int(m[5, 0]), 10]
        # val6 = trans2[0:int(m[5, 0]), 11]
        # seq7 = trans2[0:int(m[6, 0]), 12]
        # val7 = trans2[0:int(m[6, 0]), 13]
        # seq8 = trans2[0:int(m[7, 0]), 14]
        # val8 = trans2[0:int(m[7, 0]), 15]

        seq1 = trans2[0:m[0, 0], 0]
        val1 = trans2[0:m[0, 0], 1]
        seq2 = trans2[0:m[1, 0], 2]
        val2 = trans2[0:m[1, 0], 3]
        seq3 = trans2[0:m[2, 0], 4]
        val3 = trans2[0:m[2, 0], 5]
        seq4 = trans2[0:m[3, 0], 6]
        val4 = trans2[0:m[3, 0], 7]
        seq5 = trans2[0:m[4, 0], 8]
        val5 = trans2[0:m[4, 0], 9]
        seq6 = trans2[0:m[5, 0], 10]
        val6 = trans2[0:m[5, 0], 11]
        seq7 = trans2[0:m[6, 0], 12]
        val7 = trans2[0:m[6, 0], 13]
        seq8 = trans2[0:m[7, 0], 14]
        val8 = trans2[0:m[7, 0], 15]

        # 创建dict文件
        dict1 = dict(zip(seq1, val1))
        dict2 = dict(zip(seq2, val2))
        dict3 = dict(zip(seq3, val3))
        dict4 = dict(zip(seq4, val4))
        dict5 = dict(zip(seq5, val5))
        dict6 = dict(zip(seq6, val6))
        dict7 = dict(zip(seq7, val7))
        dict8 = dict(zip(seq8, val8))

        # 将前4个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        T1 = key1 * key2 * key3 * key4
                        V1 = value1 * value2 * value3 * value4
                        for i in range(stp1):
                            if start1[i] <= T1 <= end1[i]:
                            # 如果key在该区间内，则将该区间的value累加
                                trans_step[i, 1] += V1

        dict1_4 = dict(zip(trans_step[:, 0], trans_step[:, 1]))

        for key1_4, value1_4 in dict1_4.items():
            for key5, value5 in dict5.items():
                for key6, value6 in dict6.items():
                    for key7, value7 in dict7.items():
                        T2 = key1_4 * key5 * key6 * key7
                        V2 = value1_4 * value5 * value6 * value7
                        for i in range(stp2):
                            if start2[i] <= T2 <= end2[i]:
                            # 如果key在该区间内，则将该区间的value累加
                                Final_trans_step[i, 1] += V2

        dict_trans = dict(zip(Final_trans_step[:, 0], Final_trans_step[:, 1]))

        for key_trans, value_trans in dict_trans.items():
            for key_blu, value_blu in dict8.items():
                T3 = key_trans * key_blu
                V3 = value_trans * value_blu
                for i in range(stp3):
                    if start3[i] <= T3 <= end3[i]:
                    # 如果key在该区间内，则将该区间的value累加
                        Final_lum_step[i, 1] += V3
    
    elif l == 9:
        # seq1 = trans2[0:int(m[0, 0]), 0]
        # val1 = trans2[0:int(m[0, 0]), 1]
        # seq2 = trans2[0:int(m[1, 0]), 2]
        # val2 = trans2[0:int(m[1, 0]), 3]
        # seq3 = trans2[0:int(m[2, 0]), 4]
        # val3 = trans2[0:int(m[2, 0]), 5]
        # seq4 = trans2[0:int(m[3, 0]), 6]
        # val4 = trans2[0:int(m[3, 0]), 7]
        # seq5 = trans2[0:int(m[4, 0]), 8]
        # val5 = trans2[0:int(m[4, 0]), 9]
        # seq6 = trans2[0:int(m[5, 0]), 10]
        # val6 = trans2[0:int(m[5, 0]), 11]
        # seq7 = trans2[0:int(m[6, 0]), 12]
        # val7 = trans2[0:int(m[6, 0]), 13]
        # seq8 = trans2[0:int(m[7, 0]), 14]
        # val8 = trans2[0:int(m[7, 0]), 15]
        # seq9 = trans2[0:int(m[8, 0]), 16]
        # val9 = trans2[0:int(m[8, 0]), 17]

        seq1 = trans2[0:m[0, 0], 0]
        val1 = trans2[0:m[0, 0], 1]
        seq2 = trans2[0:m[1, 0], 2]
        val2 = trans2[0:m[1, 0], 3]
        seq3 = trans2[0:m[2, 0], 4]
        val3 = trans2[0:m[2, 0], 5]
        seq4 = trans2[0:m[3, 0], 6]
        val4 = trans2[0:m[3, 0], 7]
        seq5 = trans2[0:m[4, 0], 8]
        val5 = trans2[0:m[4, 0], 9]
        seq6 = trans2[0:m[5, 0], 10]
        val6 = trans2[0:m[5, 0], 11]
        seq7 = trans2[0:m[6, 0], 12]
        val7 = trans2[0:m[6, 0], 13]
        seq8 = trans2[0:m[7, 0], 14]
        val8 = trans2[0:m[7, 0], 15]
        seq9 = trans2[0:m[8, 0], 16]
        val9 = trans2[0:m[8, 0], 17]

        # 创建dict文件
        dict1 = dict(zip(seq1, val1))
        dict2 = dict(zip(seq2, val2))
        dict3 = dict(zip(seq3, val3))
        dict4 = dict(zip(seq4, val4))
        dict5 = dict(zip(seq5, val5))
        dict6 = dict(zip(seq6, val6))
        dict7 = dict(zip(seq7, val7))
        dict8 = dict(zip(seq8, val8))
        dict9 = dict(zip(seq9, val9))

        # 将前5个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            T1 = key1 * key2 * key3 * key4 * key5
                            V1 = value1 * value2 * value3 * value4 * value5
                            for i in range(stp1):
                                if start1[i] <= T1 <= end1[i]:
                                # 如果key在该区间内，则将该区间的value累加
                                    trans_step[i, 1] += V1

        dict1_5 = dict(zip(trans_step[:, 0], trans_step[:, 1]))

        for key1_5, value1_5 in dict1_5.items():
            for key6, value6 in dict6.items():
                for key7, value7 in dict7.items():
                    for key8, value8 in dict8.items():
                        T2 = key1_5 * key5 * key6 * key7 * key8
                        V2 = value1_5 * value5 * value6 * value7 * value8
                        for i in range(stp2):
                            if start2[i] <= T2 <= end2[i]:
                            # 如果key在该区间内，则将该区间的value累加
                                Final_trans_step[i, 1] += V2

        dict_trans = dict(zip(Final_trans_step[:, 0], Final_trans_step[:, 1]))

        for key_trans, value_trans in dict_trans.items():
            for key_blu, value_blu in dict9.items():
                T3 = key_trans * key_blu
                V3 = value_trans * value_blu
                for i in range(stp3):
                    if start3[i] <= T3 <= end3[i]:
                    # 如果key在该区间内，则将该区间的value累加
                        Final_lum_step[i, 1] += V3
    
    elif l == 10:
        # seq1 = trans2[0:int(m[0, 0]), 0]
        # val1 = trans2[0:int(m[0, 0]), 1]
        # seq2 = trans2[0:int(m[1, 0]), 2]
        # val2 = trans2[0:int(m[1, 0]), 3]
        # seq3 = trans2[0:int(m[2, 0]), 4]
        # val3 = trans2[0:int(m[2, 0]), 5]
        # seq4 = trans2[0:int(m[3, 0]), 6]
        # val4 = trans2[0:int(m[3, 0]), 7]
        # seq5 = trans2[0:int(m[4, 0]), 8]
        # val5 = trans2[0:int(m[4, 0]), 9]
        # seq6 = trans2[0:int(m[5, 0]), 10]
        # val6 = trans2[0:int(m[5, 0]), 11]
        # seq7 = trans2[0:int(m[6, 0]), 12]
        # val7 = trans2[0:int(m[6, 0]), 13]
        # seq8 = trans2[0:int(m[7, 0]), 14]
        # val8 = trans2[0:int(m[7, 0]), 15]
        # seq9 = trans2[0:int(m[8, 0]), 16]
        # val9 = trans2[0:int(m[8, 0]), 17]
        # seq10 = trans2[0:int(m[9, 0]), 18]
        # val10 = trans2[0:int(m[9, 0]), 19]

        seq1 = trans2[0:m[0, 0], 0]
        val1 = trans2[0:m[0, 0], 1]
        seq2 = trans2[0:m[1, 0], 2]
        val2 = trans2[0:m[1, 0], 3]
        seq3 = trans2[0:m[2, 0], 4]
        val3 = trans2[0:m[2, 0], 5]
        seq4 = trans2[0:m[3, 0], 6]
        val4 = trans2[0:m[3, 0], 7]
        seq5 = trans2[0:m[4, 0], 8]
        val5 = trans2[0:m[4, 0], 9]
        seq6 = trans2[0:m[5, 0], 10]
        val6 = trans2[0:m[5, 0], 11]
        seq7 = trans2[0:m[6, 0], 12]
        val7 = trans2[0:m[6, 0], 13]
        seq8 = trans2[0:m[7, 0], 14]
        val8 = trans2[0:m[7, 0], 15]
        seq9 = trans2[0:m[8, 0], 16]
        val9 = trans2[0:m[8, 0], 17]
        seq10 = trans2[0:m[9, 0], 18]
        val10 = trans2[0:m[9, 0], 19]

        # 创建dict文件
        dict1 = dict(zip(seq1, val1))
        dict2 = dict(zip(seq2, val2))
        dict3 = dict(zip(seq3, val3))
        dict4 = dict(zip(seq4, val4))
        dict5 = dict(zip(seq5, val5))
        dict6 = dict(zip(seq6, val6))
        dict7 = dict(zip(seq7, val7))
        dict8 = dict(zip(seq8, val8))
        dict9 = dict(zip(seq9, val9))
        dict10 = dict(zip(seq10, val10))

        # 将前5个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            T1 = key1 * key2 * key3 * key4 * key5
                            V1 = value1 * value2 * value3 * value4 * value5
                            for i in range(stp1):
                                if start1[i] <= T1 <= end1[i]:
                                # 如果key在该区间内，则将该区间的value累加
                                    trans_step[i, 1] += V1

        dict1_5 = dict(zip(trans_step[:, 0], trans_step[:, 1]))

        for key1_5, value1_5 in dict1_5.items():
            for key6, value6 in dict6.items():
                for key7, value7 in dict7.items():
                    for key8, value8 in dict8.items():
                        for key9, value9 in dict9.items():
                            T2 = key1_5 * key6 * key7 * key8 * key9
                            V2 = value1_5 * value6 * value7 * value8 * value9
                            for i in range(stp2):
                                if start2[i] <= T2 <= end2[i]:
                                # 如果key在该区间内，则将该区间的value累加
                                    Final_trans_step[i, 1] += V2

        dict_trans = dict(zip(Final_trans_step[:, 0], Final_trans_step[:, 1]))

        for key_trans, value_trans in dict_trans.items():
            for key_blu, value_blu in dict10.items():
                T3 = key_trans * key_blu
                V3 = value_trans * value_blu
                for i in range(stp3):
                    if start3[i] <= T3 <= end3[i]:
                    # 如果key在该区间内，则将该区间的value累加
                        Final_lum_step[i, 1] += V3
    
    elif l == 11:
        # seq1 = trans2[0:int(m[0, 0]), 0]
        # val1 = trans2[0:int(m[0, 0]), 1]
        # seq2 = trans2[0:int(m[1, 0]), 2]
        # val2 = trans2[0:int(m[1, 0]), 3]
        # seq3 = trans2[0:int(m[2, 0]), 4]
        # val3 = trans2[0:int(m[2, 0]), 5]
        # seq4 = trans2[0:int(m[3, 0]), 6]
        # val4 = trans2[0:int(m[3, 0]), 7]
        # seq5 = trans2[0:int(m[4, 0]), 8]
        # val5 = trans2[0:int(m[4, 0]), 9]
        # seq6 = trans2[0:int(m[5, 0]), 10]
        # val6 = trans2[0:int(m[5, 0]), 11]
        # seq7 = trans2[0:int(m[6, 0]), 12]
        # val7 = trans2[0:int(m[6, 0]), 13]
        # seq8 = trans2[0:int(m[7, 0]), 14]
        # val8 = trans2[0:int(m[7, 0]), 15]
        # seq9 = trans2[0:int(m[8, 0]), 16]
        # val9 = trans2[0:int(m[8, 0]), 17]
        # seq10 = trans2[0:int(m[9, 0]), 18]
        # val10 = trans2[0:int(m[9, 0]), 19]
        # seq11 = trans2[0:int(m[10, 0]), 20]
        # val11 = trans2[0:int(m[10, 0]), 21]

        seq1 = trans2[0:m[0, 0], 0]
        val1 = trans2[0:m[0, 0], 1]
        seq2 = trans2[0:m[1, 0], 2]
        val2 = trans2[0:m[1, 0], 3]
        seq3 = trans2[0:m[2, 0], 4]
        val3 = trans2[0:m[2, 0], 5]
        seq4 = trans2[0:m[3, 0], 6]
        val4 = trans2[0:m[3, 0], 7]
        seq5 = trans2[0:m[4, 0], 8]
        val5 = trans2[0:m[4, 0], 9]
        seq6 = trans2[0:m[5, 0], 10]
        val6 = trans2[0:m[5, 0], 11]
        seq7 = trans2[0:m[6, 0], 12]
        val7 = trans2[0:m[6, 0], 13]
        seq8 = trans2[0:m[7, 0], 14]
        val8 = trans2[0:m[7, 0], 15]
        seq9 = trans2[0:m[8, 0], 16]
        val9 = trans2[0:m[8, 0], 17]
        seq10 = trans2[0:m[9, 0], 18]
        val10 = trans2[0:m[9, 0], 19]
        seq11 = trans2[0:m[10, 0], 20]
        val11 = trans2[0:m[10, 0], 21]

        # 创建dict文件
        dict1 = dict(zip(seq1, val1))
        dict2 = dict(zip(seq2, val2))
        dict3 = dict(zip(seq3, val3))
        dict4 = dict(zip(seq4, val4))
        dict5 = dict(zip(seq5, val5))
        dict6 = dict(zip(seq6, val6))
        dict7 = dict(zip(seq7, val7))
        dict8 = dict(zip(seq8, val8))
        dict9 = dict(zip(seq9, val9))
        dict10 = dict(zip(seq10, val10))
        dict11 = dict(zip(seq11, val11))

        # 将前6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                T1 = key1 * key2 * key3 * key4 * key5 * key6
                                V1 = value1 * value2 * value3 * value4 * value5 * value6
                                for i in range(stp1):
                                    if start1[i] <= T1 <= end1[i]:
                                    # 如果key在该区间内，则将该区间的value累加
                                        trans_step[i, 1] += V1

        dict1_6 = dict(zip(trans_step[:, 0], trans_step[:, 1]))

        for key1_6, value1_6 in dict1_6.items():
            for key7, value7 in dict7.items():
                for key8, value8 in dict8.items():
                    for key9, value9 in dict9.items():
                        for key10, value10 in dict10.items():
                            T2 = key1_6 * key7 * key8 * key9 * key10
                            V2 = value1_6 * value7 * value8 * value9 * value10
                            for i in range(stp2):
                                if start2[i] <= T2 <= end2[i]:
                                # 如果key在该区间内，则将该区间的value累加
                                    Final_trans_step[i, 1] += V2

        dict_trans = dict(zip(Final_trans_step[:, 0], Final_trans_step[:, 1]))

        for key_trans, value_trans in dict_trans.items():
            for key_blu, value_blu in dict11.items():
                T3 = key_trans * key_blu
                V3 = value_trans * value_blu
                for i in range(stp3):
                    if start3[i] <= T3 <= end3[i]:
                    # 如果key在该区间内，则将该区间的value累加
                        Final_lum_step[i, 1] += V3
    
    elif l == 12:
        seq1 = trans2[0:m[0, 0], 0]
        val1 = trans2[0:m[0, 0], 1]
        seq2 = trans2[0:m[1, 0], 2]
        val2 = trans2[0:m[1, 0], 3]
        seq3 = trans2[0:m[2, 0], 4]
        val3 = trans2[0:m[2, 0], 5]
        seq4 = trans2[0:m[3, 0], 6]
        val4 = trans2[0:m[3, 0], 7]
        seq5 = trans2[0:m[4, 0], 8]
        val5 = trans2[0:m[4, 0], 9]
        seq6 = trans2[0:m[5, 0], 10]
        val6 = trans2[0:m[5, 0], 11]
        seq7 = trans2[0:m[6, 0], 12]
        val7 = trans2[0:m[6, 0], 13]
        seq8 = trans2[0:m[7, 0], 14]
        val8 = trans2[0:m[7, 0], 15]
        seq9 = trans2[0:m[8, 0], 16]
        val9 = trans2[0:m[8, 0], 17]
        seq10 = trans2[0:m[9, 0], 18]
        val10 = trans2[0:m[9, 0], 19]
        seq11 = trans2[0:m[10, 0], 20]
        val11 = trans2[0:m[10, 0], 21]
        seq12 = trans2[0:m[11, 0], 22]
        val12 = trans2[0:m[11, 0], 23]

        # 创建dict文件
        dict1 = dict(zip(seq1, val1))
        dict2 = dict(zip(seq2, val2))
        dict3 = dict(zip(seq3, val3))
        dict4 = dict(zip(seq4, val4))
        dict5 = dict(zip(seq5, val5))
        dict6 = dict(zip(seq6, val6))
        dict7 = dict(zip(seq7, val7))
        dict8 = dict(zip(seq8, val8))
        dict9 = dict(zip(seq9, val9))
        dict10 = dict(zip(seq10, val10))
        dict11 = dict(zip(seq11, val11))
        dict12 = dict(zip(seq12, val12))

        # 将前6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                T1 = key1 * key2 * key3 * key4 * key5 * key6
                                V1 = value1 * value2 * value3 * value4 * value5 * value6
                                for i in range(stp1):
                                    if start1[i] <= T1 <= end1[i]:
                                    # 如果key在该区间内，则将该区间的value累加
                                        trans_step[i, 1] += V1

        dict1_6 = dict(zip(trans_step[:, 0], trans_step[:, 1]))

        for key1_6, value1_6 in dict1_6.items():
            for key7, value7 in dict7.items():
                for key8, value8 in dict8.items():
                    for key9, value9 in dict9.items():
                        for key10, value10 in dict10.items():
                            for key11, value11 in dict11.items():
                                T2 = key1_6 * key7 * key8 * key9 * key10 * key11
                                V2 = value1_6 * value7 * value8 * value9 * value10 * value11
                                for i in range(stp2):
                                    if start2[i] <= T2 <= end2[i]:
                                    # 如果key在该区间内，则将该区间的value累加
                                        Final_trans_step[i, 1] += V2

        dict_trans = dict(zip(Final_trans_step[:, 0], Final_trans_step[:, 1]))

        for key_trans, value_trans in dict_trans.items():
            for key_blu, value_blu in dict12.items():
                T3 = key_trans * key_blu
                V3 = value_trans * value_blu
                for i in range(stp3):
                    if start3[i] <= T3 <= end3[i]:
                    # 如果key在该区间内，则将该区间的value累加
                        Final_lum_step[i, 1] += V3

    elif l == 13:
        seq1 = trans2[0:m[0, 0], 0]
        val1 = trans2[0:m[0, 0], 1]
        seq2 = trans2[0:m[1, 0], 2]
        val2 = trans2[0:m[1, 0], 3]
        seq3 = trans2[0:m[2, 0], 4]
        val3 = trans2[0:m[2, 0], 5]
        seq4 = trans2[0:m[3, 0], 6]
        val4 = trans2[0:m[3, 0], 7]
        seq5 = trans2[0:m[4, 0], 8]
        val5 = trans2[0:m[4, 0], 9]
        seq6 = trans2[0:m[5, 0], 10]
        val6 = trans2[0:m[5, 0], 11]
        seq7 = trans2[0:m[6, 0], 12]
        val7 = trans2[0:m[6, 0], 13]
        seq8 = trans2[0:m[7, 0], 14]
        val8 = trans2[0:m[7, 0], 15]
        seq9 = trans2[0:m[8, 0], 16]
        val9 = trans2[0:m[8, 0], 17]
        seq10 = trans2[0:m[9, 0], 18]
        val10 = trans2[0:m[9, 0], 19]
        seq11 = trans2[0:m[10, 0], 20]
        val11 = trans2[0:m[10, 0], 21]
        seq12 = trans2[0:m[11, 0], 22]
        val12 = trans2[0:m[11, 0], 23]
        seq13 = trans2[0:m[12, 0], 24]
        val13 = trans2[0:m[12, 0], 25]

        # 创建dict文件
        dict1 = dict(zip(seq1, val1))
        dict2 = dict(zip(seq2, val2))
        dict3 = dict(zip(seq3, val3))
        dict4 = dict(zip(seq4, val4))
        dict5 = dict(zip(seq5, val5))
        dict6 = dict(zip(seq6, val6))
        dict7 = dict(zip(seq7, val7))
        dict8 = dict(zip(seq8, val8))
        dict9 = dict(zip(seq9, val9))
        dict10 = dict(zip(seq10, val10))
        dict11 = dict(zip(seq11, val11))
        dict12 = dict(zip(seq12, val12))
        dict13 = dict(zip(seq13, val13))

        # 将前7个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    T1 = key1 * key2 * key3 * key4 * key5 * key6 * key7
                                    V1 = value1 * value2 * value3 * value4 * value5 * value6 * value7
                                    for i in range(stp1):
                                        if start1[i] <= T1 <= end1[i]:
                                        # 如果key在该区间内，则将该区间的value累加
                                            trans_step[i, 1] += V1

        dict1_7 = dict(zip(trans_step[:, 0], trans_step[:, 1]))

        for key1_7, value1_7 in dict1_7.items():
            for key8, value8 in dict8.items():
                for key9, value9 in dict9.items():
                    for key10, value10 in dict10.items():
                        for key11, value11 in dict11.items():
                            for key12, value12 in dict12.items():
                                T2 = key1_7 * key8 * key9 * key10 * key11 * key12
                                V2 = value1_7 * value8 * value9 * value10 * value11 * value12
                                for i in range(stp2):
                                    if start2[i] <= T2 <= end2[i]:
                                    # 如果key在该区间内，则将该区间的value累加
                                        Final_trans_step[i, 1] += V2

        dict_trans = dict(zip(Final_trans_step[:, 0], Final_trans_step[:, 1]))

        for key_trans, value_trans in dict_trans.items():
            for key_blu, value_blu in dict13.items():
                T3 = key_trans * key_blu
                V3 = value_trans * value_blu
                for i in range(stp3):
                    if start3[i] <= T3 <= end3[i]:
                    # 如果key在该区间内，则将该区间的value累加
                        Final_lum_step[i, 1] += V3
    elif l == 14:
        seq1 = trans2[0:m[0, 0], 0]
        val1 = trans2[0:m[0, 0], 1]
        seq2 = trans2[0:m[1, 0], 2]
        val2 = trans2[0:m[1, 0], 3]
        seq3 = trans2[0:m[2, 0], 4]
        val3 = trans2[0:m[2, 0], 5]
        seq4 = trans2[0:m[3, 0], 6]
        val4 = trans2[0:m[3, 0], 7]
        seq5 = trans2[0:m[4, 0], 8]
        val5 = trans2[0:m[4, 0], 9]
        seq6 = trans2[0:m[5, 0], 10]
        val6 = trans2[0:m[5, 0], 11]
        seq7 = trans2[0:m[6, 0], 12]
        val7 = trans2[0:m[6, 0], 13]
        seq8 = trans2[0:m[7, 0], 14]
        val8 = trans2[0:m[7, 0], 15]
        seq9 = trans2[0:m[8, 0], 16]
        val9 = trans2[0:m[8, 0], 17]
        seq10 = trans2[0:m[9, 0], 18]
        val10 = trans2[0:m[9, 0], 19]
        seq11 = trans2[0:m[10, 0], 20]
        val11 = trans2[0:m[10, 0], 21]
        seq12 = trans2[0:m[11, 0], 22]
        val12 = trans2[0:m[11, 0], 23]
        seq13 = trans2[0:m[12, 0], 24]
        val13 = trans2[0:m[12, 0], 25]
        seq14 = trans2[0:m[13, 0], 26]
        val14 = trans2[0:m[13, 0], 27]

        # 创建dict文件
        dict1 = dict(zip(seq1, val1))
        dict2 = dict(zip(seq2, val2))
        dict3 = dict(zip(seq3, val3))
        dict4 = dict(zip(seq4, val4))
        dict5 = dict(zip(seq5, val5))
        dict6 = dict(zip(seq6, val6))
        dict7 = dict(zip(seq7, val7))
        dict8 = dict(zip(seq8, val8))
        dict9 = dict(zip(seq9, val9))
        dict10 = dict(zip(seq10, val10))
        dict11 = dict(zip(seq11, val11))
        dict12 = dict(zip(seq12, val12))
        dict13 = dict(zip(seq13, val13))
        dict14 = dict(zip(seq14, val14))

        # 将前7个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    T1 = key1 * key2 * key3 * key4 * key5 * key6 * key7
                                    V1 = value1 * value2 * value3 * value4 * value5 * value6 * value7
                                    for i in range(stp1):
                                        if start1[i] <= T1 <= end1[i]:
                                        # 如果key在该区间内，则将该区间的value累加
                                            trans_step[i, 1] += V1

        dict1_7 = dict(zip(trans_step[:, 0], trans_step[:, 1]))

        for key1_7, value1_7 in dict1_7.items():
            for key8, value8 in dict8.items():
                for key9, value9 in dict9.items():
                    for key10, value10 in dict10.items():
                        for key11, value11 in dict11.items():
                            for key12, value12 in dict12.items():
                                for key13, value13 in dict13.items():
                                    T2 = key1_7 * key8 * key9 * key10 * key11 * key12 * key13
                                    V2 = value1_7 * value8 * value9 * value10 * value11 * value12 * value13
                                    for i in range(stp2):
                                        if start2[i] <= T2 <= end2[i]:
                                        # 如果key在该区间内，则将该区间的value累加
                                            Final_trans_step[i, 1] += V2

        dict_trans = dict(zip(Final_trans_step[:, 0], Final_trans_step[:, 1]))

        for key_trans, value_trans in dict_trans.items():
            for key_blu, value_blu in dict14.items():
                T3 = key_trans * key_blu
                V3 = value_trans * value_blu
                for i in range(stp3):
                    if start3[i] <= T3 <= end3[i]:
                    # 如果key在该区间内，则将该区间的value累加
                        Final_lum_step[i, 1] += V3

    elif l == 15:
        seq1 = trans2[0:m[0, 0], 0]
        val1 = trans2[0:m[0, 0], 1]
        seq2 = trans2[0:m[1, 0], 2]
        val2 = trans2[0:m[1, 0], 3]
        seq3 = trans2[0:m[2, 0], 4]
        val3 = trans2[0:m[2, 0], 5]
        seq4 = trans2[0:m[3, 0], 6]
        val4 = trans2[0:m[3, 0], 7]
        seq5 = trans2[0:m[4, 0], 8]
        val5 = trans2[0:m[4, 0], 9]
        seq6 = trans2[0:m[5, 0], 10]
        val6 = trans2[0:m[5, 0], 11]
        seq7 = trans2[0:m[6, 0], 12]
        val7 = trans2[0:m[6, 0], 13]
        seq8 = trans2[0:m[7, 0], 14]
        val8 = trans2[0:m[7, 0], 15]
        seq9 = trans2[0:m[8, 0], 16]
        val9 = trans2[0:m[8, 0], 17]
        seq10 = trans2[0:m[9, 0], 18]
        val10 = trans2[0:m[9, 0], 19]
        seq11 = trans2[0:m[10, 0], 20]
        val11 = trans2[0:m[10, 0], 21]
        seq12 = trans2[0:m[11, 0], 22]
        val12 = trans2[0:m[11, 0], 23]
        seq13 = trans2[0:m[12, 0], 24]
        val13 = trans2[0:m[12, 0], 25]
        seq14 = trans2[0:m[13, 0], 26]
        val14 = trans2[0:m[13, 0], 27]
        seq15 = trans2[0:m[14, 0], 28]
        val15 = trans2[0:m[14, 0], 29]

        # 创建dict文件
        dict1 = dict(zip(seq1, val1))
        dict2 = dict(zip(seq2, val2))
        dict3 = dict(zip(seq3, val3))
        dict4 = dict(zip(seq4, val4))
        dict5 = dict(zip(seq5, val5))
        dict6 = dict(zip(seq6, val6))
        dict7 = dict(zip(seq7, val7))
        dict8 = dict(zip(seq8, val8))
        dict9 = dict(zip(seq9, val9))
        dict10 = dict(zip(seq10, val10))
        dict11 = dict(zip(seq11, val11))
        dict12 = dict(zip(seq12, val12))
        dict13 = dict(zip(seq13, val13))
        dict14 = dict(zip(seq14, val14))
        dict15 = dict(zip(seq15, val15))


        # 将前8个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    for key8, value8 in dict8.items():
                                        T1 = key1 * key2 * key3 * key4 * key5 * key6 * key7 * key8
                                        V1 = value1 * value2 * value3 * value4 * value5 * value6 * value7 * value8
                                        for i in range(stp1):
                                            if start1[i] <= T1 <= end1[i]:
                                            # 如果key在该区间内，则将该区间的value累加
                                                trans_step[i, 1] += V1

        dict1_8 = dict(zip(trans_step[:, 0], trans_step[:, 1]))

        for key1_8, value1_8 in dict1_8.items():
            for key9, value9 in dict9.items():
                for key10, value10 in dict10.items():
                    for key11, value11 in dict11.items():
                        for key12, value12 in dict12.items():
                            for key13, value13 in dict13.items():
                                for key14, value14 in dict14.items():
                                    T2 = key1_8 * key9 * key10 * key11 * key12 * key13 * key14
                                    V2 = value1_8 * value9 * value10 * value11 * value12 * value13 * value14
                                    for i in range(stp2):
                                        if start2[i] <= T2 <= end2[i]:
                                        # 如果key在该区间内，则将该区间的value累加
                                            Final_trans_step[i, 1] += V2

        dict_trans = dict(zip(Final_trans_step[:, 0], Final_trans_step[:, 1]))

        for key_trans, value_trans in dict_trans.items():
            for key_blu, value_blu in dict15.items():
                T3 = key_trans * key_blu
                V3 = value_trans * value_blu
                for i in range(stp3):
                    if start3[i] <= T3 <= end3[i]:
                    # 如果key在该区间内，则将该区间的value累加
                        Final_lum_step[i, 1] += V3
    
    elif l == 16:
        seq1 = trans2[0:m[0, 0], 0]
        val1 = trans2[0:m[0, 0], 1]
        seq2 = trans2[0:m[1, 0], 2]
        val2 = trans2[0:m[1, 0], 3]
        seq3 = trans2[0:m[2, 0], 4]
        val3 = trans2[0:m[2, 0], 5]
        seq4 = trans2[0:m[3, 0], 6]
        val4 = trans2[0:m[3, 0], 7]
        seq5 = trans2[0:m[4, 0], 8]
        val5 = trans2[0:m[4, 0], 9]
        seq6 = trans2[0:m[5, 0], 10]
        val6 = trans2[0:m[5, 0], 11]
        seq7 = trans2[0:m[6, 0], 12]
        val7 = trans2[0:m[6, 0], 13]
        seq8 = trans2[0:m[7, 0], 14]
        val8 = trans2[0:m[7, 0], 15]
        seq9 = trans2[0:m[8, 0], 16]
        val9 = trans2[0:m[8, 0], 17]
        seq10 = trans2[0:m[9, 0], 18]
        val10 = trans2[0:m[9, 0], 19]
        seq11 = trans2[0:m[10, 0], 20]
        val11 = trans2[0:m[10, 0], 21]
        seq12 = trans2[0:m[11, 0], 22]
        val12 = trans2[0:m[11, 0], 23]
        seq13 = trans2[0:m[12, 0], 24]
        val13 = trans2[0:m[12, 0], 25]
        seq14 = trans2[0:m[13, 0], 26]
        val14 = trans2[0:m[13, 0], 27]
        seq15 = trans2[0:m[14, 0], 28]
        val15 = trans2[0:m[14, 0], 29]
        seq16 = trans2[0:m[15, 0], 30]
        val16 = trans2[0:m[15, 0], 31]

        # 创建dict文件
        dict1 = dict(zip(seq1, val1))
        dict2 = dict(zip(seq2, val2))
        dict3 = dict(zip(seq3, val3))
        dict4 = dict(zip(seq4, val4))
        dict5 = dict(zip(seq5, val5))
        dict6 = dict(zip(seq6, val6))
        dict7 = dict(zip(seq7, val7))
        dict8 = dict(zip(seq8, val8))
        dict9 = dict(zip(seq9, val9))
        dict10 = dict(zip(seq10, val10))
        dict11 = dict(zip(seq11, val11))
        dict12 = dict(zip(seq12, val12))
        dict13 = dict(zip(seq13, val13))
        dict14 = dict(zip(seq14, val14))
        dict15 = dict(zip(seq15, val15))
        dict16 = dict(zip(seq16, val16))


        # 将前8个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    for key8, value8 in dict8.items():
                                        T1 = key1 * key2 * key3 * key4 * key5 * key6 * key7 * key8
                                        V1 = value1 * value2 * value3 * value4 * value5 * value6 * value7 * value8
                                        for i in range(stp1):
                                            if start1[i] <= T1 <= end1[i]:
                                            # 如果key在该区间内，则将该区间的value累加
                                                trans_step[i, 1] += V1

        dict1_8 = dict(zip(trans_step[:, 0], trans_step[:, 1]))

        for key1_8, value1_8 in dict1_8.items():
            for key9, value9 in dict9.items():
                for key10, value10 in dict10.items():
                    for key11, value11 in dict11.items():
                        for key12, value12 in dict12.items():
                            for key13, value13 in dict13.items():
                                for key14, value14 in dict14.items():
                                    for key15, value15 in dict15.items():
                                        T2 = key1_8 * key9 * key10 * key11 * key12 * key13 * key14 * key15
                                        V2 = value1_8 * value9 * value10 * value11 * value12 * value13 * value14 * value15
                                        for i in range(stp2):
                                            if start2[i] <= T2 <= end2[i]:
                                            # 如果key在该区间内，则将该区间的value累加
                                                Final_trans_step[i, 1] += V2

        dict_trans = dict(zip(Final_trans_step[:, 0], Final_trans_step[:, 1]))

        for key_trans, value_trans in dict_trans.items():
            for key_blu, value_blu in dict16.items():
                T3 = key_trans * key_blu
                V3 = value_trans * value_blu
                for i in range(stp3):
                    if start3[i] <= T3 <= end3[i]:
                    # 如果key在该区间内，则将该区间的value累加
                        Final_lum_step[i, 1] += V3

try:
    # # # 设置步骤2
    col5, col6 = st.columns([2, 1])
    bz3_1, bz3_2 = st.columns([1, 20])
    with col5:
        st.write("<h6>步骤3：点击计算结果</h6>", unsafe_allow_html=True)
    with bz3_2:
        if st.button('***点击计算***'):
            # 将使用者保存到txt文件中
            fp_save = 'D:\\python_work\\project\\1_PDT\\users\\网站使用者.txt'
            mode = 'a'
            with open(fp_save, mode) as f:
                f.write('使用了透过率波动1step工具' + '\n')

            main_code(trans2, l, m, start1, end1, start2, end2, start3, end3, trans_step, Final_trans_step, Final_lum_step)
            bz3_3, bz3_4, bz3_5, bz3_6 = st.columns([1, 5, 5, 8])
            with bz3_4:
                st.write('透过率概率分布', Final_trans_step)
            with bz3_5:
                st.write('亮度概率分布',Final_lum_step)

            TT = pd.DataFrame(Final_trans_step, columns=['透过率比例', '概率分布'])
            LL = pd.DataFrame(Final_lum_step, columns=['亮度比例', '概率分布'])

            st.line_chart(TT, x='透过率比例', y='概率分布')
            st.line_chart(LL, x='亮度比例', y='概率分布')
            # 获取代码执行后时间戳
            end_time = time.time()
            # 计算执行时间
            run_time = round(end_time - start_time, 2)
            st.write("代码执行时间为：{}秒".format(run_time))

except NameError:
    bz5_3, bz5_4, bz5_5 = st.columns([1, 6, 19])
    with bz5_5:
        st.write(':red[请加载TXT文件后在点击计算!]')

# 编辑button - Final计算
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-gh2jqd.ea3mdgi5 > div > div > div > div:nth-child(8) > div.st-emotion-cache-15qpf3q.e1f1d6gn3 > div > div > div > div > div > button
    {
    background-color: rgb(220, 240, 220) !important;
    height: 70px !important;
    width: 150px !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑TXT数据加载button
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-gh2jqd.ea3mdgi5 > div > div > div > div:nth-child(4) > div.st-emotion-cache-15qpf3q.e1f1d6gn3 > div > div > div > div > div > section > button
    {
    background-color: rgb(220, 240, 220) !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑精度填写数据加载button
st.markdown(
    '''
    <style>
    input {
        background-color: rgb(220, 240, 220) !important; /*设置背景颜色*/
        text-align: center !important; /*设置字体水平居中*/
        vertical-align: middle !important; /*设置字体垂直居中*/
    }
    </style>
    ''',
    unsafe_allow_html=True
)
