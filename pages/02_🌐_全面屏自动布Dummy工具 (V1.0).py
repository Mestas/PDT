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
st.sidebar.write("<h4 style='color: blue;'>本工具为全面屏自动布Dummy(全屏版)</h4>", unsafe_allow_html=True)

# # # 工具名称、版本号
st.write("# 全面屏自动布Dummy(全屏版) #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V1.0</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2024/08/29</h5>", unsafe_allow_html=True)

# # # 设置步骤1
st.write("<h6>步骤1：请加载PS及Dummy灰阶过渡txt文件</h6>", unsafe_allow_html=True)
col11, col12 = st.columns([1, 25])
with col12:
    fp_PS = st.file_uploader("请上传PS周期TXT文件", type=['txt'], help="请选择TXT文件进行上传", key='PS')
if fp_PS is not None:
    PS0 = pd.read_csv(fp_PS, header=None, sep="\t", skip_blank_lines=True)
    PS = np.int16(PS0)
with col12:
    fp_AA = st.file_uploader("请上传AA区灰阶过渡TXT文件", type=['txt'], help="请选择TXT文件进行上传", key='AA')
if fp_AA is not None:
    AA0 = pd.read_csv(fp_AA, header=None, sep="\t", skip_blank_lines=True)
    AA = np.int16(AA0)
with col12:
    fp_Dummy1 = st.file_uploader("请上传DUmmy1区灰阶过渡TXT文件", type=['txt'], help="请选择TXT文件进行上传", key='Dummy1')
if fp_Dummy1 is not None:
    Dummy10 = pd.read_csv(fp_Dummy1, header=None, sep="\t", skip_blank_lines=True)
    Dummy1 = np.int16(Dummy10)
with col12:
    fp_Dummy2 = st.file_uploader("请上传Dummy2区灰阶过渡TXT文件", type=['txt'], help="请选择TXT文件进行上传", key='Dummy2')
if fp_Dummy2 is not None:
    Dummy20 = pd.read_csv(fp_Dummy2, header=None, sep="\t", skip_blank_lines=True)
    Dummy2 = np.int16(Dummy20)

# # # 设置步骤2
st.write("<h6>步骤2：请输入全面屏特性参数</h6>", unsafe_allow_html=True)
# col21, col22, col23 = st.columns([1, 6, 13])
col21, col22, col23, col24, col25, col26, col27 = st.columns([1, 6, 1, 4, 1, 6, 1])
with col22:
    my_case = st.radio('全面屏特性', ('AA边界有中间直线区', 'AA边界无规则'))
    if my_case == 'AA边界有中间直线区':
        case = 1
        with col24:
            my_hole = st.radio('有无圆孔设计？', ('无圆孔', '有圆孔'))
            if my_hole == '无圆孔':
                hole = 0
                with col26:
                    TTT = st.number_input(label='AA到圆孔顶部的pixel数量', value=hole, disabled=True)
            else:
                hole = 1
                with col26:
                    TTT = st.number_input(label='AA到圆孔顶部的pixel数量', value=hole)
    else:
        case = 2

# # # 设置步骤3
st.write("<h6>步骤3：请输入CF Dummy设计情况</h6>", unsafe_allow_html=True)
col31, col32, col33, col34, col35, col36, col37 = st.columns([1, 2, 1, 4, 1, 4, 10])
with col32:
    st.write(' ')
    st.write(' ')
    st.write(' ')
with col32:
    st.write('DO')
    st.write(' ')
with col32:
    st.write('DP')
    st.write(' ')
with col32:
    st.write('GOA-L')
    st.write(' ')
with col32:
    st.write('GOA-R')

with col34:
    st.write('Dummy1区')
    Top1 = st.number_input(label='Dummy1区, DO侧Dummy pixel数量', value=0, label_visibility='collapsed')
    Bot1 = st.number_input(label='Dummy1区, DP侧Dummy pixel数量', value=0, label_visibility='collapsed')
    L1 = st.number_input(label='Dummy1区, GOA-L侧Dummy pixel数量', value=0, label_visibility='collapsed')
    R1 = st.number_input(label='Dummy1区, GOA-R侧Dummy pixel数量', value=0, label_visibility='collapsed')
with col36:
    st.write('Dummy2区')
    Top2 = st.number_input(label='Dummy2区, DO侧Dummy pixel数量', value=0, label_visibility='collapsed')
    Bot2 = st.number_input(label='Dummy2区, DP侧Dummy pixel数量', value=0, label_visibility='collapsed')
    L2 = st.number_input(label='Dummy2区, GOA-L侧Dummy pixel数量', value=0, label_visibility='collapsed')
    R2 = st.number_input(label='Dummy2区, GOA-R侧Dummy pixel数量', value=0, label_visibility='collapsed')

# # 设置步骤4
st.write("<h6>步骤4：设置异形区边缘允许放置PS的pixel灰阶数</h6>", unsafe_allow_html=True)
col41, col42, col43 = st.columns([1, 4, 20])
with col42:
    Gray = st.number_input(label='默认为211灰阶', value=211)

# # 设置步骤5
st.write("<h6>步骤5：点击生成按钮，生成全屏Dummy Pattern CSV文件</h6>", unsafe_allow_html=True)
# 设置点击按钮，并进入Main code
col51, col52, col53 = st.columns([1, 6, 19])
with col52:
    Generate = st.button('***点击获取CSV***')
