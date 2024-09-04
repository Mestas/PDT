import pandas as pd
import streamlit as st
import time

# 设置主页标题
st.set_page_config(
    page_title="欢迎使用Panel Design Tools",
    page_icon="👋",
    # layout='wide',
)

# 设置主页内容
st.write("<h1>  </h1>", unsafe_allow_html=True)
st.write("<h1>  </h1>", unsafe_allow_html=True)
st.write("<h1>《Panel Design Tools合集》</h1>", unsafe_allow_html=True)
# 设置作者
# col1, col2 = st.columns([3, 1])
# with col2:
#     st.write("<h4 style='color: blue;'>作者：xxx</h4>", unsafe_allow_html=True)

# # 设置引导栏
# st.write("<h1>  </h1>", unsafe_allow_html=True)
# st.write("<h1>  </h1>", unsafe_allow_html=True)
# st.write("<h1>  </h1>", unsafe_allow_html=True)
# st.write("### 👈 请在左侧边栏点击想要使用的工具 ###")


# 设置反馈信息栏
col3, col4 = st.columns([3, 2])
with col4:
    st.write("<h1>  </h1>", unsafe_allow_html=True)
    st.write("<h1>  </h1>", unsafe_allow_html=True)
    st.write("<h1>  </h1>", unsafe_allow_html=True)
    st.write("<h6 style='color: rgb(255,0,255);'>使用过程如遇问题，请及时与作者联系</h6>", unsafe_allow_html=True)

# 设置侧边栏引导
st.sidebar.write("## 👆请在上方点击所要使用的工具 ##")


# # #设置登录
# 设置侧边栏隐藏
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-vk3wp9.eczjsme11
    {
    visibility: hidden !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 输入用户名
col5, col6, col7 = st.columns([1, 4, 10])
col15, col16, col17 = st.columns([1.3, 5, 10])
col25, col26, col27 = st.columns([1.3, 8, 10])
with col6:
    name = st.text_input('请输入姓名并点击登录', key=1)
    # code = st.text_input('请输入密码', key=2)
    btn = st.button('点击登录')
p = len(name)
namelist = ['admin', 'b6kf', '刘晓辉', '刘瑞超', '任静峰', '陈凯', '李泽亮', '吴兆君', '李小艳', '张小凤', '纪浩晨', '许曦', '佟洁', '栗晓亚', '梁鹏', '王宁', '李忻放']
if btn is True:
    if p > 0 and name in namelist:
        with col16:
            st.write(name + ' 登录成功，欢迎使用')
        # 设置登录框关闭
        st.markdown(
            '''
            <style>
            input
            {
            visibility: collapsed !important;
            background-color: rgb(220, 240, 220) !important;
            }
            </style>
            ''',
            unsafe_allow_html=True
        )
        # 设置侧边栏隐藏
        st.markdown(
            '''
            <style>
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-vk3wp9.eczjsme11
            {
            visibility: visible !important;
            }
            </style>
            ''',
            unsafe_allow_html=True
        )
        # 设置引导栏
        st.write("### 👈 请在左侧边栏点击想要使用的工具 ###")

        # 将使用者保存到txt文件中
        fp_save = 'users/网站使用者.txt'
        mode = 'a'
        date = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        with open(fp_save, mode) as f:
            f.write(name + '于' + date + '进行了登录: ')
    elif p > 0 and name not in namelist:
        with col26:
            st.write('请联系作者，注册后使用')
    elif p == 0:
        with col26:
            st.write('请输入姓名，登录后使用')

# 设置按钮底色
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div.st-emotion-cache-ndxjbj.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > button
    {
    background-color: rgb(220, 240, 220) !important;
    height: 70px !important !important;
    width: 150px !important !important;
    }
    input {
        background-color: rgb(220, 240, 220) !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)
