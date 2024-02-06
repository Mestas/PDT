import numpy as np
import pandas as pd
import math
import streamlit as st
from PIL import Image
import os
from scipy.interpolate import interp1d

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具可以计算整数波长数据</h4>", unsafe_allow_html=True)

# # # 工具名称、版本号
st.write("# 整数波长转换工具 #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V1.0</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2024/02/02</h5>", unsafe_allow_html=True)

# # # 设置步骤1
st.write("<h6>步骤1：请选择加载需要转换的TXT文件(包含波长列和数据列)</h6>", unsafe_allow_html=True)

bz1_2, bz1_2 = st.columns([1, 25])
with bz1_2:
    fp_TXT = st.file_uploader("请上传txt文件(包含波长列和数据列)", type=['txt'], help="请选择TXT文件进行上传", accept_multiple_files=True, key='txt1')
    

# # # 设置步骤2
st.write("<h6>步骤2：请点击按钮生成所要转换的波长step</h6>", unsafe_allow_html=True)
# 创建button布局
col1, col2 = st.columns([1, 25])
col11, col12 = st.columns([1, 25])
with col2:
    cal_1nm = st.button('***点击计算1nm波长***', key='cal_1nm')
with col2:
    cal_5nm = st.button('***点击计算5nm波长***', key='cal_5nm')
with col2:
    if cal_1nm:
        if fp_TXT is not None:
            for fname in fp_TXT:
                fname1 = fname.name
                TXT0 = pd.read_csv(fname, header=None, sep="\t", skip_blank_lines=True)
                TXT = np.float64(TXT0)
                n = TXT.shape[1]
                x = TXT[:, 0]
                y = TXT[:, 1 : n]
                interpolators = [interp1d(x, yi) for yi in y.T] 
                wl = np.arange(380, 781, 1)
                wl_list = wl.tolist()
                y_new = [f(wl) for f in interpolators]
                transposed_y = list(map(list, zip(*y_new)))
                data = np.zeros((401, n))
                data[:, 0] = wl_list
                data[:, 1 : n] = transposed_y
                st.write('以下数据对应的文件名为：', fname1, data)

    elif cal_5nm:
        if fp_TXT is not None:
            for fname in fp_TXT:
                fname1 = fname.name
                TXT0 = pd.read_csv(fname, header=None, sep="\t", skip_blank_lines=True)
                TXT = np.float64(TXT0)
                n = TXT.shape[1]
                x = TXT[:, 0]
                y = TXT[:, 1 : n]
                interpolators = [interp1d(x, yi) for yi in y.T] 
                wl = np.arange(380, 785, 5)
                wl_list = wl.tolist()
                y_new = [f(wl) for f in interpolators]
                transposed_y = list(map(list, zip(*y_new)))
                data = np.zeros((81, n))
                data[:, 0] = wl_list
                data[:, 1 : n] = transposed_y
                st.write('以下数据对应的文件名为：', fname1, data)

# 编辑button - Final计算状态
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(6) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div:nth-child(1) > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px !important;
    width: 160px !important;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(6) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px !important;
    width: 160px !important;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(4) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    </style>
    ''',
    unsafe_allow_html=True
)