if Generate is True:
    try:
        if case == 1:
            ps_sub_h = PS.shape[0]
            ps_sub_l = PS.shape[1]
            aa_h = AA.shape[0]
            aa_l = AA.shape[1]
            d1_h = Dummy1.shape[0]
            d1_l = Dummy1.shape[1]
            d2_h = Dummy2.shape[0]
            d2_l = Dummy2.shape[1]
            aa_sub_h = aa_h
            aa_sub_l = aa_l * 3
            d1_sub_h = d1_h
            d1_sub_l = d1_l * 3
            d2_sub_h = d2_h
            d2_sub_l = d2_l * 3
            ps_aa_h = aa_sub_h
            ps_aa_l = aa_sub_l

            # # # # #以下部分为设置用于判断边界位置PS放置哪种的判断矩阵DummyAA_Sub,Dummy11_Sub,Dummy2_Sub# # # # #
            AA_Sub = [] # 将CAD导出的AA做成Sub pixel（列数*3），用来判断Main PS去掉的区域
            DummyAA_Sub = np.zeros((d2_sub_h, d2_sub_l))  # 将AA按照Dummy2大小放置
            Dummy1_Sub = [] # 将CAD导出的Dummy1做成Sub pixel（列数*3）
            Dummy11_Sub = np.zeros((d2_sub_h, d2_sub_l)) # 将Dummy1按照Dummy2大小放置
            Dummy2_Sub = [] # 将CAD导出的Dummy2做成Sub pixel（列数*3）
            for i in range(aa_sub_h):
                 AA_Sub.append([-1 for x in range(aa_sub_l)])  # 在当前的C中新增一行元素，C[i][j]就可以做引用了
                 for j in range(aa_sub_l):
                    AA_Sub[i][j] = AA[i][divmod(j, 3)[0]] # 将AA区的Pixel数据变成Sub pixel

            for i in range(d1_sub_h):
                Dummy1_Sub.append([-1 for x in range(d1_sub_l)])
                for j in range(d1_sub_l):
                    Dummy1_Sub[i][j] = Dummy1[i][divmod(j, 3)[0]] # 将Dummy1的pixel数据变成Sub pixel

            for i in range(d2_sub_h):
                Dummy2_Sub.append([-1 for x in range(d2_sub_l)])
                for j in range(d2_sub_l):
                    Dummy2_Sub[i][j] = Dummy2[i][divmod(j, 3)[0]] # 将Dummy2的pixel数据变成Sub pixel，用于计算PS放哪种

            for i in range(Top2, Top2 + aa_sub_h):
                for j in range(L2, L2 + aa_sub_l):
                    DummyAA_Sub[i][j] = AA_Sub[i - Top2][j - L2]  # 将AA按照Dummy2大小放置，用于计算PS放哪种

            for i in range(Top2 - Top1, Top2 - Top1 + d1_sub_h):
                for j in range(L2 - L1, L2 - L1 + d1_sub_l):
                    Dummy11_Sub[i][j] = Dummy1_Sub[i - Top2 + Top1][j - L2 + L1]  # 将Dummy1按照Dummy2大小放置，用于计算PS放哪种

            # data113 = pd.DataFrame(DummyAA_Sub)
            # path113 = self.fp + '/DummyAA_Sub.csv'
            # data113.index = np.arange(1, data113.shape[0] + 1)
            # data113.columns = np.arange(1, data113.shape[1] + 1)
            # data113.to_csv(path113)
            #
            # data112 = pd.DataFrame(Dummy11_Sub)
            # path112 = self.fp + '/Dummy11_Sub.csv'
            # data112.index = np.arange(1, data112.shape[0] + 1)
            # data112.columns = np.arange(1, data112.shape[1] + 1)
            # data112.to_csv(path112)
            #
            # data111 = pd.DataFrame(Dummy2_Sub)
            # path111 = self.fp + '/Dummy2_Sub.csv'
            # data111.index = np.arange(1, data111.shape[0] + 1)
            # data111.columns = np.arange(1, data111.shape[1] + 1)
            # data111.to_csv(path111)
            # #
            # 以下为将PS周期放到AA区中，PS_AA_Sub
            PS_AA_Sub = []
            for i in range(ps_aa_h):
                PS_AA_Sub.append([-1 for x in range(ps_aa_l)])  # 在当前的C中新增一行元素，C[i][j]就可以做引用了
                for j in range(ps_aa_l):
                    PS_AA_Sub[i][j] = PS[divmod(i, ps_sub_h)[1]][divmod(j, ps_sub_l)[1]]
                    # 通过余数判断整个AA区PS放置

            # # # 定义最终的输出Excel矩阵行列数，并将摆放PS的AA区放入
            PS_Final_Sub = np.zeros((d2_sub_h, d2_sub_l))  # 定义最终输出矩阵范围，并先将其设置为0

            # 左上角的块
            for i in range(Top2):
                for j in range(L2):
                    PS_Final_Sub[i][j] = PS[ps_sub_h - Top2 + i][ps_sub_l - L2 + j]

            # 左边一直到最后一行的块
            for i in range(Top2, d2_sub_h):
                for j in range(L2):
                    PS_Final_Sub[i][j] = PS[divmod(i - Top2, ps_sub_h)[1]][ps_sub_l - L2 + j]

            # 顶部一直到最后一列的块
            for i in range(Top2):
                for j in range(L2, d2_sub_l):
                    PS_Final_Sub[i][j] = PS[ps_sub_h - Top2 + i][divmod(j - L2, ps_sub_l)[1]]

            # 剩余部分块
            for i in range(Top2, d2_sub_h):
                for j in range(L2, d2_sub_l):
                    PS_Final_Sub[i][j] = PS[divmod(i - Top2, ps_sub_h)[1]][divmod(j - L2, ps_sub_l)[1]]
                    # 通过余数判断整个Dummy2内的区域内均为PS周期放置

            for i in range(Top2, Top2 + aa_sub_h):
                for j in range(L2, L2 + aa_sub_l):
                    PS_Final_Sub[i][j] = PS_AA_Sub[i - Top2][j - L2]  # 将放有PS的AA区，放置到PS_Final_Sub中


            # # # 通过该判断将除最后一行，将灰阶过度位置非255灰阶的main PS转为sub PS，下一段程序更换最后一行
            for i in range(d2_sub_h-1):
                for j in range(d2_sub_l-1):
                    if (DummyAA_Sub[i][j] < 255 and (PS_Final_Sub[i][j] == 1 or PS_Final_Sub[i][j] == 3)) or (DummyAA_Sub[i+1][j] < 255 and (PS_Final_Sub[i][j] == 1 or PS_Final_Sub[i][j] == 3)) or (DummyAA_Sub[i][j+1] < 255 and (PS_Final_Sub[i][j] == 1 or PS_Final_Sub[i][j] == 3)) or (DummyAA_Sub[i+1][j+1] < 255 and (PS_Final_Sub[i][j] == 1 or PS_Final_Sub[i][j] == 3)):
                        PS_Final_Sub[i][j] = 2

            # 通过该判断，将Dummy2区最后一行中的Main PS变为Sub PS
            for j in range(d2_sub_l):
                if PS_Final_Sub[d2_sub_h-1][j] == 1 or PS_Final_Sub[d2_sub_h-1][j] == 3:
                    PS_Final_Sub[d2_sub_h-1][j] = 2
            # 通过该判断，将Dummy2区最后一列中的main PS变为Sub PS
            for i in range(d2_sub_h):
                if PS_Final_Sub[i][d2_sub_l-1] == 1 or PS_Final_Sub[d2_sub_h-1][j] == 3:
                    PS_Final_Sub[i][d2_sub_l-1] = 2

            # 通过该判断，定义Dummy2范围的外到Seal胶位置均为0(无PS),PS放置完成 Dummy2边界为211灰阶
            for i in range(d2_sub_h):
                for j in range(d2_sub_l):
                    if Dummy2_Sub[i][j] < 211 and DummyAA_Sub[i][j] == 0:
                        PS_Final_Sub[i][j] = 0
                    elif Dummy2_Sub[i][j] < 255 and Dummy2_Sub[i][j] > 210 and (PS_Final_Sub[i][j] == 1 or PS_Final_Sub[i][j] == 3):
                        PS_Final_Sub[i][j] = 2

            # # # 通过以下判断如果无island区(Dummy2)，最后一行和最右侧一列sub pixel上的PS去除，如果有island区(dummy2)则不作处理
            if Bot1 > 0:
                for j in range(d2_sub_l):
                    PS_Final_Sub[d2_sub_h - 1][j] = 0
            if R1 > 0:
                for i in range(d2_sub_h):
                    PS_Final_Sub[i][d2_sub_l - 1] = 0

            # # # 将Dummy2区右侧多余的sub PS去掉
            for i in range(d2_sub_h-1):
                for j in range(d2_sub_l-1):
                    if Dummy2_Sub[i][j] > 210 and Dummy2_Sub[i][j+1] < 211:
                        PS_Final_Sub[i][j] = 0

            # # # Stripe内包含AA区灰阶过度位置，若某个sub pixel上有PS，且PS占位的4个sub pixel中只要有一个灰阶低于Gray，则把该位置PS去掉，但是保留BM补偿，即PS 2-->4，开口率~83%进行删除PS
            for i in range(d2_sub_h - 1):
                for j in range(d2_sub_l - 1):
                    if PS_Final_Sub[i][j] > 0 and (DummyAA_Sub[i][j] < Gray or DummyAA_Sub[i+1][j] < Gray or DummyAA_Sub[i+1][j+1] < Gray or DummyAA_Sub[i][j+1] < Gray) and Dummy11_Sub[i][j] > 210: # and (DummyAA_Sub[i][j] != 255 and DummyAA_Sub[i+1][j] != 0): # i != Top2 + aa_h - 1:
                        PS_Final_Sub[i][j] = 4

            # # # Panel左侧，island区和stripe区接触的位置，如果有PS，则这个PS需去掉，防止island和stripe区RGB和PS干涉
            for i in range(d2_sub_h - 1):
                for j in range(d2_sub_l - 1):
                    if Dummy11_Sub[i][j] < 211 and (Dummy11_Sub[i][j+1] > 210 or Dummy11_Sub[i+1][j+1] > 210 or Dummy11_Sub[i+1][j] > 210):
                        PS_Final_Sub[i][j] = 0

            # 以下为Excel输出代码
            if TTT == 0:
                for i in range(int(aa_h/2)):
                    if AA[i][0] < 255 and AA[i+1][0] == 255:
                        a = i
                U_SP = math.ceil(a / ps_sub_h)
                num_U = U_SP * ps_sub_h + Top2
                uh = num_U
                ul = d2_sub_l
                Up_SP = []
                for i in range(uh):
                    Up_SP.append([-1 for x in range(ul)])
                    for j in range(ul):
                        Up_SP[i][j] = PS_Final_Sub[i][j]
            elif TTT != 0:
                tt_num = math.ceil(TTT / ps_sub_h)  # 包含圆孔底部，最小的PS周期数
                mt = tt_num * ps_sub_h
                mtd = mt + Top2
                uh = mtd
                ul = d2_sub_l
                Up_SP = []
                for i in range(uh):
                    Up_SP.append([-1 for x in range(ul)])
                    for j in range(ul):
                        Up_SP[i][j] = PS_Final_Sub[i][j]

            pix1 = []  # top位置，包含R角圆孔的sub pixel
            if divmod(Top2, 2)[1] != 0:
                for i in range(uh):
                    pix1.append([-1 for x in range(ul)])
                    for j in range(ul):
                        if divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and (DummyAA_Sub[i][j] > 0 or Dummy11_Sub[i][j] > 210):
                            pix1[i][j] = str(int(Up_SP[i][j])) + 'BA'
                            pix1[i][j - 1] = str(int(Up_SP[i][j - 1])) + 'GA'
                            pix1[i][j - 2] = str(int(Up_SP[i][j - 2])) + 'RA'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] > 210:
                            pix1[i][j] = str(int(Up_SP[i][j])) + 'ZA'
                            pix1[i][j - 1] = str(int(Up_SP[i][j - 1])) + 'YA'
                            pix1[i][j - 2] = str(int(Up_SP[i][j - 2])) + 'XA'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] < 211:
                            pix1[i][j] = str(int(Up_SP[i][j])) + 'NBA'
                            pix1[i][j - 1] = str(int(Up_SP[i][j - 1])) + 'NGA'
                            pix1[i][j - 2] = str(int(Up_SP[i][j - 2])) + 'NRA'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and (DummyAA_Sub[i][j] > 0 or Dummy11_Sub[i][j] > 210):
                            pix1[i][j] = str(int(Up_SP[i][j])) + 'BB'
                            pix1[i][j - 1] = str(int(Up_SP[i][j - 1])) + 'GB'
                            pix1[i][j - 2] = str(int(Up_SP[i][j - 2])) + 'RB'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] > 210:
                            pix1[i][j] = str(int(Up_SP[i][j])) + 'ZB'
                            pix1[i][j - 1] = str(int(Up_SP[i][j - 1])) + 'YB'
                            pix1[i][j - 2] = str(int(Up_SP[i][j - 2])) + 'XB'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] < 211:
                            pix1[i][j] = str(int(Up_SP[i][j])) + 'NBB'
                            pix1[i][j - 1] = str(int(Up_SP[i][j - 1])) + 'NGB'
                            pix1[i][j - 2] = str(int(Up_SP[i][j - 2])) + 'NRB'
            elif divmod(Top2, 2)[1] == 0:
                for i in range(uh):
                    pix1.append([-1 for x in range(ul)])
                    for j in range(ul):
                        if divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and (DummyAA_Sub[i][j] > 0 or Dummy11_Sub[i][j] > 210):
                            pix1[i][j] = str(int(Up_SP[i][j])) + 'BB'
                            pix1[i][j - 1] = str(int(Up_SP[i][j - 1])) + 'GB'
                            pix1[i][j - 2] = str(int(Up_SP[i][j - 2])) + 'RB'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] > 210:
                            pix1[i][j] = str(int(Up_SP[i][j])) + 'ZB'
                            pix1[i][j - 1] = str(int(Up_SP[i][j - 1])) + 'YB'
                            pix1[i][j - 2] = str(int(Up_SP[i][j - 2])) + 'XB'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] < 211:
                            pix1[i][j] = str(int(Up_SP[i][j])) + 'NBB'
                            pix1[i][j - 1] = str(int(Up_SP[i][j - 1])) + 'NGB'
                            pix1[i][j - 2] = str(int(Up_SP[i][j - 2])) + 'NRB'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and (DummyAA_Sub[i][j] > 0 or Dummy11_Sub[i][j] > 210):
                            pix1[i][j] = str(int(Up_SP[i][j])) + 'BA'
                            pix1[i][j - 1] = str(int(Up_SP[i][j - 1])) + 'GA'
                            pix1[i][j - 2] = str(int(Up_SP[i][j - 2])) + 'RA'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] > 210:
                            pix1[i][j] = str(int(Up_SP[i][j])) + 'ZA'
                            pix1[i][j - 1] = str(int(Up_SP[i][j - 1])) + 'YA'
                            pix1[i][j - 2] = str(int(Up_SP[i][j - 2])) + 'XA'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and  Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] < 211:
                            pix1[i][j] = str(int(Up_SP[i][j])) + 'NBA'
                            pix1[i][j - 1] = str(int(Up_SP[i][j - 1])) + 'NGA'
                            pix1[i][j - 2] = str(int(Up_SP[i][j - 2])) + 'NRA'

            pix2 = []
            cc = math.floor(aa_h / 2)
            c_num = math.floor(cc / ps_sub_h)
            mc = c_num * ps_sub_h
            mcd = mc + Top2
            ch = ps_sub_h
            cl = d2_sub_l

            Center_PS = []
            for i in range(ch):
                Center_PS.append([-1 for x in range(cl)])
                for j in range(cl):
                    Center_PS[i][j] = PS_Final_Sub[mcd + i][j]

            if divmod(mc, 2)[1] != 0:
                for i in range(ch):
                    pix2.append([-1 for x in range(cl)])
                    for j in range(cl):
                        if divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and (DummyAA_Sub[mcd + i][j] > 0 or Dummy11_Sub[mcd + i][j] > 210):
                            pix2[i][j] = str(int(Center_PS[i][j])) + 'BA'
                            pix2[i][j - 1] = str(int(Center_PS[i][j - 1])) + 'GA'
                            pix2[i][j - 2] = str(int(Center_PS[i][j - 2])) + 'RA'
                        elif  divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[mcd + i][j] == 0 and Dummy11_Sub[mcd + i][j] < 211 and Dummy2_Sub[mcd + i][j] > 210:
                            pix2[i][j] = str(int(Center_PS[i][j])) + 'ZA'
                            pix2[i][j - 1] = str(int(Center_PS[i][j - 1])) + 'YA'
                            pix2[i][j - 2] = str(int(Center_PS[i][j - 2])) + 'XA'
                        elif  divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[mcd + i][j] == 0 and Dummy11_Sub[mcd + i][j] < 211 and Dummy2_Sub[mcd + i][j] < 211:
                            pix2[i][j] = str(int(Center_PS[i][j])) + 'NBA'
                            pix2[i][j - 1] = str(int(Center_PS[i][j - 1])) + 'NGA'
                            pix2[i][j - 2] = str(int(Center_PS[i][j - 2])) + 'NRA'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and (DummyAA_Sub[mcd + i][j] > 0 or Dummy11_Sub[mcd + i][j] > 210):
                            pix2[i][j] = str(int(Center_PS[i][j])) + 'BB'
                            pix2[i][j - 1] = str(int(Center_PS[i][j - 1])) + 'GB'
                            pix2[i][j - 2] = str(int(Center_PS[i][j - 2])) + 'RB'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[mcd + i][j] == 0 and Dummy11_Sub[mcd + i][j] < 211 and Dummy2_Sub[mcd + i][j] > 210:
                            pix2[i][j] = str(int(Center_PS[i][j])) + 'ZB'
                            pix2[i][j - 1] = str(int(Center_PS[i][j - 1])) + 'YB'
                            pix2[i][j - 2] = str(int(Center_PS[i][j - 2])) + 'XB'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[mcd + i][j] == 0 and Dummy11_Sub[mcd + i][j] < 211 and Dummy2_Sub[mcd + i][j] < 211:
                            pix2[i][j] = str(int(Center_PS[i][j])) + 'NBB'
                            pix2[i][j - 1] = str(int(Center_PS[i][j - 1])) + 'NGB'
                            pix2[i][j - 2] = str(int(Center_PS[i][j - 2])) + 'NRB'
            elif divmod(mc, 2)[1] == 0:
                for i in range(ch):
                    pix2.append([-1 for x in range(cl)])
                    for j in range(cl):
                        if divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and (DummyAA_Sub[mcd + i][j] > 0 or Dummy11_Sub[mcd + i][j] > 210):
                            pix2[i][j] = str(int(Center_PS[i][j])) + 'BB'
                            pix2[i][j - 1] = str(int(Center_PS[i][j - 1])) + 'GB'
                            pix2[i][j - 2] = str(int(Center_PS[i][j - 2])) + 'RB'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[mcd + i][j] == 0 and Dummy11_Sub[mcd + i][j] < 211 and Dummy2_Sub[mcd + i][j] > 210:
                            pix2[i][j] = str(int(Center_PS[i][j])) + 'ZB'
                            pix2[i][j - 1] = str(int(Center_PS[i][j - 1])) + 'YB'
                            pix2[i][j - 2] = str(int(Center_PS[i][j - 2])) + 'XB'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[mcd + i][j] == 0 and Dummy11_Sub[mcd + i][j] < 211 and Dummy2_Sub[mcd + i][j] < 211:
                            pix2[i][j] = str(int(Center_PS[i][j])) + 'NBB'
                            pix2[i][j - 1] = str(int(Center_PS[i][j - 1])) + 'NGB'
                            pix2[i][j - 2] = str(int(Center_PS[i][j - 2])) + 'NRB'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and (DummyAA_Sub[mcd + i][j] > 0 or Dummy11_Sub[mcd + i][j] > 210):
                            pix2[i][j] = str(int(Center_PS[i][j])) + 'BA'
                            pix2[i][j - 1] = str(int(Center_PS[i][j - 1])) + 'GA'
                            pix2[i][j - 2] = str(int(Center_PS[i][j - 2])) + 'RA'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[mcd + i][j] == 0 and Dummy11_Sub[mcd + i][j] < 211 and Dummy2_Sub[mcd + i][j] > 210:
                            pix2[i][j] = str(int(Center_PS[i][j])) + 'ZA'
                            pix2[i][j - 1] = str(int(Center_PS[i][j - 1])) + 'YA'
                            pix2[i][j - 2] = str(int(Center_PS[i][j - 2])) + 'XA'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[mcd + i][j] == 0 and Dummy11_Sub[mcd + i][j] < 211 and Dummy2_Sub[mcd + i][j] < 211:
                            pix2[i][j] = str(int(Center_PS[i][j])) + 'NBA'
                            pix2[i][j - 1] = str(int(Center_PS[i][j - 1])) + 'NGA'
                            pix2[i][j - 2] = str(int(Center_PS[i][j - 2])) + 'NRA'

            # # # Bottom CSV生成
            pix3 = []
            # global b
            for i in range(int(aa_h / 2), int(aa_h)):
                if AA[i-1][1] == 255 and AA[i][1] < 255:
                    b = math.floor(i / ps_sub_h)
                elif AA[aa_h - 1][1] == 255 and AA[aa_h - 2][1] == 255:
                    b = math.floor((aa_h - 1) / ps_sub_h)
            #print(b)
            num_D = aa_h - b * ps_sub_h + Bot2 #  包括整周期main PS + Bottom Dummy2后，总共行数多少(dh)，列数(dl)
            dh = num_D
            dl = d2_sub_l

            Down_SP = []
            for i in range(dh):
                Down_SP.append([-1 for x in range(dl)])
                for j in range(dl):
                    Down_SP[i][j] = PS_Final_Sub[d2_sub_h - dh + i][j]

            if divmod(dh - Bot2, 2)[1] != 0:
                for i in range(dh):
                    pix3.append([-1 for x in range(dl)])
                    for j2 in range(dl):
                        if divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and (DummyAA_Sub[d2_sub_h - dh + i][j] > 0 or Dummy11_Sub[d2_sub_h - dh + i][j] > 210):
                            pix3[i][j] = str(int(Down_SP[i][j])) + 'BA'
                            pix3[i][j - 1] = str(int(Down_SP[i][j - 1])) + 'GA'
                            pix3[i][j - 2] = str(int(Down_SP[i][j - 2])) + 'RA'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[d2_sub_h - dh + i][j] == 0 and Dummy11_Sub[d2_sub_h - dh + i][j] < 211 and Dummy2_Sub[d2_sub_h - dh + i][j] > 210:
                            pix3[i][j] = str(int(Down_SP[i][j])) + 'ZA'
                            pix3[i][j - 1] = str(int(Down_SP[i][j - 1])) + 'YA'
                            pix3[i][j - 2] = str(int(Down_SP[i][j - 2])) + 'XA'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[d2_sub_h - dh + i][j] == 0 and Dummy11_Sub[d2_sub_h - dh + i][j] < 211 and Dummy2_Sub[d2_sub_h - dh + i][j] < 211:
                            pix3[i][j] = str(int(Down_SP[i][j])) + 'NBA'
                            pix3[i][j - 1] = str(int(Down_SP[i][j - 1])) + 'NGA'
                            pix3[i][j - 2] = str(int(Down_SP[i][j - 2])) + 'NRA'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and (DummyAA_Sub[d2_sub_h - dh + i][j] > 0 or Dummy11_Sub[d2_sub_h - dh + i][j] > 210):
                            pix3[i][j] = str(int(Down_SP[i][j])) + 'BB'
                            pix3[i][j - 1] = str(int(Down_SP[i][j - 1])) + 'GB'
                            pix3[i][j - 2] = str(int(Down_SP[i][j - 2])) + 'RB'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[d2_sub_h - dh + i][j] == 0 and Dummy11_Sub[d2_sub_h - dh + i][j] < 211 and Dummy2_Sub[d2_sub_h - dh + i][j] > 210:
                            pix3[i][j] = str(int(Down_SP[i][j])) + 'ZA'
                            pix3[i][j - 1] = str(int(Down_SP[i][j - 1])) + 'YB'
                            pix3[i][j - 2] = str(int(Down_SP[i][j - 2])) + 'XB'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[d2_sub_h - dh + i][j] == 0 and Dummy11_Sub[d2_sub_h - dh + i][j] < 211 and Dummy2_Sub[d2_sub_h - dh + i][j] < 211:
                            pix3[i][j] = str(int(Down_SP[i][j])) + 'NBB'
                            pix3[i][j - 1] = str(int(Down_SP[i][j - 1])) + 'NGB'
                            pix3[i][j - 2] = str(int(Down_SP[i][j - 2])) + 'NRB'
            elif divmod(dh - Bot2, 2)[1] == 0:
                for i in range(dh):
                    pix3.append([-1 for x in range(dl)])
                    for j in range(dl):
                        if divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and (DummyAA_Sub[d2_sub_h - dh + i][j] > 0 or Dummy11_Sub[d2_sub_h - dh + i][j] > 210):
                            pix3[i][j] = str(int(Down_SP[i][j])) + 'BB'
                            pix3[i][j - 1] = str(int(Down_SP[i][j - 1])) + 'GB'
                            pix3[i][j - 2] = str(int(Down_SP[i][j - 2])) + 'RB'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[d2_sub_h - dh + i][j] == 0 and Dummy11_Sub[d2_sub_h - dh + i][j] < 211 and Dummy2_Sub[d2_sub_h - dh + i][j] > 210:
                            pix3[i][j] = str(int(Down_SP[i][j])) + 'ZB'
                            pix3[i][j - 1] = str(int(Down_SP[i][j - 1])) + 'YB'
                            pix3[i][j - 2] = str(int(Down_SP[i][j - 2])) + 'XB'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[d2_sub_h - dh + i][j] == 0 and Dummy11_Sub[d2_sub_h - dh + i][j] < 211 and Dummy2_Sub[d2_sub_h - dh + i][j] < 211:
                            pix3[i][j] = str(int(Down_SP[i][j])) + 'NBB'
                            pix3[i][j - 1] = str(int(Down_SP[i][j - 1])) + 'NGB'
                            pix3[i][j - 2] = str(int(Down_SP[i][j - 2])) + 'NRB'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and (DummyAA_Sub[d2_sub_h - dh + i][j] > 0 or Dummy11_Sub[d2_sub_h - dh + i][j] > 210):
                            pix3[i][j] = str(int(Down_SP[i][j])) + 'BA'
                            pix3[i][j - 1] = str(int(Down_SP[i][j - 1])) + 'GA'
                            pix3[i][j - 2] = str(int(Down_SP[i][j - 2])) + 'RA'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[d2_sub_h - dh + i][j] == 0 and Dummy11_Sub[d2_sub_h - dh + i][j] < 211 and Dummy2_Sub[d2_sub_h - dh + i][j] > 210:
                            pix3[i][j] = str(int(Down_SP[i][j])) + 'ZA'
                            pix3[i][j - 1] = str(int(Down_SP[i][j - 1])) + 'YA'
                            pix3[i][j - 2] = str(int(Down_SP[i][j - 2])) + 'XA'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[d2_sub_h - dh + i][j] == 0 and Dummy11_Sub[d2_sub_h - dh + i][j] < 211 and Dummy2_Sub[d2_sub_h - dh + i][j] < 211:
                            pix3[i][j] = str(int(Down_SP[i][j])) + 'NBA'
                            pix3[i][j - 1] = str(int(Down_SP[i][j - 1])) + 'NGA'
                            pix3[i][j - 2] = str(int(Down_SP[i][j - 2])) + 'NRA'
            # 将全屏数据生成DataFrame
            data_Top = pd.DataFrame(pix1)
            data_Center = pd.DataFrame(pix2)
            data_Bottom = pd.DataFrame(pix3)

            data_Top.index = np.arange(1, data_Top.shape[0] + 1)
            data_Top.columns = np.arange(1, data_Top.shape[1] + 1)
            data_Center.index = np.arange(1, data_Center.shape[0] + 1)
            data_Center.columns = np.arange(1, data_Center.shape[1] + 1)
            data_Bottom.index = np.arange(1, data_Bottom.shape[0] + 1)
            data_Bottom.columns = np.arange(1, data_Bottom.shape[1] + 1)

            data_All = pd.concat([data_Top, data_Center, data_Bottom], axis = 0, ignore_index = True) # 参数axis=0表示上下合并，1表示左右合并，ignore_index=True表示忽略原来的索引

            # 获取所有非重复元素，并写入Excel
            elel = np.unique(data_All)
            data_el = pd.DataFrame(elel)
            data_el.index = np.arange(1, data_el.shape[0] + 1)
            data_el.columns = np.arange(1, data_el.shape[1] + 1)

            # 显示示意说明
            state = np.empty([9, 3], dtype=object)
            state[0, 0] = '0: 该位置无PS'
            state[1, 0] = '1: 该位置为Main PS'
            state[2, 0] = '2: 该位置为Sub PS'
            state[3, 0] = '3: 该位置无PS, 但BM按照Main PS补偿'
            state[4, 0] = '4: 该位置无PS, 但BM按照Sub PS补偿'

            state[0, 1] = 'R: Stripe Red'
            state[1, 1] = 'G: Stripe Green'
            state[2, 1] = 'B: Stripe Blue'
            state[3, 1] = 'X: island Red'
            state[4, 1] = 'Y: island Green'
            state[5, 1] = 'Z: island Blue'
            state[6, 1] = 'NR: 无Red层, 但是像素形貌按照Red像素'
            state[7, 1] = 'NG: 无Green层, 但是像素形貌按照Green像素'
            state[8, 1] = 'NB: 无Blue层, 但是像素形貌按照Blue像素'

            state[0, 2] = 'A: 奇数行'
            state[1, 2] = 'B: 偶数行'

            stt = pd.DataFrame(state, columns=['PS类型', 'RGB类型', '奇偶行'])

            col61, col62, col63, col64, col65, col66, col67, col68, col69 = st.columns([1, 3, 1, 3, 1, 3, 1, 3, 1])
            with col62:
                st.write(data_Top)
            with col64:
                st.write(data_Center)
            with col66:
                st.write(data_Bottom)
            with col68:
                st.write(data_el)

            col71, col72, col73 = st.columns([1, 15, 2])
            with col72:
                st.write(stt)

        else:
            ps_sub_h = PS.shape[0]
            ps_sub_l = PS.shape[1]
            aa_h = AA.shape[0]
            aa_l = AA.shape[1]
            d1_h = Dummy1.shape[0]
            d1_l = Dummy1.shape[1]
            d2_h = Dummy2.shape[0]
            d2_l = Dummy2.shape[1]
            aa_sub_h = aa_h
            aa_sub_l = aa_l * 3
            d1_sub_h = d1_h
            d1_sub_l = d1_l * 3
            d2_sub_h = d2_h
            d2_sub_l = d2_l * 3
            ps_aa_h = aa_sub_h
            ps_aa_l = aa_sub_l

            # # # # #以下部分为设置用于判断边界位置PS放置哪种的判断矩阵DummyAA_Sub,Dummy11_Sub,Dummy2_Sub# # # # #
            AA_Sub = [] # 将CAD导出的AA做成Sub pixel（列数*3），用来判断Main PS去掉的区域
            DummyAA_Sub = np.zeros((d2_sub_h, d2_sub_l))  # 将AA按照Dummy2大小放置
            Dummy1_Sub = [] # 将CAD导出的Dummy1做成Sub pixel（列数*3）
            Dummy11_Sub = np.zeros((d2_sub_h, d2_sub_l)) # 将Dummy1按照Dummy2大小放置
            Dummy2_Sub = [] # 将CAD导出的Dummy2做成Sub pixel（列数*3）
            for i in range(aa_sub_h):
                AA_Sub.append([-1 for x in range(aa_sub_l)])  # 在当前的C中新增一行元素，C[i][j]就可以做引用了
                for j in range(aa_sub_l):
                    AA_Sub[i][j] = AA[i][divmod(j, 3)[0]] # 将AA区的Pixel数据变成Sub pixel

            for i in range(d1_sub_h):
                Dummy1_Sub.append([-1 for x in range(d1_sub_l)])
                for j in range(d1_sub_l):
                    Dummy1_Sub[i][j] = Dummy1[i][divmod(j, 3)[0]] # 将Dummy1的pixel数据变成Sub pixel

            for i in range(d2_sub_h):
                Dummy2_Sub.append([-1 for x in range(d2_sub_l)])
                for j in range(d2_sub_l):
                    Dummy2_Sub[i][j] = Dummy2[i][divmod(j, 3)[0]] # 将Dummy2的pixel数据变成Sub pixel，用于计算PS放哪种

            for i in range(Top2, Top2 + aa_sub_h):
                for j in range(L2, L2 + aa_sub_l):
                    DummyAA_Sub[i][j] = AA_Sub[i - Top2][j - L2]  # 将AA按照Dummy2大小放置，用于计算PS放哪种

            for i in range(Top2 - Top1, Top2 - Top1 + d1_sub_h):
                for j in range(L2 - L1, L2 - L1 + d1_sub_l):
                    Dummy11_Sub[i][j] = Dummy1_Sub[i - Top2 + Top1][j - L2 + L1]  # 将Dummy1按照Dummy2大小放置，用于计算PS放哪种

            # 以下为将PS周期放到AA区中，PS_AA_Sub
            PS_AA_Sub = []
            for i in range(ps_aa_h):
                PS_AA_Sub.append([-1 for x in range(ps_aa_l)])  # 在当前的C中新增一行元素，C[i][j]就可以做引用了
                for j in range(ps_aa_l):
                    PS_AA_Sub[i][j] = PS[divmod(i, ps_sub_h)[1]][divmod(j, ps_sub_l)[1]]
                    # 通过余数判断整个AA区PS放置

            # # # 定义最终的输出Excel矩阵行列数，并将摆放PS的AA区放入
            PS_Final_Sub = np.zeros((d2_sub_h, d2_sub_l))  # 定义最终输出矩阵范围，并先将其设置为0

            # 将Dummy2区内都布满PS周期
            for i in range(d2_sub_h):
                for j in range(d2_sub_l):
                    PS_Final_Sub[i][j] = PS[divmod(i + Top2, ps_sub_h)[1]][divmod(j + L2, ps_sub_l)[1]]  # 通过余数判断整个Dummy2内的区域内均为PS周期放置

            for i in range(Top2, Top2 + aa_sub_h):
                for j in range(L2, L2 + aa_sub_l):
                    PS_Final_Sub[i][j] = PS_AA_Sub[i - Top2][j - L2]  # 将放有PS的AA区，放置到PS_Final_Sub中

            # # # 通过该判断将除最后一行，将灰阶过度位置非255灰阶的main PS转为sub PS，下一段程序更换最后一行
            for i in range(d2_sub_h-1):
                for j in range(d2_sub_l-1):
                    if (DummyAA_Sub[i][j] < 255 and (PS_Final_Sub[i][j] == 1 or PS_Final_Sub[i][j] == 3)) or (DummyAA_Sub[i+1][j] < 255 and (PS_Final_Sub[i][j] == 1 or PS_Final_Sub[i][j] == 3)) or (DummyAA_Sub[i][j+1] < 255 and (PS_Final_Sub[i][j] == 1 or PS_Final_Sub[i][j] == 3)) or (DummyAA_Sub[i+1][j+1] < 255 and (PS_Final_Sub[i][j] == 1 or PS_Final_Sub[i][j] == 3)):
                        PS_Final_Sub[i][j] = 2
            # 通过该判断，将Dummy2区最后一行中的Main PS变为Sub PS
            for j in range(d2_sub_l):
                if PS_Final_Sub[d2_sub_h-1][j] == 1 or PS_Final_Sub[d2_sub_h-1][j] == 3:
                    PS_Final_Sub[d2_sub_h-1][j] = 2
            # 通过该判断，将Dummy2区最后一列中的main PS变为Sub PS
            for i in range(d2_sub_h):
                if PS_Final_Sub[i][d2_sub_l-1] == 1 or PS_Final_Sub[d2_sub_h-1][j] == 3:
                    PS_Final_Sub[i][d2_sub_l-1] = 2
            # 通过该判断，定义Dummy2范围的外到Seal胶位置均为0(无PS),PS放置完成 Dummy2边界为211灰阶
            for i in range(d2_sub_h):
                for j in range(d2_sub_l):
                    if Dummy2_Sub[i][j] < 211 and DummyAA_Sub[i][j] == 0:
                        PS_Final_Sub[i][j] = 0
                    elif Dummy2_Sub[i][j] < 255 and Dummy2_Sub[i][j] > 210 and (PS_Final_Sub[i][j] == 1 or PS_Final_Sub[i][j] == 3):
                        PS_Final_Sub[i][j] = 2

            # # # 通过以下判断如果无island区(Dummy2)，最后一行和最右侧一列sub pixel上的PS去除，如果有island区(dummy2)则不作处理
            if Bot1 > 0:
                for j in range(d2_sub_l):
                    PS_Final_Sub[d2_sub_h - 1][j] = 0

            if R1 > 0:
                for i in range(d2_sub_h):
                    PS_Final_Sub[i][d2_sub_l - 1] = 0

            # # #将右侧多余的sub PS去掉
            for i in range(d2_sub_h-1):
                for j in range(d2_sub_l-1):
                    if Dummy2_Sub[i][j] > 210 and Dummy2_Sub[i][j+1] < 211:
                        PS_Final_Sub[i][j] = 0

            # # # Stripe内包含AA区灰阶过度位置，若某个sub pixel上有PS，且PS占位的4个sub pixel中只要有一个灰阶低于Gray，则把该位置PS去掉，但是保留BM补偿，即PS 2-->4，开口率~83%进行删除PS
            for i in range(d2_sub_h - 1):
                for j in range(d2_sub_l - 1):
                    if PS_Final_Sub[i][j] > 0 and (DummyAA_Sub[i][j] < Gray or DummyAA_Sub[i+1][j] < Gray or DummyAA_Sub[i+1][j+1] < Gray or DummyAA_Sub[i][j+1] < Gray) and Dummy11_Sub[i][j] > 210:  # and (DummyAA_Sub[i][j] != 255 and DummyAA_Sub[i+1][j] != 0): # i != Top2 + aa_h - 1:
                        PS_Final_Sub[i][j] = 4

            # # 输出Excel
            # data55 = pd.DataFrame(Dummy11_Sub)
            # path55 = self.fp + '/Dummy11_Sub_All.csv'
            # data55.index = np.arange(1, data55.shape[0] + 1)
            # data55.columns = np.arange(1, data55.shape[1] + 1)
            # data55.to_csv(path55)

            # # # 整个Panel, island区和stripe区接触的位置，如果有PS，则这个PS需去掉，防止island和stripe区RGB和PS干涉
            for i in range(d2_sub_h - 1):
                for j in range(d2_sub_l - 1):
                    if Dummy11_Sub[i][j] < 211 and (Dummy11_Sub[i][j+1] > 210 or Dummy11_Sub[i+1][j] > 210 or Dummy11_Sub[i+1][j+1] > 210):  # and PS_Final_Sub[i][j] == 2:and Dummy2_Sub[i][j] > 210
                        PS_Final_Sub[i][j] = 0

            # # 以下为Excel输出代码
            pix1 = []  # top位置，包含R角圆孔的sub pixel
            if divmod(Top2, 2)[1] != 0:
                for i in range(d2_sub_h):
                    pix1.append([-1 for x in range(d2_sub_l)])
                    for j in range(d2_sub_l):
                        if divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and (
                                DummyAA_Sub[i][j] > 0 or Dummy11_Sub[i][j] > 210):
                            pix1[i][j] = str(int(PS_Final_Sub[i][j])) + 'BA'
                            pix1[i][j - 1] = str(int(PS_Final_Sub[i][j - 1])) + 'GA'
                            pix1[i][j - 2] = str(int(PS_Final_Sub[i][j - 2])) + 'RA'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and \
                                Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] > 210:
                            pix1[i][j] = str(int(PS_Final_Sub[i][j])) + 'ZA'
                            pix1[i][j - 1] = str(int(PS_Final_Sub[i][j - 1])) + 'YA'
                            pix1[i][j - 2] = str(int(PS_Final_Sub[i][j - 2])) + 'XA'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and \
                                Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] < 211:
                            pix1[i][j] = str(int(PS_Final_Sub[i][j])) + 'NBA'
                            pix1[i][j - 1] = str(int(PS_Final_Sub[i][j - 1])) + 'NGA'
                            pix1[i][j - 2] = str(int(PS_Final_Sub[i][j - 2])) + 'NRA'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and (
                                DummyAA_Sub[i][j] > 0 or Dummy11_Sub[i][j] > 210):
                            pix1[i][j] = str(int(PS_Final_Sub[i][j])) + 'BB'
                            pix1[i][j - 1] = str(int(PS_Final_Sub[i][j - 1])) + 'GB'
                            pix1[i][j - 2] = str(int(PS_Final_Sub[i][j - 2])) + 'RB'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and \
                                Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] > 210:
                            pix1[i][j] = str(int(PS_Final_Sub[i][j])) + 'ZB'
                            pix1[i][j - 1] = str(int(PS_Final_Sub[i][j - 1])) + 'YB'
                            pix1[i][j - 2] = str(int(PS_Final_Sub[i][j - 2])) + 'XB'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and \
                                Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] < 211:
                            pix1[i][j] = str(int(PS_Final_Sub[i][j])) + 'NBB'
                            pix1[i][j - 1] = str(int(PS_Final_Sub[i][j - 1])) + 'NGB'
                            pix1[i][j - 2] = str(int(PS_Final_Sub[i][j - 2])) + 'NRB'
            elif divmod(Top2, 2)[1] == 0:
                for i in range(d2_sub_h):
                    pix1.append([-1 for x in range(d2_sub_l)])
                    for j in range(d2_sub_l):
                        if divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and (
                                DummyAA_Sub[i][j] > 0 or Dummy11_Sub[i][j] > 210):
                            pix1[i][j] = str(int(PS_Final_Sub[i][j])) + 'BB'
                            pix1[i][j - 1] = str(int(PS_Final_Sub[i][j - 1])) + 'GB'
                            pix1[i][j - 2] = str(int(PS_Final_Sub[i][j - 2])) + 'RB'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and \
                                Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] > 210:
                            pix1[i][j] = str(int(PS_Final_Sub[i][j])) + 'ZB'
                            pix1[i][j - 1] = str(int(PS_Final_Sub[i][j - 1])) + 'YB'
                            pix1[i][j - 2] = str(int(PS_Final_Sub[i][j - 2])) + 'XB'
                        elif divmod(i, 2)[1] != 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and \
                                Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] < 211:
                            pix1[i][j] = str(int(PS_Final_Sub[i][j])) + 'NBB'
                            pix1[i][j - 1] = str(int(PS_Final_Sub[i][j - 1])) + 'NGB'
                            pix1[i][j - 2] = str(int(PS_Final_Sub[i][j - 2])) + 'NRB'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and (
                                DummyAA_Sub[i][j] > 0 or Dummy11_Sub[i][j] > 210):
                            pix1[i][j] = str(int(PS_Final_Sub[i][j])) + 'BA'
                            pix1[i][j - 1] = str(int(PS_Final_Sub[i][j - 1])) + 'GA'
                            pix1[i][j - 2] = str(int(PS_Final_Sub[i][j - 2])) + 'RA'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and \
                                Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] > 210:
                            pix1[i][j] = str(int(PS_Final_Sub[i][j])) + 'ZA'
                            pix1[i][j - 1] = str(int(PS_Final_Sub[i][j - 1])) + 'YA'
                            pix1[i][j - 2] = str(int(PS_Final_Sub[i][j - 2])) + 'XA'
                        elif divmod(i, 2)[1] == 0 and divmod(j, 3)[1] == 2 and DummyAA_Sub[i][j] == 0 and \
                                Dummy11_Sub[i][j] < 211 and Dummy2_Sub[i][j] < 211:
                            pix1[i][j] = str(int(PS_Final_Sub[i][j])) + 'NBA'
                            pix1[i][j - 1] = str(int(PS_Final_Sub[i][j - 1])) + 'NGA'
                            pix1[i][j - 2] = str(int(PS_Final_Sub[i][j - 2])) + 'NRA'
            
            # 将全屏数据生成DataFrame
            data = pd.DataFrame(pix1)
            data.index = np.arange(1, data.shape[0] + 1)
            data.columns = np.arange(1, data.shape[1] + 1)

            # 获取所有非重复元素，并写入Excel
            elel = np.unique(data)
            data_el = pd.DataFrame(elel)
            data_el.index = np.arange(1, data_el.shape[0] + 1)
            data_el.columns = np.arange(1, data_el.shape[1] + 1)
            
            # 显示示意说明
            state = np.empty([9, 3], dtype=object)
            state[0, 0] = '0: 该位置无PS'
            state[1, 0] = '1: 该位置为Main PS'
            state[2, 0] = '2: 该位置为Sub PS'
            state[3, 0] = '3: 该位置无PS, 但BM按照Main PS补偿'
            state[4, 0] = '4: 该位置无PS, 但BM按照Sub PS补偿'

            state[0, 1] = 'R: Stripe Red'
            state[1, 1] = 'G: Stripe Green'
            state[2, 1] = 'B: Stripe Blue'
            state[3, 1] = 'X: island Red'
            state[4, 1] = 'Y: island Green'
            state[5, 1] = 'Z: island Blue'
            state[6, 1] = 'NR: 无Red层, 但是像素形貌按照Red像素'
            state[7, 1] = 'NG: 无Green层, 但是像素形貌按照Green像素'
            state[8, 1] = 'NB: 无Blue层, 但是像素形貌按照Blue像素'

            state[0, 2] = 'A: 奇数行'
            state[1, 2] = 'B: 偶数行'

            stt = pd.DataFrame(state, columns=['PS类型', 'RGB类型', '奇偶行'])

            col61, col62, col63, col64, col65 = st.columns([1, 5, 1, 3, 1])
            with col62:
                st.write(data)
            with col64:
                st.write(data_el)
            col71, col72, col73 = st.columns([1, 15, 2])
            with col72:
                st.write(stt)
    # 判断错误信息
    except NameError:
        col81, col82, col83 = st.columns([1, 8, 10])
        with col82:
            st.write("<h6 style='color: red;'>请确认所有信息已填写完成！</h6>", unsafe_allow_html=True)


# 编辑button - Final计算
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(12) > div.st-emotion-cache-vft1hk.e1f1d6gn3 > div > div > div > div > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px !important;
    width: 150px !important;
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
