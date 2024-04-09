import numpy as np
import pandas as pd
import math
import streamlit as st
from PIL import Image
# st.balloons()  #过场动画

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具可以计算LCD新产品串色水平</h4>", unsafe_allow_html=True)


# # # 工具名称、版本号
st.write("# LCD新产品串色评估工具(非VR) #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V1.0</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2023/11/17</h5>", unsafe_allow_html=True)


# # # 设置步骤1
bz1_1, bz1_2 = st.columns([1, 2])
with bz1_1:
    st.write("<h6>步骤1：请选择Pixel类型</h6>", unsafe_allow_html=True)

# 设置步骤1的radio图标
bz1_3, bz1_4, bz1_5 = st.columns([1, 8, 32])
with bz1_4:
    my_pixel = st.radio('不显示label', ('RGB', 'RGBW'), label_visibility='collapsed')
    if my_pixel == 'RGB':
        case = 1
    elif my_pixel == 'RGBW':
        case = 2

# 设置步骤1的图片显示，并按照选择输出case value
with bz1_5:
    if case == 1:
        fp1 = 'pic/Color_Mix/RGB.jpg'
        image = Image.open(fp1)
        st.image(image)
        # 设置Pixel尺寸输入区
        bm1, bm2, bm3, bm4, bm5, bm6, bm7 = st.columns([2, 1, 2, 1, 2, 1, 2])
        with bm1:
            BM0 = st.number_input(label='**a**', format='%f')
        with bm3:
            BM3 = st.number_input(label='**b**', format='%f')
        with bm5:
            BM5 = st.number_input(label='**c**', format='%f')
        with bm7:
            BM8 = st.number_input(label='**d**', format='%f')

        aa1, aa2, aa3, aa4, aa5, aa6, aa7 = st.columns([1, 2, 1, 2, 1, 2, 1])
        with aa2:
            AR2 = st.number_input(label='**A**', format='%f')
        with aa4:
            AR6 = st.number_input(label='**B**', format='%f')
        with aa6:
            AR10 = st.number_input(label='**C**', format='%f')

        sd1, sd2, sd3, sd4, sd5, sd6, sd7 = st.columns([2, 1, 2, 1, 2, 1, 2])
        with sd1:
            SD0 = st.number_input(label='**I**', format='%f')
        with sd3:
            SD3 = st.number_input(label='**II**', format='%f')
        with sd5:
            SD5 = st.number_input(label='**III**', format='%f')
        with sd7:
            SD8 = st.number_input(label='**IV**', format='%f')

    elif case == 2:
        fp2 = 'pic/Color_Mix/RGBW.jpg'
        image = Image.open(fp2)
        st.image(image)
        # 设置Pixel尺寸输入区
        bm1, bm2, bm3, bm4, bm5, bm6, bm7, bm8, bm9 = st.columns([8, 1, 8, 1, 8, 1, 8, 1, 8])
        with bm1:
            BM0 = st.number_input(label='**a**', format='%f')
        with bm3:
            BM2 = st.number_input(label='**b**', format='%f')
        with bm5:
            BM4 = st.number_input(label='**c**', format='%f')
        with bm7:
            BM6 = st.number_input(label='**d**', format='%f')
        with bm9:
            BM8 = st.number_input(label='**e**', format='%f')

        aa1, aa2, aa3, aa4, aa5, aa6, aa7, aa8, aa9 = st.columns([2, 4, 1, 4, 1, 4, 1, 4, 2])
        with aa2:
            AR1 = st.number_input(label='**A**', format='%f')
        with aa4:
            AR4 = st.number_input(label='**B**', format='%f')
        with aa6:
            AR8 = st.number_input(label='**C**', format='%f')
        with aa8:
            AR11 = st.number_input(label='**D**', format='%f')

        sd1, sd2, sd3, sd4, sd5, sd6, sd7, sd8, sd9 = st.columns([8, 1, 8, 1, 8, 1, 8, 1, 8])
        with sd1:
            SD0 = st.number_input(label='**I**', format='%f')
        with sd3:
            SD2 = st.number_input(label='**II**', format='%f')
        with sd5:
            SD4 = st.number_input(label='**III**', format='%f')
        with sd7:
            SD6 = st.number_input(label='**IV**', format='%f')
        with sd9:
            SD8 = st.number_input(label='**V**', format='%f')


# # # 设置步骤2
bz2_1, bz2_2 = st.columns([1, 2])
with bz2_1:
    st.write("<h6>步骤2：请设置仿真参数</h6>", unsafe_allow_html=True)

# 设置步骤2下面的填入框
bz2_3, bz2_4, bz2_5, bz2_6 = st.columns([4, 6, 1, 4])
with bz2_4:
    st.write('***请填写膜层参数***', unsafe_allow_html=True)
with bz2_6:
    st.write('***请填写模拟参数***', unsafe_allow_html=True)

bz2_11, bz2_12, bz2_13, bz2_14, bz2_15, bz2_16, bz2_17, bz2_18 = st.columns([1, 2, 3, 3, 3, 2, 3, 1])
with bz2_12:
    st.write(' ')
    st.write(' ')
    st.write('BM')
with bz2_13:
    BM_THK = st.number_input(label='膜厚', value=1.2, format='%f', key=1)
with bz2_14:
    BM_N = st.text_input(label='折射率', value='N/A', disabled=True, key=2)
with bz2_16:
    st.write(' ')
    st.write(' ')
    st.write('Cell Gap')
with bz2_17:
    Cell_Gap = st.number_input(label=' ', format='%f', key=4)

with bz2_12:
    st.write(' ')
    st.write('RGB')
with bz2_13:
    RGB_THK = st.number_input(label='膜厚', label_visibility='collapsed', format='%f', key=5)
with bz2_14:
    RGB_N = st.number_input(label='折射率', value=1.6, label_visibility='collapsed', format='%f', key=6)
with bz2_16:
    st.write(' ')
    st.write('Assy')
with bz2_17:
    Assy = st.number_input(label='没有label', label_visibility='collapsed', format='%f', key=8)

with bz2_12:
    st.write(' ')
    st.write('OC')
with bz2_13:
    OC_THK = st.number_input(label='膜厚', value=1.5, label_visibility='collapsed', format='%f', key=9)
with bz2_14:
    OC_N = st.number_input(label='折射率', value=1.55, label_visibility='collapsed', format='%f', key=10)
with bz2_16:
    st.write(' ')
    st.write('观察角度')
with bz2_17:
    Air_Angle = st.number_input(label='没有label', label_visibility='collapsed', format='%f', key=12)

