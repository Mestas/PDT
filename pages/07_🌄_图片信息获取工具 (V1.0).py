import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time
import base64

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

# 侧边栏说明介绍
st.sidebar.write("<h4 style='color: blue;'>本工具可以读取bmp图片的多种信息</h4>", unsafe_allow_html=True)
# 工具名称、版本号
st.write("# PIC_Info工具 #")
cll1, cll2 = st.columns([2, 1])
with cll2:
    st.write("<h5 style='color: blue;'>版本号：V1.0</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2024/02/01</h5>", unsafe_allow_html=True)

# # # 设置步骤1
st.write("<h6>请上传bmp图片，并点击计算按钮</h6>", unsafe_allow_html=True)

# 上传图片，files为ByteIO的子类
files = st.file_uploader("请选择bmp图片文件", accept_multiple_files=True, type=['bmp'], help="请选择bmp图片进行上传，可同时选择多个图片")
start_time = time.time()
# 确认files中的文件数量，用于显示进度条总长度
m = len(files)

# 创建布局
col1, col2 = st.columns([1, 5])
col11, col12 = st.columns([3, 5])
col3, col4 = st.columns([1000, 1])
with col1:
    cal_button_trans = st.button('***点击计算透过率***', key='cal_button_trans')
with col1:
    cal_button_csv = st.button('***点击生成csv***', key='cal_button_csv')
with col1:
    cal_button_base64 = st.button('***点击生成base64***', key='cal_button_base64')

# # #主程序

if cal_button_trans:
    if m > 0:
        D1 = []
        D2 = []
        data = ""
        with col3:
            # 进度条创建
            pro = st.progress(0)
        n = 0
        for file in files:
            # 获取图片名称
            fname = file.name
            # 打开图片
            imgs = Image.open(file)
            # 转换为灰度图
            gray_imgs = imgs.convert("L")
            # 获取所有像素的灰阶数值
            h, l = gray_imgs.size
            Pixel_gray = np.zeros((h, l))
            for i in range(h):
                for j in range(l):
                    Pixel_gray[i, j] = gray_imgs.getpixel((i, j))
            # 将所有像素的灰阶数值计算为trans值
            Pixel_trans = (Pixel_gray / 255) ** 2.2
            Trans = np.mean(Pixel_trans)
            Trans = float(Trans)

            with col3:
                # 显示进度条
                n = n + 1
                d = n / m
                pro.progress(d)
            # 将数据整理到数组中
            D1.append(fname)
            D2.append(Trans)
            data = pd.DataFrame({'PIC_Name': D1, 'Trans': D2})

        with col3:
            # 在网页上显示运行时长
            if len(data) == 0:
                st.write()
            else:
                end_time = time.time()
                st.write("<h6 style='color: green;'>计算完成，请及时保存数据！</h6>", unsafe_allow_html=True)
                st.write("计算时长为", round(end_time - start_time, 2), "s")
        with col3:
            # 将数据在网页上显示
            st.write(data)
    else:
        with col3:
            st.write("<h6 style='color: red;'>请先加载bmp图片！</h6>", unsafe_allow_html=True)

    # 将使用者保存到txt文件中
    fp_save = 'users/网站使用者.txt'
    mode = 'a'
    with open(fp_save, mode) as f:
        f.write('使用了图片转透过率工具' + '\n')

elif cal_button_csv:
    start_time = time.time()
    if m > 0:
        data = []
        with col3:
            # 进度条创建
            pro = st.progress(0)
        n = 0
        for file in files:
            # 获取图片名称
            fname = file.name
            # 打开图片
            imgs = Image.open(file)
            # 转换为灰度图
            gray_imgs = imgs.convert("L")
            # 获取所有像素的灰阶数值
            h, l = gray_imgs.size
            Pixel_gray = np.zeros((h, l))
            for i in range(h):
                for j in range(l):
                    Pixel_gray[i, j] = gray_imgs.getpixel((i, j))
            # 将Pixel_gray转换为list，然后可以进行dataframe生成，或者拼接
            Pixel_gray = Pixel_gray.tolist()
            # 将Pixel_gray生成dataframe
            data = pd.DataFrame(Pixel_gray)
            with col3:
                # 显示进度条
                n = n + 1
                d = n / m
                pro.progress(d)
        with col3:
            # 在网页上显示运行时长
            if len(data) == 0:
                st.write()
            else:
                end_time = time.time()
                st.write("<h6 style='color: green;'>计算完成，请及时保存数据！</h6>", unsafe_allow_html=True)
                st.write("计算时长为", round(end_time - start_time, 2), "s")
        with col3:
            # 将数据在网页上显示
            st.write("图片名为", fname, data)
    else:
        with col3:
            st.write("<h6 style='color: red;'>请先加载bmp图片！</h6>", unsafe_allow_html=True)

    # 将使用者保存到txt文件中
    fp_save = 'users/网站使用者.txt'
    mode = 'a'
    with open(fp_save, mode) as f:
        f.write('使用了图片转csv工具' + '\n')
elif cal_button_base64:
    if m > 0:
        with col3:
            # 进度条创建
            pro = st.progress(0)
        n = 0
        for file in files:
            # 获取图片名称
            fname = file.name
            data = base64.b64encode(file.read()).decode("utf8")
            with col3:
                # 显示进度条
                n = n + 1
                d = n / m
                pro.progress(d)
                
        with col3:
            # 在网页上显示运行时长
            if len(data) == 0:
                st.write()
            else:
                end_time = time.time()
                st.write("<h6 style='color: green;'>计算完成，请及时保存数据！</h6>", unsafe_allow_html=True)
                st.write("计算时长为", round(end_time - start_time, 2), "s")
        with col3:
            # 将数据在网页上显示
            st.write("图片名为", fname, data)
    else:
        with col3:
            st.write("<h6 style='color: red;'>请先加载bmp图片！</h6>", unsafe_allow_html=True)

    # 将使用者保存到txt文件中
    fp_save = 'users/网站使用者.txt'
    mode = 'a'
    with open(fp_save, mode) as f:
        f.write('使用了图片转base64工具' + '\n')

# 编辑计算按钮底色
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(5) > div.st-emotion-cache-1l269bu.e1f1d6gn3 > div > div > div > div:nth-child(1) > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px;
    width: 150px;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(5) > div.st-emotion-cache-1l269bu.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px;
    width: 150px;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(5) > div.st-emotion-cache-1l269bu.e1f1d6gn3 > div > div > div > div:nth-child(3) > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px;
    width: 150px;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑上传按钮底色
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(4) > div > section > button
    {
    background-color: rgb(220, 240, 220);
    text = "点击加载";
    }
    </style>
    ''',
    unsafe_allow_html=True
)
