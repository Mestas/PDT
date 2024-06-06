import numpy as np
import pandas as pd
import streamlit as st
import time
import math
# from numba import njit
import itertools

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具可以计算影响因子为5~16个的亮度波动概率分布</h4>", unsafe_allow_html=True)

# # # 工具名称、版本号
st.write("# 亮度波动概率计算工具 #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V2.0</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2024/06/06</h5>", unsafe_allow_html=True)
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
    # # fp_trans = 'D:\\samui LCM brightness (15).txt'
    # fp_trans = 'D:\\test9.txt'
    if fp_trans is not None:
        trans = pd.read_csv(fp_trans, header=None, sep="\t", skip_blank_lines=True)  # 使用pandas来读取txt，sep="t"为逗号分隔符
        trans1 = round(trans, 6)  # 用于计算行数的dataframe series
        trans2 = trans1.values  # Dataframe转换为ndarray

        # print(trans2)

        # 获取影响因子个数
        l = int(trans.iloc[0, :].dropna().shape[0] / 2)
        # print(l)
        # 获取每个影响因子的step数
        m = np.zeros((l, 1))
        for i in range(l):
            m[i] = int(trans1.iloc[:, i * 2].dropna().shape[0])
        # print(m)

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

    stp1 = int(round((max1 - min1) / vac_trans + 1))

    trans_step = np.zeros((stp1, 2))

    for i in range(stp1):
        trans_step[i, 0] = min1 + i * vac_trans
    start1 = np.zeros((stp1, 1))
    end1 = np.zeros((stp1, 1))
    for i in range(stp1):
        start1[i] = round(trans_step[i, 0] - vac_trans / 2, 4)
        end1[i] = round(trans_step[i, 0] + vac_trans / 2, 4)

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

    stp2 = int(round((max2 - min2) / vac_trans + 1))
    
    Final_trans_step = np.zeros((stp2, 2))
    
    for i in range(stp2):
        Final_trans_step[i, 0] = min2 + i * vac_trans
    # print(Final_trans_step)

    start2 = np.zeros((stp2, 1))
    end2 = np.zeros((stp2, 1))
    for i in range(stp2):
        start2[i] = round(Final_trans_step[i, 0] - vac_trans / 2, 4)
        end2[i] = round(Final_trans_step[i, 0] + vac_trans / 2, 4)
    
    # print(min1, max1, stp1)
    # print(trans_step)
    # print(start1, end1, stp1)

    # print(min2, max2, stp2)
    # print(Final_trans_step)
    # print(start2, end2, stp2)


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

    stp3 = int(round((max3 - min3) / vac_lum + 1))
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

# @njit # (nopython=True)