with bz2_12:
    st.write(' ')
    st.write('LC')
with bz2_13:
    LC_THK = st.text_input(label='膜厚', value='折射率填No→', disabled=True, label_visibility='collapsed', key=13)
with bz2_14:
    LC_N = st.number_input(label='折射率', label_visibility='collapsed', format='%f', key=14)

with bz2_12:
    st.write(' ')
    st.write('PLN')
with bz2_13:
    PLN_THK = st.number_input(label='膜厚', value=2.3, label_visibility='collapsed', format='%f', key=28)
with bz2_14:
    PLN_N = st.number_input(label='折射率', value=1.524, label_visibility='collapsed', format='%f', key=29)

with bz2_12:
    st.write(' ')
    st.write('SD')
with bz2_13:
    SD_THK = st.number_input(label='膜厚', value=0.48, label_visibility='collapsed', format='%f', key=31)
with bz2_14:
    SD_N = st.text_input(label='折射率', value='N/A', disabled=True, label_visibility='collapsed', key=32)

# # # 设置步骤3
st.write("<h6>步骤3：请加载TechWiz仿真结果TXT文件</h6>", unsafe_allow_html=True)

# 设置上传方式
bz3_3, bz3_4 = st.columns([1, 25])
with bz3_4:
    fp_techwiz = st.file_uploader("请上传techwiz仿真结果TXT文件", type=['txt'], help="请选择TXT文件进行上传")
    if fp_techwiz is not None:
        st10 = pd.read_csv(fp_techwiz, header=None, sep="\t", skip_blank_lines=True)
        st1 = np.float64(st10)


# # # 设置步骤4
st.write("<h6>步骤4：请加载BLU光谱和RGB光谱TXT文件</h6>", unsafe_allow_html=True)

# 设置光谱上传按钮，并将数据读取到BLU和RGB变量中
# 初始化结束
bz4_3, bz4_4 = st.columns([1, 25])
with bz4_4:
    fp_BLU = st.file_uploader("请上传BLU光谱txt文件(请确保数据为380~780nm，step 1nm，无需行标和波长数据列)", type=['txt'], help="请选择TXT文件进行上传", key=101)
if fp_BLU is not None:
    BLU0 = pd.read_csv(fp_BLU, header=None, sep="\t", skip_blank_lines=True)
    BLU = np.float64(BLU0)

with bz4_4:
    fp_RGB = st.file_uploader("请上传RGB光谱txt文件(请确保数据为380~780nm，step 1nm，无需行标和波长数据列)", type=['txt'], help="请选择TXT文件进行上传", key=102)
if fp_RGB is not None:
    RGB0 = pd.read_csv(fp_RGB, header=None, sep="\t", skip_blank_lines=True)
    RGB = np.float64(RGB0)

fp_CMF = 'source/CMF.txt'
CMF0 = pd.read_csv(fp_CMF, header=None, sep="\t", skip_blank_lines=True)
CMF = np.float64(CMF0)
OC_Spec0 = np.ones((401, 1)) * 0.98  # 认为OC的透过率为98%
OC_Spec = np.float64(OC_Spec0)

