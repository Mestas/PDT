from shapely.geometry import Polygon
import math
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具可以计算LCD产品开口率</h4>", unsafe_allow_html=True)

# # # 工具名称、版本号
st.write("# LCD产品开口率评估工具 #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V1.0</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2024/08/12</h5>", unsafe_allow_html=True)

# # # 设置步骤1：选择像素排布和PS设计方案
st.write("<h6>步骤1：请选择Pixel及PS设计方案</h6>", unsafe_allow_html=True)

c11, c12, c13, c14, c15, c16, c17 = st.columns([1, 5, 1, 5, 1, 5, 1])
with c12:
    my_pix = st.radio('选择像素设计', ('Normal像素', 'TX in Dot', '1Dual Source', '2Dual Source', '3Dual Source'))
    if my_pix == 'Normal像素':
        pix = 1
    elif my_pix == 'TX in Dot':
        pix = 2
    elif my_pix == '1Dual Source':
        pix = 3
    elif my_pix == '2Dual Source':
        pix = 4
    elif my_pix == '3Dual Source':
        pix = 5

with c14:
    my_ps = st.radio('选择PS设计', ('Normal PS', 'XPS'))
    if my_ps == 'Normal PS':
        ps = 1
    elif my_ps == 'XPS':
        ps = 2

with c16:
    my_density = st.radio('选择PS密度方案', ('全密度', '1/2密度'))
    if my_density == '全密度':
        density = 1
    elif my_density == '1/2密度':
        density = 2

# # # 设置步骤2：输入像素及PS设计参数
st.write("<h6>步骤2：请输入像素及PS设计参数</h6>", unsafe_allow_html=True)

c21, c22, c23, c24, c25, c26, c27 = st.columns([1, 3, 2, 3, 2, 3, 2])
with c22:
    pix_x = st.number_input(label='Pixel宽度', format='%f', key='pix_x')  # 像素尺寸-X方向
with c22:
    pix_y = st.number_input(label='Pixel高度', format='%f', key='pix_y')  # 像素尺寸-Y方向
with c22:
    angle = st.number_input(label='Pixel角度', format='%f', key='angle')  # 像素倾斜角度
with c22:
    BM_Gate = st.number_input(label='Gate向BM CD', format='%f', key='BM_Gate')  # Gate向BM CD

if pix == 1:
    with c22:
        BM_SD = st.number_input(label='SD向BM CD', format='%f', disabled= False, key='BM_SD')  # SD向BM CD
    with c22:
        TX_CD = st.number_input(label='TX CD', value = 0, disabled= True, key='TX_CD')  # SD向BM CD
    with c22:
        BM_DS = st.number_input(label='Dual Source位置BM CD', value = 0, disabled= True, key="Dual Source BM CD")  # SD向BM CD
elif pix == 2:
    with c22:
        BM_SD = st.number_input(label='SD向BM CD', format='%f', disabled= False, key='BM_SD')  # SD向BM CD
    with c22:
        TX_CD = st.number_input(label='TX CD', format='%f', disabled= False, key='TX_CD')  # SD向BM CD
    with c22:
        BM_DS = st.number_input(label='Dual Source位置BM CD', value = 0, disabled= True, key="Dual Source BM CD")  # SD向BM CD
elif pix == 3 or pix == 4:
    with c22:
        BM_SD = st.number_input(label='SD向BM CD', format='%f', disabled= False, key='BM_SD')  # SD向BM CD
    with c22:
        TX_CD = st.number_input(label='TX CD', format='%f', disabled= True, key='TX_CD')  # SD向BM CD
    with c22:
        BM_DS = st.number_input(label='Dual Source位置BM CD', value = 0, disabled= False, key="Dual Source BM CD")  # SD向BM CD
else:
    with c22:
        BM_SD = st.number_input(label='SD向BM CD', format='%f', disabled= True, key='BM_SD')  # SD向BM CD
    with c22:
        TX_CD = st.number_input(label='TX CD', format='%f', disabled= True, key='TX_CD')  # SD向BM CD
    with c22:
        BM_DS = st.number_input(label='Dual Source位置BM CD', value = 0, disabled= False, key="Dual Source BM CD")  # SD向BM CD

with c24:
    hps_x = st.number_input(label='PS-X方向Size', format='%f', key='hps_x')  # HPS尺寸-X方向
with c24:
    hps_y = st.number_input(label='PS-Y方向Size', format='%f', key='hps_y')  # HPS尺寸-Y方向
with c24:
    hps_BM = st.number_input(label='PS-BM补偿', format='%f', key='hps_BM')  # HPS的BM补偿

if ps == 2:
    with c26:
        vps_x = st.number_input(label='XPS-X方向Size', format='%f', disabled= False, key='vps_x')  # VPS尺寸-X方向
    with c26:
        vps_y = st.number_input(label='XPS-Y方向Size', format='%f', disabled= False, key='vps_y')  # VPS尺寸-Y方向
    with c26:
        vps_BM = st.number_input(label='XPS-BM补偿', format='%f', disabled= False, key='vps_BM')  # VPS的BM补偿
else:
    with c26:
        vps_x = st.number_input(label='XPS-X方向Size', value = 0, disabled= True, key='vps_x')  # VPS尺寸-X方向
    with c26:
        vps_y = st.number_input(label='XPS-Y方向Size', value = 0, disabled= True, key='vps_y')  # VPS尺寸-Y方向
    with c26:
        vps_BM = st.number_input(label='XPS-BM补偿', value = 0, disabled= True, key='vps_BM')  # VPS的BM补偿

# # # 设置步骤3：点击按钮计算开口率
st.write("<h6>步骤3：点击按钮计算开口率</h6>", unsafe_allow_html=True)