def main_code(trans2, l, m, start1, end1, stp1, start2, end2, stp2, start3, end3, stp3, trans_step, Final_trans_step, Final_lum_step):
    if l == 3:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]

        # 创建itertools迭代列表
        F2 = [a * b for a, b in itertools.product(f1, f2)]
        V2 = [a * b for a, b in itertools.product(v1, v2)]

        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f3)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v3)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]

    elif l == 5:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]
        f4 = trans2[0:int(m[3, 0]), 6]
        v4 = trans2[0:int(m[3, 0]), 7]
        f5 = trans2[0:int(m[4, 0]), 8]
        v5 = trans2[0:int(m[4, 0]), 9]

        # 创建itertools迭代列表1
        F2 = [a * b * c * d for a, b, c, d in itertools.product(f1, f2, f3, f4)]
        V2 = [a * b * c * d for a, b, c, d in itertools.product(v1, v2, v3, v4)]

        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f5)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v5)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]
    
    elif l == 6:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]
        f4 = trans2[0:int(m[3, 0]), 6]
        v4 = trans2[0:int(m[3, 0]), 7]
        f5 = trans2[0:int(m[4, 0]), 8]
        v5 = trans2[0:int(m[4, 0]), 9]
        f6 = trans2[0:int(m[5, 0]), 10]
        v6 = trans2[0:int(m[5, 0]), 11]

        # 创建itertools迭代列表2
        F2 = [a * b * c * d * e for a, b, c, d, e in itertools.product(f1, f2, f3, f4, f5)]
        V2 = [a * b * c * d * e for a, b, c, d, e in itertools.product(v1, v2, v3, v4, v5)]
        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f6)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v6)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]

    elif l == 7:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]
        f4 = trans2[0:int(m[3, 0]), 6]
        v4 = trans2[0:int(m[3, 0]), 7]
        f5 = trans2[0:int(m[4, 0]), 8]
        v5 = trans2[0:int(m[4, 0]), 9]
        f6 = trans2[0:int(m[5, 0]), 10]
        v6 = trans2[0:int(m[5, 0]), 11]
        f7 = trans2[0:int(m[6, 0]), 12]
        v7 = trans2[0:int(m[6, 0]), 13]

        # 创建itertools迭代列表1
        F1 = [a * b * c * d for a, b, c, d in itertools.product(f1, f2, f3, f4)]
        V1 = [a * b * c * d for a, b, c, d in itertools.product(v1, v2, v3, v4)]
        num1 = len(F1)

        for i in range(num1):
            for j in range(stp1):
                if start1[j] < F1[i] <= end1[j]:
                # 如果key在该区间内，则将该区间的value累加
                    trans_step[j, 1] += V1[i]

        # 创建itertools迭代列表2
        F2 = [a * b * c for a, b, c in itertools.product(trans_step[:, 0], f5, f6)]
        V2 = [a * b * c for a, b, c in itertools.product(trans_step[:, 1], v5, v6)]
        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f7)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v7)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]

    elif l == 8:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]
        f4 = trans2[0:int(m[3, 0]), 6]
        v4 = trans2[0:int(m[3, 0]), 7]
        f5 = trans2[0:int(m[4, 0]), 8]
        v5 = trans2[0:int(m[4, 0]), 9]
        f6 = trans2[0:int(m[5, 0]), 10]
        v6 = trans2[0:int(m[5, 0]), 11]
        f7 = trans2[0:int(m[6, 0]), 12]
        v7 = trans2[0:int(m[6, 0]), 13]
        f8 = trans2[0:int(m[7, 0]), 14]
        v8 = trans2[0:int(m[7, 0]), 15]

        # 创建itertools迭代列表1
        F1 = [a * b * c * d for a, b, c, d in itertools.product(f1, f2, f3, f4)]
        V1 = [a * b * c * d for a, b, c, d in itertools.product(v1, v2, v3, v4)]
        num1 = len(F1)

        for i in range(num1):
            for j in range(stp1):
                if start1[j] < F1[i] <= end1[j]:
                # 如果key在该区间内，则将该区间的value累加
                    trans_step[j, 1] += V1[i]

        # 创建itertools迭代列表2
        F2 = [a * b * c * d for a, b, c, d in itertools.product(trans_step[:, 0], f5, f6, f7)]
        V2 = [a * b * c * d for a, b, c, d in itertools.product(trans_step[:, 1], v5, v6, v7)]
        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f8)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v8)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]
        print(Final_lum_step)
    
    elif l == 9:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]
        f4 = trans2[0:int(m[3, 0]), 6]
        v4 = trans2[0:int(m[3, 0]), 7]
        f5 = trans2[0:int(m[4, 0]), 8]
        v5 = trans2[0:int(m[4, 0]), 9]
        f6 = trans2[0:int(m[5, 0]), 10]
        v6 = trans2[0:int(m[5, 0]), 11]
        f7 = trans2[0:int(m[6, 0]), 12]
        v7 = trans2[0:int(m[6, 0]), 13]
        f8 = trans2[0:int(m[7, 0]), 14]
        v8 = trans2[0:int(m[7, 0]), 15]
        f9 = trans2[0:int(m[8, 0]), 16]
        v9 = trans2[0:int(m[8, 0]), 17]

        # 创建itertools迭代列表1
        F1 = [a * b * c * d * e for a, b, c, d, e in itertools.product(f1, f2, f3, f4, f5)]
        V1 = [a * b * c * d * e for a, b, c, d, e in itertools.product(v1, v2, v3, v4, v5)]
        num1 = len(F1)

        for i in range(num1):
            for j in range(stp1):
                if start1[j] < F1[i] <= end1[j]:
                # 如果key在该区间内，则将该区间的value累加
                    trans_step[j, 1] += V1[i]

        # 创建itertools迭代列表2
        F2 = [a * b * c * d for a, b, c, d in itertools.product(trans_step[:, 0], f6, f7, f8)]
        V2 = [a * b * c * d for a, b, c, d in itertools.product(trans_step[:, 1], v6, v7, v8)]
        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f9)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v9)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]
        print(Final_lum_step)
    
    elif l == 10:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]
        f4 = trans2[0:int(m[3, 0]), 6]
        v4 = trans2[0:int(m[3, 0]), 7]
        f5 = trans2[0:int(m[4, 0]), 8]
        v5 = trans2[0:int(m[4, 0]), 9]
        f6 = trans2[0:int(m[5, 0]), 10]
        v6 = trans2[0:int(m[5, 0]), 11]
        f7 = trans2[0:int(m[6, 0]), 12]
        v7 = trans2[0:int(m[6, 0]), 13]
        f8 = trans2[0:int(m[7, 0]), 14]
        v8 = trans2[0:int(m[7, 0]), 15]
        f9 = trans2[0:int(m[8, 0]), 16]
        v9 = trans2[0:int(m[8, 0]), 17]
        f10 = trans2[0:int(m[9, 0]), 18]
        v10 = trans2[0:int(m[9, 0]), 19]

        # 创建itertools迭代列表1
        F1 = [a * b * c * d * e for a, b, c, d, e in itertools.product(f1, f2, f3, f4, f5)]
        V1 = [a * b * c * d * e for a, b, c, d, e in itertools.product(v1, v2, v3, v4, v5)]
        num1 = len(F1)

        for i in range(num1):
            for j in range(stp1):
                if start1[j] < F1[i] <= end1[j]:
                # 如果key在该区间内，则将该区间的value累加
                    trans_step[j, 1] += V1[i]

        # 创建itertools迭代列表2
        F2 = [a * b * c * d * e for a, b, c, d, e in itertools.product(trans_step[:, 0], f6, f7, f8, f9)]
        V2 = [a * b * c * d * e for a, b, c, d, e in itertools.product(trans_step[:, 1], v6, v7, v8, v9)]
        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f10)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v10)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]
        print(Final_lum_step)
    
    elif l == 11:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]
        f4 = trans2[0:int(m[3, 0]), 6]
        v4 = trans2[0:int(m[3, 0]), 7]
        f5 = trans2[0:int(m[4, 0]), 8]
        v5 = trans2[0:int(m[4, 0]), 9]
        f6 = trans2[0:int(m[5, 0]), 10]
        v6 = trans2[0:int(m[5, 0]), 11]
        f7 = trans2[0:int(m[6, 0]), 12]
        v7 = trans2[0:int(m[6, 0]), 13]
        f8 = trans2[0:int(m[7, 0]), 14]
        v8 = trans2[0:int(m[7, 0]), 15]
        f9 = trans2[0:int(m[8, 0]), 16]
        v9 = trans2[0:int(m[8, 0]), 17]
        f10 = trans2[0:int(m[9, 0]), 18]
        v10 = trans2[0:int(m[9, 0]), 19]
        f11 = trans2[0:int(m[10, 0]), 20]
        v11 = trans2[0:int(m[10, 0]), 21]
        
         # 创建itertools迭代列表1
        F1 = [a * b * c * d * e * f for a, b, c, d, e, f in itertools.product(f1, f2, f3, f4, f5, f6)]
        V1 = [a * b * c * d * e * f for a, b, c, d, e, f in itertools.product(v1, v2, v3, v4, v5, v6)]
        num1 = len(F1)

        for i in range(num1):
            for j in range(stp1):
                if start1[j] < F1[i] <= end1[j]:
                # 如果key在该区间内，则将该区间的value累加
                    trans_step[j, 1] += V1[i]

        # 创建itertools迭代列表2
        F2 = [a * b * c * d * e for a, b, c, d, e in itertools.product(trans_step[:, 0], f7, f8, f9, f10)]
        V2 = [a * b * c * d * e for a, b, c, d, e in itertools.product(trans_step[:, 1], v7, v8, v9, v10)]
        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f11)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v11)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]
        print(Final_lum_step)
        
    
    elif l == 12:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]
        f4 = trans2[0:int(m[3, 0]), 6]
        v4 = trans2[0:int(m[3, 0]), 7]
        f5 = trans2[0:int(m[4, 0]), 8]
        v5 = trans2[0:int(m[4, 0]), 9]
        f6 = trans2[0:int(m[5, 0]), 10]
        v6 = trans2[0:int(m[5, 0]), 11]
        f7 = trans2[0:int(m[6, 0]), 12]
        v7 = trans2[0:int(m[6, 0]), 13]
        f8 = trans2[0:int(m[7, 0]), 14]
        v8 = trans2[0:int(m[7, 0]), 15]
        f9 = trans2[0:int(m[8, 0]), 16]
        v9 = trans2[0:int(m[8, 0]), 17]
        f10 = trans2[0:int(m[9, 0]), 18]
        v10 = trans2[0:int(m[9, 0]), 19]
        f11 = trans2[0:int(m[10, 0]), 20]
        v11 = trans2[0:int(m[10, 0]), 21]
        f12 = trans2[0:int(m[11, 0]), 22]
        v12 = trans2[0:int(m[11, 0]), 23]
        
         # 创建itertools迭代列表1
        F1 = [a * b * c * d * e * f for a, b, c, d, e, f in itertools.product(f1, f2, f3, f4, f5, f6)]
        V1 = [a * b * c * d * e * f for a, b, c, d, e, f in itertools.product(v1, v2, v3, v4, v5, v6)]
        num1 = len(F1)

        for i in range(num1):
            for j in range(stp1):
                if start1[j] < F1[i] <= end1[j]:
                # 如果key在该区间内，则将该区间的value累加
                    trans_step[j, 1] += V1[i]

        # 创建itertools迭代列表2
        F2 = [a * b * c * d * e * f for a, b, c, d, e, f in itertools.product(trans_step[:, 0], f7, f8, f9, f10, f11)]
        V2 = [a * b * c * d * e * f for a, b, c, d, e, f in itertools.product(trans_step[:, 1], v7, v8, v9, v10, v11)]
        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f12)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v12)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]
        print(Final_lum_step)

    elif l == 13:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]
        f4 = trans2[0:int(m[3, 0]), 6]
        v4 = trans2[0:int(m[3, 0]), 7]
        f5 = trans2[0:int(m[4, 0]), 8]
        v5 = trans2[0:int(m[4, 0]), 9]
        f6 = trans2[0:int(m[5, 0]), 10]
        v6 = trans2[0:int(m[5, 0]), 11]
        f7 = trans2[0:int(m[6, 0]), 12]
        v7 = trans2[0:int(m[6, 0]), 13]
        f8 = trans2[0:int(m[7, 0]), 14]
        v8 = trans2[0:int(m[7, 0]), 15]
        f9 = trans2[0:int(m[8, 0]), 16]
        v9 = trans2[0:int(m[8, 0]), 17]
        f10 = trans2[0:int(m[9, 0]), 18]
        v10 = trans2[0:int(m[9, 0]), 19]
        f11 = trans2[0:int(m[10, 0]), 20]
        v11 = trans2[0:int(m[10, 0]), 21]
        f12 = trans2[0:int(m[11, 0]), 22]
        v12 = trans2[0:int(m[11, 0]), 23]
        f13 = trans2[0:int(m[12, 0]), 24]
        v13 = trans2[0:int(m[12, 0]), 25]
        
         # 创建itertools迭代列表1
        F1 = [a * b * c * d * e * f * g for a, b, c, d, e, f, g in itertools.product(f1, f2, f3, f4, f5, f6, f7)]
        V1 = [a * b * c * d * e * f * g for a, b, c, d, e, f, g in itertools.product(v1, v2, v3, v4, v5, v6, v7)]
        num1 = len(F1)

        for i in range(num1):
            for j in range(stp1):
                if start1[j] < F1[i] <= end1[j]:
                # 如果key在该区间内，则将该区间的value累加
                    trans_step[j, 1] += V1[i]

        # 创建itertools迭代列表2
        F2 = [a * b * c * d * e * f for a, b, c, d, e, f in itertools.product(trans_step[:, 0], f8, f9, f10, f11, f12)]
        V2 = [a * b * c * d * e * f for a, b, c, d, e, f in itertools.product(trans_step[:, 1], v8, v9, v10, v11, v12)]
        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f13)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v13)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]
        print(Final_lum_step)

    elif l == 14:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]
        f4 = trans2[0:int(m[3, 0]), 6]
        v4 = trans2[0:int(m[3, 0]), 7]
        f5 = trans2[0:int(m[4, 0]), 8]
        v5 = trans2[0:int(m[4, 0]), 9]
        f6 = trans2[0:int(m[5, 0]), 10]
        v6 = trans2[0:int(m[5, 0]), 11]
        f7 = trans2[0:int(m[6, 0]), 12]
        v7 = trans2[0:int(m[6, 0]), 13]
        f8 = trans2[0:int(m[7, 0]), 14]
        v8 = trans2[0:int(m[7, 0]), 15]
        f9 = trans2[0:int(m[8, 0]), 16]
        v9 = trans2[0:int(m[8, 0]), 17]
        f10 = trans2[0:int(m[9, 0]), 18]
        v10 = trans2[0:int(m[9, 0]), 19]
        f11 = trans2[0:int(m[10, 0]), 20]
        v11 = trans2[0:int(m[10, 0]), 21]
        f12 = trans2[0:int(m[11, 0]), 22]
        v12 = trans2[0:int(m[11, 0]), 23]
        f13 = trans2[0:int(m[12, 0]), 24]
        v13 = trans2[0:int(m[12, 0]), 25]
        f14 = trans2[0:int(m[13, 0]), 26]
        v14 = trans2[0:int(m[13, 0]), 27]
        
         # 创建itertools迭代列表1
        F1 = [a * b * c * d * e * f * g for a, b, c, d, e, f, g in itertools.product(f1, f2, f3, f4, f5, f6, f7)]
        V1 = [a * b * c * d * e * f * g for a, b, c, d, e, f, g in itertools.product(v1, v2, v3, v4, v5, v6, v7)]
        num1 = len(F1)

        for i in range(num1):
            for j in range(stp1):
                if start1[j] < F1[i] <= end1[j]:
                # 如果key在该区间内，则将该区间的value累加
                    trans_step[j, 1] += V1[i]

        # 创建itertools迭代列表2
        F2 = [a * b * c * d * e * f * g for a, b, c, d, e, f, g in itertools.product(trans_step[:, 0], f8, f9, f10, f11, f12, f13)]
        V2 = [a * b * c * d * e * f * g for a, b, c, d, e, f, g in itertools.product(trans_step[:, 1], v8, v9, v10, v11, v12, f13)]
        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f14)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v14)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]
        print(Final_lum_step)
        
    elif l == 15:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]
        f4 = trans2[0:int(m[3, 0]), 6]
        v4 = trans2[0:int(m[3, 0]), 7]
        f5 = trans2[0:int(m[4, 0]), 8]
        v5 = trans2[0:int(m[4, 0]), 9]
        f6 = trans2[0:int(m[5, 0]), 10]
        v6 = trans2[0:int(m[5, 0]), 11]
        f7 = trans2[0:int(m[6, 0]), 12]
        v7 = trans2[0:int(m[6, 0]), 13]
        f8 = trans2[0:int(m[7, 0]), 14]
        v8 = trans2[0:int(m[7, 0]), 15]
        f9 = trans2[0:int(m[8, 0]), 16]
        v9 = trans2[0:int(m[8, 0]), 17]
        f10 = trans2[0:int(m[9, 0]), 18]
        v10 = trans2[0:int(m[9, 0]), 19]
        f11 = trans2[0:int(m[10, 0]), 20]
        v11 = trans2[0:int(m[10, 0]), 21]
        f12 = trans2[0:int(m[11, 0]), 22]
        v12 = trans2[0:int(m[11, 0]), 23]
        f13 = trans2[0:int(m[12, 0]), 24]
        v13 = trans2[0:int(m[12, 0]), 25]
        f14 = trans2[0:int(m[13, 0]), 26]
        v14 = trans2[0:int(m[13, 0]), 27]
        f15 = trans2[0:int(m[14, 0]), 28]
        v15 = trans2[0:int(m[14, 0]), 29]
        f16 = trans2[0:int(m[15, 0]), 30]
        v16 = trans2[0:int(m[15, 0]), 31]

        # 创建itertools迭代列表1
        F1 = [a * b * c * d * e * f * g * h for a, b, c, d, e, f, g, h in itertools.product(f1, f2, f3, f4, f5, f6, f7, f8)]
        V1 = [a * b * c * d * e * f * g * h for a, b, c, d, e, f, g, h in itertools.product(v1, v2, v3, v4, v5, v6, v7, v8)]

        num1 = len(F1)

        for i in range(num1):
            for j in range(stp1):
                if start1[j] < F1[i] <= end1[j]:
                # 如果key在该区间内，则将该区间的value累加
                    trans_step[j, 1] += V1[i]

        # 创建itertools迭代列表2
        F2 = [a * b * c * d * e * f * g for a, b, c, d, e, f, g in itertools.product(trans_step[:, 0], f9, f10, f11, f12, f13, f14)]
        V2 = [a * b * c * d * e * f * g for a, b, c, d, e, f, g in itertools.product(trans_step[:, 1], v9, v10, v11, v12, v13, v14)]
        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f15)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v15)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]
        print(Final_lum_step)

    elif l == 16:
        f1 = trans2[0:int(m[0, 0]), 0]
        v1 = trans2[0:int(m[0, 0]), 1]
        f2 = trans2[0:int(m[1, 0]), 2]
        v2 = trans2[0:int(m[1, 0]), 3]
        f3 = trans2[0:int(m[2, 0]), 4]
        v3 = trans2[0:int(m[2, 0]), 5]
        f4 = trans2[0:int(m[3, 0]), 6]
        v4 = trans2[0:int(m[3, 0]), 7]
        f5 = trans2[0:int(m[4, 0]), 8]
        v5 = trans2[0:int(m[4, 0]), 9]
        f6 = trans2[0:int(m[5, 0]), 10]
        v6 = trans2[0:int(m[5, 0]), 11]
        f7 = trans2[0:int(m[6, 0]), 12]
        v7 = trans2[0:int(m[6, 0]), 13]
        f8 = trans2[0:int(m[7, 0]), 14]
        v8 = trans2[0:int(m[7, 0]), 15]
        f9 = trans2[0:int(m[8, 0]), 16]
        v9 = trans2[0:int(m[8, 0]), 17]
        f10 = trans2[0:int(m[9, 0]), 18]
        v10 = trans2[0:int(m[9, 0]), 19]
        f11 = trans2[0:int(m[10, 0]), 20]
        v11 = trans2[0:int(m[10, 0]), 21]
        f12 = trans2[0:int(m[11, 0]), 22]
        v12 = trans2[0:int(m[11, 0]), 23]
        f13 = trans2[0:int(m[12, 0]), 24]
        v13 = trans2[0:int(m[12, 0]), 25]
        f14 = trans2[0:int(m[13, 0]), 26]
        v14 = trans2[0:int(m[13, 0]), 27]
        f15 = trans2[0:int(m[14, 0]), 28]
        v15 = trans2[0:int(m[14, 0]), 29]
        f16 = trans2[0:int(m[15, 0]), 30]
        v16 = trans2[0:int(m[15, 0]), 31]

        # 创建itertools迭代列表1
        F1 = [a * b * c * d * e * f * g * h for a, b, c, d, e, f, g, h in itertools.product(f1, f2, f3, f4, f5, f6, f7, f8)]
        V1 = [a * b * c * d * e * f * g * h for a, b, c, d, e, f, g, h in itertools.product(v1, v2, v3, v4, v5, v6, v7, v8)]

        num1 = len(F1)

        for i in range(num1):
            for j in range(stp1):
                if start1[j] < F1[i] <= end1[j]:
                # 如果key在该区间内，则将该区间的value累加
                    trans_step[j, 1] += V1[i]

        # 创建itertools迭代列表2
        F2 = [a * b * c * d * e * f * g * h for a, b, c, d, e, f, g, h in itertools.product(trans_step[:, 0], f9, f10, f11, f12, f13, f14, f15)]
        V2 = [a * b * c * d * e * f * g * h for a, b, c, d, e, f, g, h in itertools.product(trans_step[:, 1], v9, v10, v11, v12, v13, v14, v15)]
        num2 = len(F2)

        for i in range(num2):
            for j in range(stp2):
                if start2[j] < F2[i] <= end2[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_trans_step[j, 1] += V2[i]

        F3 = [a * b for a, b in itertools.product(Final_trans_step[:, 0], f16)]
        V3 = [a * b for a, b in itertools.product(Final_trans_step[:, 1], v16)]
        num3 = len(F3)

        for i in range(num3):
            for j in range(stp3):
                if start3[j] < F3[i] <= end3[j]:
                # 如果key在该区间内，则将该区间的value累加
                    Final_lum_step[j, 1] += V3[i]
        print(Final_lum_step)

        
                        
# main_code(trans2, l, m, start1, end1, start2, end2, start3, end3, trans_step, Final_trans_step, Final_lum_step)

# TT = pd.DataFrame(Final_trans_step, columns=['透过率比例', '概率分布'])
# LL = pd.DataFrame(Final_lum_step, columns=['亮度比例', '概率分布'])

# print(TT)
# print(LL)
# data1 = pd.DataFrame(TT)
# path1 = 'D:/Samui_Final_Trans_step.csv'
# data1.index = np.arange(1, data1.shape[0] + 1)
# data1.columns = np.arange(1, data1.shape[1] + 1)
# data1.to_csv(path1)

# data2 = pd.DataFrame(LL)
# path2 = 'D:/Samui_Final_Lum_step.csv'
# data2.index = np.arange(1, data2.shape[0] + 1)
# data2.columns = np.arange(1, data2.shape[1] + 1)
# data2.to_csv(path2)

# end_time = time.time()
# # 计算执行时间
# run_time = round(end_time - start_time, 2)
# print("代码执行时间为：{}秒".format(run_time))
# # print(T_step)


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

            main_code(trans2, l, m, start1, end1, stp1, start2, end2, stp2, start3, end3, stp3, trans_step, Final_trans_step, Final_lum_step)
            bz3_3, bz3_4, bz3_5, bz3_6 = st.columns([1, 5, 5, 8])
            with bz3_4:
                st.write('透过率概率分布', Final_trans_step)
            with bz3_5:
                st.write('亮度概率分布', Final_lum_step)

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
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(8) > div.st-emotion-cache-15qpf3q.e1f1d6gn3 > div > div > div > div.element-container.st-emotion-cache-1sx39vv.e1f1d6gn4 > div > button
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
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(4) > div.st-emotion-cache-15qpf3q.e1f1d6gn3 > div > div > div > div > div > section > button
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