# # # 设置步骤5，main code
try:
    bz5_1, bz5_2 = st.columns([1, 2])
    with bz5_1:
        st.write("<h6>步骤5：请点击计算结果</h6>", unsafe_allow_html=True)

    # 设置点击按钮，并进入Main code
    bz5_3, bz5_4, bz5_5 = st.columns([1, 6, 19])
    with bz5_4:
        final_click = st.button('***点击获取结果***', key=99)
    if final_click is True:
        # 将使用者保存到txt文件中
        fp_save = 'sers/网站使用者.txt'
        mode = 'a'
        with open(fp_save, mode) as f:
            f.write('使用了LCD串色仿真工具非VR版' + '\n')
            
        # print(RX)
        # 计算BLU在三刺激值Y-bar的积分亮度sum_BLU
        BLU_Y = np.zeros((401, 1))
        for i in range(401):
            BLU_Y[i, 0] = BLU[i, 0] * CMF[i, 1]
        sum_BLU = sum(sum(BLU_Y))
        sum1 = sum(BLU_Y)

        # 创建RGB三刺激值，并计算
        RX0 = np.zeros((401, 1))
        RY0 = np.zeros((401, 1))
        RZ0 = np.zeros((401, 1))
        GX0 = np.zeros((401, 1))
        GY0 = np.zeros((401, 1))
        GZ0 = np.zeros((401, 1))
        BX0 = np.zeros((401, 1))
        BY0 = np.zeros((401, 1))
        BZ0 = np.zeros((401, 1))
        OCX0 = np.zeros((401, 1))
        OCY0 = np.zeros((401, 1))
        OCZ0 = np.zeros((401, 1))
        for i in range(401):
            RX0[i, 0] = BLU[i, 0] * RGB[i, 0] * CMF[i, 0] / sum_BLU
            RY0[i, 0] = BLU[i, 0] * RGB[i, 0] * CMF[i, 1] / sum_BLU
            RZ0[i, 0] = BLU[i, 0] * RGB[i, 0] * CMF[i, 2] / sum_BLU
            GX0[i, 0] = BLU[i, 0] * RGB[i, 1] * CMF[i, 0] / sum_BLU
            GY0[i, 0] = BLU[i, 0] * RGB[i, 1] * CMF[i, 1] / sum_BLU
            GZ0[i, 0] = BLU[i, 0] * RGB[i, 1] * CMF[i, 2] / sum_BLU
            BX0[i, 0] = BLU[i, 0] * RGB[i, 2] * CMF[i, 0] / sum_BLU
            BY0[i, 0] = BLU[i, 0] * RGB[i, 2] * CMF[i, 1] / sum_BLU
            BZ0[i, 0] = BLU[i, 0] * RGB[i, 2] * CMF[i, 2] / sum_BLU
            OCX0[i, 0] = BLU[i, 0] * OC_Spec[i, 0] * CMF[i, 0] / sum_BLU
            OCY0[i, 0] = BLU[i, 0] * OC_Spec[i, 0] * CMF[i, 1] / sum_BLU
            OCZ0[i, 0] = BLU[i, 0] * OC_Spec[i, 0] * CMF[i, 2] / sum_BLU
        RX = sum(sum(RX0))
        RY = sum(sum(RY0))
        RZ = sum(sum(RZ0))
        GX = sum(sum(GX0))
        GY = sum(sum(GY0))
        GZ = sum(sum(GZ0))
        BX = sum(sum(BX0))
        BY = sum(sum(BY0))
        BZ = sum(sum(BZ0))
        OCX = sum(sum(OCX0))
        OCY = sum(sum(OCY0))
        OCZ = sum(sum(OCZ0))
        if case == 1:
            WX = (RX + GX + BX) / 3
            WY = (RY + GY + BY) / 3
            WZ = (RZ + GZ + BZ) / 3
        elif case == 2:
            WX = (RX + GX + BX + OCX) / 3
            WY = (RY + GY + BY + OCY) / 3
            WZ = (RZ + GZ + BZ + OCZ) / 3

        # 计算几何X位移
        RGB_X = (RGB_THK - BM_THK) * math.tan(math.asin(math.sin(Air_Angle / 180 * math.pi) / RGB_N))  # # 从BM底部算
        OC_X = OC_THK * math.tan(math.asin(math.sin(Air_Angle / 180 * math.pi) / OC_N))
        Gap_X = Cell_Gap * math.tan(math.asin(math.sin(Air_Angle / 180 * math.pi) / LC_N))
        PLN_X = PLN_THK * math.tan(math.asin(math.sin(Air_Angle / 180 * math.pi) / PLN_N))
        SD_X = SD_THK * math.tan(math.asin(math.sin(Air_Angle / 180 * math.pi) / PLN_N))  # # 单SD层shift量

        # # # 第一种情况 RGB像素
        if case == 1:
            # 加载techwiz数据
            st1 = np.float_(st1)
            rgb_h = st1.shape[0]
            A = np.zeros((rgb_h, 3))
            for i in range(rgb_h):
                A[i, 0] = i
                A[i, 1] = st1[i, 0]
                A[i, 2] = st1[i, 1]
            # # # 正视角观察时，中间像素积分坐标点(按BM轮廓积分)，此处未考虑Assy
            C_X0 = SD0 + AR2 + SD3 / 2 + BM3 / 2
            C_X1 = C_X0 + AR6 - (BM3 - SD3) / 2 + (SD5 - BM5) / 2
            # # # 左侧观察时，中间像素(B像素)亮时,G像素会混入B颜色中
            L_A = C_X0 - BM3 / 2 + SD3 / 2 + SD_X
            L_B = C_X0 - BM3 + RGB_X + OC_X + Gap_X + PLN_X + Assy
            if L_A < L_B or L_A == L_B:
                L_X0 = L_A
                L_X1 = L_B
            elif L_A > L_B:
                L_X0 = L_B
                L_X1 = L_A
            # # # 右侧观察时，中间像素(B像素)亮时，R像素会混入B颜色中
            R_A = C_X1 + BM5 - RGB_X - OC_X - Gap_X - PLN_X - Assy
            R_B = C_X1 + BM5 / 2 - SD5 / 2 - SD_X
            if R_A < R_B or R_A == R_B:
                R_X0 = R_A
                R_X1 = R_B
            elif R_A > R_B:
                R_X0 = R_B
                R_X1 = R_A
            # # # 计算出起终点在矩阵中的位置
            # 将techwiz数据st1，放到A矩阵中，A矩阵第一列为0~x的自然数分布，A矩阵2~3列为st1
            for i in range(rgb_h):
                if (A[i, 1] < C_X0 and A[i + 1, 1] > C_X0) or A[i, 1] == C_X0:
                    C0 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < C_X1 and A[i + 1, 1] > C_X1) or A[i, 1] == C_X1:
                    C1 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < L_X0 and A[i + 1, 1] > L_X0) or A[i, 1] == L_X0:
                    L0 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < L_X1 and A[i + 1, 1] > L_X1) or A[i, 1] == L_X1:
                    L1 = A[i, 0]

            for i in range(rgb_h):
                if (A[i, 1] < R_X0 and A[i + 1, 1] > R_X0) or A[i, 1] == R_X0:
                    R0 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < R_X1 and A[i + 1, 1] > R_X1) or A[i, 1] == R_X1:
                    R1 = A[i, 0]

            # # # 计算center/left/right像素，首尾行数据
            C_0 = A[int(C0), 2] + (C_X0 - A[int(C0), 1]) * (A[int(C0) + 1, 2] - A[int(C0), 2]) / (
                        A[int(C0) + 1, 1] - A[int(C0), 1])
            C_1 = A[int(C1), 2] + (C_X1 - A[int(C1), 1]) * (A[int(C1) + 1, 2] - A[int(C1), 2]) / (
                        A[int(C1) + 1, 1] - A[int(C1), 1])
            L_0 = A[int(L0), 2] + (L_X0 - A[int(L0), 1]) * (A[int(L0) + 1, 2] - A[int(L0), 2]) / (
                        A[int(L0) + 1, 1] - A[int(L0), 1])
            L_1 = A[int(L1), 2] + (L_X1 - A[int(L1), 1]) * (A[int(L1) + 1, 2] - A[int(L1), 2]) / (
                        A[int(L1) + 1, 1] - A[int(L1), 1])
            R_0 = A[int(R0), 2] + (R_X0 - A[int(R0), 1]) * (A[int(R0) + 1, 2] - A[int(R0), 2]) / (
                        A[int(R0) + 1, 1] - A[int(R0), 1])
            R_1 = A[int(R1), 2] + (R_X1 - A[int(R1), 1]) * (A[int(R1) + 1, 2] - A[int(R1), 2]) / (
                        A[int(R1) + 1, 1] - A[int(R1), 1])

            # # # 创造Center/Left/Right矩阵并将首尾行数据替换到矩阵中
            Center = np.zeros((int(C1 - C0 + 2), 3))
            for i in range(int(C1 - C0 + 2)):
                Center[i, 0] = i
                Center[i, 1] = A[int(C0) + i, 1]
                Center[i, 2] = A[int(C0) + i, 2]
                Center[0, 1] = C_X0
                Center[0, 2] = C_0
                Center[int(C1 - C0 + 1), 1] = C_X1
                Center[int(C1 - C0 + 1), 2] = C_1

            Left = np.zeros((int(L1 - L0 + 2), 3))
            for i in range(int(L1 - L0 + 2)):
                Left[i, 0] = i
                Left[i, 1] = A[int(L0) + i, 1]
                Left[i, 2] = A[int(L0) + i, 2]
                Left[0, 1] = L_X0
                Left[0, 2] = L_0
                Left[int(L1 - L0 + 1), 1] = L_X1
                Left[int(L1 - L0 + 1), 2] = L_1

            Right = np.zeros((int(R1 - R0 + 2), 3))
            for i in range(int(R1 - R0 + 2)):
                Right[i, 0] = i
                Right[i, 1] = A[int(R0) + i, 1]
                Right[i, 2] = A[int(R0) + i, 2]
                Right[0, 1] = R_X0
                Right[0, 2] = R_0
                Right[int(R1 - R0 + 1), 1] = R_X1
                Right[int(R1 - R0 + 1), 2] = R_1

            # # # 计算center/left/right像素的积分面积
            area_C = np.zeros((Center.shape[0], 1))
            area_L = np.zeros((Left.shape[0], 1))
            area_R = np.zeros((Right.shape[0], 1))
            for i in range(Center.shape[0] - 1):
                area_C[i] = ((Center[i, 2] + Center[i + 1, 2]) * (Center[i + 1, 1] - Center[i, 1])) / 2
                area_Center = sum(sum(area_C))

            for i in range(Left.shape[0] - 1):
                area_L[i] = ((Left[i, 2] + Left[i + 1, 2]) * (Left[i + 1, 1] - Left[i, 1])) / 2
                area_Left = sum(sum(area_L))

            for i in range(Right.shape[0] - 1):
                area_R[i] = ((Right[i, 2] + Right[i + 1, 2]) * (Right[i + 1, 1] - Right[i, 1])) / 2
                area_Right = sum(sum(area_R))

            # # # 计算最终JNCD结果
            # # 计算串色比例
            Ratio_RG = area_Left / area_Center  # 此处考虑了Dual source on RB之间，area_Left为非dual source位置串色比例系数
            Ratio_RB = area_Right / area_Center  # 此处考虑了Dual source on RB之间，area_Right为dual source位置串色比例系数
            Ratio_BG = area_Left / area_Center  # 此处考虑了Dual source on RB之间，area_Left为非dual source位置串色比例系数
            Ratio_BR = area_Right / area_Center  # 此处考虑了Dual source on RB之间，area_Right为dual source位置串色比例系数
            Ratio_GB = area_Left / area_Center  # 此处考虑了Dual source on RB之间，area_Left为非dual source位置串色比例系数
            Ratio_GR = area_Left / area_Center  # 此处考虑了Dual source on RB之间，area_Left为非dual source位置串色比例系数

            # # 计算JNCD
            # 正视角颜色
            Rx_C = RX / (RX + RY + RZ)
            Ry_C = RY / (RX + RY + RZ)
            Gx_C = GX / (GX + GY + GZ)
            Gy_C = GY / (GX + GY + GZ)
            Bx_C = BX / (BX + BY + BZ)
            By_C = BY / (BX + BY + BZ)

            Ru_C = 4 * Rx_C / (-2 * Rx_C + 12 * Ry_C + 3)
            Rv_C = 9 * Ry_C / (-2 * Rx_C + 12 * Ry_C + 3)
            Gu_C = 4 * Gx_C / (-2 * Gx_C + 12 * Gy_C + 3)
            Gv_C = 9 * Gy_C / (-2 * Gx_C + 12 * Gy_C + 3)
            Bu_C = 4 * Bx_C / (-2 * Bx_C + 12 * By_C + 3)
            Bv_C = 9 * By_C / (-2 * Bx_C + 12 * By_C + 3)

            # 侧视角+对位偏差后的颜色，R亮 → 混入G
            RX_RG = RX + GX * Ratio_RG
            RY_RG = RY + GY * Ratio_RG
            RZ_RG = RZ + GZ * Ratio_RG
            Rx_RG = RX_RG / (RX_RG + RY_RG + RZ_RG)
            Ry_RG = RY_RG / (RX_RG + RY_RG + RZ_RG)
            Ru_RG = 4 * Rx_RG / (-2 * Rx_RG + 12 * Ry_RG + 3)
            Rv_RG = 9 * Ry_RG / (-2 * Rx_RG + 12 * Ry_RG + 3)
            # 侧视角+对位偏差后的颜色，R亮 → 混入B
            RX_RB = RX + BX * Ratio_RB
            RY_RB = RY + BY * Ratio_RB
            RZ_RB = RZ + BZ * Ratio_RB
            Rx_RB = RX_RB / (RX_RB + RY_RB + RZ_RB)
            Ry_RB = RY_RB / (RX_RB + RY_RB + RZ_RB)
            Ru_RB = 4 * Rx_RB / (-2 * Rx_RB + 12 * Ry_RB + 3)
            Rv_RB = 9 * Ry_RB / (-2 * Rx_RB + 12 * Ry_RB + 3)
            # 侧视角+对位偏差后的颜色，B亮 → 混入G
            BX_BG = BX + GX * Ratio_BG
            BY_BG = BY + GY * Ratio_BG
            BZ_BG = BZ + GZ * Ratio_BG
            Bx_BG = BX_BG / (BX_BG + BY_BG + BZ_BG)
            By_BG = BY_BG / (BX_BG + BY_BG + BZ_BG)
            Bu_BG = 4 * Bx_BG / (-2 * Bx_BG + 12 * By_BG + 3)
            Bv_BG = 9 * By_BG / (-2 * Bx_BG + 12 * By_BG + 3)
            # 侧视角+对位偏差后的颜色，B亮 → 混入R
            BX_BR = BX + RX * Ratio_BR
            BY_BR = BY + RY * Ratio_BR
            BZ_BR = BZ + RZ * Ratio_BR
            Bx_BR = BX_BR / (BX_BR + BY_BR + BZ_BR)
            By_BR = BY_BR / (BX_BR + BY_BR + BZ_BR)
            Bu_BR = 4 * Bx_BR / (-2 * Bx_BR + 12 * By_BR + 3)
            Bv_BR = 9 * By_BR / (-2 * Bx_BR + 12 * By_BR + 3)
            # 侧视角+对位偏差后的颜色，G亮 → 混入B
            GX_GB = GX + BX * Ratio_GB
            GY_GB = GY + BY * Ratio_GB
            GZ_GB = GZ + BZ * Ratio_GB
            Gx_GB = GX_GB / (GX_GB + GY_GB + GZ_GB)
            Gy_GB = GY_GB / (GX_GB + GY_GB + GZ_GB)
            Gu_GB = 4 * Gx_GB / (-2 * Gx_GB + 12 * Gy_GB + 3)
            Gv_GB = 9 * Gy_GB / (-2 * Gx_GB + 12 * Gy_GB + 3)
            # 侧视角+对位偏差后的颜色，G亮 → 混入R
            GX_GR = GX + RX * Ratio_GR
            GY_GR = GY + RY * Ratio_GR
            GZ_GR = GZ + RZ * Ratio_GR
            Gx_GR = GX_GR / (GX_GR + GY_GR + GZ_GR)
            Gy_GR = GY_GR / (GX_GR + GY_GR + GZ_GR)
            Gu_GR = 4 * Gx_GR / (-2 * Gx_GR + 12 * Gy_GR + 3)
            Gv_GR = 9 * Gy_GR / (-2 * Gx_GR + 12 * Gy_GR + 3)

            # 侧视角与正视角色偏JNCD计算
            JNCD_RG = (((Ru_RG - Ru_C) ** 2 + (Rv_RG - Rv_C) ** 2) ** 0.5) / 0.004
            JNCD_RB = (((Ru_RB - Ru_C) ** 2 + (Rv_RB - Rv_C) ** 2) ** 0.5) / 0.004
            JNCD_BG = (((Bu_BG - Bu_C) ** 2 + (Bv_BG - Bv_C) ** 2) ** 0.5) / 0.004
            JNCD_BR = (((Bu_BR - Bu_C) ** 2 + (Bv_BR - Bv_C) ** 2) ** 0.5) / 0.004
            JNCD_GB = (((Gu_GB - Gu_C) ** 2 + (Gv_GB - Gv_C) ** 2) ** 0.5) / 0.004
            JNCD_GR = (((Gu_GR - Gu_C) ** 2 + (Gv_GR - Gv_C) ** 2) ** 0.5) / 0.004

            JNCD = np.zeros((2, 3))
            JNCD[0, 0] = round(JNCD_RG, 2)
            JNCD[1, 0] = round(JNCD_RB, 2)
            JNCD[0, 1] = round(JNCD_GB, 2)
            JNCD[1, 1] = round(JNCD_GR, 2)
            JNCD[0, 2] = round(JNCD_BR, 2)
            JNCD[1, 2] = round(JNCD_BG, 2)

            JNCD_dis = pd.DataFrame(JNCD, columns=['R画面', 'G画面', 'B画面'], index=['右侧视角', '左侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis)

        # # # 第二种情况 RGBW像素
        elif case == 2:
            st1 = np.float_(st1)
            rgb_h = st1.shape[0]
            A = np.zeros((rgb_h, 3))
            for i in range(rgb_h):
                A[i, 0] = i
                A[i, 1] = st1[i, 0]
                A[i, 2] = st1[i, 1]

            # # # 正视角观察时，中间G及W全亮像素积分坐标点(按BM轮廓积分)
            C_X0 = SD0 + AR1 + SD2 / 2 + BM2 / 2
            C_X1 = C_X0 - BM2 / 2 + SD2 / 2 + AR4 + SD4 / 2 - BM4 / 2
            C_X2 = SD0 + AR1 + SD2 + AR4 + SD4 + AR8 + SD6 / 2 + BM6 / 2
            C_X3 = C_X2 - BM6 / 2 + SD6 / 2 + AR11 + SD8 - BM8

            # # # 左侧视角观察
            # 左侧观察时，左二像素(G像素)全亮，R像素混入G颜色中
            L_A = C_X0 - BM2 / 2 + SD2 / 2 + SD_X
            L_B = C_X0 - BM2 + RGB_X + OC_X + Gap_X + PLN_X + Assy
            if L_A < L_B or L_A == L_B:
                L_X0 = L_A
                L_X1 = L_B
            elif L_A > L_B:
                L_X0 = L_B
                L_X1 = L_A
            # 左侧观察时，左四像素(W像素)全亮，B像素混入W颜色中
            L_C = C_X2 - BM6 / 2 + SD6 / 2 + SD_X
            L_D = C_X2 - BM6 + RGB_X + OC_X + Gap_X + PLN_X + Assy
            if L_C < L_D or L_C == L_D:
                L_X2 = L_C
                L_X3 = L_D
            elif L_C > L_D:
                L_X2 = L_D
                L_X3 = L_C

            # # 右侧视角观察
            # 右侧观察时，左二像素(G像素)全亮，B像素混入G颜色中
            R_A = C_X1 + BM4 - RGB_X - OC_X - Gap_X - PLN_X - Assy
            R_B = C_X1 + BM4 / 2 - SD4 / 2 - SD_X
            if R_A < R_B or R_A == R_B:
                R_X0 = R_A
                R_X1 = R_B
            elif R_A > R_B:
                R_X0 = R_B
                R_X1 = R_A
            # 右侧观察时，左四像素(W像素)全亮，R像素混入W颜色中，与左侧观察W像素全亮-->B像素混入相同
            R_X2 = L_X2
            R_X3 = L_X3

            # # 计算出起终点在矩阵中的位置
            # 将techwiz数据st1，放到A矩阵中，A矩阵第一列为0~x的自然数分布，A矩阵2~3列为st1
            for i in range(rgb_h):
                if (A[i, 1] < C_X0 and A[i + 1, 1] > C_X0) or A[i, 1] == C_X0:
                    C0 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < C_X1 and A[i + 1, 1] > C_X1) or A[i, 1] == C_X1:
                    C1 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < C_X2 and A[i + 1, 1] > C_X2) or A[i, 1] == C_X2:
                    C2 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < C_X3 and A[i + 1, 1] > C_X3) or A[i, 1] == C_X3:
                    C3 = A[i, 0]

            for i in range(rgb_h):
                if (A[i, 1] < L_X0 and A[i + 1, 1] > L_X0) or A[i, 1] == L_X0:
                    L0 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < L_X1 and A[i + 1, 1] > L_X1) or A[i, 1] == L_X1:
                    L1 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < L_X2 and A[i + 1, 1] > L_X2) or A[i, 1] == L_X2:
                    L2 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < L_X3 and A[i + 1, 1] > L_X3) or A[i, 1] == L_X3:
                    L3 = A[i, 0]

            for i in range(rgb_h):
                if (A[i, 1] < R_X0 and A[i + 1, 1] > R_X0) or A[i, 1] == R_X0:
                    R0 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < R_X1 and A[i + 1, 1] > R_X1) or A[i, 1] == R_X1:
                    R1 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < R_X2 and A[i + 1, 1] > R_X2) or A[i, 1] == R_X2:
                    R2 = A[i, 0]
            for i in range(rgb_h):
                if (A[i, 1] < R_X3 and A[i + 1, 1] > R_X3) or A[i, 1] == R_X3:
                    R3 = A[i, 0]

            # # 计算center/left/right像素，首尾行数据
            C_0 = A[int(C0), 2] + (C_X0 - A[int(C0), 1]) * (A[int(C0) + 1, 2] - A[int(C0), 2]) / (
                        A[int(C0) + 1, 1] - A[int(C0), 1])
            C_1 = A[int(C1), 2] + (C_X1 - A[int(C1), 1]) * (A[int(C1) + 1, 2] - A[int(C1), 2]) / (
                        A[int(C1) + 1, 1] - A[int(C1), 1])
            C_2 = A[int(C2), 2] + (C_X2 - A[int(C2), 1]) * (A[int(C2) + 1, 2] - A[int(C2), 2]) / (
                        A[int(C2) + 1, 1] - A[int(C2), 1])
            C_3 = A[int(C3), 2] + (C_X3 - A[int(C3), 1]) * (A[int(C3) + 1, 2] - A[int(C3), 2]) / (
                        A[int(C3) + 1, 1] - A[int(C3), 1])
            L_0 = A[int(L0), 2] + (L_X0 - A[int(L0), 1]) * (A[int(L0) + 1, 2] - A[int(L0), 2]) / (
                        A[int(L0) + 1, 1] - A[int(L0), 1])
            L_1 = A[int(L1), 2] + (L_X1 - A[int(L1), 1]) * (A[int(L1) + 1, 2] - A[int(L1), 2]) / (
                        A[int(L1) + 1, 1] - A[int(L1), 1])
            L_2 = A[int(L2), 2] + (L_X2 - A[int(L2), 1]) * (A[int(L2) + 1, 2] - A[int(L2), 2]) / (
                        A[int(L2) + 1, 1] - A[int(L2), 1])
            L_3 = A[int(L3), 2] + (L_X3 - A[int(L3), 1]) * (A[int(L3) + 1, 2] - A[int(L3), 2]) / (
                        A[int(L3) + 1, 1] - A[int(L3), 1])
            R_0 = A[int(R0), 2] + (R_X0 - A[int(R0), 1]) * (A[int(R0) + 1, 2] - A[int(R0), 2]) / (
                        A[int(R0) + 1, 1] - A[int(R0), 1])
            R_1 = A[int(R1), 2] + (R_X1 - A[int(R1), 1]) * (A[int(R1) + 1, 2] - A[int(R1), 2]) / (
                        A[int(R1) + 1, 1] - A[int(R1), 1])
            R_2 = A[int(R2), 2] + (R_X2 - A[int(R2), 1]) * (A[int(R2) + 1, 2] - A[int(R2), 2]) / (
                        A[int(R2) + 1, 1] - A[int(R2), 1])
            R_3 = A[int(R3), 2] + (R_X3 - A[int(R3), 1]) * (A[int(R3) + 1, 2] - A[int(R3), 2]) / (
                        A[int(R3) + 1, 1] - A[int(R3), 1])

            # # # 创造Center/Left/Right矩阵并将首尾行数据替换到矩阵中
            Center_G = np.zeros((int(C1 - C0 + 2), 3))  # 创造Center_G中间像素
            for i in range(int(C1 - C0 + 2)):
                Center_G[i, 0] = i
                Center_G[i, 1] = A[int(C0) + i, 1]
                Center_G[i, 2] = A[int(C0) + i, 2]
                Center_G[0, 1] = C_X0
                Center_G[0, 2] = C_0
                Center_G[int(C1 - C0 + 1), 1] = C_X1
                Center_G[int(C1 - C0 + 1), 2] = C_1
            Center_W = np.zeros((int(C3 - C2 + 2), 3))  # 创造Center_W中间像素
            for i in range(int(C3 - C2 + 2)):
                Center_W[i, 0] = i
                Center_W[i, 1] = A[int(C2) + i, 1]
                Center_W[i, 2] = A[int(C2) + i, 2]
                Center_W[0, 1] = C_X2
                Center_W[0, 2] = C_2
                Center_W[int(C3 - C2 + 1), 1] = C_X3
                Center_W[int(C3 - C2 + 1), 2] = C_3

            Left_G = np.zeros((int(L1 - L0 + 2), 3))
            for i in range(int(L1 - L0 + 2)):
                Left_G[i, 0] = i
                Left_G[i, 1] = A[int(L0) + i, 1]
                Left_G[i, 2] = A[int(L0) + i, 2]
                Left_G[0, 1] = L_X0
                Left_G[0, 2] = L_0
                Left_G[int(L1 - L0 + 1), 1] = L_X1
                Left_G[int(L1 - L0 + 1), 2] = L_1
            Left_W = np.zeros((int(L3 - L2 + 2), 3))
            for i in range(int(L3 - L2 + 2)):
                Left_W[i, 0] = i
                Left_W[i, 1] = A[int(L2) + i, 1]
                Left_W[i, 2] = A[int(L2) + i, 2]
                Left_W[0, 1] = L_X2
                Left_W[0, 2] = L_2
                Left_W[int(L3 - L2 + 1), 1] = L_X3
                Left_W[int(L3 - L2 + 1), 2] = L_3

            Right_G = np.zeros((int(R1 - R0 + 2), 3))
            for i in range(int(R1 - R0 + 2)):
                Right_G[i, 0] = i
                Right_G[i, 1] = A[int(R0) + i, 1]
                Right_G[i, 2] = A[int(R0) + i, 2]
                Right_G[0, 1] = R_X0
                Right_G[0, 2] = R_0
                Right_G[int(R1 - R0 + 1), 1] = R_X1
                Right_G[int(R1 - R0 + 1), 2] = R_1
            Right_W = np.zeros((int(R3 - R2 + 2), 3))
            for i in range(int(R3 - R2 + 2)):
                Right_W[i, 0] = i
                Right_W[i, 1] = A[int(R2) + i, 1]
                Right_W[i, 2] = A[int(R2) + i, 2]
                Right_W[0, 1] = R_X2
                Right_W[0, 2] = R_2
                Right_W[int(R3 - R2 + 1), 1] = R_X3
                Right_W[int(R3 - R2 + 1), 2] = R_3

            # # # 计算center/left/right像素的积分面积
            area_C_G = np.zeros((Center_G.shape[0], 1))
            area_L_G = np.zeros((Left_G.shape[0], 1))
            area_R_G = np.zeros((Right_G.shape[0], 1))
            area_C_W = np.zeros((Center_W.shape[0], 1))
            area_L_W = np.zeros((Left_W.shape[0], 1))
            area_R_W = np.zeros((Right_W.shape[0], 1))

            for i in range(Center_G.shape[0] - 1):
                area_C_G[i] = ((Center_G[i, 2] + Center_G[i + 1, 2]) * (Center_G[i + 1, 1] - Center_G[i, 1])) / 2
                area_Center_G = sum(sum(area_C_G))
            for i in range(Left_G.shape[0] - 1):
                area_L_G[i] = ((Left_G[i, 2] + Left_G[i + 1, 2]) * (Left_G[i + 1, 1] - Left_G[i, 1])) / 2
                area_Left_G = sum(sum(area_L_G))
            for i in range(Right_G.shape[0] - 1):
                area_R_G[i] = ((Right_G[i, 2] + Right_G[i + 1, 2]) * (Right_G[i + 1, 1] - Right_G[i, 1])) / 2
                area_Right_G = sum(sum(area_R_G))
            for i in range(Center_W.shape[0] - 1):
                area_C_W[i] = ((Center_W[i, 2] + Center_W[i + 1, 2]) * (Center_W[i + 1, 1] - Center_W[i, 1])) / 2
                area_Center_W = sum(sum(area_C_W))
            for i in range(Left_W.shape[0] - 1):
                area_L_W[i] = ((Left_W[i, 2] + Left_W[i + 1, 2]) * (Left_W[i + 1, 1] - Left_W[i, 1])) / 2
                area_Left_W = sum(sum(area_L_W))
            for i in range(Right_W.shape[0] - 1):
                area_R_W[i] = ((Right_W[i, 2] + Right_W[i + 1, 2]) * (Right_W[i + 1, 1] - Right_W[i, 1])) / 2
                area_Right_W = sum(sum(area_R_W))

            # # # 计算最终JNCD结果
            # # 计算串色比例
            Ratio_GR = area_Left_G / area_Center_G
            Ratio_GB = area_Right_G / area_Center_G
            Ratio_BG = Ratio_GB
            Ratio_RG = Ratio_GR
            Ratio_WB = area_Left_W / area_Center_W
            Ratio_WR = area_Right_W / area_Center_W
            Ratio_BW = Ratio_BG
            Ratio_RW = Ratio_RG

            # # 计算JNCD
            # 正视角颜色
            Rx_C = RX / (RX + RY + RZ)
            Ry_C = RY / (RX + RY + RZ)
            Gx_C = GX / (GX + GY + GZ)
            Gy_C = GY / (GX + GY + GZ)
            Bx_C = BX / (BX + BY + BZ)
            By_C = BY / (BX + BY + BZ)
            Wx_C = WX / (WX + WY + WZ)
            Wy_C = WY / (WX + WY + WZ)

            Ru_C = 4 * Rx_C / (-2 * Rx_C + 12 * Ry_C + 3)
            Rv_C = 9 * Ry_C / (-2 * Rx_C + 12 * Ry_C + 3)
            Gu_C = 4 * Gx_C / (-2 * Gx_C + 12 * Gy_C + 3)
            Gv_C = 9 * Gy_C / (-2 * Gx_C + 12 * Gy_C + 3)
            Bu_C = 4 * Bx_C / (-2 * Bx_C + 12 * By_C + 3)
            Bv_C = 9 * By_C / (-2 * Bx_C + 12 * By_C + 3)
            Wu_C = 4 * Wx_C / (-2 * Wx_C + 12 * Wy_C + 3)
            Wv_C = 9 * Wy_C / (-2 * Wx_C + 12 * Wy_C + 3)

            # 侧视角+对位偏差后的颜色，R亮 → 混入G
            RX_RG = RX + GX * Ratio_RG
            RY_RG = RY + GY * Ratio_RG
            RZ_RG = RZ + GZ * Ratio_RG
            Rx_RG = RX_RG / (RX_RG + RY_RG + RZ_RG)
            Ry_RG = RY_RG / (RX_RG + RY_RG + RZ_RG)
            Ru_RG = 4 * Rx_RG / (-2 * Rx_RG + 12 * Ry_RG + 3)
            Rv_RG = 9 * Ry_RG / (-2 * Rx_RG + 12 * Ry_RG + 3)
            # 侧视角+对位偏差后的颜色，R亮 → 混入W
            RX_RW = RX + WX * Ratio_RW
            RY_RW = RY + WY * Ratio_RW
            RZ_RW = RZ + WZ * Ratio_RW
            Rx_RW = RX_RW / (RX_RW + RY_RW + RZ_RW)
            Ry_RW = RY_RW / (RX_RW + RY_RW + RZ_RW)
            Ru_RW = 4 * Rx_RW / (-2 * Rx_RW + 12 * Ry_RW + 3)
            Rv_RW = 9 * Ry_RW / (-2 * Rx_RW + 12 * Ry_RW + 3)
            # 侧视角+对位偏差后的颜色，B亮 → 混入G
            BX_BG = BX + GX * Ratio_BG
            BY_BG = BY + GY * Ratio_BG
            BZ_BG = BZ + GZ * Ratio_BG
            Bx_BG = BX_BG / (BX_BG + BY_BG + BZ_BG)
            By_BG = BY_BG / (BX_BG + BY_BG + BZ_BG)
            Bu_BG = 4 * Bx_BG / (-2 * Bx_BG + 12 * By_BG + 3)
            Bv_BG = 9 * By_BG / (-2 * Bx_BG + 12 * By_BG + 3)
            # 侧视角+对位偏差后的颜色，B亮 → 混入W
            BX_BW = BX + WX * Ratio_BW
            BY_BW = BY + WY * Ratio_BW
            BZ_BW = BZ + WZ * Ratio_BW
            Bx_BW = BX_BW / (BX_BW + BY_BW + BZ_BW)
            By_BW = BY_BW / (BX_BW + BY_BW + BZ_BW)
            Bu_BW = 4 * Bx_BW / (-2 * Bx_BW + 12 * By_BW + 3)
            Bv_BW = 9 * By_BW / (-2 * Bx_BW + 12 * By_BW + 3)
            # 侧视角+对位偏差后的颜色，G亮 → 混入B
            GX_GB = GX + BX * Ratio_GB
            GY_GB = GY + BY * Ratio_GB
            GZ_GB = GZ + BZ * Ratio_GB
            Gx_GB = GX_GB / (GX_GB + GY_GB + GZ_GB)
            Gy_GB = GY_GB / (GX_GB + GY_GB + GZ_GB)
            Gu_GB = 4 * Gx_GB / (-2 * Gx_GB + 12 * Gy_GB + 3)
            Gv_GB = 9 * Gy_GB / (-2 * Gx_GB + 12 * Gy_GB + 3)
            # 侧视角+对位偏差后的颜色，G亮 → 混入R
            GX_GR = GX + RX * Ratio_GR
            GY_GR = GY + RY * Ratio_GR
            GZ_GR = GZ + RZ * Ratio_GR
            Gx_GR = GX_GR / (GX_GR + GY_GR + GZ_GR)
            Gy_GR = GY_GR / (GX_GR + GY_GR + GZ_GR)
            Gu_GR = 4 * Gx_GR / (-2 * Gx_GR + 12 * Gy_GR + 3)
            Gv_GR = 9 * Gy_GR / (-2 * Gx_GR + 12 * Gy_GR + 3)
            # 侧视角+对位偏差后的颜色，W亮 → 混入B
            WX_WB = WX + BX * Ratio_WB
            WY_WB = WY + BY * Ratio_WB
            WZ_WB = WZ + BZ * Ratio_WB
            Wx_WB = WX_WB / (WX_WB + WY_WB + WZ_WB)
            Wy_WB = WY_WB / (WX_WB + WY_WB + WZ_WB)
            Wu_WB = 4 * Wx_WB / (-2 * Wx_WB + 12 * Wy_WB + 3)
            Wv_WB = 9 * Wy_WB / (-2 * Wx_WB + 12 * Wy_WB + 3)
            # 侧视角+对位偏差后的颜色，W亮 → 混入R
            WX_WR = WX + RX * Ratio_WR
            WY_WR = WY + RY * Ratio_WR
            WZ_WR = WZ + RZ * Ratio_WR
            Wx_WR = WX_WR / (WX_WR + WY_WR + WZ_WR)
            Wy_WR = WY_WR / (WX_WR + WY_WR + WZ_WR)
            Wu_WR = 4 * Wx_WR / (-2 * Wx_WR + 12 * Wy_WR + 3)
            Wv_WR = 9 * Wy_WR / (-2 * Wx_WR + 12 * Wy_WR + 3)

            # 侧视角与正视角色偏JNCD计算
            JNCD_RG = (((Ru_RG - Ru_C) ** 2 + (Rv_RG - Rv_C) ** 2) ** 0.5) / 0.004
            JNCD_RW = (((Ru_RW - Ru_C) ** 2 + (Rv_RW - Rv_C) ** 2) ** 0.5) / 0.004
            JNCD_BG = (((Bu_BG - Bu_C) ** 2 + (Bv_BG - Bv_C) ** 2) ** 0.5) / 0.004
            JNCD_BW = (((Bu_BW - Bu_C) ** 2 + (Bv_BW - Bv_C) ** 2) ** 0.5) / 0.004
            JNCD_GB = (((Gu_GB - Gu_C) ** 2 + (Gv_GB - Gv_C) ** 2) ** 0.5) / 0.004
            JNCD_GR = (((Gu_GR - Gu_C) ** 2 + (Gv_GR - Gv_C) ** 2) ** 0.5) / 0.004
            JNCD_WB = (((Wu_WB - Wu_C) ** 2 + (Wv_WB - Wv_C) ** 2) ** 0.5) / 0.004
            JNCD_WR = (((Wu_WR - Wu_C) ** 2 + (Wv_WR - Wv_C) ** 2) ** 0.5) / 0.004

            JNCD = np.zeros((2, 4))
            JNCD[0, 0] = round(JNCD_RG, 2)
            JNCD[1, 0] = round(JNCD_RW, 2)
            JNCD[0, 1] = round(JNCD_GB, 2)
            JNCD[1, 1] = round(JNCD_GR, 2)
            JNCD[0, 2] = round(JNCD_BW, 2)
            JNCD[1, 2] = round(JNCD_BG, 2)
            JNCD[0, 3] = round(JNCD_WR, 2)
            JNCD[1, 3] = round(JNCD_WB, 2)

            JNCD_dis = pd.DataFrame(JNCD, columns=['R画面', 'G画面', 'B画面', 'W画面'], index=['右侧视角', '左侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis)

        

except AttributeError:
    with bz5_5:
        st.write(' ')
        st.write(' ')
        st.write(':red[请确认所有项目已填写完成1!]')
except ValueError:
    with bz5_5:
        st.write(' ')
        st.write(' ')
        st.write(':red[请确认所有项目已填写完成2!]')
except NameError:
    with bz5_5:
        st.write(' ')
        st.write(' ')
        st.write(':red[请确认加载的BLU和RGB光谱!]')
except ZeroDivisionError:
    with bz5_5:
        st.write(' ')
        st.write(' ')
        st.write(':red[请检查<步骤2：仿真参数>是否正确!]')

# 编辑button - Final计算
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-gh2jqd.ea3mdgi5 > div > div > div > div:nth-child(13) > div.st-emotion-cache-vft1hk.e1f1d6gn3 > div > div > div > div > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px !important;
    width: 150px !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑techwiz数据加载button
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-gh2jqd.ea3mdgi5 > div > div > div > div:nth-child(9) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑BLU数据加载button
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-gh2jqd.ea3mdgi5 > div > div > div > div:nth-child(11) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div:nth-child(1) > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑CF数据加载button
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-gh2jqd.ea3mdgi5 > div > div > div > div:nth-child(11) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 通过markdown设置textarea区域的字体和input字体
st.markdown(
    """
    <style>
    textarea {
        font-size: 0.9rem !important;
    }
    input {
        font-size: 0.9rem !important; /*设置字体大小，加上!important是避免被 Markdown 样式覆盖*/
        color: rgb(0, 0, 0) !important; /*设置字体颜色*/
        background-color: rgb(220, 240, 220) !important; /*设置背景颜色*/
        /background-color: rgb(220, 240, 220, 50%) !important; /*设置背景颜色*/
        justify-content: center !important;
        text-align: center !important; /*设置字体水平居中*/
        vertical-align: middle !important; /*设置字体垂直居中*/
        height: 39px !important;/ /*设置input的高度*/
    }
    label {
        color: rgb(0, 0, 0) !important; /*设置字体颜色*/
        background-color: rgb(255, 255, 255) !important; /*设置背景颜色*/
        text-align: center !important; /*设置字体水平居中*/
        vertical-align: middle !important; /*设置字体垂直居中*/
        justify-content: center !important; /*设置label居中*/
        /outline: 5px solid rgb(15,15,15) !important;/ /*大小不变，设置边框*/
        /border: 5px solid rgb(15,15,15) !important;/ /*外形变大，增加边框并设置*/
        /*letter-spacing: 30px !important;*/ /*设置字体间距*/
        /*text-transform: uppercase !important;*/ /*强制大写*/
        /align-items: center !important;
        /height: 1vh !important;/ /*调节label垂直间距*/
    }
    </style>
    """,
    unsafe_allow_html=True,
)