calc = st.button('***点击计算***', key='calc')
if calc is True:
    # # # # # # 计算开口区尺寸
    if pix < 2:
        # 计算开口区大小
        AR_x = (pix_x * math.cos(angle / 180 * math.pi) - BM_SD) / math.cos(angle / 180 * math.pi)
        AR_y = pix_y - BM_Gate

        # 计算开口区右上坐标点x方向位移量
        d_AR_x = AR_y * math.tan(angle / 180 * math.pi)

        # 第一个pixel的左下点坐标
        db = BM_SD / 2 / math.cos(angle / 180 * math.pi)
        dg = BM_Gate / 2 * math.tan(angle / 180 * math.pi)
        P1_x = db - dg
        P1_y = BM_Gate / 2

        # 计算RGB的pitch
        R_pitch = BM_SD / math.cos(angle / 180 * math.pi) + AR_x
        G_pitch = BM_SD / math.cos(angle / 180 * math.pi) + AR_x
        B_pitch = BM_SD / math.cos(angle / 180 * math.pi) + AR_x

        PS_R_pitch = R_pitch
        PS_G_pitch = G_pitch
        PS_B_pitch = B_pitch

        AR_pitch = R_pitch + G_pitch + B_pitch
        # print(R_pitch, G_pitch, B_pitch, AR_pitch)

    elif pix == 3:
        # 计算开口区大小
        AR_x = (pix_x * 3 * math.cos(angle / 180 * math.pi) - BM_SD * 2 - BM_DS) / 3 / math.cos(angle / 180 * math.pi)
        AR_y = pix_y - BM_Gate
         # 计算开口区右上坐标点x方向位移量
        d_AR_x = AR_y * math.tan(angle / 180 * math.pi)

        # 第一个pixel的左下点坐标
        db = BM_DS / 2 / math.cos(angle / 180 * math.pi)
        dg = BM_Gate / 2 * math.tan(angle / 180 * math.pi)
        P1_x = db - dg
        P1_y = BM_Gate / 2

        # 计算RGB的pitch
        R_pitch = BM_SD / math.cos(angle / 180 * math.pi) + AR_x
        G_pitch = BM_SD / math.cos(angle / 180 * math.pi) + AR_x
        B_pitch = BM_DS / math.cos(angle / 180 * math.pi) + AR_x

        PS_R_pitch = (BM_SD + BM_DS) / 2 / math.cos(angle / 180 * math.pi) + AR_x
        PS_G_pitch = BM_SD / math.cos(angle / 180 * math.pi) + AR_x
        PS_B_pitch = (BM_SD + BM_DS) / 2 / math.cos(angle / 180 * math.pi) + AR_x

        AR_pitch = R_pitch + G_pitch + B_pitch
        # print(R_pitch, G_pitch, B_pitch, AR_pitch)

    elif pix == 4:
        # 计算开口区大小
        AR_x = (pix_x * 3 * math.cos(angle / 180 * math.pi) - BM_SD - BM_DS * 2) / 3 / math.cos(angle / 180 * math.pi)
        AR_y = pix_y - BM_Gate
         # 计算开口区右上坐标点x方向位移量
        d_AR_x = AR_y * math.tan(angle / 180 * math.pi)

        # 第一个pixel的左下点坐标
        db = BM_DS / 2 / math.cos(angle / 180 * math.pi)
        dg = BM_Gate / 2 * math.tan(angle / 180 * math.pi)
        P1_x = db - dg
        P1_y = BM_Gate / 2

        # 计算RGB的pitch
        R_pitch = BM_SD / math.cos(angle / 180 * math.pi) + AR_x
        G_pitch = BM_DS / math.cos(angle / 180 * math.pi) + AR_x
        B_pitch = BM_DS / math.cos(angle / 180 * math.pi) + AR_x

        PS_R_pitch = (BM_SD + BM_DS) / 2 / math.cos(angle / 180 * math.pi) + AR_x
        PS_G_pitch = (BM_SD + BM_DS) / 2 / math.cos(angle / 180 * math.pi) + AR_x
        PS_B_pitch = BM_DS / math.cos(angle / 180 * math.pi) + AR_x

        AR_pitch = R_pitch + G_pitch + B_pitch
        # print(R_pitch, G_pitch, B_pitch, AR_pitch)

    elif pix == 5:
        # 计算开口区大小
        AR_x = (pix_x * math.cos(angle / 180 * math.pi) - BM_DS) / math.cos(angle / 180 * math.pi)
        AR_y = pix_y - BM_Gate
         # 计算开口区右上坐标点x方向位移量
        d_AR_x = AR_y * math.tan(angle / 180 * math.pi)

        # 第一个pixel的左下点坐标
        db = BM_DS / 2 / math.cos(angle / 180 * math.pi)
        dg = BM_Gate / 2 * math.tan(angle / 180 * math.pi)
        P1_x = db - dg
        P1_y = BM_Gate / 2

        # 计算RGB的pitch
        R_pitch = BM_DS / math.cos(angle / 180 * math.pi) + AR_x
        G_pitch = BM_DS / math.cos(angle / 180 * math.pi) + AR_x
        B_pitch = BM_DS / math.cos(angle / 180 * math.pi) + AR_x

        PS_R_pitch = BM_DS / math.cos(angle / 180 * math.pi) + AR_x
        PS_G_pitch = BM_DS / math.cos(angle / 180 * math.pi) + AR_x
        PS_B_pitch = BM_DS / math.cos(angle / 180 * math.pi) + AR_x

        AR_pitch = R_pitch + G_pitch + B_pitch
        # print(R_pitch, G_pitch, B_pitch, AR_pitch)

    # # # 绘制12个pixel的开口区
    P1 = Polygon([(P1_x, P1_y), (P1_x + AR_x, P1_y), (P1_x + AR_x - d_AR_x, P1_y + AR_y), (P1_x - d_AR_x, P1_y + AR_y), (P1_x, P1_y)])
    P2 = Polygon([(P1_x + R_pitch, P1_y), (P1_x + AR_x + R_pitch, P1_y), (P1_x + AR_x - d_AR_x + R_pitch, P1_y + AR_y), (P1_x - d_AR_x + R_pitch, P1_y + AR_y), (P1_x + R_pitch, P1_y)])
    P3 = Polygon([(P1_x + R_pitch + G_pitch, P1_y), (P1_x + AR_x + R_pitch + G_pitch, P1_y), (P1_x + AR_x - d_AR_x + R_pitch + G_pitch, P1_y + AR_y), (P1_x - d_AR_x + R_pitch + G_pitch, P1_y + AR_y), (P1_x + R_pitch + G_pitch, P1_y)])
    P4 = Polygon([(P1_x + AR_pitch, P1_y), (P1_x + AR_x + AR_pitch, P1_y), (P1_x + AR_x - d_AR_x + AR_pitch, P1_y + AR_y), (P1_x - d_AR_x + AR_pitch, P1_y + AR_y), (P1_x + AR_pitch, P1_y)])
    P5 = Polygon([(P1_x + R_pitch + AR_pitch, P1_y), (P1_x + AR_x + R_pitch + AR_pitch, P1_y), (P1_x + AR_x - d_AR_x + R_pitch + AR_pitch, P1_y + AR_y), (P1_x - d_AR_x + R_pitch + AR_pitch, P1_y + AR_y), (P1_x + R_pitch + AR_pitch, P1_y)])
    P6 = Polygon([(P1_x + R_pitch + G_pitch + AR_pitch, P1_y), (P1_x + AR_x + R_pitch + G_pitch + AR_pitch, P1_y), (P1_x + AR_x - d_AR_x + R_pitch + G_pitch + AR_pitch, P1_y + AR_y), (P1_x - d_AR_x + R_pitch + G_pitch + AR_pitch, P1_y + AR_y), (P1_x + R_pitch + G_pitch + AR_pitch, P1_y)])

    P7 = Polygon([(P1_x - d_AR_x, P1_y + pix_y), (P1_x - d_AR_x + AR_x, P1_y + pix_y), (P1_x + AR_x, P1_y + AR_y + pix_y), (P1_x, P1_y + AR_y + pix_y), (P1_x - d_AR_x, P1_y + pix_y)])
    P8 = Polygon([(P1_x - d_AR_x + R_pitch, P1_y + pix_y), (P1_x - d_AR_x + R_pitch + AR_x, P1_y + pix_y), (P1_x + AR_x + R_pitch, P1_y + AR_y + pix_y), (P1_x + R_pitch, P1_y + AR_y + pix_y), (P1_x - d_AR_x + R_pitch, P1_y + pix_y)])
    P9 = Polygon([(P1_x - d_AR_x + R_pitch + G_pitch, P1_y + pix_y), (P1_x - d_AR_x + AR_x + R_pitch + G_pitch, P1_y + pix_y), (P1_x + AR_x + R_pitch + G_pitch, P1_y + AR_y + pix_y), (P1_x + R_pitch + G_pitch, P1_y + AR_y + pix_y), (P1_x - d_AR_x + R_pitch + G_pitch, P1_y + pix_y)])
    P10 = Polygon([(P1_x - d_AR_x + AR_pitch, P1_y + pix_y), (P1_x - d_AR_x + AR_x + AR_pitch, P1_y + pix_y), (P1_x + AR_x + AR_pitch, P1_y + AR_y + pix_y), (P1_x + AR_pitch, P1_y + AR_y + pix_y), (P1_x - d_AR_x + AR_pitch, P1_y + pix_y)])
    P11 = Polygon([(P1_x - d_AR_x + R_pitch + AR_pitch, P1_y + pix_y), (P1_x - d_AR_x + AR_x + R_pitch + AR_pitch, P1_y + pix_y), (P1_x + AR_x + R_pitch + AR_pitch, P1_y + AR_y + pix_y), (P1_x + R_pitch + AR_pitch, P1_y + AR_y + pix_y), (P1_x - d_AR_x + R_pitch + AR_pitch, P1_y + pix_y)])
    P12 = Polygon([(P1_x - d_AR_x + R_pitch + G_pitch + AR_pitch, P1_y + pix_y), (P1_x - d_AR_x + AR_x + R_pitch + G_pitch + AR_pitch, P1_y + pix_y), (P1_x + AR_x + R_pitch + G_pitch + AR_pitch, P1_y + AR_y + pix_y), (P1_x + R_pitch + G_pitch + AR_pitch, P1_y + AR_y + pix_y), (P1_x - d_AR_x + R_pitch + G_pitch + AR_pitch, P1_y + pix_y)])
    # print(AR_x)

    # print(list(P1.exterior.coords))
    # print(list(P2.exterior.coords))
    # print(list(P3.exterior.coords))
    # print(list(P4.exterior.coords))
    # print(list(P5.exterior.coords))
    # print(list(P6.exterior.coords))
    # print(list(P7.exterior.coords))
    # print(list(P8.exterior.coords))
    # print(list(P9.exterior.coords))
    # print(list(P10.exterior.coords))
    # print(list(P11.exterior.coords))
    # print(list(P12.exterior.coords))


    # # # # # # 根据PS size，绘制所有PS
    if ps == 1:
        HPS_x = -1 * BM_Gate / 2 * math.tan(angle / 180 * math.pi)  # 计算HPS中心坐标
        HPS_y = 0
        VPS_x = HPS_x
        VPS_y = HPS_y
        d_pix_x = pix_y * math.tan(angle / 180 * math.pi) - 2 * BM_Gate / 2 * math.tan(angle / 180 * math.pi)  # 以Gate BM为中心点
    elif ps == 2:
        HPS_x = -1 * (hps_y / 2 + hps_BM) * math.tan(angle / 180 * math.pi)  # 计算HPS中心坐标
        HPS_y = 0
        VPS_x = HPS_x
        VPS_y = HPS_y
        d_pix_x = pix_y * math.tan(angle / 180 * math.pi) - 2 * (hps_y / 2 + hps_BM) * math.tan(angle / 180 * math.pi)  # 以HPS + BM补偿后为中心点
    
    # HPS_x = -1 * BM_Gate / 2 * math.tan(angle / 180 * math.pi)  # 计算HPS中心坐标
    # HPS_y = 0
    # VPS_x = HPS_x
    # VPS_y = HPS_y
    # d_pix_x = pix_y * math.tan(angle / 180 * math.pi) - 2 * BM_Gate / 2 * math.tan(angle / 180 * math.pi)  # 以Gate BM为中心点
    

    # 计算第一个HPS的坐标点
    min_HPS_BM = hps_y / 2 + hps_BM  # HPS绘制step1

    HPS1_x = HPS_x - min_HPS_BM * math.tan(22.5 / 180 * math.pi) - (hps_x - hps_y) / 2
    HPS1_y = -1 * (hps_y / 2 + hps_BM)
    HPS2_x = HPS_x + min_HPS_BM * math.tan(22.5 / 180 * math.pi) + (hps_x - hps_y) / 2
    HPS2_y = HPS1_y
    HPS3_x = hps_x / 2 + hps_BM + HPS_x
    HPS3_y = -1 * (min_HPS_BM * math.tan(22.5 / 180 * math.pi))
    HPS4_x = HPS3_x
    HPS4_y = -1 * HPS3_y
    HPS5_x = HPS2_x
    HPS5_y = -1 * HPS2_y
    HPS6_x = HPS1_x
    HPS6_y = -1 * HPS1_y
    HPS7_x = HPS_x - hps_x / 2 - hps_BM
    HPS7_y = HPS4_y
    HPS8_x = HPS7_x
    HPS8_y = -1 * HPS7_y

    # print(HPS_x, HPS_y, min_HPS_BM)

    # 绘制12个pixel的HPS
    HPS1 = Polygon([(HPS1_x, HPS1_y), (HPS2_x, HPS2_y), (HPS3_x, HPS3_y), (HPS4_x, HPS4_y), (HPS5_x, HPS5_y), (HPS6_x, HPS6_y), (HPS7_x, HPS7_y), (HPS8_x, HPS8_y), (HPS1_x, HPS1_y)])
    HPS2 = Polygon([(HPS1_x + PS_R_pitch, HPS1_y), (HPS2_x + PS_R_pitch, HPS2_y), (HPS3_x + PS_R_pitch, HPS3_y), (HPS4_x + PS_R_pitch, HPS4_y), (HPS5_x + PS_R_pitch, HPS5_y), (HPS6_x + PS_R_pitch, HPS6_y), (HPS7_x + pix_x, HPS7_y), (HPS8_x + PS_R_pitch, HPS8_y), (HPS1_x + PS_R_pitch, HPS1_y)])
    HPS3 = Polygon([(HPS1_x + PS_R_pitch + PS_G_pitch, HPS1_y), (HPS2_x + PS_R_pitch + PS_G_pitch, HPS2_y), (HPS3_x + PS_R_pitch + PS_G_pitch, HPS3_y), (HPS4_x + PS_R_pitch + PS_G_pitch, HPS4_y), (HPS5_x + PS_R_pitch + PS_G_pitch, HPS5_y), (HPS6_x + PS_R_pitch + PS_G_pitch, HPS6_y), (HPS7_x + PS_R_pitch + PS_G_pitch, HPS7_y), (HPS8_x + PS_R_pitch + PS_G_pitch, HPS8_y), (HPS1_x + PS_R_pitch + PS_G_pitch, HPS1_y)])
    HPS4 = Polygon([(HPS1_x + AR_pitch, HPS1_y), (HPS2_x + AR_pitch, HPS2_y), (HPS3_x + AR_pitch, HPS3_y), (HPS4_x + AR_pitch, HPS4_y), (HPS5_x + AR_pitch, HPS5_y), (HPS6_x + AR_pitch, HPS6_y), (HPS7_x + AR_pitch, HPS7_y), (HPS8_x + AR_pitch, HPS8_y), (HPS1_x + AR_pitch, HPS1_y)])
    HPS5 = Polygon([(HPS1_x + AR_pitch + PS_R_pitch, HPS1_y), (HPS2_x + AR_pitch + PS_R_pitch, HPS2_y), (HPS3_x + AR_pitch + PS_R_pitch, HPS3_y), (HPS4_x + AR_pitch + PS_R_pitch, HPS4_y), (HPS5_x + AR_pitch + PS_R_pitch, HPS5_y), (HPS6_x + AR_pitch + PS_R_pitch, HPS6_y), (HPS7_x + AR_pitch + PS_R_pitch, HPS7_y), (HPS8_x + AR_pitch + PS_R_pitch, HPS8_y), (HPS1_x + AR_pitch + PS_R_pitch, HPS1_y)])
    HPS6 = Polygon([(HPS1_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS1_y), (HPS2_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS2_y), (HPS3_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS3_y), (HPS4_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS4_y), (HPS5_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS5_y), (HPS6_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS6_y), (HPS7_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS7_y), (HPS8_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS8_y), (HPS1_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS1_y)])
    HPS7 = Polygon([(HPS1_x + AR_pitch * 2, HPS1_y), (HPS2_x + AR_pitch * 2, HPS2_y), (HPS3_x + AR_pitch * 2, HPS3_y), (HPS4_x + AR_pitch * 2, HPS4_y), (HPS5_x + AR_pitch * 2, HPS5_y), (HPS6_x + AR_pitch * 2, HPS6_y), (HPS7_x + AR_pitch * 2, HPS7_y), (HPS8_x + AR_pitch * 2, HPS8_y), (HPS1_x + AR_pitch * 2, HPS1_y)])

    HPS8 = Polygon([(HPS1_x - d_pix_x, HPS1_y + pix_y), (HPS2_x - d_pix_x, HPS2_y + pix_y), (HPS3_x - d_pix_x, HPS3_y + pix_y), (HPS4_x - d_pix_x, HPS4_y + pix_y), (HPS5_x - d_pix_x, HPS5_y + pix_y), (HPS6_x - d_pix_x, HPS6_y + pix_y), (HPS7_x - d_pix_x, HPS7_y + pix_y), (HPS8_x - d_pix_x, HPS8_y + pix_y), (HPS1_x - d_pix_x, HPS1_y + pix_y)])
    HPS9 = Polygon([(HPS1_x + PS_R_pitch - d_pix_x, HPS1_y + pix_y), (HPS2_x + PS_R_pitch - d_pix_x, HPS2_y + pix_y), (HPS3_x + PS_R_pitch - d_pix_x, HPS3_y + pix_y), (HPS4_x + PS_R_pitch - d_pix_x, HPS4_y + pix_y), (HPS5_x + PS_R_pitch - d_pix_x, HPS5_y + pix_y), (HPS6_x + PS_R_pitch - d_pix_x, HPS6_y + pix_y), (HPS7_x + PS_R_pitch - d_pix_x, HPS7_y + pix_y), (HPS8_x + PS_R_pitch - d_pix_x, HPS8_y + pix_y), (HPS1_x + PS_R_pitch - d_pix_x, HPS1_y + pix_y)])
    HPS10 = Polygon([(HPS1_x + PS_R_pitch + PS_G_pitch - d_pix_x, HPS1_y + pix_y), (HPS2_x + PS_R_pitch + PS_G_pitch - d_pix_x, HPS2_y + pix_y), (HPS3_x + PS_R_pitch + PS_G_pitch - d_pix_x, HPS3_y + pix_y), (HPS4_x + PS_R_pitch + PS_G_pitch - d_pix_x, HPS4_y + pix_y), (HPS5_x + PS_R_pitch + PS_G_pitch - d_pix_x, HPS5_y + pix_y), (HPS6_x + PS_R_pitch + PS_G_pitch - d_pix_x, HPS6_y + pix_y), (HPS7_x + PS_R_pitch + PS_G_pitch - d_pix_x, HPS7_y + pix_y), (HPS8_x + PS_R_pitch + PS_G_pitch - d_pix_x, HPS8_y + pix_y), (HPS1_x + PS_R_pitch + PS_G_pitch - d_pix_x, HPS1_y + pix_y)])
    HPS11 = Polygon([(HPS1_x + AR_pitch - d_pix_x, HPS1_y + pix_y), (HPS2_x + AR_pitch - d_pix_x, HPS2_y + pix_y), (HPS3_x + AR_pitch - d_pix_x, HPS3_y + pix_y), (HPS4_x + AR_pitch - d_pix_x, HPS4_y + pix_y), (HPS5_x + AR_pitch - d_pix_x, HPS5_y + pix_y), (HPS6_x + AR_pitch - d_pix_x, HPS6_y + pix_y), (HPS7_x + AR_pitch - d_pix_x, HPS7_y + pix_y), (HPS8_x + AR_pitch - d_pix_x, HPS8_y + pix_y), (HPS1_x + AR_pitch - d_pix_x, HPS1_y + pix_y)])
    HPS12 = Polygon([(HPS1_x + AR_pitch + PS_R_pitch - d_pix_x, HPS1_y + pix_y), (HPS2_x + AR_pitch + PS_R_pitch - d_pix_x, HPS2_y + pix_y), (HPS3_x + AR_pitch + PS_R_pitch - d_pix_x, HPS3_y + pix_y), (HPS4_x + AR_pitch + PS_R_pitch - d_pix_x, HPS4_y + pix_y), (HPS5_x + AR_pitch + PS_R_pitch - d_pix_x, HPS5_y + pix_y), (HPS6_x + AR_pitch + PS_R_pitch - d_pix_x, HPS6_y + pix_y), (HPS7_x + AR_pitch + PS_R_pitch - d_pix_x, HPS7_y + pix_y), (HPS8_x + AR_pitch + PS_R_pitch - d_pix_x, HPS8_y + pix_y), (HPS1_x + AR_pitch + PS_R_pitch - d_pix_x, HPS1_y + pix_y)])
    HPS13 = Polygon([(HPS1_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, HPS1_y + pix_y), (HPS2_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, HPS2_y + pix_y), (HPS3_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, HPS3_y + pix_y), (HPS4_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, HPS4_y + pix_y), (HPS5_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, HPS5_y + pix_y), (HPS6_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, HPS6_y + pix_y), (HPS7_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, HPS7_y + pix_y), (HPS8_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, HPS8_y + pix_y), (HPS1_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, HPS1_y + pix_y)])
    HPS14 = Polygon([(HPS1_x + AR_pitch * 2 - d_pix_x, HPS1_y + pix_y), (HPS2_x + AR_pitch * 2 - d_pix_x, HPS2_y + pix_y), (HPS3_x + AR_pitch * 2 - d_pix_x, HPS3_y + pix_y), (HPS4_x + AR_pitch * 2 - d_pix_x, HPS4_y + pix_y), (HPS5_x + AR_pitch * 2 - d_pix_x, HPS5_y + pix_y), (HPS6_x + AR_pitch * 2 - d_pix_x, HPS6_y + pix_y), (HPS7_x + AR_pitch * 2 - d_pix_x, HPS7_y + pix_y), (HPS8_x + AR_pitch * 2 - d_pix_x, HPS8_y + pix_y), (HPS1_x + AR_pitch * 2 - d_pix_x, HPS1_y + pix_y)])

    HPS15 = Polygon([(HPS1_x, HPS1_y + pix_y * 2), (HPS2_x, HPS2_y + pix_y * 2), (HPS3_x, HPS3_y + pix_y * 2), (HPS4_x, HPS4_y + pix_y * 2), (HPS5_x, HPS5_y + pix_y * 2), (HPS6_x, HPS6_y + pix_y * 2), (HPS7_x, HPS7_y + pix_y * 2), (HPS8_x, HPS8_y + pix_y * 2), (HPS1_x, HPS1_y + pix_y * 2)])
    HPS16 = Polygon([(HPS1_x + PS_R_pitch, HPS1_y + pix_y * 2), (HPS2_x + PS_R_pitch, HPS2_y + pix_y * 2), (HPS3_x + PS_R_pitch, HPS3_y + pix_y * 2), (HPS4_x + PS_R_pitch, HPS4_y + pix_y * 2), (HPS5_x + PS_R_pitch, HPS5_y + pix_y * 2), (HPS6_x + PS_R_pitch, HPS6_y + pix_y * 2), (HPS7_x + PS_R_pitch, HPS7_y + pix_y * 2), (HPS8_x + PS_R_pitch, HPS8_y + pix_y * 2), (HPS1_x + PS_R_pitch, HPS1_y + pix_y * 2)])
    HPS17 = Polygon([(HPS1_x + PS_R_pitch + PS_G_pitch, HPS1_y + pix_y * 2), (HPS2_x + PS_R_pitch + PS_G_pitch, HPS2_y + pix_y * 2), (HPS3_x + PS_R_pitch + PS_G_pitch, HPS3_y + pix_y * 2), (HPS4_x + PS_R_pitch + PS_G_pitch, HPS4_y + pix_y * 2), (HPS5_x + PS_R_pitch + PS_G_pitch, HPS5_y + pix_y * 2), (HPS6_x + PS_R_pitch + PS_G_pitch, HPS6_y + pix_y * 2), (HPS7_x + PS_R_pitch + PS_G_pitch, HPS7_y + pix_y * 2), (HPS8_x + PS_R_pitch + PS_G_pitch, HPS8_y + pix_y * 2), (HPS1_x + PS_R_pitch + PS_G_pitch, HPS1_y + pix_y * 2)])
    HPS18 = Polygon([(HPS1_x + AR_pitch, HPS1_y + pix_y * 2), (HPS2_x + AR_pitch, HPS2_y + pix_y * 2), (HPS3_x + AR_pitch, HPS3_y + pix_y * 2), (HPS4_x + AR_pitch, HPS4_y + pix_y * 2), (HPS5_x + AR_pitch, HPS5_y + pix_y * 2), (HPS6_x + AR_pitch, HPS6_y + pix_y * 2), (HPS7_x + AR_pitch, HPS7_y + pix_y * 2), (HPS8_x + AR_pitch, HPS8_y + pix_y * 2), (HPS1_x + AR_pitch, HPS1_y + pix_y * 2)])
    HPS19 = Polygon([(HPS1_x + AR_pitch + PS_R_pitch, HPS1_y + pix_y * 2), (HPS2_x + AR_pitch + PS_R_pitch, HPS2_y + pix_y * 2), (HPS3_x + AR_pitch + PS_R_pitch, HPS3_y + pix_y * 2), (HPS4_x + AR_pitch + PS_R_pitch, HPS4_y + pix_y * 2), (HPS5_x + AR_pitch + PS_R_pitch, HPS5_y + pix_y * 2), (HPS6_x + AR_pitch + PS_R_pitch, HPS6_y + pix_y * 2), (HPS7_x + AR_pitch + PS_R_pitch, HPS7_y + pix_y * 2), (HPS8_x + AR_pitch + PS_R_pitch, HPS8_y + pix_y * 2), (HPS1_x + AR_pitch + PS_R_pitch, HPS1_y + pix_y * 2)])
    HPS20 = Polygon([(HPS1_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS1_y + pix_y * 2), (HPS2_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS2_y + pix_y * 2), (HPS3_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS3_y + pix_y * 2), (HPS4_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS4_y + pix_y * 2), (HPS5_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS5_y + pix_y * 2), (HPS6_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS6_y + pix_y * 2), (HPS7_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS7_y + pix_y * 2), (HPS8_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS8_y + pix_y * 2), (HPS1_x + AR_pitch + PS_R_pitch + PS_G_pitch, HPS1_y + pix_y * 2)])
    HPS21 = Polygon([(HPS1_x + AR_pitch * 2, HPS1_y + pix_y * 2), (HPS2_x + AR_pitch * 2, HPS2_y + pix_y * 2), (HPS3_x + AR_pitch * 2, HPS3_y + pix_y * 2), (HPS4_x + AR_pitch * 2, HPS4_y + pix_y * 2), (HPS5_x + AR_pitch * 2, HPS5_y + pix_y * 2), (HPS6_x + AR_pitch * 2, HPS6_y + pix_y * 2), (HPS7_x + AR_pitch * 2, HPS7_y + pix_y * 2), (HPS8_x + AR_pitch * 2, HPS8_y + pix_y * 2), (HPS1_x + AR_pitch * 2, HPS1_y + pix_y * 2)])
    

    # print(list(HPS1.exterior.coords))
    # print(list(HPS2.exterior.coords))
    # print(list(HPS3.exterior.coords))
    # print(list(HPS8.exterior.coords))
    # print(list(HPS9.exterior.coords))

    # 计算第一个VPS的坐标点
    min_VPS_BM = vps_x / 2 + vps_BM  # VPS绘制step1

    VPS1_x = VPS_x - min_VPS_BM * math.tan(22.5 / 180 * math.pi)
    VPS1_y = -1 * (vps_y / 2 + vps_BM)
    VPS2_x = VPS_x + min_VPS_BM * math.tan(22.5 / 180 * math.pi)
    VPS2_y = VPS1_y
    VPS3_x = vps_x / 2 + vps_BM + VPS_x
    VPS3_y = -1 * (min_VPS_BM * math.tan(22.5 / 180 * math.pi)) - (vps_y - vps_x) / 2
    VPS4_x = VPS3_x
    VPS4_y = -1 * VPS3_y
    VPS5_x = VPS2_x
    VPS5_y = -1 * VPS2_y
    VPS6_x = VPS1_x
    VPS6_y = -1 * VPS1_y
    VPS7_x = VPS_x - vps_x / 2 - vps_BM
    VPS7_y = VPS4_y
    VPS8_x = VPS7_x
    VPS8_y = -1 * VPS7_y

    # 绘制12个pixel的VPS
    VPS1 = Polygon([(VPS1_x, VPS1_y), (VPS2_x, VPS2_y), (VPS3_x, VPS3_y), (VPS4_x, VPS4_y), (VPS5_x, VPS5_y), (VPS6_x, VPS6_y), (VPS7_x, VPS7_y), (VPS8_x, VPS8_y), (VPS1_x, VPS1_y)])
    VPS2 = Polygon([(VPS1_x + PS_R_pitch, VPS1_y), (VPS2_x + PS_R_pitch, VPS2_y), (VPS3_x + PS_R_pitch, VPS3_y), (VPS4_x + PS_R_pitch, VPS4_y), (VPS5_x + PS_R_pitch, VPS5_y), (VPS6_x + PS_R_pitch, VPS6_y), (VPS7_x + PS_R_pitch, VPS7_y), (VPS8_x + PS_R_pitch, VPS8_y), (VPS1_x + PS_R_pitch, VPS1_y)])
    VPS3 = Polygon([(VPS1_x + PS_R_pitch + PS_G_pitch, VPS1_y), (VPS2_x + PS_R_pitch + PS_G_pitch, VPS2_y), (VPS3_x + PS_R_pitch + PS_G_pitch, VPS3_y), (VPS4_x + PS_R_pitch + PS_G_pitch, VPS4_y), (VPS5_x + PS_R_pitch + PS_G_pitch, VPS5_y), (VPS6_x + PS_R_pitch + PS_G_pitch, VPS6_y), (VPS7_x + PS_R_pitch + PS_G_pitch, VPS7_y), (VPS8_x + PS_R_pitch + PS_G_pitch, VPS8_y), (VPS1_x + PS_R_pitch + PS_G_pitch, VPS1_y)])
    VPS4 = Polygon([(VPS1_x + AR_pitch, VPS1_y), (VPS2_x + AR_pitch, VPS2_y), (VPS3_x + AR_pitch, VPS3_y), (VPS4_x + AR_pitch, VPS4_y), (VPS5_x + AR_pitch, VPS5_y), (VPS6_x + AR_pitch, VPS6_y), (VPS7_x + AR_pitch, VPS7_y), (VPS8_x + AR_pitch, VPS8_y), (VPS1_x + AR_pitch, VPS1_y)])
    VPS5 = Polygon([(VPS1_x + AR_pitch + PS_R_pitch, VPS1_y), (VPS2_x + AR_pitch + PS_R_pitch, VPS2_y), (VPS3_x + AR_pitch + PS_R_pitch, VPS3_y), (VPS4_x + AR_pitch + PS_R_pitch, VPS4_y), (VPS5_x + AR_pitch + PS_R_pitch, VPS5_y), (VPS6_x + AR_pitch + PS_R_pitch, VPS6_y), (VPS7_x + AR_pitch + PS_R_pitch, VPS7_y), (VPS8_x + AR_pitch + PS_R_pitch, VPS8_y), (VPS1_x + AR_pitch + PS_R_pitch, VPS1_y)])
    VPS6 = Polygon([(VPS1_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS1_y), (VPS2_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS2_y), (VPS3_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS3_y), (VPS4_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS4_y), (VPS5_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS5_y), (VPS6_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS6_y), (VPS7_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS7_y), (VPS8_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS8_y), (VPS1_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS1_y)])
    VPS7 = Polygon([(VPS1_x + AR_pitch * 2, VPS1_y), (VPS2_x + AR_pitch * 2, VPS2_y), (VPS3_x + AR_pitch * 2, VPS3_y), (VPS4_x + AR_pitch * 2, VPS4_y), (VPS5_x + AR_pitch * 2, VPS5_y), (VPS6_x + AR_pitch * 2, VPS6_y), (VPS7_x + AR_pitch * 2, VPS7_y), (VPS8_x + AR_pitch * 2, VPS8_y), (VPS1_x + AR_pitch * 2, VPS1_y)])

    VPS8 = Polygon([(VPS1_x - d_pix_x, VPS1_y + pix_y), (VPS2_x - d_pix_x, VPS2_y + pix_y), (VPS3_x - d_pix_x, VPS3_y + pix_y), (VPS4_x - d_pix_x, VPS4_y + pix_y), (VPS5_x - d_pix_x, VPS5_y + pix_y), (VPS6_x - d_pix_x, VPS6_y + pix_y), (VPS7_x - d_pix_x, VPS7_y + pix_y), (VPS8_x - d_pix_x, VPS8_y + pix_y), (VPS1_x - d_pix_x, VPS1_y + pix_y)])
    VPS9 = Polygon([(VPS1_x + PS_R_pitch - d_pix_x, VPS1_y + pix_y), (VPS2_x + PS_R_pitch - d_pix_x, VPS2_y + pix_y), (VPS3_x + PS_R_pitch - d_pix_x, VPS3_y + pix_y), (VPS4_x + PS_R_pitch - d_pix_x, VPS4_y + pix_y), (VPS5_x + PS_R_pitch - d_pix_x, VPS5_y + pix_y), (VPS6_x + PS_R_pitch - d_pix_x, VPS6_y + pix_y), (VPS7_x + PS_R_pitch - d_pix_x, VPS7_y + pix_y), (VPS8_x + PS_R_pitch - d_pix_x, VPS8_y + pix_y), (VPS1_x + PS_R_pitch - d_pix_x, VPS1_y + pix_y)])
    VPS10 = Polygon([(VPS1_x + PS_R_pitch + PS_G_pitch - d_pix_x, VPS1_y + pix_y), (VPS2_x + PS_R_pitch + PS_G_pitch - d_pix_x, VPS2_y + pix_y), (VPS3_x + PS_R_pitch + PS_G_pitch - d_pix_x, VPS3_y + pix_y), (VPS4_x + PS_R_pitch + PS_G_pitch - d_pix_x, VPS4_y + pix_y), (VPS5_x + PS_R_pitch + PS_G_pitch - d_pix_x, VPS5_y + pix_y), (VPS6_x + PS_R_pitch + PS_G_pitch - d_pix_x, VPS6_y + pix_y), (VPS7_x + PS_R_pitch + PS_G_pitch - d_pix_x, VPS7_y + pix_y), (VPS8_x + PS_R_pitch + PS_G_pitch - d_pix_x, VPS8_y + pix_y), (VPS1_x + PS_R_pitch + PS_G_pitch - d_pix_x, VPS1_y + pix_y)])
    VPS11 = Polygon([(VPS1_x + AR_pitch - d_pix_x, VPS1_y + pix_y), (VPS2_x + AR_pitch - d_pix_x, VPS2_y + pix_y), (VPS3_x + AR_pitch - d_pix_x, VPS3_y + pix_y), (VPS4_x + AR_pitch - d_pix_x, VPS4_y + pix_y), (VPS5_x + AR_pitch - d_pix_x, VPS5_y + pix_y), (VPS6_x + AR_pitch - d_pix_x, VPS6_y + pix_y), (VPS7_x + AR_pitch - d_pix_x, VPS7_y + pix_y), (VPS8_x + AR_pitch - d_pix_x, VPS8_y + pix_y), (VPS1_x + AR_pitch - d_pix_x, VPS1_y + pix_y)])
    VPS12 = Polygon([(VPS1_x + AR_pitch + PS_R_pitch - d_pix_x, VPS1_y + pix_y), (VPS2_x + AR_pitch + PS_R_pitch - d_pix_x, VPS2_y + pix_y), (VPS3_x + AR_pitch + PS_R_pitch - d_pix_x, VPS3_y + pix_y), (VPS4_x + AR_pitch + PS_R_pitch - d_pix_x, VPS4_y + pix_y), (VPS5_x + AR_pitch + PS_R_pitch - d_pix_x, VPS5_y + pix_y), (VPS6_x + AR_pitch + PS_R_pitch - d_pix_x, VPS6_y + pix_y), (VPS7_x + AR_pitch + PS_R_pitch - d_pix_x, VPS7_y + pix_y), (VPS8_x + AR_pitch + PS_R_pitch - d_pix_x, VPS8_y + pix_y), (VPS1_x + AR_pitch + PS_R_pitch - d_pix_x, VPS1_y + pix_y)])
    VPS13 = Polygon([(VPS1_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, VPS1_y + pix_y), (VPS2_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, VPS2_y + pix_y), (VPS3_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, VPS3_y + pix_y), (VPS4_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, VPS4_y + pix_y), (VPS5_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, VPS5_y + pix_y), (VPS6_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, VPS6_y + pix_y), (VPS7_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, VPS7_y + pix_y), (VPS8_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, VPS8_y + pix_y), (VPS1_x + AR_pitch + PS_R_pitch + PS_G_pitch - d_pix_x, VPS1_y + pix_y)])
    VPS14 = Polygon([(VPS1_x + AR_pitch * 2 - d_pix_x, VPS1_y + pix_y), (VPS2_x + AR_pitch * 2 - d_pix_x, VPS2_y + pix_y), (VPS3_x + AR_pitch * 2 - d_pix_x, VPS3_y + pix_y), (VPS4_x + AR_pitch * 2 - d_pix_x, VPS4_y + pix_y), (VPS5_x + AR_pitch * 2 - d_pix_x, VPS5_y + pix_y), (VPS6_x + AR_pitch * 2 - d_pix_x, VPS6_y + pix_y), (VPS7_x + AR_pitch * 2 - d_pix_x, VPS7_y + pix_y), (VPS8_x + AR_pitch * 2 - d_pix_x, VPS8_y + pix_y), (VPS1_x + AR_pitch * 2 - d_pix_x, VPS1_y + pix_y)])

    VPS15 = Polygon([(VPS1_x, VPS1_y + pix_y * 2), (VPS2_x, VPS2_y + pix_y * 2), (VPS3_x, VPS3_y + pix_y * 2), (VPS4_x, VPS4_y + pix_y * 2), (VPS5_x, VPS5_y + pix_y * 2), (VPS6_x, VPS6_y + pix_y * 2), (VPS7_x, VPS7_y + pix_y * 2), (VPS8_x, VPS8_y + pix_y * 2), (VPS1_x, VPS1_y + pix_y * 2)])
    VPS16 = Polygon([(VPS1_x + PS_R_pitch, VPS1_y + pix_y * 2), (VPS2_x + PS_R_pitch, VPS2_y + pix_y * 2), (VPS3_x + PS_R_pitch, VPS3_y + pix_y * 2), (VPS4_x + PS_R_pitch, VPS4_y + pix_y * 2), (VPS5_x + PS_R_pitch, VPS5_y + pix_y * 2), (VPS6_x + PS_R_pitch, VPS6_y + pix_y * 2), (VPS7_x + PS_R_pitch, VPS7_y + pix_y * 2), (VPS8_x + PS_R_pitch, VPS8_y + pix_y * 2), (VPS1_x + PS_R_pitch, VPS1_y + pix_y * 2)])
    VPS17 = Polygon([(VPS1_x + PS_R_pitch + PS_G_pitch, VPS1_y + pix_y * 2), (VPS2_x + PS_R_pitch + PS_G_pitch, VPS2_y + pix_y * 2), (VPS3_x + PS_R_pitch + PS_G_pitch, VPS3_y + pix_y * 2), (VPS4_x + PS_R_pitch + PS_G_pitch, VPS4_y + pix_y * 2), (VPS5_x + PS_R_pitch + PS_G_pitch, VPS5_y + pix_y * 2), (VPS6_x + PS_R_pitch + PS_G_pitch, VPS6_y + pix_y * 2), (VPS7_x + PS_R_pitch + PS_G_pitch, VPS7_y + pix_y * 2), (VPS8_x + PS_R_pitch + PS_G_pitch, VPS8_y + pix_y * 2), (VPS1_x + PS_R_pitch + PS_G_pitch, VPS1_y + pix_y * 2)])
    VPS18 = Polygon([(VPS1_x + AR_pitch, VPS1_y + pix_y * 2), (VPS2_x + AR_pitch, VPS2_y + pix_y * 2), (VPS3_x + AR_pitch, VPS3_y + pix_y * 2), (VPS4_x + AR_pitch, VPS4_y + pix_y * 2), (VPS5_x + AR_pitch, VPS5_y + pix_y * 2), (VPS6_x + AR_pitch, VPS6_y + pix_y * 2), (VPS7_x + AR_pitch, VPS7_y + pix_y * 2), (VPS8_x + AR_pitch, VPS8_y + pix_y * 2), (VPS1_x + AR_pitch, VPS1_y + pix_y * 2)])
    VPS19 = Polygon([(VPS1_x + AR_pitch + PS_R_pitch, VPS1_y + pix_y * 2), (VPS2_x + AR_pitch + PS_R_pitch, VPS2_y + pix_y * 2), (VPS3_x + AR_pitch + PS_R_pitch, VPS3_y + pix_y * 2), (VPS4_x + AR_pitch + PS_R_pitch, VPS4_y + pix_y * 2), (VPS5_x + AR_pitch + PS_R_pitch, VPS5_y + pix_y * 2), (VPS6_x + AR_pitch + PS_R_pitch, VPS6_y + pix_y * 2), (VPS7_x + AR_pitch + PS_R_pitch, VPS7_y + pix_y * 2), (VPS8_x + AR_pitch + PS_R_pitch, VPS8_y + pix_y * 2), (VPS1_x + AR_pitch + PS_R_pitch, VPS1_y + pix_y * 2)])
    VPS20 = Polygon([(VPS1_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS1_y + pix_y * 2), (VPS2_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS2_y + pix_y * 2), (VPS3_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS3_y + pix_y * 2), (VPS4_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS4_y + pix_y * 2), (VPS5_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS5_y + pix_y * 2), (VPS6_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS6_y + pix_y * 2), (VPS7_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS7_y + pix_y * 2), (VPS8_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS8_y + pix_y * 2), (VPS1_x + AR_pitch + PS_R_pitch + PS_G_pitch, VPS1_y + pix_y * 2)])
    VPS21 = Polygon([(VPS1_x + AR_pitch * 2, VPS1_y + pix_y * 2), (VPS2_x + AR_pitch * 2, VPS2_y + pix_y * 2), (VPS3_x + AR_pitch * 2, VPS3_y + pix_y * 2), (VPS4_x + AR_pitch * 2, VPS4_y + pix_y * 2), (VPS5_x + AR_pitch * 2, VPS5_y + pix_y * 2), (VPS6_x + AR_pitch * 2, VPS6_y + pix_y * 2), (VPS7_x + AR_pitch * 2, VPS7_y + pix_y * 2), (VPS8_x + AR_pitch * 2, VPS8_y + pix_y * 2), (VPS1_x + AR_pitch * 2, VPS1_y + pix_y * 2)])

    # # # # # # 绘制12个像素的TX走线
    delta_x = pix_y / 2 * math.tan(angle / 180 * math.pi)
    TX1 = Polygon([(PS_R_pitch / 2 - delta_x - TX_CD / 2, 0), (PS_R_pitch / 2 - delta_x + TX_CD / 2, 0), (PS_R_pitch / 2 - delta_x + TX_CD / 2, pix_y * 2), (PS_R_pitch / 2 - delta_x - TX_CD / 2, pix_y * 2), (PS_R_pitch / 2 - delta_x - TX_CD / 2, 0)])
    TX2 = Polygon([(PS_R_pitch / 2 - delta_x - TX_CD / 2 + PS_R_pitch, 0), (PS_R_pitch / 2 - delta_x + TX_CD / 2 + PS_R_pitch, 0), (PS_R_pitch / 2 - delta_x + TX_CD / 2 + PS_R_pitch, pix_y * 2), (PS_R_pitch / 2 - delta_x - TX_CD / 2 + PS_R_pitch, pix_y * 2), (PS_R_pitch / 2 - delta_x - TX_CD / 2 + PS_R_pitch, 0)])
    TX3 = Polygon([(PS_R_pitch / 2 - delta_x - TX_CD / 2 + PS_R_pitch + PS_G_pitch, 0), (PS_R_pitch / 2 - delta_x + TX_CD / 2 + PS_R_pitch + PS_G_pitch, 0), (PS_R_pitch / 2 - delta_x + TX_CD / 2 + PS_R_pitch + PS_G_pitch, pix_y * 2), (PS_R_pitch / 2 - delta_x - TX_CD / 2 + PS_R_pitch + PS_G_pitch, pix_y * 2), (PS_R_pitch / 2 - delta_x - TX_CD / 2 + PS_R_pitch + PS_G_pitch, 0)])
    TX4 = Polygon([(PS_R_pitch / 2 - delta_x - TX_CD / 2 + AR_pitch, 0), (PS_R_pitch / 2 - delta_x + TX_CD / 2 + AR_pitch, 0), (PS_R_pitch / 2 - delta_x + TX_CD / 2 + AR_pitch, pix_y * 2), (PS_R_pitch / 2 - delta_x - TX_CD / 2 + AR_pitch, pix_y * 2), (PS_R_pitch / 2 - delta_x - TX_CD / 2 + AR_pitch, 0)])
    TX5 = Polygon([(PS_R_pitch / 2 - delta_x - TX_CD / 2 + AR_pitch + PS_R_pitch, 0), (PS_R_pitch / 2 - delta_x + TX_CD / 2 + AR_pitch + PS_R_pitch, 0), (PS_R_pitch / 2 - delta_x + TX_CD / 2 + AR_pitch + PS_R_pitch, pix_y * 2), (PS_R_pitch / 2 - delta_x - TX_CD / 2 + AR_pitch + PS_R_pitch, pix_y * 2), (PS_R_pitch / 2 - delta_x - TX_CD / 2 + AR_pitch + PS_R_pitch, 0)])
    TX6 = Polygon([(PS_R_pitch / 2 - delta_x - TX_CD / 2 + AR_pitch + PS_R_pitch + PS_G_pitch, 0), (PS_R_pitch / 2 - delta_x + TX_CD / 2 + AR_pitch + PS_R_pitch + PS_G_pitch, 0), (PS_R_pitch / 2 - delta_x + TX_CD / 2 + AR_pitch + PS_R_pitch + PS_G_pitch, pix_y * 2), (PS_R_pitch / 2 - delta_x - TX_CD / 2 + AR_pitch + PS_R_pitch + PS_G_pitch, pix_y * 2), (PS_R_pitch / 2 - delta_x - TX_CD / 2 + AR_pitch + PS_R_pitch + PS_G_pitch, 0)])

    # # # # # # 绘制12个像素的TX走线
    delta_x = pix_y / 2 * math.tan(angle / 180 * math.pi)
    TX1 = Polygon([(pix_x / 2 - delta_x - TX_CD / 2, 0), (pix_x / 2 - delta_x + TX_CD / 2, 0), (pix_x / 2 - delta_x + TX_CD / 2, pix_y * 2), (pix_x / 2 - delta_x - TX_CD / 2, pix_y * 2), (pix_x / 2 - delta_x - TX_CD / 2, 0)])
    TX2 = Polygon([(pix_x / 2 - delta_x - TX_CD / 2 + pix_x, 0), (pix_x / 2 - delta_x + TX_CD / 2 + pix_x, 0), (pix_x / 2 - delta_x + TX_CD / 2 + pix_x, pix_y * 2), (pix_x / 2 - delta_x - TX_CD / 2 + pix_x, pix_y * 2), (pix_x / 2 - delta_x - TX_CD / 2 + pix_x, 0)])
    TX3 = Polygon([(pix_x / 2 - delta_x - TX_CD / 2 + pix_x * 2, 0), (pix_x / 2 - delta_x + TX_CD / 2 + pix_x * 2, 0), (pix_x / 2 - delta_x + TX_CD / 2 + pix_x * 2, pix_y * 2), (pix_x / 2 - delta_x - TX_CD / 2 + pix_x * 2, pix_y * 2), (pix_x / 2 - delta_x - TX_CD / 2 + pix_x * 2, 0)])
    TX4 = Polygon([(pix_x / 2 - delta_x - TX_CD / 2 + pix_x * 3, 0), (pix_x / 2 - delta_x + TX_CD / 2 + pix_x * 3, 0), (pix_x / 2 - delta_x + TX_CD / 2 + pix_x * 3, pix_y * 2), (pix_x / 2 - delta_x - TX_CD / 2 + pix_x * 3, pix_y * 2), (pix_x / 2 - delta_x - TX_CD / 2 + pix_x * 3, 0)])
    TX5 = Polygon([(pix_x / 2 - delta_x - TX_CD / 2 + pix_x * 4, 0), (pix_x / 2 - delta_x + TX_CD / 2 + pix_x * 4, 0), (pix_x / 2 - delta_x + TX_CD / 2 + pix_x * 4, pix_y * 2), (pix_x / 2 - delta_x - TX_CD / 2 + pix_x * 4, pix_y * 2), (pix_x / 2 - delta_x - TX_CD / 2 + pix_x * 4, 0)])
    TX6 = Polygon([(pix_x / 2 - delta_x - TX_CD / 2 + pix_x * 5, 0), (pix_x / 2 - delta_x + TX_CD / 2 + pix_x * 5, 0), (pix_x / 2 - delta_x + TX_CD / 2 + pix_x * 5, pix_y * 2), (pix_x / 2 - delta_x - TX_CD / 2 + pix_x * 5, pix_y * 2), (pix_x / 2 - delta_x - TX_CD / 2 + pix_x * 5, 0)])


    # print(list(VPS1.exterior.coords))
    # print(list(VPS2.exterior.coords))
    # print(list(VPS3.exterior.coords))
    # print(list(VPS8.exterior.coords))
    # print(list(VPS9.exterior.coords))

    # # # # # # 计算12个pixel的开口率
    if density == 1:
        # pix1开口率
        area_pix1 = P1.difference(HPS1).difference(HPS2).difference(HPS8).difference(HPS9).difference(VPS1).difference(VPS2).difference(VPS8).difference(VPS9).difference(TX1).area / pix_x / pix_y
        # pix2开口率
        area_pix2 = P2.difference(HPS2).difference(HPS3).difference(HPS9).difference(HPS10).difference(VPS2).difference(VPS3).difference(VPS9).difference(VPS10).difference(TX2).area / pix_x / pix_y
        # pix3开口率
        area_pix3 = P3.difference(HPS3).difference(HPS4).difference(HPS10).difference(HPS11).difference(VPS3).difference(VPS4).difference(VPS10).difference(VPS11).difference(TX3).area / pix_x / pix_y
        # pix4开口率
        area_pix4 = P4.difference(HPS4).difference(HPS5).difference(HPS11).difference(HPS12).difference(VPS4).difference(VPS5).difference(VPS11).difference(VPS12).difference(TX4).area / pix_x / pix_y
        # pix5开口率
        area_pix5 = P5.difference(HPS5).difference(HPS6).difference(HPS12).difference(HPS13).difference(VPS5).difference(VPS6).difference(VPS12).difference(VPS13).difference(TX5).area / pix_x / pix_y
        # pix6开口率
        area_pix6 = P6.difference(HPS6).difference(HPS7).difference(HPS13).difference(HPS14).difference(VPS6).difference(VPS7).difference(VPS13).difference(VPS14).difference(TX6).area / pix_x / pix_y
        # pix7开口率
        area_pix7 = P7.difference(HPS8).difference(HPS9).difference(HPS15).difference(HPS16).difference(VPS8).difference(VPS9).difference(VPS15).difference(VPS16).difference(TX1).area / pix_x / pix_y
        # pix8开口率
        area_pix8 = P8.difference(HPS9).difference(HPS10).difference(HPS16).difference(HPS17).difference(VPS9).difference(VPS10).difference(VPS16).difference(VPS17).difference(TX2).area / pix_x / pix_y
        # pix9开口率
        area_pix9 = P9.difference(HPS10).difference(HPS11).difference(HPS17).difference(HPS18).difference(VPS10).difference(VPS11).difference(VPS17).difference(VPS18).difference(TX3).area / pix_x / pix_y
        # pix10开口率
        area_pix10 = P10.difference(HPS11).difference(HPS12).difference(HPS18).difference(HPS19).difference(VPS11).difference(VPS12).difference(VPS18).difference(VPS19).difference(TX4).area / pix_x / pix_y
        # pix11开口率
        area_pix11 = P11.difference(HPS12).difference(HPS13).difference(HPS19).difference(HPS20).difference(VPS12).difference(VPS13).difference(VPS19).difference(VPS20).difference(TX5).area / pix_x / pix_y
        # pix12开口率
        area_pix12 = P12.difference(HPS13).difference(HPS14).difference(HPS20).difference(HPS21).difference(VPS13).difference(VPS14).difference(VPS20).difference(VPS21).difference(TX6).area / pix_x / pix_y

    elif density == 2:
        # pix1开口率
        area_pix1 = P1.difference(HPS1).difference(HPS9).difference(VPS1).difference(VPS9).difference(TX1).area / pix_x / pix_y
        # pix2开口率
        area_pix2 = P2.difference(HPS9).difference(HPS3).difference(VPS9).difference(VPS3).difference(TX2).area / pix_x / pix_y
        # pix3开口率
        area_pix3 = P3.difference(HPS3).difference(HPS11).difference(VPS3).difference(VPS11).difference(TX3).area / pix_x / pix_y
        # pix4开口率
        area_pix4 = P4.difference(HPS11).difference(HPS5).difference(VPS11).difference(VPS5).difference(TX4).area / pix_x / pix_y
        # pix5开口率
        area_pix5 = P5.difference(HPS5).difference(HPS13).difference(VPS5).difference(VPS13).difference(TX5).area / pix_x / pix_y
        # pix6开口率
        area_pix6 = P6.difference(HPS13).difference(HPS7).difference(VPS13).difference(VPS7).difference(TX6).area / pix_x / pix_y
        # pix7开口率
        area_pix7 = P7.difference(HPS15).difference(HPS9).difference(VPS15).difference(VPS9).difference(TX1).area / pix_x / pix_y
        # pix8开口率
        area_pix8 = P8.difference(HPS9).difference(HPS17).difference(VPS9).difference(VPS17).difference(TX2).area / pix_x / pix_y
        # pix9开口率
        area_pix9 = P9.difference(HPS17).difference(HPS11).difference(VPS17).difference(VPS11).difference(TX3).area / pix_x / pix_y
        # pix10开口率
        area_pix10 = P10.difference(HPS11).difference(HPS19).difference(VPS11).difference(VPS19).difference(TX4).area / pix_x / pix_y
        # pix11开口率
        area_pix11 = P11.difference(HPS19).difference(HPS13).difference(VPS19).difference(VPS13).difference(TX5).area / pix_x / pix_y
        # pix12开口率
        area_pix12 = P12.difference(HPS13).difference(HPS21).difference(VPS13).difference(VPS21).difference(TX6).area / pix_x / pix_y

    area_pix1 = round(area_pix1, 4)
    area_pix2 = round(area_pix2, 4)
    area_pix3 = round(area_pix3, 4)
    area_pix4 = round(area_pix4, 4)
    area_pix5 = round(area_pix5, 4)
    area_pix6 = round(area_pix6, 4)
    area_pix7 = round(area_pix7, 4)
    area_pix8 = round(area_pix8, 4)
    area_pix9 = round(area_pix9, 4)
    area_pix10 = round(area_pix10, 4)
    area_pix11 = round(area_pix11, 4)
    area_pix12 = round(area_pix12, 4)
    # print(area_pix1, area_pix2, area_pix3, area_pix4, area_pix5, area_pix6)
    # print(area_pix7, area_pix8, area_pix9, area_pix10, area_pix11, area_pix12)

    area = np.zeros((12, 2), dtype=object)
    area[0, 0] = 'R11'
    area[1, 0] = 'G11'
    area[2, 0] = 'B11'
    area[3, 0] = 'R12'
    area[4, 0] = 'G12'
    area[5, 0] = 'B12'
    area[6, 0] = 'R21'
    area[7, 0] = 'G21'
    area[8, 0] = 'B21'
    area[9, 0] = 'R22'
    area[10, 0] = 'G22'
    area[11, 0] = 'B22'
    area[0, 1] = area_pix1
    area[1, 1] = area_pix2
    area[2, 1] = area_pix3
    area[3, 1] = area_pix4
    area[4, 1] = area_pix5
    area[5, 1] = area_pix6
    area[6, 1] = area_pix7
    area[7, 1] = area_pix8
    area[8, 1] = area_pix9
    area[9, 1] = area_pix10
    area[10, 1] = area_pix11
    area[11, 1] = area_pix12

    area = pd.DataFrame(area, columns=['像素', '开口率'])
    st.write(area)
