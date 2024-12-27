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
st.sidebar.write("<h4 style='color: blue;'>本工具可以计算LCD产品正视角混色水平</h4>", unsafe_allow_html=True)


# # # 工具名称、版本号
st.write("# LCD产品正视角混色评估工具 #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V1.1</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2023/11/28</h5>", unsafe_allow_html=True)


# # # 设置步骤1
st.write("<h6>步骤1：请选择RGB顺序</h6>", unsafe_allow_html=True)

bz1_1, bz1_2, bz1_3 = st.columns([1, 8, 10])
with bz1_2:
    my_RGB = st.radio('不显示label', ('RGB', 'GBR', 'BRG'), label_visibility='collapsed')

    if my_RGB == 'RGB':
        case = 1
    elif my_RGB == 'GBR':
        case = 2
    elif my_RGB == 'BRG':
        case = 3
    
with bz1_3:
    if case == 1:
        fp1 = 'pic/Color_Mix_VR/COA_RGB.bmp'
        image = Image.open(fp1)
        st.image(image)
    elif case == 2:
        fp2 = 'pic/Color_Mix_VR/COA_GBR.bmp'
        image = Image.open(fp2)
        st.image(image)
    elif case == 3:
        fp3 = 'pic/Color_Mix_VR/COA_BRG.bmp'
        image = Image.open(fp3)
        st.image(image)

# # # 设置步骤2
st.write("<h6>步骤2：请加载对应RGB顺序的txt文件</h6>", unsafe_allow_html=True)
bz2_1, bz2_2 = st.columns([1, 25])
with bz2_2:
    fp_techwiz_C = st.file_uploader("请上传techwiz正视角仿真结果TXT文件", accept_multiple_files=True, type=['txt'], help="请选择TXT文件进行上传", key=1)
    

# # # 设置步骤3
st.write("<h6>步骤3：请填写SD走线角度 (注：一般为0度设计，Olivia/TJ3/Varjo为10度设计)</h6>", unsafe_allow_html=True)
bz3_1, bz3_2, bz3_3 = st.columns([1, 3, 20])
with bz3_2:
    Slit_Angle = st.number_input(label='**a**', value=0.0, format='%f', label_visibility='collapsed')

# # # 设置步骤4
st.write("<h6>步骤4：请加载BLU光谱和RGB光谱TXT文件</h6>", unsafe_allow_html=True)

# 设置光谱上传按钮，并将数据读取到BLU和RGB变量中
# 初始化结束
bz4_1, bz4_2 = st.columns([1, 25])
with bz4_2:
    fp_BLU = st.file_uploader("请上传BLU光谱TXT文件 (请确保数据为380~780nm，step 1nm，无需行标和波长数据列)", type=['txt'], help="请选择TXT文件进行上传", key=3)
if fp_BLU is not None:
    BLU0 = pd.read_csv(fp_BLU, header=None, sep="\t", skip_blank_lines=True)
    BLU = np.float64(BLU0)

with bz4_2:
    fp_RGB = st.file_uploader("请上传RGB光谱TXT文件(请确保数据为380~780nm，step 1nm，无需行标和波长数据列)", type=['txt'], help="请选择TXT文件进行上传", key=4)
if fp_RGB is not None:
    RGB0 = pd.read_csv(fp_RGB, header=None, sep="\t", skip_blank_lines=True)
    RGB = np.float64(RGB0)

fp_CMF = 'source/CMF.txt'
CMF0 = pd.read_csv(fp_CMF, header=None, sep="\t", skip_blank_lines=True)
CMF = np.float64(CMF0)

# # # 设置步骤5，main code
bz5_1, bz5_2 = st.columns([1, 2])
with bz5_1:
    st.write("<h6>步骤5：请点击计算，获取结果</h6>", unsafe_allow_html=True)

# 设置点击按钮，并进入Main code
bz5_3, bz5_4, bz5_5 = st.columns([1, 6, 19])
bz5_13, bz5_14, bz5_15 = st.columns([1, 10, 3])
with bz5_4:
    final_click = st.button('***点击获取结果***', key=99)
