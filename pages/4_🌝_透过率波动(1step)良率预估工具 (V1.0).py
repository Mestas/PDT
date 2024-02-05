import numpy as np
import pandas as pd
import streamlit as st
import time

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具可以计算透过率波动概率分布</h4>", unsafe_allow_html=True)

# # # 工具名称、版本号
st.write("# 透过率波动概率计算工具 #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V1.0</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2023/12/07</h5>", unsafe_allow_html=True)

# 创建文件上传按钮
fp_trans = st.file_uploader("请上传techwiz正视角仿真结果TXT文件", type=['txt'], help="请选择TXT文件进行上传", key=1)
if fp_trans is not None:
    trans = pd.read_csv(fp_trans, header=None, sep="\t", skip_blank_lines=True)  # 使用pandas来读取txt，sep="t"为逗号分隔符
    trans1 = round(trans, 6)  # 用于计算行数的dataframe series
    trans2 = trans1.values  # Dataframe转换为ndarray
    # 获取各行行数
    l = int(trans.iloc[0, :].dropna().shape[0] / 2)
    # 获取每个参数的行数
    m = np.zeros((15, 1))
    for i in range(l):
        m[i] = int(trans1.iloc[:, i * 2].dropna().shape[0])

# 创建透过率矩阵，透过率分布0.6~1.3 step 0.01，共计71个数据
T_step = np.zeros((71, 2))
for i in range(71):
    T_step[i, 0] = 0.6 + i * 0.01

# 获取代码执行前时间戳
start_time = time.time()

from numba import njit
@njit # (nopython=True)

