import numpy as np
import pandas as pd
import streamlit as st
import math
# st.balloons()  #过场动画

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

import numpy as np
from scipy.stats import norm

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具可以由Cpk数据计算概率分布</h4>", unsafe_allow_html=True)

# # # 工具名称、版本号
st.write("# Cpk计算概率分布工具 #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V2.0</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2024/01/28</h5>", unsafe_allow_html=True)

# # # 设置步骤1
st.write("<h6>请输入Cpk相关数据</h6>", unsafe_allow_html=True)

bz_1, bz_2, bz_3, bz_4 = st.columns([1, 6, 3, 10])
with bz_2:
    st.write('  ')
    st.write('输入规格下限')
with bz_3:
    lsl = st.number_input(label='tolerance', label_visibility='collapsed', format='%f', key=1)

with bz_2:
    st.write('  ')
    st.write('输入规格上限')
with bz_3:
    usl = st.number_input(label='tolerance', label_visibility='collapsed', format='%f', key=2)

with bz_2:
    st.write('  ')
    st.write('输入规格中心值')
with bz_3:
    sl = st.number_input(label='规格中心值', value=0.0, label_visibility='collapsed', format='%f', key=3)

with bz_2:
    st.write('  ')
    st.write('输入Cpk')
with bz_3:
    Cpk = st.number_input(label='Cpk', label_visibility='collapsed', format='%f', key=4)

with bz_2:
    st.write('  ')
    st.write('输入生成数据的step精度')
with bz_3:
    step = st.number_input(label='step', label_visibility='collapsed', format='%f', key=5)

# # #Main code
try:
    col3, col4 = st.columns([3, 5])
    col5, col6, col7, col8 = st.columns([1, 6, 20, 1])
    col15, col16 = st.columns([1, 26])
    with col3:
        if st.button('***点击计算概率分布***'):
            # 将使用者保存到txt文件中
            fp_save = 'users/网站使用者.txt'
            mode = 'a'
            with open(fp_save, mode) as f:
                f.write('使用了Cpk计算概率正态分布工具' + '\n')
            # 以下为主程序
            Cp = Cpk
            T = usl - lsl
            stedv = T / Cp / 6
            layer = int(math.ceil(T / step + 1))
            
            A = np.zeros((layer + 1, 2))
            B = np.zeros((layer, 2))

            for i in range(layer + 1):
                A[i, 0] = (i - 0.5) * step - T / 2 + sl
                A[i, 1] = norm.pdf(A[i, 0], sl, stedv)
            for i in range(layer):
                B[i, 0] = i * step - T / 2 + sl
                B[i, 1] = (A[i + 1, 1] + A[i, 1]) * (A[i + 1, 0] - A[i, 0]) / 2
            s = round(sum(B[:, 1]), 9)
            
            ccc = ['规格', '概率分布']
            df = pd.DataFrame(B, columns=ccc)
            with col6:
                st.write(B)
            with col16:
                st.write('规格内的总概率为', s)
            with col7:
                st.line_chart(df, x='规格', y='概率分布')
            

except ZeroDivisionError:
    c1, c2, c3 = st.columns([1, 5, 5])
    with c2:
        st.write(':red[请检查Cpk参数是否填写正确!]')
except ValueError:
    c1, c2, c3 = st.columns([1, 5, 5])
    with c2:
        st.write(':red[请检查规格上下限是否填写正确!]')
        
# 编辑button - Final计算
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(5) > div.st-emotion-cache-19pmq3u.e1f1d6gn3 > div > div > div > div > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px !important;
    width: 180px !important;
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