if final_click is True:
    # 将登陆者信息传递过来
    if 'user_name' in st.session_state:
        user_name = st.session_state['user_name']
        # st.write(user_name)

    # 将登录者以及使用的信息保存到《网站使用者.txt》文件中
    import requests
    import json
    import base64
    from hashlib import sha1
    from datetime import datetime
    import pytz

    # 从 Streamlit Secret 获取 GitHub PAT
    github_pat = st.secrets['github_token']

    # GitHub 仓库信息
    owner = 'Mestas'  # 仓库所有者
    repo = 'PDT'  # 仓库名称
    branch = 'main'  # 分支名称
    filepath = 'users/网站使用者.txt'  # 文件路径

    # 文件内容
    # 获取特定时区
    timezone = pytz.timezone('Asia/Shanghai')  # 例如，获取东八区的时间

    # 获取当前时间，并将其本地化到特定时区
    local_time = datetime.now(timezone)
    # 格式化时间
    date = local_time.strftime('%Y-%m-%d %H:%M:%S')
    new_content = user_name + '于' + date + '使用了《10-Color Difference工具 (V1.0)》;  ' + '\n'

    # GitHub API URL
    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{filepath}'

    # 设置请求头，包括你的 PAT
    headers = {
        'Authorization': f'token {github_pat}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }

    # 发送请求以获取当前文件内容
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        file_data = response.json()
        # 读取现有文件内容
        existing_content = base64.b64decode(file_data['content']).decode('utf-8')
        # 将新内容追加到现有内容
        updated_content = existing_content + new_content
        # 计算更新后内容的 SHA1 哈希值
        content_sha1 = sha1(updated_content.encode('utf-8')).hexdigest()
    else:
        # 如果文件不存在，就创建新文件
        updated_content = new_content
        content_sha1 = sha1(new_content.encode('utf-8')).hexdigest()

    # 将更新后的内容转换为 Base64 编码
    encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')

    # 构建请求体
    data = {
        "message": "Append to file via Streamlit",
        "content": encoded_content,
        "branch": branch,
        "sha": file_data['sha'] if response.status_code == 200 else None  # 如果文件不存在，这将被忽略
    }

    # 发送请求以更新文件内容
    response = requests.put(api_url, headers=headers, data=json.dumps(data))

    # # 检查响应状态
    # if response.status_code == 200:
    #     # 请求成功，显示成功信息
    #     print('File updated successfully on GitHub!')
    # else:
    #     # 请求失败，显示错误信息
    #     print(f'Error: {response.status_code}')
    #     print(response.text)

    # # # # # # # # # # # # 分隔符，以上为保存使用者信息 # # # # # # # # # # # #
    # # # # # # # # # # # # 分隔符，以下为正式代码 # # # # # # # # # # # #

    try:
        if fp_techwiz_C is not None:
            name = []
            color_x = []
            color_y = []
            # print(color)
            mm = len(fp_techwiz_C)

            with bz5_14:
            # 进度条创建
                pro = st.progress(0)
            nn = 0

            for file in fp_techwiz_C:
                fname = file.name
                st0 = pd.read_csv(file, sep="\t", skip_blank_lines=True)
                st1 = st0[::-1]
                m = st0.shape[0] - 1
                n = st0.shape[1] - 1
                Pixel_C0 = np.zeros((m, n))
                Pixel_C0[:, :] = st1.iloc[0:int(m), 1:int(n + 1)].values
                Pixel_C = np.float64(Pixel_C0)

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

                RX = sum(sum(RX0))
                RY = sum(sum(RY0))
                RZ = sum(sum(RZ0))
                GX = sum(sum(GX0))
                GY = sum(sum(GY0))
                GZ = sum(sum(GZ0))
                BX = sum(sum(BX0))
                BY = sum(sum(BY0))
                BZ = sum(sum(BZ0))

                # # 从techwiz数据中找到RGB对应的透过率
                sub_Pixel_l = math.floor(m / 3)  # sub Pixel对应的列数，用floor防止，Right的数据超过范围
                shift_X_l = round(m * math.tan(Slit_Angle / 180 * math.pi))

                # # 创建正视角观察的三个子像素
                Left_C = np.zeros((m, sub_Pixel_l))
                Center_C = np.zeros((m, sub_Pixel_l))
                Right_C = np.zeros((m, sub_Pixel_l))

                for i in range(m):
                    for j in range(sub_Pixel_l):
                        Left_C[i, j] = Pixel_C[i, int(j + shift_X_l / (m - 1) * i)]
                        Center_C[i, j] = Pixel_C[i, int(j + shift_X_l / (m - 1) * i + sub_Pixel_l)]
                        Right_C[i, j] = Pixel_C[i, int(j + shift_X_l / (m - 1) * i + sub_Pixel_l * 2)]
                sum_C_L = sum(sum(Left_C))
                sum_C_C = sum(sum(Center_C))
                sum_C_R = sum(sum(Right_C))

                if case == 1:  # # # 第1种情况 COA结构，右视角，G点亮，混入了R
                    # # # 计算正视角G颜色 @uv坐标系
                    Wx_C = (RX * sum_C_L + GX * sum_C_C + BX * sum_C_R) / (
                            (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (
                            BX + BY + BZ) * sum_C_R)
                    Wy_C = (RY * sum_C_L + GY * sum_C_C + BY * sum_C_R) / (
                            (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (
                            BX + BY + BZ) * sum_C_R)

                elif case == 2:  # # # 第2种情况 COA结构，右视角，B点亮，混入了G
                    # # # 计算正视角B颜色 @uv坐标系
                    Wx_C = (GX * sum_C_L + BX * sum_C_C + RX * sum_C_R) / (
                            (GX + GY + GZ) * sum_C_L + (
                            BX + BY + BZ) * sum_C_C + (
                                    RX + RY + RZ) * sum_C_R)
                    Wy_C = (GY * sum_C_L + BY * sum_C_C + RY * sum_C_R) / (
                            (GX + GY + GZ) * sum_C_L + (
                            BX + BY + BZ) * sum_C_C + (
                                    RX + RY + RZ) * sum_C_R)
                
                elif case == 3:  # # # 第3种情况 COA结构，右视角，R点亮，混入了B
                    # # # 计算正视角R颜色 @uv坐标系
                    Wx_C = (BX * sum_C_L + RX * sum_C_C + GX * sum_C_R) / (
                            (BX + BY + BZ) * sum_C_L + (
                            RX + RY + RZ) * sum_C_C + (
                                    GX + GY + GZ) * sum_C_R)
                    Wy_C = (BY * sum_C_L + RY * sum_C_C + GY * sum_C_R) / (
                            (BX + BY + BZ) * sum_C_L + (
                            RX + RY + RZ) * sum_C_C + (
                                    GX + GY + GZ) * sum_C_R)
               
                name.append(file.name)
                color_x.append(Wx_C)
                color_y.append(Wy_C)
                data = pd.DataFrame({'txt_Name': name, 'color_x': color_x, 'color_y': color_y})
                
                with bz5_14:
                    # 显示进度条
                    nn = nn + 1
                    dd = nn / mm
                    pro.progress(dd)
            # m = len(color_x)
            # data = np.empty((m, 3), dtype=object)
            # for i in range(m):
            #     data[i, 0] = name[i]
            #     data[i, 1] = color_x[i]
            #     data[i, 2] = color_y[i]
            st.write(data)
    except NameError:
        with bz5_5:
            st.write(' ')
            st.write(' ')
            st.write(':red[请确认加载的Tehcwiz仿真数据以及BLU和RGB光谱!]')

# 编辑计算按钮底色
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(12) > div.st-emotion-cache-vft1hk.e1f1d6gn3 > div > div > div > div > div > button
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
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(10) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div:nth-child(1) > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(10) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑input底色
st.markdown(
    '''
    <style>
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
    </style>
    ''',
    unsafe_allow_html=True
)
