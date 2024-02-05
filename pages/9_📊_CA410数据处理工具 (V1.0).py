import numpy as np
import pandas as pd
import streamlit as st
# st.balloons()  #过场动画

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具可以批量处理CA410测试的数据</h4>", unsafe_allow_html=True)


# # # 工具名称、版本号
st.write("# CA410数据处理工具 #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V1.0</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2023/11/24</h5>", unsafe_allow_html=True)


# # # 设置步骤1
st.write("<h6>请上传CA410测试数据CSV文件，并点击计算按钮</h6>", unsafe_allow_html=True)

# 设置步骤1的radio图标
bz1_1, bz1_2 = st.columns([1, 25])
with bz1_2:
    files = st.file_uploader("请上传CA410测试数据CSV文件", type=['csv'], accept_multiple_files=True, help="请选择CSV文件进行上传", key=1)
D1 = []
D2 = []
DD = []
fname = []

col1, col2 = st.columns([1, 5])
col3, col4 = st.columns([10000, 1])
### 主程序
with col1:
    if st.button("***点击计算***"):
        if files is not None:
            for file in files:
                file_name = file.name
                fsplit = file_name.split('.')  # 使用"."作为分隔符
                fname = fsplit[0]
                data = pd.read_csv(file, header=None)

                Final = np.zeros((16, 1))
                Final[0, 0] = data.iloc[1, 4]
                Final[1, 0] = data.iloc[1, 5]
                Final[2, 0] = data.iloc[1, 6]
                Final[3, 0] = data.iloc[2, 4]
                Final[4, 0] = data.iloc[2, 5]
                Final[5, 0] = data.iloc[2, 6]
                Final[6, 0] = data.iloc[3, 4]
                Final[7, 0] = data.iloc[3, 5]
                Final[8, 0] = data.iloc[3, 6]
                Final[9, 0] = data.iloc[4, 4]
                Final[10, 0] = data.iloc[4, 5]
                Final[11, 0] = data.iloc[4, 6]
                Final[12, 0] = data.iloc[5, 4]
                Final[13, 0] = data.iloc[5, 5]
                Final[14, 0] = data.iloc[5, 6]
                Final[15, 0] = max(float(data.iloc[1, 6]), float(data.iloc[2, 6]), float(data.iloc[3, 6]), float(data.iloc[4, 6]), float(data.iloc[5, 6])) / min(float(data.iloc[1, 6]), float(data.iloc[2, 6]), float(data.iloc[3, 6]), float(data.iloc[4, 6]), float(data.iloc[5, 6]))

                # 数据粘接，list为行数据
                D1.append(fname)
                D2.append(Final)
                # 将D2的list进行行列转换
                t_data = list(zip(*D2))
                DD = [list(row) for row in t_data]

        with col3:
            Final_Data = pd.DataFrame(DD, columns=D1)
            st.write(Final_Data)

        # 将使用者保存到txt文件中
        fp_save = 'users/网站使用者.txt'
        mode = 'a'
        with open(fp_save, mode) as f:
            f.write('使用了CA410数据处理工具' + '\n')

# 编辑点击计算按钮
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(5) > div.st-emotion-cache-1l269bu.e1f1d6gn3 > div > div > div > div > div > button
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
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(4) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    </style>
    ''',
    unsafe_allow_html=True
)