# 定义主程序函数 main_code
def main_code(trans2, l, m, T_step):
    if l == 5:
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
        # 将5个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            T = key1 * key2 * key3 * key4 * key5
                            V = value1 * value2 * value3 * value4 * value5
                            if T > 0.595 and T <= 0.605:
                                T_step[0, 1] += V
                            elif T > 0.605 and T <= 0.615:
                                T_step[1, 1] += V
                            elif T > 0.615 and T <= 0.625:
                                T_step[2, 1] += V
                            elif T > 0.625 and T <= 0.635:
                                T_step[3, 1] += V
                            elif T > 0.635 and T <= 0.645:
                                T_step[4, 1] += V
                            elif T > 0.645 and T <= 0.655:
                                T_step[5, 1] += V
                            elif T > 0.655 and T <= 0.665:
                                T_step[6, 1] += V
                            elif T > 0.665 and T <= 0.675:
                                T_step[7, 1] += V
                            elif T > 0.675 and T <= 0.685:
                                T_step[8, 1] += V
                            elif T > 0.685 and T <= 0.695:
                                T_step[9, 1] += V
                            elif T > 0.695 and T <= 0.705:
                                T_step[10, 1] += V
                            elif T > 0.705 and T <= 0.715:
                                T_step[11, 1] += V
                            elif T > 0.715 and T <= 0.725:
                                T_step[12, 1] += V
                            elif T > 0.725 and T <= 0.735:
                                T_step[13, 1] += V
                            elif T > 0.735 and T <= 0.745:
                                T_step[14, 1] += V
                            elif T > 0.745 and T <= 0.755:
                                T_step[15, 1] += V
                            elif T > 0.755 and T <= 0.765:
                                T_step[16, 1] += V
                            elif T > 0.765 and T <= 0.775:
                                T_step[17, 1] += V
                            elif T > 0.775 and T <= 0.785:
                                T_step[18, 1] += V
                            elif T > 0.785 and T <= 0.795:
                                T_step[19, 1] += V
                            elif T > 0.795 and T <= 0.805:
                                T_step[20, 1] += V
                            elif T > 0.805 and T <= 0.815:
                                T_step[21, 1] += V
                            elif T > 0.815 and T <= 0.825:
                                T_step[22, 1] += V
                            elif T > 0.825 and T <= 0.835:
                                T_step[23, 1] += V
                            elif T > 0.835 and T <= 0.845:
                                T_step[24, 1] += V
                            elif T > 0.845 and T <= 0.855:
                                T_step[25, 1] += V
                            elif T > 0.855 and T <= 0.865:
                                T_step[26, 1] += V
                            elif T > 0.865 and T <= 0.875:
                                T_step[27, 1] += V
                            elif T > 0.875 and T <= 0.885:
                                T_step[28, 1] += V
                            elif T > 0.885 and T <= 0.895:
                                T_step[29, 1] += V
                            elif T > 0.895 and T <= 0.905:
                                T_step[30, 1] += V
                            elif T > 0.905 and T <= 0.915:
                                T_step[31, 1] += V
                            elif T > 0.915 and T <= 0.925:
                                T_step[32, 1] += V
                            elif T > 0.925 and T <= 0.935:
                                T_step[33, 1] += V
                            elif T > 0.935 and T <= 0.945:
                                T_step[34, 1] += V
                            elif T > 0.945 and T <= 0.955:
                                T_step[35, 1] += V
                            elif T > 0.955 and T <= 0.965:
                                T_step[36, 1] += V
                            elif T > 0.965 and T <= 0.975:
                                T_step[37, 1] += V
                            elif T > 0.975 and T <= 0.985:
                                T_step[38, 1] += V
                            elif T > 0.985 and T <= 0.995:
                                T_step[39, 1] += V
                            elif T > 0.995 and T <= 1.005:
                                T_step[40, 1] += V
                            elif T > 1.005 and T <= 1.015:
                                T_step[41, 1] += V
                            elif T > 1.015 and T <= 1.025:
                                T_step[42, 1] += V
                            elif T > 1.025 and T <= 1.035:
                                T_step[43, 1] += V
                            elif T > 1.035 and T <= 1.045:
                                T_step[44, 1] += V
                            elif T > 1.045 and T <= 1.055:
                                T_step[45, 1] += V
                            elif T > 1.055 and T <= 1.065:
                                T_step[46, 1] += V
                            elif T > 1.065 and T <= 1.075:
                                T_step[47, 1] += V
                            elif T > 1.075 and T <= 1.085:
                                T_step[48, 1] += V
                            elif T > 1.085 and T <= 1.095:
                                T_step[49, 1] += V
                            elif T > 1.095 and T <= 1.105:
                                T_step[50, 1] += V
                            elif T > 1.105 and T <= 1.115:
                                T_step[51, 1] += V
                            elif T > 1.115 and T <= 1.125:
                                T_step[52, 1] += V
                            elif T > 1.125 and T <= 1.135:
                                T_step[53, 1] += V
                            elif T > 1.165 and T <= 1.145:
                                T_step[54, 1] += V
                            elif T > 1.145 and T <= 1.155:
                                T_step[55, 1] += V
                            elif T > 1.155 and T <= 1.165:
                                T_step[56, 1] += V
                            elif T > 1.165 and T <= 1.175:
                                T_step[57, 1] += V
                            elif T > 1.175 and T <= 1.185:
                                T_step[58, 1] += V
                            elif T > 1.185 and T <= 1.195:
                                T_step[59, 1] += V
                            elif T > 1.195 and T <= 1.205:
                                T_step[60, 1] += V
                            elif T > 1.205 and T <= 1.215:
                                T_step[61, 1] += V
                            elif T > 1.215 and T <= 1.225:
                                T_step[62, 1] += V
                            elif T > 1.225 and T <= 1.235:
                                T_step[63, 1] += V
                            elif T > 1.235 and T <= 1.245:
                                T_step[64, 1] += V
                            elif T > 1.245 and T <= 1.255:
                                T_step[65, 1] += V
                            elif T > 1.255 and T <= 1.265:
                                T_step[66, 1] += V
                            elif T > 1.265 and T <= 1.275:
                                T_step[67, 1] += V
                            elif T > 1.275 and T <= 1.285:
                                T_step[68, 1] += V
                            elif T > 1.285 and T <= 1.295:
                                T_step[69, 1] += V
                            elif T > 1.295 and T <= 1.305:
                                T_step[70, 1] += V

                            
                            
    elif l == 6:
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
        # 将6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                T = key1 * key2 * key3 * key4 * key5 * key6
                                V = value1 * value2 * value3 * value4 * value5 * value6
                                if T > 0.595 and T <= 0.605:
                                    T_step[0, 1] += V
                                elif T > 0.605 and T <= 0.615:
                                    T_step[1, 1] += V
                                elif T > 0.615 and T <= 0.625:
                                    T_step[2, 1] += V
                                elif T > 0.625 and T <= 0.635:
                                    T_step[3, 1] += V
                                elif T > 0.635 and T <= 0.645:
                                    T_step[4, 1] += V
                                elif T > 0.645 and T <= 0.655:
                                    T_step[5, 1] += V
                                elif T > 0.655 and T <= 0.665:
                                    T_step[6, 1] += V
                                elif T > 0.665 and T <= 0.675:
                                    T_step[7, 1] += V
                                elif T > 0.675 and T <= 0.685:
                                    T_step[8, 1] += V
                                elif T > 0.685 and T <= 0.695:
                                    T_step[9, 1] += V
                                elif T > 0.695 and T <= 0.705:
                                    T_step[10, 1] += V
                                elif T > 0.705 and T <= 0.715:
                                    T_step[11, 1] += V
                                elif T > 0.715 and T <= 0.725:
                                    T_step[12, 1] += V
                                elif T > 0.725 and T <= 0.735:
                                    T_step[13, 1] += V
                                elif T > 0.735 and T <= 0.745:
                                    T_step[14, 1] += V
                                elif T > 0.745 and T <= 0.755:
                                    T_step[15, 1] += V
                                elif T > 0.755 and T <= 0.765:
                                    T_step[16, 1] += V
                                elif T > 0.765 and T <= 0.775:
                                    T_step[17, 1] += V
                                elif T > 0.775 and T <= 0.785:
                                    T_step[18, 1] += V
                                elif T > 0.785 and T <= 0.795:
                                    T_step[19, 1] += V
                                elif T > 0.795 and T <= 0.805:
                                    T_step[20, 1] += V
                                elif T > 0.805 and T <= 0.815:
                                    T_step[21, 1] += V
                                elif T > 0.815 and T <= 0.825:
                                    T_step[22, 1] += V
                                elif T > 0.825 and T <= 0.835:
                                    T_step[23, 1] += V
                                elif T > 0.835 and T <= 0.845:
                                    T_step[24, 1] += V
                                elif T > 0.845 and T <= 0.855:
                                    T_step[25, 1] += V
                                elif T > 0.855 and T <= 0.865:
                                    T_step[26, 1] += V
                                elif T > 0.865 and T <= 0.875:
                                    T_step[27, 1] += V
                                elif T > 0.875 and T <= 0.885:
                                    T_step[28, 1] += V
                                elif T > 0.885 and T <= 0.895:
                                    T_step[29, 1] += V
                                elif T > 0.895 and T <= 0.905:
                                    T_step[30, 1] += V
                                elif T > 0.905 and T <= 0.915:
                                    T_step[31, 1] += V
                                elif T > 0.915 and T <= 0.925:
                                    T_step[32, 1] += V
                                elif T > 0.925 and T <= 0.935:
                                    T_step[33, 1] += V
                                elif T > 0.935 and T <= 0.945:
                                    T_step[34, 1] += V
                                elif T > 0.945 and T <= 0.955:
                                    T_step[35, 1] += V
                                elif T > 0.955 and T <= 0.965:
                                    T_step[36, 1] += V
                                elif T > 0.965 and T <= 0.975:
                                    T_step[37, 1] += V
                                elif T > 0.975 and T <= 0.985:
                                    T_step[38, 1] += V
                                elif T > 0.985 and T <= 0.995:
                                    T_step[39, 1] += V
                                elif T > 0.995 and T <= 1.005:
                                    T_step[40, 1] += V
                                elif T > 1.005 and T <= 1.015:
                                    T_step[41, 1] += V
                                elif T > 1.015 and T <= 1.025:
                                    T_step[42, 1] += V
                                elif T > 1.025 and T <= 1.035:
                                    T_step[43, 1] += V
                                elif T > 1.035 and T <= 1.045:
                                    T_step[44, 1] += V
                                elif T > 1.045 and T <= 1.055:
                                    T_step[45, 1] += V
                                elif T > 1.055 and T <= 1.065:
                                    T_step[46, 1] += V
                                elif T > 1.065 and T <= 1.075:
                                    T_step[47, 1] += V
                                elif T > 1.075 and T <= 1.085:
                                    T_step[48, 1] += V
                                elif T > 1.085 and T <= 1.095:
                                    T_step[49, 1] += V
                                elif T > 1.095 and T <= 1.105:
                                    T_step[50, 1] += V
                                elif T > 1.105 and T <= 1.115:
                                    T_step[51, 1] += V
                                elif T > 1.115 and T <= 1.125:
                                    T_step[52, 1] += V
                                elif T > 1.125 and T <= 1.135:
                                    T_step[53, 1] += V
                                elif T > 1.165 and T <= 1.145:
                                    T_step[54, 1] += V
                                elif T > 1.145 and T <= 1.155:
                                    T_step[55, 1] += V
                                elif T > 1.155 and T <= 1.165:
                                    T_step[56, 1] += V
                                elif T > 1.165 and T <= 1.175:
                                    T_step[57, 1] += V
                                elif T > 1.175 and T <= 1.185:
                                    T_step[58, 1] += V
                                elif T > 1.185 and T <= 1.195:
                                    T_step[59, 1] += V
                                elif T > 1.195 and T <= 1.205:
                                    T_step[60, 1] += V
                                elif T > 1.205 and T <= 1.215:
                                    T_step[61, 1] += V
                                elif T > 1.215 and T <= 1.225:
                                    T_step[62, 1] += V
                                elif T > 1.225 and T <= 1.235:
                                    T_step[63, 1] += V
                                elif T > 1.235 and T <= 1.245:
                                    T_step[64, 1] += V
                                elif T > 1.245 and T <= 1.255:
                                    T_step[65, 1] += V
                                elif T > 1.255 and T <= 1.265:
                                    T_step[66, 1] += V
                                elif T > 1.265 and T <= 1.275:
                                    T_step[67, 1] += V
                                elif T > 1.275 and T <= 1.285:
                                    T_step[68, 1] += V
                                elif T > 1.285 and T <= 1.295:
                                    T_step[69, 1] += V
                                elif T > 1.295 and T <= 1.305:
                                    T_step[70, 1] += V
    elif l == 7:
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
        # 将6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    T = key1 * key2 * key3 * key4 * key5 * key6 * key7
                                    V = value1 * value2 * value3 * value4 * value5 * value6 * value7
                                    if T > 0.595 and T <= 0.605:
                                        T_step[0, 1] += V
                                    elif T > 0.605 and T <= 0.615:
                                        T_step[1, 1] += V
                                    elif T > 0.615 and T <= 0.625:
                                        T_step[2, 1] += V
                                    elif T > 0.625 and T <= 0.635:
                                        T_step[3, 1] += V
                                    elif T > 0.635 and T <= 0.645:
                                        T_step[4, 1] += V
                                    elif T > 0.645 and T <= 0.655:
                                        T_step[5, 1] += V
                                    elif T > 0.655 and T <= 0.665:
                                        T_step[6, 1] += V
                                    elif T > 0.665 and T <= 0.675:
                                        T_step[7, 1] += V
                                    elif T > 0.675 and T <= 0.685:
                                        T_step[8, 1] += V
                                    elif T > 0.685 and T <= 0.695:
                                        T_step[9, 1] += V
                                    elif T > 0.695 and T <= 0.705:
                                        T_step[10, 1] += V
                                    elif T > 0.705 and T <= 0.715:
                                        T_step[11, 1] += V
                                    elif T > 0.715 and T <= 0.725:
                                        T_step[12, 1] += V
                                    elif T > 0.725 and T <= 0.735:
                                        T_step[13, 1] += V
                                    elif T > 0.735 and T <= 0.745:
                                        T_step[14, 1] += V
                                    elif T > 0.745 and T <= 0.755:
                                        T_step[15, 1] += V
                                    elif T > 0.755 and T <= 0.765:
                                        T_step[16, 1] += V
                                    elif T > 0.765 and T <= 0.775:
                                        T_step[17, 1] += V
                                    elif T > 0.775 and T <= 0.785:
                                        T_step[18, 1] += V
                                    elif T > 0.785 and T <= 0.795:
                                        T_step[19, 1] += V
                                    elif T > 0.795 and T <= 0.805:
                                        T_step[20, 1] += V
                                    elif T > 0.805 and T <= 0.815:
                                        T_step[21, 1] += V
                                    elif T > 0.815 and T <= 0.825:
                                        T_step[22, 1] += V
                                    elif T > 0.825 and T <= 0.835:
                                        T_step[23, 1] += V
                                    elif T > 0.835 and T <= 0.845:
                                        T_step[24, 1] += V
                                    elif T > 0.845 and T <= 0.855:
                                        T_step[25, 1] += V
                                    elif T > 0.855 and T <= 0.865:
                                        T_step[26, 1] += V
                                    elif T > 0.865 and T <= 0.875:
                                        T_step[27, 1] += V
                                    elif T > 0.875 and T <= 0.885:
                                        T_step[28, 1] += V
                                    elif T > 0.885 and T <= 0.895:
                                        T_step[29, 1] += V
                                    elif T > 0.895 and T <= 0.905:
                                        T_step[30, 1] += V
                                    elif T > 0.905 and T <= 0.915:
                                        T_step[31, 1] += V
                                    elif T > 0.915 and T <= 0.925:
                                        T_step[32, 1] += V
                                    elif T > 0.925 and T <= 0.935:
                                        T_step[33, 1] += V
                                    elif T > 0.935 and T <= 0.945:
                                        T_step[34, 1] += V
                                    elif T > 0.945 and T <= 0.955:
                                        T_step[35, 1] += V
                                    elif T > 0.955 and T <= 0.965:
                                        T_step[36, 1] += V
                                    elif T > 0.965 and T <= 0.975:
                                        T_step[37, 1] += V
                                    elif T > 0.975 and T <= 0.985:
                                        T_step[38, 1] += V
                                    elif T > 0.985 and T <= 0.995:
                                        T_step[39, 1] += V
                                    elif T > 0.995 and T <= 1.005:
                                        T_step[40, 1] += V
                                    elif T > 1.005 and T <= 1.015:
                                        T_step[41, 1] += V
                                    elif T > 1.015 and T <= 1.025:
                                        T_step[42, 1] += V
                                    elif T > 1.025 and T <= 1.035:
                                        T_step[43, 1] += V
                                    elif T > 1.035 and T <= 1.045:
                                        T_step[44, 1] += V
                                    elif T > 1.045 and T <= 1.055:
                                        T_step[45, 1] += V
                                    elif T > 1.055 and T <= 1.065:
                                        T_step[46, 1] += V
                                    elif T > 1.065 and T <= 1.075:
                                        T_step[47, 1] += V
                                    elif T > 1.075 and T <= 1.085:
                                        T_step[48, 1] += V
                                    elif T > 1.085 and T <= 1.095:
                                        T_step[49, 1] += V
                                    elif T > 1.095 and T <= 1.105:
                                        T_step[50, 1] += V
                                    elif T > 1.105 and T <= 1.115:
                                        T_step[51, 1] += V
                                    elif T > 1.115 and T <= 1.125:
                                        T_step[52, 1] += V
                                    elif T > 1.125 and T <= 1.135:
                                        T_step[53, 1] += V
                                    elif T > 1.165 and T <= 1.145:
                                        T_step[54, 1] += V
                                    elif T > 1.145 and T <= 1.155:
                                        T_step[55, 1] += V
                                    elif T > 1.155 and T <= 1.165:
                                        T_step[56, 1] += V
                                    elif T > 1.165 and T <= 1.175:
                                        T_step[57, 1] += V
                                    elif T > 1.175 and T <= 1.185:
                                        T_step[58, 1] += V
                                    elif T > 1.185 and T <= 1.195:
                                        T_step[59, 1] += V
                                    elif T > 1.195 and T <= 1.205:
                                        T_step[60, 1] += V
                                    elif T > 1.205 and T <= 1.215:
                                        T_step[61, 1] += V
                                    elif T > 1.215 and T <= 1.225:
                                        T_step[62, 1] += V
                                    elif T > 1.225 and T <= 1.235:
                                        T_step[63, 1] += V
                                    elif T > 1.235 and T <= 1.245:
                                        T_step[64, 1] += V
                                    elif T > 1.245 and T <= 1.255:
                                        T_step[65, 1] += V
                                    elif T > 1.255 and T <= 1.265:
                                        T_step[66, 1] += V
                                    elif T > 1.265 and T <= 1.275:
                                        T_step[67, 1] += V
                                    elif T > 1.275 and T <= 1.285:
                                        T_step[68, 1] += V
                                    elif T > 1.285 and T <= 1.295:
                                        T_step[69, 1] += V
                                    elif T > 1.295 and T <= 1.305:
                                        T_step[70, 1] += V

    elif l == 8:
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

        # 将6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    for key8, value8 in dict8.items():
                                        T = key1 * key2 * key3 * key4 * key5 * key6 * key7 * key8
                                        V = value1 * value2 * value3 * value4 * value5 * value6 * value7 * value8
                                        if T > 0.595 and T <= 0.605:
                                            T_step[0, 1] += V
                                        elif T > 0.605 and T <= 0.615:
                                            T_step[1, 1] += V
                                        elif T > 0.615 and T <= 0.625:
                                            T_step[2, 1] += V
                                        elif T > 0.625 and T <= 0.635:
                                            T_step[3, 1] += V
                                        elif T > 0.635 and T <= 0.645:
                                            T_step[4, 1] += V
                                        elif T > 0.645 and T <= 0.655:
                                            T_step[5, 1] += V
                                        elif T > 0.655 and T <= 0.665:
                                            T_step[6, 1] += V
                                        elif T > 0.665 and T <= 0.675:
                                            T_step[7, 1] += V
                                        elif T > 0.675 and T <= 0.685:
                                            T_step[8, 1] += V
                                        elif T > 0.685 and T <= 0.695:
                                            T_step[9, 1] += V
                                        elif T > 0.695 and T <= 0.705:
                                            T_step[10, 1] += V
                                        elif T > 0.705 and T <= 0.715:
                                            T_step[11, 1] += V
                                        elif T > 0.715 and T <= 0.725:
                                            T_step[12, 1] += V
                                        elif T > 0.725 and T <= 0.735:
                                            T_step[13, 1] += V
                                        elif T > 0.735 and T <= 0.745:
                                            T_step[14, 1] += V
                                        elif T > 0.745 and T <= 0.755:
                                            T_step[15, 1] += V
                                        elif T > 0.755 and T <= 0.765:
                                            T_step[16, 1] += V
                                        elif T > 0.765 and T <= 0.775:
                                            T_step[17, 1] += V
                                        elif T > 0.775 and T <= 0.785:
                                            T_step[18, 1] += V
                                        elif T > 0.785 and T <= 0.795:
                                            T_step[19, 1] += V
                                        elif T > 0.795 and T <= 0.805:
                                            T_step[20, 1] += V
                                        elif T > 0.805 and T <= 0.815:
                                            T_step[21, 1] += V
                                        elif T > 0.815 and T <= 0.825:
                                            T_step[22, 1] += V
                                        elif T > 0.825 and T <= 0.835:
                                            T_step[23, 1] += V
                                        elif T > 0.835 and T <= 0.845:
                                            T_step[24, 1] += V
                                        elif T > 0.845 and T <= 0.855:
                                            T_step[25, 1] += V
                                        elif T > 0.855 and T <= 0.865:
                                            T_step[26, 1] += V
                                        elif T > 0.865 and T <= 0.875:
                                            T_step[27, 1] += V
                                        elif T > 0.875 and T <= 0.885:
                                            T_step[28, 1] += V
                                        elif T > 0.885 and T <= 0.895:
                                            T_step[29, 1] += V
                                        elif T > 0.895 and T <= 0.905:
                                            T_step[30, 1] += V
                                        elif T > 0.905 and T <= 0.915:
                                            T_step[31, 1] += V
                                        elif T > 0.915 and T <= 0.925:
                                            T_step[32, 1] += V
                                        elif T > 0.925 and T <= 0.935:
                                            T_step[33, 1] += V
                                        elif T > 0.935 and T <= 0.945:
                                            T_step[34, 1] += V
                                        elif T > 0.945 and T <= 0.955:
                                            T_step[35, 1] += V
                                        elif T > 0.955 and T <= 0.965:
                                            T_step[36, 1] += V
                                        elif T > 0.965 and T <= 0.975:
                                            T_step[37, 1] += V
                                        elif T > 0.975 and T <= 0.985:
                                            T_step[38, 1] += V
                                        elif T > 0.985 and T <= 0.995:
                                            T_step[39, 1] += V
                                        elif T > 0.995 and T <= 1.005:
                                            T_step[40, 1] += V
                                        elif T > 1.005 and T <= 1.015:
                                            T_step[41, 1] += V
                                        elif T > 1.015 and T <= 1.025:
                                            T_step[42, 1] += V
                                        elif T > 1.025 and T <= 1.035:
                                            T_step[43, 1] += V
                                        elif T > 1.035 and T <= 1.045:
                                            T_step[44, 1] += V
                                        elif T > 1.045 and T <= 1.055:
                                            T_step[45, 1] += V
                                        elif T > 1.055 and T <= 1.065:
                                            T_step[46, 1] += V
                                        elif T > 1.065 and T <= 1.075:
                                            T_step[47, 1] += V
                                        elif T > 1.075 and T <= 1.085:
                                            T_step[48, 1] += V
                                        elif T > 1.085 and T <= 1.095:
                                            T_step[49, 1] += V
                                        elif T > 1.095 and T <= 1.105:
                                            T_step[50, 1] += V
                                        elif T > 1.105 and T <= 1.115:
                                            T_step[51, 1] += V
                                        elif T > 1.115 and T <= 1.125:
                                            T_step[52, 1] += V
                                        elif T > 1.125 and T <= 1.135:
                                            T_step[53, 1] += V
                                        elif T > 1.165 and T <= 1.145:
                                            T_step[54, 1] += V
                                        elif T > 1.145 and T <= 1.155:
                                            T_step[55, 1] += V
                                        elif T > 1.155 and T <= 1.165:
                                            T_step[56, 1] += V
                                        elif T > 1.165 and T <= 1.175:
                                            T_step[57, 1] += V
                                        elif T > 1.175 and T <= 1.185:
                                            T_step[58, 1] += V
                                        elif T > 1.185 and T <= 1.195:
                                            T_step[59, 1] += V
                                        elif T > 1.195 and T <= 1.205:
                                            T_step[60, 1] += V
                                        elif T > 1.205 and T <= 1.215:
                                            T_step[61, 1] += V
                                        elif T > 1.215 and T <= 1.225:
                                            T_step[62, 1] += V
                                        elif T > 1.225 and T <= 1.235:
                                            T_step[63, 1] += V
                                        elif T > 1.235 and T <= 1.245:
                                            T_step[64, 1] += V
                                        elif T > 1.245 and T <= 1.255:
                                            T_step[65, 1] += V
                                        elif T > 1.255 and T <= 1.265:
                                            T_step[66, 1] += V
                                        elif T > 1.265 and T <= 1.275:
                                            T_step[67, 1] += V
                                        elif T > 1.275 and T <= 1.285:
                                            T_step[68, 1] += V
                                        elif T > 1.285 and T <= 1.295:
                                            T_step[69, 1] += V
                                        elif T > 1.295 and T <= 1.305:
                                            T_step[70, 1] += V
    elif l == 9:
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

        # 将6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    for key8, value8 in dict8.items():
                                        for key9, value9 in dict9.items():
                                            T = key1 * key2 * key3 * key4 * key5 * key6 * key7 * key8 * key9
                                            V = value1 * value2 * value3 * value4 * value5 * value6 * value7 * value8 * value9
                                            if T > 0.595 and T <= 0.605:
                                                T_step[0, 1] += V
                                            elif T > 0.605 and T <= 0.615:
                                                T_step[1, 1] += V
                                            elif T > 0.615 and T <= 0.625:
                                                T_step[2, 1] += V
                                            elif T > 0.625 and T <= 0.635:
                                                T_step[3, 1] += V
                                            elif T > 0.635 and T <= 0.645:
                                                T_step[4, 1] += V
                                            elif T > 0.645 and T <= 0.655:
                                                T_step[5, 1] += V
                                            elif T > 0.655 and T <= 0.665:
                                                T_step[6, 1] += V
                                            elif T > 0.665 and T <= 0.675:
                                                T_step[7, 1] += V
                                            elif T > 0.675 and T <= 0.685:
                                                T_step[8, 1] += V
                                            elif T > 0.685 and T <= 0.695:
                                                T_step[9, 1] += V
                                            elif T > 0.695 and T <= 0.705:
                                                T_step[10, 1] += V
                                            elif T > 0.705 and T <= 0.715:
                                                T_step[11, 1] += V
                                            elif T > 0.715 and T <= 0.725:
                                                T_step[12, 1] += V
                                            elif T > 0.725 and T <= 0.735:
                                                T_step[13, 1] += V
                                            elif T > 0.735 and T <= 0.745:
                                                T_step[14, 1] += V
                                            elif T > 0.745 and T <= 0.755:
                                                T_step[15, 1] += V
                                            elif T > 0.755 and T <= 0.765:
                                                T_step[16, 1] += V
                                            elif T > 0.765 and T <= 0.775:
                                                T_step[17, 1] += V
                                            elif T > 0.775 and T <= 0.785:
                                                T_step[18, 1] += V
                                            elif T > 0.785 and T <= 0.795:
                                                T_step[19, 1] += V
                                            elif T > 0.795 and T <= 0.805:
                                                T_step[20, 1] += V
                                            elif T > 0.805 and T <= 0.815:
                                                T_step[21, 1] += V
                                            elif T > 0.815 and T <= 0.825:
                                                T_step[22, 1] += V
                                            elif T > 0.825 and T <= 0.835:
                                                T_step[23, 1] += V
                                            elif T > 0.835 and T <= 0.845:
                                                T_step[24, 1] += V
                                            elif T > 0.845 and T <= 0.855:
                                                T_step[25, 1] += V
                                            elif T > 0.855 and T <= 0.865:
                                                T_step[26, 1] += V
                                            elif T > 0.865 and T <= 0.875:
                                                T_step[27, 1] += V
                                            elif T > 0.875 and T <= 0.885:
                                                T_step[28, 1] += V
                                            elif T > 0.885 and T <= 0.895:
                                                T_step[29, 1] += V
                                            elif T > 0.895 and T <= 0.905:
                                                T_step[30, 1] += V
                                            elif T > 0.905 and T <= 0.915:
                                                T_step[31, 1] += V
                                            elif T > 0.915 and T <= 0.925:
                                                T_step[32, 1] += V
                                            elif T > 0.925 and T <= 0.935:
                                                T_step[33, 1] += V
                                            elif T > 0.935 and T <= 0.945:
                                                T_step[34, 1] += V
                                            elif T > 0.945 and T <= 0.955:
                                                T_step[35, 1] += V
                                            elif T > 0.955 and T <= 0.965:
                                                T_step[36, 1] += V
                                            elif T > 0.965 and T <= 0.975:
                                                T_step[37, 1] += V
                                            elif T > 0.975 and T <= 0.985:
                                                T_step[38, 1] += V
                                            elif T > 0.985 and T <= 0.995:
                                                T_step[39, 1] += V
                                            elif T > 0.995 and T <= 1.005:
                                                T_step[40, 1] += V
                                            elif T > 1.005 and T <= 1.015:
                                                T_step[41, 1] += V
                                            elif T > 1.015 and T <= 1.025:
                                                T_step[42, 1] += V
                                            elif T > 1.025 and T <= 1.035:
                                                T_step[43, 1] += V
                                            elif T > 1.035 and T <= 1.045:
                                                T_step[44, 1] += V
                                            elif T > 1.045 and T <= 1.055:
                                                T_step[45, 1] += V
                                            elif T > 1.055 and T <= 1.065:
                                                T_step[46, 1] += V
                                            elif T > 1.065 and T <= 1.075:
                                                T_step[47, 1] += V
                                            elif T > 1.075 and T <= 1.085:
                                                T_step[48, 1] += V
                                            elif T > 1.085 and T <= 1.095:
                                                T_step[49, 1] += V
                                            elif T > 1.095 and T <= 1.105:
                                                T_step[50, 1] += V
                                            elif T > 1.105 and T <= 1.115:
                                                T_step[51, 1] += V
                                            elif T > 1.115 and T <= 1.125:
                                                T_step[52, 1] += V
                                            elif T > 1.125 and T <= 1.135:
                                                T_step[53, 1] += V
                                            elif T > 1.165 and T <= 1.145:
                                                T_step[54, 1] += V
                                            elif T > 1.145 and T <= 1.155:
                                                T_step[55, 1] += V
                                            elif T > 1.155 and T <= 1.165:
                                                T_step[56, 1] += V
                                            elif T > 1.165 and T <= 1.175:
                                                T_step[57, 1] += V
                                            elif T > 1.175 and T <= 1.185:
                                                T_step[58, 1] += V
                                            elif T > 1.185 and T <= 1.195:
                                                T_step[59, 1] += V
                                            elif T > 1.195 and T <= 1.205:
                                                T_step[60, 1] += V
                                            elif T > 1.205 and T <= 1.215:
                                                T_step[61, 1] += V
                                            elif T > 1.215 and T <= 1.225:
                                                T_step[62, 1] += V
                                            elif T > 1.225 and T <= 1.235:
                                                T_step[63, 1] += V
                                            elif T > 1.235 and T <= 1.245:
                                                T_step[64, 1] += V
                                            elif T > 1.245 and T <= 1.255:
                                                T_step[65, 1] += V
                                            elif T > 1.255 and T <= 1.265:
                                                T_step[66, 1] += V
                                            elif T > 1.265 and T <= 1.275:
                                                T_step[67, 1] += V
                                            elif T > 1.275 and T <= 1.285:
                                                T_step[68, 1] += V
                                            elif T > 1.285 and T <= 1.295:
                                                T_step[69, 1] += V
                                            elif T > 1.295 and T <= 1.305:
                                                T_step[70, 1] += V
    elif l == 10:
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

        # 将6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    for key8, value8 in dict8.items():
                                        for key9, value9 in dict9.items():
                                            for key10, value10 in dict10.items():
                                                T = key1 * key2 * key3 * key4 * key5 * key6 * key7 * key8 * key9 * key10
                                                V = value1 * value2 * value3 * value4 * value5 * value6 * value7 * value8 * value9 * value10
                                                if T > 0.595 and T <= 0.605:
                                                    T_step[0, 1] += V
                                                elif T > 0.605 and T <= 0.615:
                                                    T_step[1, 1] += V
                                                elif T > 0.615 and T <= 0.625:
                                                    T_step[2, 1] += V
                                                elif T > 0.625 and T <= 0.635:
                                                    T_step[3, 1] += V
                                                elif T > 0.635 and T <= 0.645:
                                                    T_step[4, 1] += V
                                                elif T > 0.645 and T <= 0.655:
                                                    T_step[5, 1] += V
                                                elif T > 0.655 and T <= 0.665:
                                                    T_step[6, 1] += V
                                                elif T > 0.665 and T <= 0.675:
                                                    T_step[7, 1] += V
                                                elif T > 0.675 and T <= 0.685:
                                                    T_step[8, 1] += V
                                                elif T > 0.685 and T <= 0.695:
                                                    T_step[9, 1] += V
                                                elif T > 0.695 and T <= 0.705:
                                                    T_step[10, 1] += V
                                                elif T > 0.705 and T <= 0.715:
                                                    T_step[11, 1] += V
                                                elif T > 0.715 and T <= 0.725:
                                                    T_step[12, 1] += V
                                                elif T > 0.725 and T <= 0.735:
                                                    T_step[13, 1] += V
                                                elif T > 0.735 and T <= 0.745:
                                                    T_step[14, 1] += V
                                                elif T > 0.745 and T <= 0.755:
                                                    T_step[15, 1] += V
                                                elif T > 0.755 and T <= 0.765:
                                                    T_step[16, 1] += V
                                                elif T > 0.765 and T <= 0.775:
                                                    T_step[17, 1] += V
                                                elif T > 0.775 and T <= 0.785:
                                                    T_step[18, 1] += V
                                                elif T > 0.785 and T <= 0.795:
                                                    T_step[19, 1] += V
                                                elif T > 0.795 and T <= 0.805:
                                                    T_step[20, 1] += V
                                                elif T > 0.805 and T <= 0.815:
                                                    T_step[21, 1] += V
                                                elif T > 0.815 and T <= 0.825:
                                                    T_step[22, 1] += V
                                                elif T > 0.825 and T <= 0.835:
                                                    T_step[23, 1] += V
                                                elif T > 0.835 and T <= 0.845:
                                                    T_step[24, 1] += V
                                                elif T > 0.845 and T <= 0.855:
                                                    T_step[25, 1] += V
                                                elif T > 0.855 and T <= 0.865:
                                                    T_step[26, 1] += V
                                                elif T > 0.865 and T <= 0.875:
                                                    T_step[27, 1] += V
                                                elif T > 0.875 and T <= 0.885:
                                                    T_step[28, 1] += V
                                                elif T > 0.885 and T <= 0.895:
                                                    T_step[29, 1] += V
                                                elif T > 0.895 and T <= 0.905:
                                                    T_step[30, 1] += V
                                                elif T > 0.905 and T <= 0.915:
                                                    T_step[31, 1] += V
                                                elif T > 0.915 and T <= 0.925:
                                                    T_step[32, 1] += V
                                                elif T > 0.925 and T <= 0.935:
                                                    T_step[33, 1] += V
                                                elif T > 0.935 and T <= 0.945:
                                                    T_step[34, 1] += V
                                                elif T > 0.945 and T <= 0.955:
                                                    T_step[35, 1] += V
                                                elif T > 0.955 and T <= 0.965:
                                                    T_step[36, 1] += V
                                                elif T > 0.965 and T <= 0.975:
                                                    T_step[37, 1] += V
                                                elif T > 0.975 and T <= 0.985:
                                                    T_step[38, 1] += V
                                                elif T > 0.985 and T <= 0.995:
                                                    T_step[39, 1] += V
                                                elif T > 0.995 and T <= 1.005:
                                                    T_step[40, 1] += V
                                                elif T > 1.005 and T <= 1.015:
                                                    T_step[41, 1] += V
                                                elif T > 1.015 and T <= 1.025:
                                                    T_step[42, 1] += V
                                                elif T > 1.025 and T <= 1.035:
                                                    T_step[43, 1] += V
                                                elif T > 1.035 and T <= 1.045:
                                                    T_step[44, 1] += V
                                                elif T > 1.045 and T <= 1.055:
                                                    T_step[45, 1] += V
                                                elif T > 1.055 and T <= 1.065:
                                                    T_step[46, 1] += V
                                                elif T > 1.065 and T <= 1.075:
                                                    T_step[47, 1] += V
                                                elif T > 1.075 and T <= 1.085:
                                                    T_step[48, 1] += V
                                                elif T > 1.085 and T <= 1.095:
                                                    T_step[49, 1] += V
                                                elif T > 1.095 and T <= 1.105:
                                                    T_step[50, 1] += V
                                                elif T > 1.105 and T <= 1.115:
                                                    T_step[51, 1] += V
                                                elif T > 1.115 and T <= 1.125:
                                                    T_step[52, 1] += V
                                                elif T > 1.125 and T <= 1.135:
                                                    T_step[53, 1] += V
                                                elif T > 1.165 and T <= 1.145:
                                                    T_step[54, 1] += V
                                                elif T > 1.145 and T <= 1.155:
                                                    T_step[55, 1] += V
                                                elif T > 1.155 and T <= 1.165:
                                                    T_step[56, 1] += V
                                                elif T > 1.165 and T <= 1.175:
                                                    T_step[57, 1] += V
                                                elif T > 1.175 and T <= 1.185:
                                                    T_step[58, 1] += V
                                                elif T > 1.185 and T <= 1.195:
                                                    T_step[59, 1] += V
                                                elif T > 1.195 and T <= 1.205:
                                                    T_step[60, 1] += V
                                                elif T > 1.205 and T <= 1.215:
                                                    T_step[61, 1] += V
                                                elif T > 1.215 and T <= 1.225:
                                                    T_step[62, 1] += V
                                                elif T > 1.225 and T <= 1.235:
                                                    T_step[63, 1] += V
                                                elif T > 1.235 and T <= 1.245:
                                                    T_step[64, 1] += V
                                                elif T > 1.245 and T <= 1.255:
                                                    T_step[65, 1] += V
                                                elif T > 1.255 and T <= 1.265:
                                                    T_step[66, 1] += V
                                                elif T > 1.265 and T <= 1.275:
                                                    T_step[67, 1] += V
                                                elif T > 1.275 and T <= 1.285:
                                                    T_step[68, 1] += V
                                                elif T > 1.285 and T <= 1.295:
                                                    T_step[69, 1] += V
                                                elif T > 1.295 and T <= 1.305:
                                                    T_step[70, 1] += V
    elif l == 11:
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

        # 将6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    for key8, value8 in dict8.items():
                                        for key9, value9 in dict9.items():
                                            for key10, value10 in dict10.items():
                                                for key11, value11 in dict11.items():
                                                    T = key1 * key2 * key3 * key4 * key5 * key6 * key7 * key8 * key9 * key10 * key11
                                                    V = value1 * value2 * value3 * value4 * value5 * value6 * value7 * value8 * value9 * value10 * value11
                                                    if T > 0.595 and T <= 0.605:
                                                        T_step[0, 1] += V
                                                    elif T > 0.605 and T <= 0.615:
                                                        T_step[1, 1] += V
                                                    elif T > 0.615 and T <= 0.625:
                                                        T_step[2, 1] += V
                                                    elif T > 0.625 and T <= 0.635:
                                                        T_step[3, 1] += V
                                                    elif T > 0.635 and T <= 0.645:
                                                        T_step[4, 1] += V
                                                    elif T > 0.645 and T <= 0.655:
                                                        T_step[5, 1] += V
                                                    elif T > 0.655 and T <= 0.665:
                                                        T_step[6, 1] += V
                                                    elif T > 0.665 and T <= 0.675:
                                                        T_step[7, 1] += V
                                                    elif T > 0.675 and T <= 0.685:
                                                        T_step[8, 1] += V
                                                    elif T > 0.685 and T <= 0.695:
                                                        T_step[9, 1] += V
                                                    elif T > 0.695 and T <= 0.705:
                                                        T_step[10, 1] += V
                                                    elif T > 0.705 and T <= 0.715:
                                                        T_step[11, 1] += V
                                                    elif T > 0.715 and T <= 0.725:
                                                        T_step[12, 1] += V
                                                    elif T > 0.725 and T <= 0.735:
                                                        T_step[13, 1] += V
                                                    elif T > 0.735 and T <= 0.745:
                                                        T_step[14, 1] += V
                                                    elif T > 0.745 and T <= 0.755:
                                                        T_step[15, 1] += V
                                                    elif T > 0.755 and T <= 0.765:
                                                        T_step[16, 1] += V
                                                    elif T > 0.765 and T <= 0.775:
                                                        T_step[17, 1] += V
                                                    elif T > 0.775 and T <= 0.785:
                                                        T_step[18, 1] += V
                                                    elif T > 0.785 and T <= 0.795:
                                                        T_step[19, 1] += V
                                                    elif T > 0.795 and T <= 0.805:
                                                        T_step[20, 1] += V
                                                    elif T > 0.805 and T <= 0.815:
                                                        T_step[21, 1] += V
                                                    elif T > 0.815 and T <= 0.825:
                                                        T_step[22, 1] += V
                                                    elif T > 0.825 and T <= 0.835:
                                                        T_step[23, 1] += V
                                                    elif T > 0.835 and T <= 0.845:
                                                        T_step[24, 1] += V
                                                    elif T > 0.845 and T <= 0.855:
                                                        T_step[25, 1] += V
                                                    elif T > 0.855 and T <= 0.865:
                                                        T_step[26, 1] += V
                                                    elif T > 0.865 and T <= 0.875:
                                                        T_step[27, 1] += V
                                                    elif T > 0.875 and T <= 0.885:
                                                        T_step[28, 1] += V
                                                    elif T > 0.885 and T <= 0.895:
                                                        T_step[29, 1] += V
                                                    elif T > 0.895 and T <= 0.905:
                                                        T_step[30, 1] += V
                                                    elif T > 0.905 and T <= 0.915:
                                                        T_step[31, 1] += V
                                                    elif T > 0.915 and T <= 0.925:
                                                        T_step[32, 1] += V
                                                    elif T > 0.925 and T <= 0.935:
                                                        T_step[33, 1] += V
                                                    elif T > 0.935 and T <= 0.945:
                                                        T_step[34, 1] += V
                                                    elif T > 0.945 and T <= 0.955:
                                                        T_step[35, 1] += V
                                                    elif T > 0.955 and T <= 0.965:
                                                        T_step[36, 1] += V
                                                    elif T > 0.965 and T <= 0.975:
                                                        T_step[37, 1] += V
                                                    elif T > 0.975 and T <= 0.985:
                                                        T_step[38, 1] += V
                                                    elif T > 0.985 and T <= 0.995:
                                                        T_step[39, 1] += V
                                                    elif T > 0.995 and T <= 1.005:
                                                        T_step[40, 1] += V
                                                    elif T > 1.005 and T <= 1.015:
                                                        T_step[41, 1] += V
                                                    elif T > 1.015 and T <= 1.025:
                                                        T_step[42, 1] += V
                                                    elif T > 1.025 and T <= 1.035:
                                                        T_step[43, 1] += V
                                                    elif T > 1.035 and T <= 1.045:
                                                        T_step[44, 1] += V
                                                    elif T > 1.045 and T <= 1.055:
                                                        T_step[45, 1] += V
                                                    elif T > 1.055 and T <= 1.065:
                                                        T_step[46, 1] += V
                                                    elif T > 1.065 and T <= 1.075:
                                                        T_step[47, 1] += V
                                                    elif T > 1.075 and T <= 1.085:
                                                        T_step[48, 1] += V
                                                    elif T > 1.085 and T <= 1.095:
                                                        T_step[49, 1] += V
                                                    elif T > 1.095 and T <= 1.105:
                                                        T_step[50, 1] += V
                                                    elif T > 1.105 and T <= 1.115:
                                                        T_step[51, 1] += V
                                                    elif T > 1.115 and T <= 1.125:
                                                        T_step[52, 1] += V
                                                    elif T > 1.125 and T <= 1.135:
                                                        T_step[53, 1] += V
                                                    elif T > 1.165 and T <= 1.145:
                                                        T_step[54, 1] += V
                                                    elif T > 1.145 and T <= 1.155:
                                                        T_step[55, 1] += V
                                                    elif T > 1.155 and T <= 1.165:
                                                        T_step[56, 1] += V
                                                    elif T > 1.165 and T <= 1.175:
                                                        T_step[57, 1] += V
                                                    elif T > 1.175 and T <= 1.185:
                                                        T_step[58, 1] += V
                                                    elif T > 1.185 and T <= 1.195:
                                                        T_step[59, 1] += V
                                                    elif T > 1.195 and T <= 1.205:
                                                        T_step[60, 1] += V
                                                    elif T > 1.205 and T <= 1.215:
                                                        T_step[61, 1] += V
                                                    elif T > 1.215 and T <= 1.225:
                                                        T_step[62, 1] += V
                                                    elif T > 1.225 and T <= 1.235:
                                                        T_step[63, 1] += V
                                                    elif T > 1.235 and T <= 1.245:
                                                        T_step[64, 1] += V
                                                    elif T > 1.245 and T <= 1.255:
                                                        T_step[65, 1] += V
                                                    elif T > 1.255 and T <= 1.265:
                                                        T_step[66, 1] += V
                                                    elif T > 1.265 and T <= 1.275:
                                                        T_step[67, 1] += V
                                                    elif T > 1.275 and T <= 1.285:
                                                        T_step[68, 1] += V
                                                    elif T > 1.285 and T <= 1.295:
                                                        T_step[69, 1] += V
                                                    elif T > 1.295 and T <= 1.305:
                                                        T_step[70, 1] += V
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

        # 将6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    for key8, value8 in dict8.items():
                                        for key9, value9 in dict9.items():
                                            for key10, value10 in dict10.items():
                                                for key11, value11 in dict11.items():
                                                    for key12, value12 in dict12.items():
                                                        T = key1 * key2 * key3 * key4 * key5 * key6 * key7 * key8 * key9 * key10 * key11 * key12
                                                        V = value1 * value2 * value3 * value4 * value5 * value6 * value7 * value8 * value9 * value10 * value11 * value12
                                                        if T > 0.595 and T <= 0.605:
                                                            T_step[0, 1] += V
                                                        elif T > 0.605 and T <= 0.615:
                                                            T_step[1, 1] += V
                                                        elif T > 0.615 and T <= 0.625:
                                                            T_step[2, 1] += V
                                                        elif T > 0.625 and T <= 0.635:
                                                            T_step[3, 1] += V
                                                        elif T > 0.635 and T <= 0.645:
                                                            T_step[4, 1] += V
                                                        elif T > 0.645 and T <= 0.655:
                                                            T_step[5, 1] += V
                                                        elif T > 0.655 and T <= 0.665:
                                                            T_step[6, 1] += V
                                                        elif T > 0.665 and T <= 0.675:
                                                            T_step[7, 1] += V
                                                        elif T > 0.675 and T <= 0.685:
                                                            T_step[8, 1] += V
                                                        elif T > 0.685 and T <= 0.695:
                                                            T_step[9, 1] += V
                                                        elif T > 0.695 and T <= 0.705:
                                                            T_step[10, 1] += V
                                                        elif T > 0.705 and T <= 0.715:
                                                            T_step[11, 1] += V
                                                        elif T > 0.715 and T <= 0.725:
                                                            T_step[12, 1] += V
                                                        elif T > 0.725 and T <= 0.735:
                                                            T_step[13, 1] += V
                                                        elif T > 0.735 and T <= 0.745:
                                                            T_step[14, 1] += V
                                                        elif T > 0.745 and T <= 0.755:
                                                            T_step[15, 1] += V
                                                        elif T > 0.755 and T <= 0.765:
                                                            T_step[16, 1] += V
                                                        elif T > 0.765 and T <= 0.775:
                                                            T_step[17, 1] += V
                                                        elif T > 0.775 and T <= 0.785:
                                                            T_step[18, 1] += V
                                                        elif T > 0.785 and T <= 0.795:
                                                            T_step[19, 1] += V
                                                        elif T > 0.795 and T <= 0.805:
                                                            T_step[20, 1] += V
                                                        elif T > 0.805 and T <= 0.815:
                                                            T_step[21, 1] += V
                                                        elif T > 0.815 and T <= 0.825:
                                                            T_step[22, 1] += V
                                                        elif T > 0.825 and T <= 0.835:
                                                            T_step[23, 1] += V
                                                        elif T > 0.835 and T <= 0.845:
                                                            T_step[24, 1] += V
                                                        elif T > 0.845 and T <= 0.855:
                                                            T_step[25, 1] += V
                                                        elif T > 0.855 and T <= 0.865:
                                                            T_step[26, 1] += V
                                                        elif T > 0.865 and T <= 0.875:
                                                            T_step[27, 1] += V
                                                        elif T > 0.875 and T <= 0.885:
                                                            T_step[28, 1] += V
                                                        elif T > 0.885 and T <= 0.895:
                                                            T_step[29, 1] += V
                                                        elif T > 0.895 and T <= 0.905:
                                                            T_step[30, 1] += V
                                                        elif T > 0.905 and T <= 0.915:
                                                            T_step[31, 1] += V
                                                        elif T > 0.915 and T <= 0.925:
                                                            T_step[32, 1] += V
                                                        elif T > 0.925 and T <= 0.935:
                                                            T_step[33, 1] += V
                                                        elif T > 0.935 and T <= 0.945:
                                                            T_step[34, 1] += V
                                                        elif T > 0.945 and T <= 0.955:
                                                            T_step[35, 1] += V
                                                        elif T > 0.955 and T <= 0.965:
                                                            T_step[36, 1] += V
                                                        elif T > 0.965 and T <= 0.975:
                                                            T_step[37, 1] += V
                                                        elif T > 0.975 and T <= 0.985:
                                                            T_step[38, 1] += V
                                                        elif T > 0.985 and T <= 0.995:
                                                            T_step[39, 1] += V
                                                        elif T > 0.995 and T <= 1.005:
                                                            T_step[40, 1] += V
                                                        elif T > 1.005 and T <= 1.015:
                                                            T_step[41, 1] += V
                                                        elif T > 1.015 and T <= 1.025:
                                                            T_step[42, 1] += V
                                                        elif T > 1.025 and T <= 1.035:
                                                            T_step[43, 1] += V
                                                        elif T > 1.035 and T <= 1.045:
                                                            T_step[44, 1] += V
                                                        elif T > 1.045 and T <= 1.055:
                                                            T_step[45, 1] += V
                                                        elif T > 1.055 and T <= 1.065:
                                                            T_step[46, 1] += V
                                                        elif T > 1.065 and T <= 1.075:
                                                            T_step[47, 1] += V
                                                        elif T > 1.075 and T <= 1.085:
                                                            T_step[48, 1] += V
                                                        elif T > 1.085 and T <= 1.095:
                                                            T_step[49, 1] += V
                                                        elif T > 1.095 and T <= 1.105:
                                                            T_step[50, 1] += V
                                                        elif T > 1.105 and T <= 1.115:
                                                            T_step[51, 1] += V
                                                        elif T > 1.115 and T <= 1.125:
                                                            T_step[52, 1] += V
                                                        elif T > 1.125 and T <= 1.135:
                                                            T_step[53, 1] += V
                                                        elif T > 1.165 and T <= 1.145:
                                                            T_step[54, 1] += V
                                                        elif T > 1.145 and T <= 1.155:
                                                            T_step[55, 1] += V
                                                        elif T > 1.155 and T <= 1.165:
                                                            T_step[56, 1] += V
                                                        elif T > 1.165 and T <= 1.175:
                                                            T_step[57, 1] += V
                                                        elif T > 1.175 and T <= 1.185:
                                                            T_step[58, 1] += V
                                                        elif T > 1.185 and T <= 1.195:
                                                            T_step[59, 1] += V
                                                        elif T > 1.195 and T <= 1.205:
                                                            T_step[60, 1] += V
                                                        elif T > 1.205 and T <= 1.215:
                                                            T_step[61, 1] += V
                                                        elif T > 1.215 and T <= 1.225:
                                                            T_step[62, 1] += V
                                                        elif T > 1.225 and T <= 1.235:
                                                            T_step[63, 1] += V
                                                        elif T > 1.235 and T <= 1.245:
                                                            T_step[64, 1] += V
                                                        elif T > 1.245 and T <= 1.255:
                                                            T_step[65, 1] += V
                                                        elif T > 1.255 and T <= 1.265:
                                                            T_step[66, 1] += V
                                                        elif T > 1.265 and T <= 1.275:
                                                            T_step[67, 1] += V
                                                        elif T > 1.275 and T <= 1.285:
                                                            T_step[68, 1] += V
                                                        elif T > 1.285 and T <= 1.295:
                                                            T_step[69, 1] += V
                                                        elif T > 1.295 and T <= 1.305:
                                                            T_step[70, 1] += V
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

        # 将6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    for key8, value8 in dict8.items():
                                        for key9, value9 in dict9.items():
                                            for key10, value10 in dict10.items():
                                                for key11, value11 in dict11.items():
                                                    for key12, value12 in dict12.items():
                                                        for key13, value13 in dict13.items():
                                                            T = key1 * key2 * key3 * key4 * key5 * key6 * key7 * key8 * key9 * key10 * key11 * key12 * key13
                                                            V = value1 * value2 * value3 * value4 * value5 * value6 * value7 * value8 * value9 * value10 * value11 * value12 * value13
                                                            if T > 0.595 and T <= 0.605:
                                                                T_step[0, 1] += V
                                                            elif T > 0.605 and T <= 0.615:
                                                                T_step[1, 1] += V
                                                            elif T > 0.615 and T <= 0.625:
                                                                T_step[2, 1] += V
                                                            elif T > 0.625 and T <= 0.635:
                                                                T_step[3, 1] += V
                                                            elif T > 0.635 and T <= 0.645:
                                                                T_step[4, 1] += V
                                                            elif T > 0.645 and T <= 0.655:
                                                                T_step[5, 1] += V
                                                            elif T > 0.655 and T <= 0.665:
                                                                T_step[6, 1] += V
                                                            elif T > 0.665 and T <= 0.675:
                                                                T_step[7, 1] += V
                                                            elif T > 0.675 and T <= 0.685:
                                                                T_step[8, 1] += V
                                                            elif T > 0.685 and T <= 0.695:
                                                                T_step[9, 1] += V
                                                            elif T > 0.695 and T <= 0.705:
                                                                T_step[10, 1] += V
                                                            elif T > 0.705 and T <= 0.715:
                                                                T_step[11, 1] += V
                                                            elif T > 0.715 and T <= 0.725:
                                                                T_step[12, 1] += V
                                                            elif T > 0.725 and T <= 0.735:
                                                                T_step[13, 1] += V
                                                            elif T > 0.735 and T <= 0.745:
                                                                T_step[14, 1] += V
                                                            elif T > 0.745 and T <= 0.755:
                                                                T_step[15, 1] += V
                                                            elif T > 0.755 and T <= 0.765:
                                                                T_step[16, 1] += V
                                                            elif T > 0.765 and T <= 0.775:
                                                                T_step[17, 1] += V
                                                            elif T > 0.775 and T <= 0.785:
                                                                T_step[18, 1] += V
                                                            elif T > 0.785 and T <= 0.795:
                                                                T_step[19, 1] += V
                                                            elif T > 0.795 and T <= 0.805:
                                                                T_step[20, 1] += V
                                                            elif T > 0.805 and T <= 0.815:
                                                                T_step[21, 1] += V
                                                            elif T > 0.815 and T <= 0.825:
                                                                T_step[22, 1] += V
                                                            elif T > 0.825 and T <= 0.835:
                                                                T_step[23, 1] += V
                                                            elif T > 0.835 and T <= 0.845:
                                                                T_step[24, 1] += V
                                                            elif T > 0.845 and T <= 0.855:
                                                                T_step[25, 1] += V
                                                            elif T > 0.855 and T <= 0.865:
                                                                T_step[26, 1] += V
                                                            elif T > 0.865 and T <= 0.875:
                                                                T_step[27, 1] += V
                                                            elif T > 0.875 and T <= 0.885:
                                                                T_step[28, 1] += V
                                                            elif T > 0.885 and T <= 0.895:
                                                                T_step[29, 1] += V
                                                            elif T > 0.895 and T <= 0.905:
                                                                T_step[30, 1] += V
                                                            elif T > 0.905 and T <= 0.915:
                                                                T_step[31, 1] += V
                                                            elif T > 0.915 and T <= 0.925:
                                                                T_step[32, 1] += V
                                                            elif T > 0.925 and T <= 0.935:
                                                                T_step[33, 1] += V
                                                            elif T > 0.935 and T <= 0.945:
                                                                T_step[34, 1] += V
                                                            elif T > 0.945 and T <= 0.955:
                                                                T_step[35, 1] += V
                                                            elif T > 0.955 and T <= 0.965:
                                                                T_step[36, 1] += V
                                                            elif T > 0.965 and T <= 0.975:
                                                                T_step[37, 1] += V
                                                            elif T > 0.975 and T <= 0.985:
                                                                T_step[38, 1] += V
                                                            elif T > 0.985 and T <= 0.995:
                                                                T_step[39, 1] += V
                                                            elif T > 0.995 and T <= 1.005:
                                                                T_step[40, 1] += V
                                                            elif T > 1.005 and T <= 1.015:
                                                                T_step[41, 1] += V
                                                            elif T > 1.015 and T <= 1.025:
                                                                T_step[42, 1] += V
                                                            elif T > 1.025 and T <= 1.035:
                                                                T_step[43, 1] += V
                                                            elif T > 1.035 and T <= 1.045:
                                                                T_step[44, 1] += V
                                                            elif T > 1.045 and T <= 1.055:
                                                                T_step[45, 1] += V
                                                            elif T > 1.055 and T <= 1.065:
                                                                T_step[46, 1] += V
                                                            elif T > 1.065 and T <= 1.075:
                                                                T_step[47, 1] += V
                                                            elif T > 1.075 and T <= 1.085:
                                                                T_step[48, 1] += V
                                                            elif T > 1.085 and T <= 1.095:
                                                                T_step[49, 1] += V
                                                            elif T > 1.095 and T <= 1.105:
                                                                T_step[50, 1] += V
                                                            elif T > 1.105 and T <= 1.115:
                                                                T_step[51, 1] += V
                                                            elif T > 1.115 and T <= 1.125:
                                                                T_step[52, 1] += V
                                                            elif T > 1.125 and T <= 1.135:
                                                                T_step[53, 1] += V
                                                            elif T > 1.165 and T <= 1.145:
                                                                T_step[54, 1] += V
                                                            elif T > 1.145 and T <= 1.155:
                                                                T_step[55, 1] += V
                                                            elif T > 1.155 and T <= 1.165:
                                                                T_step[56, 1] += V
                                                            elif T > 1.165 and T <= 1.175:
                                                                T_step[57, 1] += V
                                                            elif T > 1.175 and T <= 1.185:
                                                                T_step[58, 1] += V
                                                            elif T > 1.185 and T <= 1.195:
                                                                T_step[59, 1] += V
                                                            elif T > 1.195 and T <= 1.205:
                                                                T_step[60, 1] += V
                                                            elif T > 1.205 and T <= 1.215:
                                                                T_step[61, 1] += V
                                                            elif T > 1.215 and T <= 1.225:
                                                                T_step[62, 1] += V
                                                            elif T > 1.225 and T <= 1.235:
                                                                T_step[63, 1] += V
                                                            elif T > 1.235 and T <= 1.245:
                                                                T_step[64, 1] += V
                                                            elif T > 1.245 and T <= 1.255:
                                                                T_step[65, 1] += V
                                                            elif T > 1.255 and T <= 1.265:
                                                                T_step[66, 1] += V
                                                            elif T > 1.265 and T <= 1.275:
                                                                T_step[67, 1] += V
                                                            elif T > 1.275 and T <= 1.285:
                                                                T_step[68, 1] += V
                                                            elif T > 1.285 and T <= 1.295:
                                                                T_step[69, 1] += V
                                                            elif T > 1.295 and T <= 1.305:
                                                                T_step[70, 1] += V
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

        # 将6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    for key8, value8 in dict8.items():
                                        for key9, value9 in dict9.items():
                                            for key10, value10 in dict10.items():
                                                for key11, value11 in dict11.items():
                                                    for key12, value12 in dict12.items():
                                                        for key13, value13 in dict13.items():
                                                            for key14, value14 in dict14.items():
                                                                T = key1 * key2 * key3 * key4 * key5 * key6 * key7 * key8 * key9 * key10 * key11 * key12 * key13 * key14
                                                                V = value1 * value2 * value3 * value4 * value5 * value6 * value7 * value8 * value9 * value10 * value11 * value12 * value13 * value14
                                                                if T > 0.595 and T <= 0.605:
                                                                    T_step[0, 1] += V
                                                                elif T > 0.605 and T <= 0.615:
                                                                    T_step[1, 1] += V
                                                                elif T > 0.615 and T <= 0.625:
                                                                    T_step[2, 1] += V
                                                                elif T > 0.625 and T <= 0.635:
                                                                    T_step[3, 1] += V
                                                                elif T > 0.635 and T <= 0.645:
                                                                    T_step[4, 1] += V
                                                                elif T > 0.645 and T <= 0.655:
                                                                    T_step[5, 1] += V
                                                                elif T > 0.655 and T <= 0.665:
                                                                    T_step[6, 1] += V
                                                                elif T > 0.665 and T <= 0.675:
                                                                    T_step[7, 1] += V
                                                                elif T > 0.675 and T <= 0.685:
                                                                    T_step[8, 1] += V
                                                                elif T > 0.685 and T <= 0.695:
                                                                    T_step[9, 1] += V
                                                                elif T > 0.695 and T <= 0.705:
                                                                    T_step[10, 1] += V
                                                                elif T > 0.705 and T <= 0.715:
                                                                    T_step[11, 1] += V
                                                                elif T > 0.715 and T <= 0.725:
                                                                    T_step[12, 1] += V
                                                                elif T > 0.725 and T <= 0.735:
                                                                    T_step[13, 1] += V
                                                                elif T > 0.735 and T <= 0.745:
                                                                    T_step[14, 1] += V
                                                                elif T > 0.745 and T <= 0.755:
                                                                    T_step[15, 1] += V
                                                                elif T > 0.755 and T <= 0.765:
                                                                    T_step[16, 1] += V
                                                                elif T > 0.765 and T <= 0.775:
                                                                    T_step[17, 1] += V
                                                                elif T > 0.775 and T <= 0.785:
                                                                    T_step[18, 1] += V
                                                                elif T > 0.785 and T <= 0.795:
                                                                    T_step[19, 1] += V
                                                                elif T > 0.795 and T <= 0.805:
                                                                    T_step[20, 1] += V
                                                                elif T > 0.805 and T <= 0.815:
                                                                    T_step[21, 1] += V
                                                                elif T > 0.815 and T <= 0.825:
                                                                    T_step[22, 1] += V
                                                                elif T > 0.825 and T <= 0.835:
                                                                    T_step[23, 1] += V
                                                                elif T > 0.835 and T <= 0.845:
                                                                    T_step[24, 1] += V
                                                                elif T > 0.845 and T <= 0.855:
                                                                    T_step[25, 1] += V
                                                                elif T > 0.855 and T <= 0.865:
                                                                    T_step[26, 1] += V
                                                                elif T > 0.865 and T <= 0.875:
                                                                    T_step[27, 1] += V
                                                                elif T > 0.875 and T <= 0.885:
                                                                    T_step[28, 1] += V
                                                                elif T > 0.885 and T <= 0.895:
                                                                    T_step[29, 1] += V
                                                                elif T > 0.895 and T <= 0.905:
                                                                    T_step[30, 1] += V
                                                                elif T > 0.905 and T <= 0.915:
                                                                    T_step[31, 1] += V
                                                                elif T > 0.915 and T <= 0.925:
                                                                    T_step[32, 1] += V
                                                                elif T > 0.925 and T <= 0.935:
                                                                    T_step[33, 1] += V
                                                                elif T > 0.935 and T <= 0.945:
                                                                    T_step[34, 1] += V
                                                                elif T > 0.945 and T <= 0.955:
                                                                    T_step[35, 1] += V
                                                                elif T > 0.955 and T <= 0.965:
                                                                    T_step[36, 1] += V
                                                                elif T > 0.965 and T <= 0.975:
                                                                    T_step[37, 1] += V
                                                                elif T > 0.975 and T <= 0.985:
                                                                    T_step[38, 1] += V
                                                                elif T > 0.985 and T <= 0.995:
                                                                    T_step[39, 1] += V
                                                                elif T > 0.995 and T <= 1.005:
                                                                    T_step[40, 1] += V
                                                                elif T > 1.005 and T <= 1.015:
                                                                    T_step[41, 1] += V
                                                                elif T > 1.015 and T <= 1.025:
                                                                    T_step[42, 1] += V
                                                                elif T > 1.025 and T <= 1.035:
                                                                    T_step[43, 1] += V
                                                                elif T > 1.035 and T <= 1.045:
                                                                    T_step[44, 1] += V
                                                                elif T > 1.045 and T <= 1.055:
                                                                    T_step[45, 1] += V
                                                                elif T > 1.055 and T <= 1.065:
                                                                    T_step[46, 1] += V
                                                                elif T > 1.065 and T <= 1.075:
                                                                    T_step[47, 1] += V
                                                                elif T > 1.075 and T <= 1.085:
                                                                    T_step[48, 1] += V
                                                                elif T > 1.085 and T <= 1.095:
                                                                    T_step[49, 1] += V
                                                                elif T > 1.095 and T <= 1.105:
                                                                    T_step[50, 1] += V
                                                                elif T > 1.105 and T <= 1.115:
                                                                    T_step[51, 1] += V
                                                                elif T > 1.115 and T <= 1.125:
                                                                    T_step[52, 1] += V
                                                                elif T > 1.125 and T <= 1.135:
                                                                    T_step[53, 1] += V
                                                                elif T > 1.165 and T <= 1.145:
                                                                    T_step[54, 1] += V
                                                                elif T > 1.145 and T <= 1.155:
                                                                    T_step[55, 1] += V
                                                                elif T > 1.155 and T <= 1.165:
                                                                    T_step[56, 1] += V
                                                                elif T > 1.165 and T <= 1.175:
                                                                    T_step[57, 1] += V
                                                                elif T > 1.175 and T <= 1.185:
                                                                    T_step[58, 1] += V
                                                                elif T > 1.185 and T <= 1.195:
                                                                    T_step[59, 1] += V
                                                                elif T > 1.195 and T <= 1.205:
                                                                    T_step[60, 1] += V
                                                                elif T > 1.205 and T <= 1.215:
                                                                    T_step[61, 1] += V
                                                                elif T > 1.215 and T <= 1.225:
                                                                    T_step[62, 1] += V
                                                                elif T > 1.225 and T <= 1.235:
                                                                    T_step[63, 1] += V
                                                                elif T > 1.235 and T <= 1.245:
                                                                    T_step[64, 1] += V
                                                                elif T > 1.245 and T <= 1.255:
                                                                    T_step[65, 1] += V
                                                                elif T > 1.255 and T <= 1.265:
                                                                    T_step[66, 1] += V
                                                                elif T > 1.265 and T <= 1.275:
                                                                    T_step[67, 1] += V
                                                                elif T > 1.275 and T <= 1.285:
                                                                    T_step[68, 1] += V
                                                                elif T > 1.285 and T <= 1.295:
                                                                    T_step[69, 1] += V
                                                                elif T > 1.295 and T <= 1.305:
                                                                    T_step[70, 1] += V
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

        # 将6个dict的key和value进行交叉相乘，并进行判断
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                for key3, value3 in dict3.items():
                    for key4, value4 in dict4.items():
                        for key5, value5 in dict5.items():
                            for key6, value6 in dict6.items():
                                for key7, value7 in dict7.items():
                                    for key8, value8 in dict8.items():
                                        for key9, value9 in dict9.items():
                                            for key10, value10 in dict10.items():
                                                for key11, value11 in dict11.items():
                                                    for key12, value12 in dict12.items():
                                                        for key13, value13 in dict13.items():
                                                            for key14, value14 in dict14.items():
                                                                for key15, value15 in dict15.items():
                                                                    T = key1 * key2 * key3 * key4 * key5 * key6 * key7 * key8 * key9 * key10 * key11 * key12 * key13 * key14 * key15
                                                                    V = value1 * value2 * value3 * value4 * value5 * value6 * value7 * value8 * value9 * value10 * value11 * value12 * value13 * value14 * value15
                                                                    if T > 0.595 and T <= 0.605:
                                                                        T_step[0, 1] += V
                                                                    elif T > 0.605 and T <= 0.615:
                                                                        T_step[1, 1] += V
                                                                    elif T > 0.615 and T <= 0.625:
                                                                        T_step[2, 1] += V
                                                                    elif T > 0.625 and T <= 0.635:
                                                                        T_step[3, 1] += V
                                                                    elif T > 0.635 and T <= 0.645:
                                                                        T_step[4, 1] += V
                                                                    elif T > 0.645 and T <= 0.655:
                                                                        T_step[5, 1] += V
                                                                    elif T > 0.655 and T <= 0.665:
                                                                        T_step[6, 1] += V
                                                                    elif T > 0.665 and T <= 0.675:
                                                                        T_step[7, 1] += V
                                                                    elif T > 0.675 and T <= 0.685:
                                                                        T_step[8, 1] += V
                                                                    elif T > 0.685 and T <= 0.695:
                                                                        T_step[9, 1] += V
                                                                    elif T > 0.695 and T <= 0.705:
                                                                        T_step[10, 1] += V
                                                                    elif T > 0.705 and T <= 0.715:
                                                                        T_step[11, 1] += V
                                                                    elif T > 0.715 and T <= 0.725:
                                                                        T_step[12, 1] += V
                                                                    elif T > 0.725 and T <= 0.735:
                                                                        T_step[13, 1] += V
                                                                    elif T > 0.735 and T <= 0.745:
                                                                        T_step[14, 1] += V
                                                                    elif T > 0.745 and T <= 0.755:
                                                                        T_step[15, 1] += V
                                                                    elif T > 0.755 and T <= 0.765:
                                                                        T_step[16, 1] += V
                                                                    elif T > 0.765 and T <= 0.775:
                                                                        T_step[17, 1] += V
                                                                    elif T > 0.775 and T <= 0.785:
                                                                        T_step[18, 1] += V
                                                                    elif T > 0.785 and T <= 0.795:
                                                                        T_step[19, 1] += V
                                                                    elif T > 0.795 and T <= 0.805:
                                                                        T_step[20, 1] += V
                                                                    elif T > 0.805 and T <= 0.815:
                                                                        T_step[21, 1] += V
                                                                    elif T > 0.815 and T <= 0.825:
                                                                        T_step[22, 1] += V
                                                                    elif T > 0.825 and T <= 0.835:
                                                                        T_step[23, 1] += V
                                                                    elif T > 0.835 and T <= 0.845:
                                                                        T_step[24, 1] += V
                                                                    elif T > 0.845 and T <= 0.855:
                                                                        T_step[25, 1] += V
                                                                    elif T > 0.855 and T <= 0.865:
                                                                        T_step[26, 1] += V
                                                                    elif T > 0.865 and T <= 0.875:
                                                                        T_step[27, 1] += V
                                                                    elif T > 0.875 and T <= 0.885:
                                                                        T_step[28, 1] += V
                                                                    elif T > 0.885 and T <= 0.895:
                                                                        T_step[29, 1] += V
                                                                    elif T > 0.895 and T <= 0.905:
                                                                        T_step[30, 1] += V
                                                                    elif T > 0.905 and T <= 0.915:
                                                                        T_step[31, 1] += V
                                                                    elif T > 0.915 and T <= 0.925:
                                                                        T_step[32, 1] += V
                                                                    elif T > 0.925 and T <= 0.935:
                                                                        T_step[33, 1] += V
                                                                    elif T > 0.935 and T <= 0.945:
                                                                        T_step[34, 1] += V
                                                                    elif T > 0.945 and T <= 0.955:
                                                                        T_step[35, 1] += V
                                                                    elif T > 0.955 and T <= 0.965:
                                                                        T_step[36, 1] += V
                                                                    elif T > 0.965 and T <= 0.975:
                                                                        T_step[37, 1] += V
                                                                    elif T > 0.975 and T <= 0.985:
                                                                        T_step[38, 1] += V
                                                                    elif T > 0.985 and T <= 0.995:
                                                                        T_step[39, 1] += V
                                                                    elif T > 0.995 and T <= 1.005:
                                                                        T_step[40, 1] += V
                                                                    elif T > 1.005 and T <= 1.015:
                                                                        T_step[41, 1] += V
                                                                    elif T > 1.015 and T <= 1.025:
                                                                        T_step[42, 1] += V
                                                                    elif T > 1.025 and T <= 1.035:
                                                                        T_step[43, 1] += V
                                                                    elif T > 1.035 and T <= 1.045:
                                                                        T_step[44, 1] += V
                                                                    elif T > 1.045 and T <= 1.055:
                                                                        T_step[45, 1] += V
                                                                    elif T > 1.055 and T <= 1.065:
                                                                        T_step[46, 1] += V
                                                                    elif T > 1.065 and T <= 1.075:
                                                                        T_step[47, 1] += V
                                                                    elif T > 1.075 and T <= 1.085:
                                                                        T_step[48, 1] += V
                                                                    elif T > 1.085 and T <= 1.095:
                                                                        T_step[49, 1] += V
                                                                    elif T > 1.095 and T <= 1.105:
                                                                        T_step[50, 1] += V
                                                                    elif T > 1.105 and T <= 1.115:
                                                                        T_step[51, 1] += V
                                                                    elif T > 1.115 and T <= 1.125:
                                                                        T_step[52, 1] += V
                                                                    elif T > 1.125 and T <= 1.135:
                                                                        T_step[53, 1] += V
                                                                    elif T > 1.165 and T <= 1.145:
                                                                        T_step[54, 1] += V
                                                                    elif T > 1.145 and T <= 1.155:
                                                                        T_step[55, 1] += V
                                                                    elif T > 1.155 and T <= 1.165:
                                                                        T_step[56, 1] += V
                                                                    elif T > 1.165 and T <= 1.175:
                                                                        T_step[57, 1] += V
                                                                    elif T > 1.175 and T <= 1.185:
                                                                        T_step[58, 1] += V
                                                                    elif T > 1.185 and T <= 1.195:
                                                                        T_step[59, 1] += V
                                                                    elif T > 1.195 and T <= 1.205:
                                                                        T_step[60, 1] += V
                                                                    elif T > 1.205 and T <= 1.215:
                                                                        T_step[61, 1] += V
                                                                    elif T > 1.215 and T <= 1.225:
                                                                        T_step[62, 1] += V
                                                                    elif T > 1.225 and T <= 1.235:
                                                                        T_step[63, 1] += V
                                                                    elif T > 1.235 and T <= 1.245:
                                                                        T_step[64, 1] += V
                                                                    elif T > 1.245 and T <= 1.255:
                                                                        T_step[65, 1] += V
                                                                    elif T > 1.255 and T <= 1.265:
                                                                        T_step[66, 1] += V
                                                                    elif T > 1.265 and T <= 1.275:
                                                                        T_step[67, 1] += V
                                                                    elif T > 1.275 and T <= 1.285:
                                                                        T_step[68, 1] += V
                                                                    elif T > 1.285 and T <= 1.295:
                                                                        T_step[69, 1] += V
                                                                    elif T > 1.295 and T <= 1.305:
                                                                        T_step[70, 1] += V





try:
    if st.button('***点击计算***'):
        # 将使用者保存到txt文件中
        fp_save = 'users/网站使用者.txt'
        mode = 'a'
        with open(fp_save, mode) as f:
            f.write('使用了透过率波动1step工具' + '\n')
        # 执行main_code程序，参数为trans
        main_code(trans2, l, m, T_step)
        st.write(T_step)
        st.line_chart(T_step[:, 1])
        # print(Final)  # 打印结果
        
        # 获取代码执行后时间戳
        end_time = time.time()
        # 计算执行时间
        run_time = end_time - start_time
        st.write("代码执行时间为：{}秒".format(run_time))
except NameError:
    bz5_3, bz5_4, bz5_5 = st.columns([1, 6, 19])
    with bz5_5:
        st.write(':red[请加载TXT文件后在点击计算!]')

# 编辑button - Final计算
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(4) > div > button
    {
    background-color: rgb(220, 240, 220);
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
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(3) > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    </style>
    ''',
    unsafe_allow_html=True
)
