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
st.sidebar.write("<h4 style='color: blue;'>本工具可以计算LCD VR新产品串色水平</h4>", unsafe_allow_html=True)

# # # 工具名称、版本号
st.write("# LCD新产品串色评估工具(VR专版) #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V2.0</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2024/11/26</h5>", unsafe_allow_html=True)


# # # 设置步骤1
st.write("<h6>步骤1：请选择Pixel类型</h6>", unsafe_allow_html=True)

# 设置步骤1的radio图标
bz1_3, bz1_4, bz1_5, bz1_6 = st.columns([1, 8, 10, 10])

with bz1_4:
    my_pixel = st.radio('不显示label', ('非COA设计', 'COA设计-Real RGB', 'COA设计-SPR RGBG'), label_visibility='collapsed')
    if my_pixel == '非COA设计':
        pixel = 1
    elif my_pixel == 'COA设计-Real RGB':
        pixel = 2
    elif my_pixel == 'COA设计-SPR RGBG':
        pixel = 3

        with bz1_5:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(':red[→→ Techwiz模拟前三个像素即可]')

# # # 设置步骤2
st.write("<h6>步骤2：请选择要观察的RGB画面</h6>", unsafe_allow_html=True)

bz2_3, bz2_4, bz2_5 = st.columns([0.6, 8, 10])
with bz2_4:
    if pixel == 1:
        my_RGB = st.radio('不显示label', ('右视角，R画面，G串入', '左视角，R画面，B串入', '右视角，G画面，B串入', '左视角，G画面，R串入', '右视角，B画面，R串入', '左视角，B画面，G串入'), label_visibility='collapsed')
        if my_RGB == '右视角，R画面，G串入':
            case = 1
        elif my_RGB == '左视角，R画面，B串入':
            case = 2
        elif my_RGB == '右视角，G画面，B串入':
            case = 3
        elif my_RGB == '左视角，G画面，R串入':
            case = 4
        elif my_RGB == '右视角，B画面，R串入':
            case = 5
        elif my_RGB == '左视角，B画面，G串入':
            case = 6
    elif pixel == 2:
        my_RGB = st.radio('不显示label', ('左视角，R画面，G串入', '右视角，R画面，B串入', '左视角，G画面，B串入', '右视角，G画面，R串入', '左视角，B画面，R串入', '右视角，B画面，G串入'), label_visibility='collapsed')
        if my_RGB == '左视角，R画面，G串入':
            case = 1
        elif my_RGB == '右视角，R画面，B串入':
            case = 2
        elif my_RGB == '左视角，G画面，B串入':
            case = 3
        elif my_RGB == '右视角，G画面，R串入':
            case = 4
        elif my_RGB == '左视角，B画面，R串入':
            case = 5
        elif my_RGB == '右视角，B画面，G串入':
            case = 6
    elif pixel == 3:
        my_RGB = st.radio('不显示label', ('左视角，R画面，G串入', '右视角，R画面，G串入', '左视角，G画面，R串入', '右视角，G画面，B串入', '左视角，G画面，B串入', '右视角，G画面，R串入', '左视角，B画面，G串入', '右视角，B画面，G串入'), label_visibility='collapsed')
        if my_RGB == '左视角，R画面，G串入':
            case = 1
        elif my_RGB == '右视角，R画面，G串入':
            case = 2
        elif my_RGB == '左视角，G画面，R串入':
            case = 3
        elif my_RGB == '右视角，G画面，B串入':
            case = 4
        elif my_RGB == '左视角，G画面，B串入':
            case = 5
        elif my_RGB == '右视角，G画面，R串入':
            case = 6
        elif my_RGB == '左视角，B画面，G串入':
            case = 7
        elif my_RGB == '右视角，B画面，G串入':
            case = 8

# 设置步骤2的图片显示
with bz2_5:
    if pixel == 1 and case == 1:
        fp1 = 'pic/Color_Mix_VR/VR_normal_R_RG.bmp'
        image = Image.open(fp1)
        st.image(image)
    elif pixel == 1 and case == 2:
        fp2 = 'pic/Color_Mix_VR/VR_normal_L_RB.bmp'
        image = Image.open(fp2)
        st.image(image)
    elif pixel == 1 and case == 3:
        fp3 = 'pic/Color_Mix_VR/VR_normal_R_GB.bmp'
        image = Image.open(fp3)
        st.image(image)
    elif pixel == 1 and case == 4:
        fp4 = 'pic/Color_Mix_VR/VR_normal_L_GR.bmp'
        image = Image.open(fp4)
        st.image(image)
    elif pixel == 1 and case == 5:
        fp5 = 'pic/Color_Mix_VR/VR_normal_R_BR.bmp'
        image = Image.open(fp5)
        st.image(image)
    elif pixel == 1 and case == 6:
        fp6 = 'pic/Color_Mix_VR/VR_normal_L_BG.bmp'
        image = Image.open(fp6)
        st.image(image)

    elif pixel == 2 and case == 1:
        fp7 = 'pic/Color_Mix_VR/VR_COA_L_RG.bmp'
        image = Image.open(fp7)
        st.image(image)
    elif pixel == 2 and case == 2:
        fp8 = 'pic/Color_Mix_VR/VR_COA_R_RB.bmp'
        image = Image.open(fp8)
        st.image(image)
    elif pixel == 2 and case == 3:
        fp9 = 'pic/Color_Mix_VR/VR_COA_L_GB.bmp'
        image = Image.open(fp9)
        st.image(image)
    elif pixel == 2 and case == 4:
        fp10 = 'pic/Color_Mix_VR/VR_COA_R_GR.bmp'
        image = Image.open(fp10)
        st.image(image)
    elif pixel == 2 and case == 5:
        fp11 = 'pic/Color_Mix_VR/VR_COA_L_BR.bmp'
        image = Image.open(fp11)
        st.image(image)
    elif pixel == 2 and case == 6:
        fp12 = 'pic/Color_Mix_VR/VR_COA_R_BG.bmp'
        image = Image.open(fp12)
        st.image(image)
    
    elif pixel == 3 and case == 1:
        fp13 = 'pic/Color_Mix_VR/VR_COA_GRGB_L.bmp'
        image = Image.open(fp13)
        st.image(image)
    elif pixel == 3 and case == 2:
        fp14 = 'pic/Color_Mix_VR/VR_COA_GRGB_R.bmp'
        image = Image.open(fp14)
        st.image(image)
    elif pixel == 3 and case == 3:
        fp15 = 'pic/Color_Mix_VR/VR_COA_BGRG_L.bmp'
        image = Image.open(fp15)
        st.image(image)
    elif pixel == 3 and case == 4:
        fp16 = 'pic/Color_Mix_VR/VR_COA_BGRG_R.bmp'
        image = Image.open(fp16)
        st.image(image)
    elif pixel == 3 and case == 5:
        fp17 = 'pic/Color_Mix_VR/VR_COA_RGBG_L.bmp'
        image = Image.open(fp17)
        st.image(image)
    elif pixel == 3 and case == 6:
        fp18 = 'pic/Color_Mix_VR/VR_COA_RGBG_R.bmp'
        image = Image.open(fp18)
        st.image(image)
    elif pixel == 3 and case == 7:
        fp19 = 'pic/Color_Mix_VR/VR_COA_GBGR_L.bmp'
        image = Image.open(fp19)
        st.image(image)
    elif pixel == 3 and case == 8:
        fp20 = 'pic/Color_Mix_VR/VR_COA_GBGR_R.bmp'
        image = Image.open(fp20)
        st.image(image)

# # # 设置步骤3
st.write("<h6>步骤3：请填写SD走线角度 (注：一般为0度设计，Olivia/TJ3/Varjo为10度设计)</h6>", unsafe_allow_html=True)
bz3_1, bz3_2, bz3_3 = st.columns([1, 3, 20])
with bz3_2:
    Slit_Angle = st.number_input(label='**a**', value=0.0, format='%f', label_visibility='collapsed')

# # # 设置步骤4
st.write("<h6>步骤4：请加载Techwiz仿真结果TXT文件 (注：带BM模拟，模拟区域选择为BM中心，其他遮光层根据观察角度进行shift)</h6>", unsafe_allow_html=True)
bz4_3, bz4_4 = st.columns([1, 25])
with bz4_4:
    fp_techwiz_C = st.file_uploader("请上传techwiz正视角仿真结果TXT文件", type=['txt'], help="请选择TXT文件进行上传", key=1)
    if fp_techwiz_C is not None:
        st0 = pd.read_csv(fp_techwiz_C, sep="\t", skip_blank_lines=True)
        st1 = st0[::-1]  # 因为Techwiz输出的数据的XY坐标为倒置，该命令将Techwiz数据倒序处理
        m = st0.shape[0] - 1
        n = st0.shape[1] - 1
        Pixel_C0 = np.zeros((m, n))
        Pixel_C0[:, :] = st1.iloc[0:int(m), 1:int(n + 1)].values
        Pixel_C = np.float64(Pixel_C0)

with bz4_4:
    fp_techwiz_LR = st.file_uploader("请上传techwiz侧视角仿真结果TXT文件", type=['txt'], help="请选择TXT文件进行上传", key=2)
    if fp_techwiz_LR is not None:
        st22 = pd.read_csv(fp_techwiz_LR, sep="\t", skip_blank_lines=True)
        st2 = st22[::-1]
        mm = st22.shape[0] - 1
        nn = st22.shape[1] - 1
        Pixel_LR0 = np.zeros((mm, nn))
        Pixel_LR0[:, :] = st2.iloc[0:int(mm), 1:int(nn + 1)]
        Pixel_LR = np.float64(Pixel_LR0)

# # # 设置步骤5
st.write("<h6>步骤5：请加载BLU光谱和RGB光谱TXT文件</h6>", unsafe_allow_html=True)

# 设置光谱上传按钮，并将数据读取到BLU和RGB变量中
# 初始化结束
bz4_3, bz4_4 = st.columns([1, 25])
with bz4_4:
    fp_BLU = st.file_uploader("请上传BLU光谱TXT文件 (请确保数据为380~780nm，step 1nm，无需行标和波长数据列)", type=['txt'], help="请选择TXT文件进行上传", key=3)
if fp_BLU is not None:
    BLU0 = pd.read_csv(fp_BLU, header=None, sep="\t", skip_blank_lines=True)
    BLU = np.float64(BLU0)

with bz4_4:
    fp_RGB = st.file_uploader("请上传RGB光谱TXT文件(请确保数据为380~780nm，step 1nm，无需行标和波长数据列)", type=['txt'], help="请选择TXT文件进行上传", key=4)
if fp_RGB is not None:
    RGB0 = pd.read_csv(fp_RGB, header=None, sep="\t", skip_blank_lines=True)
    RGB = np.float64(RGB0)

fp_CMF = 'source/CMF.txt'
CMF0 = pd.read_csv(fp_CMF, header=None, sep="\t", skip_blank_lines=True)
CMF = np.float64(CMF0)

# # # 设置步骤6，main code

bz5_1, bz5_2 = st.columns([1, 2])
with bz5_1:
    st.write("<h6>步骤6：请点击计算，获取结果</h6>", unsafe_allow_html=True)

# 设置点击按钮，并进入Main code
bz5_3, bz5_4, bz5_5 = st.columns([1, 6, 19])
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
    new_content = user_name + '于' + date + '使用了《05-LCD串色仿真工具VR专版 (V1.1)》;  ' + '\n'

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
        sub_Pixel_l = math.floor(n / 3)  # sub Pixel对应的列数，用floor防止Right的数据超过范围
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

        # # 创建侧视角观察的三个子像素
        Left_LR = np.zeros((m, sub_Pixel_l))
        Center_LR = np.zeros((m, sub_Pixel_l))
        Right_LR = np.zeros((m, sub_Pixel_l))

        for i in range(m):
            for j in range(sub_Pixel_l):
                Left_LR[i, j] = Pixel_LR[i, int(j + shift_X_l / (m - 1) * i)]
                Center_LR[i, j] = Pixel_LR[i, int(j + shift_X_l / (m - 1) * i + sub_Pixel_l)]
                Right_LR[i, j] = Pixel_LR[i, int(j + shift_X_l / (m - 1) * i + sub_Pixel_l * 2)]

        sum_LR_L = sum(sum(Left_LR))
        sum_LR_C = sum(sum(Center_LR))
        sum_LR_R = sum(sum(Right_LR))

        # # 分情况讨论：
        if pixel == 1 and case == 1:  # # # 第1种情况 normal结构，右视角，R点亮，混入了G
            # # # 计算正视角R颜色 @uv坐标系
            Rx_C = (BX * sum_C_L + RX * sum_C_C + GX * sum_C_R) / (
                        (BX + BY + BZ) * sum_C_L + (RX + RY + RZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)
            Ry_C = (BY * sum_C_L + RY * sum_C_C + GY * sum_C_R) / (
                        (BX + BY + BZ) * sum_C_L + (RX + RY + RZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)

            Ru_C = 4 * Rx_C / (-2 * Rx_C + 12 * Ry_C + 3)
            Rv_C = 9 * Ry_C / (-2 * Rx_C + 12 * Ry_C + 3)

            # # # 计算侧视角R颜色 @uv坐标系
            Rx_GR = (BX * sum_LR_L + RX * sum_LR_C + GX * sum_LR_R) / (
                        (BX + BY + BZ) * sum_LR_L + (RX + RY + RZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)
            Ry_GR = (BY * sum_LR_L + RY * sum_LR_C + GY * sum_LR_R) / (
                        (BX + BY + BZ) * sum_LR_L + (RX + RY + RZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)

            Ru_GR = 4 * Rx_GR / (-2 * Rx_GR + 12 * Ry_GR + 3)
            Rv_GR = 9 * Ry_GR / (-2 * Rx_GR + 12 * Ry_GR + 3)

            # # # 计算串色JNCD计算
            JNCD_normal_R_RG = (((Ru_GR - Ru_C) ** 2 + (Rv_GR - Rv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis1 = pd.DataFrame(JNCD_normal_R_RG, columns=['R画面，G串入'], index=['右侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis1)
        elif pixel == 1 and case == 2:  # # # 第2种情况 normal结构，左视角，R点亮，混入了B
            # # # 计算正视角R颜色 @uv坐标系
            Rx_C = (BX * sum_C_L + RX * sum_C_C + GX * sum_C_R) / (
                        (BX + BY + BZ) * sum_C_L + (RX + RY + RZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)
            Ry_C = (BY * sum_C_L + RY * sum_C_C + GY * sum_C_R) / (
                        (BX + BY + BZ) * sum_C_L + (RX + RY + RZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)

            Ru_C = 4 * Rx_C / (-2 * Rx_C + 12 * Ry_C + 3)
            Rv_C = 9 * Ry_C / (-2 * Rx_C + 12 * Ry_C + 3)

            # # # 计算侧视角R颜色 @uv坐标系
            Rx_BR = (BX * sum_LR_L + RX * sum_LR_C + GX * sum_LR_R) / (
                        (BX + BY + BZ) * sum_LR_L + (RX + RY + RZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)
            Ry_BR = (BY * sum_LR_L + RY * sum_LR_C + GY * sum_LR_R) / (
                        (BX + BY + BZ) * sum_LR_L + (RX + RY + RZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)

            Ru_BR = 4 * Rx_BR / (-2 * Rx_BR + 12 * Ry_BR + 3)
            Rv_BR = 9 * Ry_BR / (-2 * Rx_BR + 12 * Ry_BR + 3)

            # # # 计算串色JNCD计算
            JNCD_normal_L_RB = (((Ru_BR - Ru_C) ** 2 + (Rv_BR - Rv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis2 = pd.DataFrame(JNCD_normal_L_RB, columns=['R画面，B串入'], index=['左侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis2)
        elif pixel == 1 and case == 3:  # # # 第3种情况 normal结构，右视角，G点亮，混入了B
            # # # 计算正视角G颜色 @uv坐标系
            Gx_C = (RX * sum_C_L + GX * sum_C_C + BX * sum_C_R) / (
                        (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (BX + BY + BZ) * sum_C_R)
            Gy_C = (RY * sum_C_L + GY * sum_C_C + BY * sum_C_R) / (
                        (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (BX + BY + BZ) * sum_C_R)

            Gu_C = 4 * Gx_C / (-2 * Gx_C + 12 * Gy_C + 3)
            Gv_C = 9 * Gy_C / (-2 * Gx_C + 12 * Gy_C + 3)

            # # # 计算侧视角G颜色， @uv坐标系
            Gx_BG = (RX * sum_LR_L + GX * sum_LR_C + BX * sum_LR_R) / (
                        (RX + RY + RZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (BX + BY + BZ) * sum_LR_R)
            Gy_BG = (RY * sum_LR_L + GY * sum_LR_C + BY * sum_LR_R) / (
                        (RX + RY + RZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (BX + BY + BZ) * sum_LR_R)

            Gu_BG = 4 * Gx_BG / (-2 * Gx_BG + 12 * Gy_BG + 3)
            Gv_BG = 9 * Gy_BG / (-2 * Gx_BG + 12 * Gy_BG + 3)

            # # # 计算串色JNCD计算
            JNCD_normal_R_GB = (((Gu_BG - Gu_C) ** 2 + (Gv_BG - Gv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis3 = pd.DataFrame(JNCD_normal_R_GB, columns=['G画面，B串入'], index=['右侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis3)
        elif pixel == 1 and case == 4:  # # # 第4种情况 normal结构，左视角，G点亮，混入了R
            # # # 计算正视角G颜色 @uv坐标系
            Gx_C = (RX * sum_C_L + GX * sum_C_C + BX * sum_C_R) / (
                        (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (BX + BY + BZ) * sum_C_R)
            Gy_C = (RY * sum_C_L + GY * sum_C_C + BY * sum_C_R) / (
                        (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (BX + BY + BZ) * sum_C_R)

            Gu_C = 4 * Gx_C / (-2 * Gx_C + 12 * Gy_C + 3)
            Gv_C = 9 * Gy_C / (-2 * Gx_C + 12 * Gy_C + 3)

            # # # 计算侧视角G颜色， @uv坐标系
            Gx_RG = (RX * sum_LR_L + GX * sum_LR_C + BX * sum_LR_R) / (
                        (RX + RY + RZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (BX + BY + BZ) * sum_LR_R)
            Gy_RG = (RY * sum_LR_L + GY * sum_LR_C + BY * sum_LR_R) / (
                        (RX + RY + RZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (BX + BY + BZ) * sum_LR_R)

            Gu_RG = 4 * Gx_RG / (-2 * Gx_RG + 12 * Gy_RG + 3)
            Gv_RG = 9 * Gy_RG / (-2 * Gx_RG + 12 * Gy_RG + 3)

            # # # 计算串色JNCD计算
            JNCD_normal_L_GR = (((Gu_RG - Gu_C) ** 2 + (Gv_RG - Gv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis4 = pd.DataFrame(JNCD_normal_L_GR, columns=['G画面，R串入'], index=['左侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis4)
        elif pixel == 1 and case == 5:  # # # 第5种情况 normal结构，右视角，B点亮，混入了R
            # # # 计算正视角B颜色 @uv坐标系
            Bx_C = (GX * sum_C_L + BX * sum_C_C + RX * sum_C_R) / (
                        (GX + GY + GZ) * sum_C_L + (BX + BY + BZ) * sum_C_C + (RX + RY + RZ) * sum_C_R)
            By_C = (GY * sum_C_L + BY * sum_C_C + RY * sum_C_R) / (
                        (GX + GY + GZ) * sum_C_L + (BX + BY + BZ) * sum_C_C + (RX + RY + RZ) * sum_C_R)

            Bu_C = 4 * Bx_C / (-2 * Bx_C + 12 * By_C + 3)
            Bv_C = 9 * By_C / (-2 * Bx_C + 12 * By_C + 3)

            # # # 计算侧视角B颜色， @uv坐标系
            Bx_RB = (GX * sum_LR_L + BX * sum_LR_C + RX * sum_LR_R) / (
                        (GX + GY + GZ) * sum_LR_L + (BX + BY + BZ) * sum_LR_C + (RX + RY + RZ) * sum_LR_R)
            By_RB = (GY * sum_LR_L + BY * sum_LR_C + RY * sum_LR_R) / (
                        (GX + GY + GZ) * sum_LR_L + (BX + BY + BZ) * sum_LR_C + (RX + RY + RZ) * sum_LR_R)

            Bu_RB = 4 * Bx_RB / (-2 * Bx_RB + 12 * By_RB + 3)
            Bv_RB = 9 * By_RB / (-2 * Bx_RB + 12 * By_RB + 3)

            # # # 计算串色JNCD计算
            JNCD_normal_R_BR = (((Bu_RB - Bu_C) ** 2 + (Bv_RB - Bv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis5 = pd.DataFrame(JNCD_normal_R_BR, columns=['B画面，R串入'], index=['右侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis5)
        elif pixel == 1 and case == 6:  # # # 第6种情况 normal结构，左视角，B点亮，混入了G
            # # # 计算正视角B颜色 @uv坐标系
            Bx_C = (GX * sum_C_L + BX * sum_C_C + RX * sum_C_R) / (
                        (GX + GY + GZ) * sum_C_L + (BX + BY + BZ) * sum_C_C + (RX + RY + RZ) * sum_C_R)
            By_C = (GY * sum_C_L + BY * sum_C_C + RY * sum_C_R) / (
                        (GX + GY + GZ) * sum_C_L + (BX + BY + BZ) * sum_C_C + (RX + RY + RZ) * sum_C_R)

            Bu_C = 4 * Bx_C / (-2 * Bx_C + 12 * By_C + 3)
            Bv_C = 9 * By_C / (-2 * Bx_C + 12 * By_C + 3)

            # # # 计算侧视角B颜色， @uv坐标系
            Bx_GB = (GX * sum_LR_L + BX * sum_LR_C + RX * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (
                    BX + BY + BZ) * sum_LR_C + (
                            RX + RY + RZ) * sum_LR_R)
            By_GB = (GY * sum_LR_L + BY * sum_LR_C + RY * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (
                    BX + BY + BZ) * sum_LR_C + (
                            RX + RY + RZ) * sum_LR_R)

            Bu_GB = 4 * Bx_GB / (-2 * Bx_GB + 12 * By_GB + 3)
            Bv_GB = 9 * By_GB / (-2 * Bx_GB + 12 * By_GB + 3)

            # # # 计算串色JNCD计算
            JNCD_normal_L_BG = (((Bu_GB - Bu_C) ** 2 + (Bv_GB - Bv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis6 = pd.DataFrame(JNCD_normal_L_BG, columns=['B画面，G串入'], index=['左侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis6)

        elif pixel == 2 and case == 1:  # # # 第7种情况 COA结构，左视角，R点亮，混入了G
            # # # 计算正视角R颜色 @uv坐标系
            Rx_C = (BX * sum_C_L + RX * sum_C_C + GX * sum_C_R) / (
                    (BX + BY + BZ) * sum_C_L + (RX + RY + RZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)
            Ry_C = (BY * sum_C_L + RY * sum_C_C + GY * sum_C_R) / (
                    (BX + BY + BZ) * sum_C_L + (RX + RY + RZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)

            Ru_C = 4 * Rx_C / (-2 * Rx_C + 12 * Ry_C + 3)
            Rv_C = 9 * Ry_C / (-2 * Rx_C + 12 * Ry_C + 3)

            # # # 计算侧视角R颜色 @uv坐标系
            Rx_GR = (BX * sum_LR_L + RX * sum_LR_C + GX * sum_LR_R) / (
                    (BX + BY + BZ) * sum_LR_L + (RX + RY + RZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)
            Ry_GR = (BY * sum_LR_L + RY * sum_LR_C + GY * sum_LR_R) / (
                    (BX + BY + BZ) * sum_LR_L + (RX + RY + RZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)

            Ru_GR = 4 * Rx_GR / (-2 * Rx_GR + 12 * Ry_GR + 3)
            Rv_GR = 9 * Ry_GR / (-2 * Rx_GR + 12 * Ry_GR + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_L_RG = (((Ru_GR - Ru_C) ** 2 + (Rv_GR - Rv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis7 = pd.DataFrame(JNCD_COA_L_RG, columns=['R画面，G串入'], index=['左侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis7)
        elif pixel == 2 and case == 2:  # # # 第8种情况 COA结构，右视角，R点亮，混入了B
            # # # 计算正视角R颜色 @uv坐标系
            Rx_C = (BX * sum_C_L + RX * sum_C_C + GX * sum_C_R) / (
                    (BX + BY + BZ) * sum_C_L + (
                    RX + RY + RZ) * sum_C_C + (
                            GX + GY + GZ) * sum_C_R)
            Ry_C = (BY * sum_C_L + RY * sum_C_C + GY * sum_C_R) / (
                    (BX + BY + BZ) * sum_C_L + (
                    RX + RY + RZ) * sum_C_C + (
                            GX + GY + GZ) * sum_C_R)

            Ru_C = 4 * Rx_C / (-2 * Rx_C + 12 * Ry_C + 3)
            Rv_C = 9 * Ry_C / (-2 * Rx_C + 12 * Ry_C + 3)

            # # # 计算侧视角R颜色 @uv坐标系
            Rx_BR = (BX * sum_LR_L + RX * sum_LR_C + GX * sum_LR_R) / (
                    (BX + BY + BZ) * sum_LR_L + (
                    RX + RY + RZ) * sum_LR_C + (
                            GX + GY + GZ) * sum_LR_R)
            Ry_BR = (BY * sum_LR_L + RY * sum_LR_C + GY * sum_LR_R) / (
                    (BX + BY + BZ) * sum_LR_L + (
                    RX + RY + RZ) * sum_LR_C + (
                            GX + GY + GZ) * sum_LR_R)

            Ru_BR = 4 * Rx_BR / (-2 * Rx_BR + 12 * Ry_BR + 3)
            Rv_BR = 9 * Ry_BR / (-2 * Rx_BR + 12 * Ry_BR + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_R_RB = (((Ru_BR - Ru_C) ** 2 + (Rv_BR - Rv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis8 = pd.DataFrame(JNCD_COA_R_RB, columns=['R画面，B串入'], index=['右侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis8)

        elif pixel == 2 and case == 3:  # # # 第9种情况 COA结构，左视角，G点亮，混入了B
            # # # 计算正视角G颜色 @uv坐标系
            Gx_C = (RX * sum_C_L + GX * sum_C_C + BX * sum_C_R) / (
                    (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (BX + BY + BZ) * sum_C_R)
            Gy_C = (RY * sum_C_L + GY * sum_C_C + BY * sum_C_R) / (
                    (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (BX + BY + BZ) * sum_C_R)

            Gu_C = 4 * Gx_C / (-2 * Gx_C + 12 * Gy_C + 3)
            Gv_C = 9 * Gy_C / (-2 * Gx_C + 12 * Gy_C + 3)

            # # # 计算侧视角G颜色， @uv坐标系
            Gx_BG = (RX * sum_LR_L + GX * sum_LR_C + BX * sum_LR_R) / (
                    (RX + RY + RZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (BX + BY + BZ) * sum_LR_R)
            Gy_BG = (RY * sum_LR_L + GY * sum_LR_C + BY * sum_LR_R) / (
                    (RX + RY + RZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (BX + BY + BZ) * sum_LR_R)

            Gu_BG = 4 * Gx_BG / (-2 * Gx_BG + 12 * Gy_BG + 3)
            Gv_BG = 9 * Gy_BG / (-2 * Gx_BG + 12 * Gy_BG + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_L_GB = (((Gu_BG - Gu_C) ** 2 + (Gv_BG - Gv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis9 = pd.DataFrame(JNCD_COA_L_GB, columns=['G画面，B串入'], index=['左侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis9)
        elif pixel == 2 and case == 4:  # # # 第10种情况 COA结构，右视角，G点亮，混入了R
            # # # 计算正视角G颜色 @uv坐标系
            Gx_C = (RX * sum_C_L + GX * sum_C_C + BX * sum_C_R) / (
                    (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (
                    BX + BY + BZ) * sum_C_R)
            Gy_C = (RY * sum_C_L + GY * sum_C_C + BY * sum_C_R) / (
                    (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (
                    BX + BY + BZ) * sum_C_R)

            Gu_C = 4 * Gx_C / (-2 * Gx_C + 12 * Gy_C + 3)
            Gv_C = 9 * Gy_C / (-2 * Gx_C + 12 * Gy_C + 3)

            # # # 计算侧视角G颜色， @uv坐标系
            Gx_RG = (RX * sum_LR_L + GX * sum_LR_C + BX * sum_LR_R) / (
                    (RX + RY + RZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (
                    BX + BY + BZ) * sum_LR_R)
            Gy_RG = (RY * sum_LR_L + GY * sum_LR_C + BY * sum_LR_R) / (
                    (RX + RY + RZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (
                    BX + BY + BZ) * sum_LR_R)

            Gu_RG = 4 * Gx_RG / (-2 * Gx_RG + 12 * Gy_RG + 3)
            Gv_RG = 9 * Gy_RG / (-2 * Gx_RG + 12 * Gy_RG + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_R_GR = (((Gu_RG - Gu_C) ** 2 + (Gv_RG - Gv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis10 = pd.DataFrame(JNCD_COA_R_GR, columns=['G画面，R串入'], index=['右侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis10)

        elif pixel == 2 and case == 5:  # # # 第11种情况 COA结构，左视角，B点亮，混入了R
            # # # 计算正视角B颜色 @uv坐标系
            Bx_C = (GX * sum_C_L + BX * sum_C_C + RX * sum_C_R) / (
                    (GX + GY + GZ) * sum_C_L + (
                    BX + BY + BZ) * sum_C_C + (
                            RX + RY + RZ) * sum_C_R)
            By_C = (GY * sum_C_L + BY * sum_C_C + RY * sum_C_R) / (
                    (GX + GY + GZ) * sum_C_L + (
                    BX + BY + BZ) * sum_C_C + (
                            RX + RY + RZ) * sum_C_R)

            Bu_C = 4 * Bx_C / (-2 * Bx_C + 12 * By_C + 3)
            Bv_C = 9 * By_C / (-2 * Bx_C + 12 * By_C + 3)

            # # # 计算侧视角B颜色， @uv坐标系
            Bx_RB = (GX * sum_LR_L + BX * sum_LR_C + RX * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (
                    BX + BY + BZ) * sum_LR_C + (
                            RX + RY + RZ) * sum_LR_R)
            By_RB = (GY * sum_LR_L + BY * sum_LR_C + RY * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (
                    BX + BY + BZ) * sum_LR_C + (
                            RX + RY + RZ) * sum_LR_R)

            Bu_RB = 4 * Bx_RB / (-2 * Bx_RB + 12 * By_RB + 3)
            Bv_RB = 9 * By_RB / (-2 * Bx_RB + 12 * By_RB + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_L_BR = (((Bu_RB - Bu_C) ** 2 + (Bv_RB - Bv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis11 = pd.DataFrame(JNCD_COA_L_BR, columns=['B画面，R串入'], index=['左侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis11)
        elif pixel == 2 and case == 6:  # # # 第12种情况 COA结构，右视角，B点亮，混入了G
            # # # 计算正视角B颜色 @uv坐标系
            Bx_C = (GX * sum_C_L + BX * sum_C_C + RX * sum_C_R) / (
                    (GX + GY + GZ) * sum_C_L + (
                    BX + BY + BZ) * sum_C_C + (
                            RX + RY + RZ) * sum_C_R)
            By_C = (GY * sum_C_L + BY * sum_C_C + RY * sum_C_R) / (
                    (GX + GY + GZ) * sum_C_L + (
                    BX + BY + BZ) * sum_C_C + (
                            RX + RY + RZ) * sum_C_R)

            Bu_C = 4 * Bx_C / (-2 * Bx_C + 12 * By_C + 3)
            Bv_C = 9 * By_C / (-2 * Bx_C + 12 * By_C + 3)

            # # # 计算侧视角B颜色， @uv坐标系
            Bx_GB = (GX * sum_LR_L + BX * sum_LR_C + RX * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (
                    BX + BY + BZ) * sum_LR_C + (
                            RX + RY + RZ) * sum_LR_R)
            By_GB = (GY * sum_LR_L + BY * sum_LR_C + RY * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (
                    BX + BY + BZ) * sum_LR_C + (
                            RX + RY + RZ) * sum_LR_R)

            Bu_GB = 4 * Bx_GB / (-2 * Bx_GB + 12 * By_GB + 3)
            Bv_GB = 9 * By_GB / (-2 * Bx_GB + 12 * By_GB + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_R_BG = (((Bu_GB - Bu_C) ** 2 + (Bv_GB - Bv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis12 = pd.DataFrame(JNCD_COA_R_BG, columns=['B画面，G串入'], index=['右侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis12)
        




        elif pixel == 3 and case == 1:  # # # 第13种情况 COA-SPR结构，左视角，R点亮，混入了G
            # # # 计算正视角R颜色 @uv坐标系
            Rx_C = (GX * sum_C_L + RX * sum_C_C + GX * sum_C_R) / (
                    (GX + GY + GZ) * sum_C_L + (RX + RY + RZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)
            Ry_C = (GY * sum_C_L + RY * sum_C_C + GY * sum_C_R) / (
                    (GX + GY + GZ) * sum_C_L + (RX + RY + RZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)

            Ru_C = 4 * Rx_C / (-2 * Rx_C + 12 * Ry_C + 3)
            Rv_C = 9 * Ry_C / (-2 * Rx_C + 12 * Ry_C + 3)

            # # # 计算侧视角R颜色 @uv坐标系
            Rx_GRG = (GX * sum_LR_L + RX * sum_LR_C + GX * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (RX + RY + RZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)
            Ry_GRG = (GY * sum_LR_L + RY * sum_LR_C + GY * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (RX + RY + RZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)

            Ru_GRG = 4 * Rx_GRG / (-2 * Rx_GRG + 12 * Ry_GRG + 3)
            Rv_GRG = 9 * Ry_GRG / (-2 * Rx_GRG + 12 * Ry_GRG + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_SPR_L_GRG = (((Ru_GRG - Ru_C) ** 2 + (Rv_GRG - Rv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis13 = pd.DataFrame(JNCD_COA_SPR_L_GRG, columns=['左视角，R画面，G串入'], index=['左侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis13)

        elif pixel == 3 and case == 2:  # # # 第14种情况 COA-SPR结构，右视角，R点亮，混入了G
            # # # 计算正视角R颜色 @uv坐标系
            Rx_C = (GX * sum_C_L + RX * sum_C_C + GX * sum_C_R) / (
                    (GX + GY + GZ) * sum_C_L + (RX + RY + RZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)
            Ry_C = (GY * sum_C_L + RY * sum_C_C + GY * sum_C_R) / (
                    (GX + GY + GZ) * sum_C_L + (RX + RY + RZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)

            Ru_C = 4 * Rx_C / (-2 * Rx_C + 12 * Ry_C + 3)
            Rv_C = 9 * Ry_C / (-2 * Rx_C + 12 * Ry_C + 3)

            # # # 计算侧视角R颜色 @uv坐标系
            Rx_GRG = (GX * sum_LR_L + RX * sum_LR_C + GX * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (RX + RY + RZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)
            Ry_GRG = (GY * sum_LR_L + RY * sum_LR_C + GY * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (RX + RY + RZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)

            Ru_GRG = 4 * Rx_GRG / (-2 * Rx_GRG + 12 * Ry_GRG + 3)
            Rv_GRG = 9 * Ry_GRG / (-2 * Rx_GRG + 12 * Ry_GRG + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_SPR_R_GRG = (((Ru_GRG - Ru_C) ** 2 + (Rv_GRG - Rv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis14 = pd.DataFrame(JNCD_COA_SPR_R_GRG, columns=['左视角，R画面，G串入'], index=['右侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis14)

        elif pixel == 3 and case == 3:  # # # 第15种情况 COA-SPR结构，左视角，G点亮，混入了R
            # # # 计算正视角R颜色 @uv坐标系
            Gx_C = (BX * sum_C_L + GX * sum_C_C + RX * sum_C_R) / (
                    (BX + BY + BZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (RX + RY + RZ) * sum_C_R)
            Gy_C = (BY * sum_C_L + GY * sum_C_C + RY * sum_C_R) / (
                    (BX + BY + BZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (RX + RY + RZ) * sum_C_R)

            Gu_C = 4 * Gx_C / (-2 * Gx_C + 12 * Gy_C + 3)
            Gv_C = 9 * Gy_C / (-2 * Gx_C + 12 * Gy_C + 3)

            # # # 计算侧视角R颜色 @uv坐标系
            Gx_BGR = (BX * sum_LR_L + GX * sum_LR_C + RX * sum_LR_R) / (
                    (BX + BY + BZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (RX + RY + RZ) * sum_LR_R)
            Gy_BGR = (BY * sum_LR_L + GY * sum_LR_C + RY * sum_LR_R) / (
                    (BX + BY + BZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (RX + RY + RZ) * sum_LR_R)

            Gu_BGR = 4 * Gx_BGR / (-2 * Gx_BGR + 12 * Gy_BGR + 3)
            Gv_BGR = 9 * Gy_BGR / (-2 * Gx_BGR + 12 * Gy_BGR + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_SPR_L_BGR = (((Gu_BGR - Gu_C) ** 2 + (Gv_BGR - Gv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis15 = pd.DataFrame(JNCD_COA_SPR_L_BGR, columns=['左视角，G画面，R串入'], index=['左侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis15)
        
        elif pixel == 3 and case == 4:  # # # 第16种情况 COA-SPR结构，右视角，G点亮，混入了B
            # # # 计算正视角R颜色 @uv坐标系
            Gx_C = (BX * sum_C_L + GX * sum_C_C + RX * sum_C_R) / (
                    (BX + BY + BZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (RX + RY + RZ) * sum_C_R)
            Gy_C = (BY * sum_C_L + GY * sum_C_C + RY * sum_C_R) / (
                    (BX + BY + BZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (RX + RY + RZ) * sum_C_R)

            Gu_C = 4 * Gx_C / (-2 * Gx_C + 12 * Gy_C + 3)
            Gv_C = 9 * Gy_C / (-2 * Gx_C + 12 * Gy_C + 3)

            # # # 计算侧视角R颜色 @uv坐标系
            Gx_BGR = (BX * sum_LR_L + GX * sum_LR_C + RX * sum_LR_R) / (
                    (BX + BY + BZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (RX + RY + RZ) * sum_LR_R)
            Gy_BGR = (BY * sum_LR_L + GY * sum_LR_C + RY * sum_LR_R) / (
                    (BX + BY + BZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (RX + RY + RZ) * sum_LR_R)

            Gu_BGR = 4 * Gx_BGR / (-2 * Gx_BGR + 12 * Gy_BGR + 3)
            Gv_BGR = 9 * Gy_BGR / (-2 * Gx_BGR + 12 * Gy_BGR + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_SPR_R_BGR = (((Gu_BGR - Gu_C) ** 2 + (Gv_BGR - Gv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis16 = pd.DataFrame(JNCD_COA_SPR_R_BGR, columns=['右视角，G画面，R串入'], index=['右侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis16)

        elif pixel == 3 and case == 5:  # # # 第17种情况 COA-SPR结构，左视角，G点亮，混入了B
            # # # 计算正视角R颜色 @uv坐标系
            Gx_C = (RX * sum_C_L + GX * sum_C_C + BX * sum_C_R) / (
                    (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (BX + BY + BZ) * sum_C_R)
            Gy_C = (RY * sum_C_L + GY * sum_C_C + BY * sum_C_R) / (
                    (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (BX + BY + BZ) * sum_C_R)

            Gu_C = 4 * Gx_C / (-2 * Gx_C + 12 * Gy_C + 3)
            Gv_C = 9 * Gy_C / (-2 * Gx_C + 12 * Gy_C + 3)

            # # # 计算侧视角R颜色 @uv坐标系
            Gx_RGB = (RX * sum_LR_L + GX * sum_LR_C + BX * sum_LR_R) / (
                    (RX + RY + RZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (BX + BY + BZ) * sum_LR_R)
            Gy_RGB = (RY * sum_LR_L + GY * sum_LR_C + BY * sum_LR_R) / (
                    (RX + RY + RZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (BX + BY + BZ) * sum_LR_R)

            Gu_RGB = 4 * Gx_RGB / (-2 * Gx_RGB + 12 * Gy_RGB + 3)
            Gv_RGB = 9 * Gy_RGB / (-2 * Gy_RGB + 12 * Gy_RGB + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_SPR_L_RGB = (((Gu_RGB - Gu_C) ** 2 + (Gv_RGB - Gv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis17 = pd.DataFrame(JNCD_COA_SPR_L_RGB, columns=['左视角，G画面，B串入'], index=['左侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis17)

        elif pixel == 3 and case == 6:  # # # 第18种情况 COA-SPR结构，右视角，G点亮，混入了R
            # # # 计算正视角R颜色 @uv坐标系
            Gx_C = (RX * sum_C_L + GX * sum_C_C + BX * sum_C_R) / (
                    (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (BX + BY + BZ) * sum_C_R)
            Gy_C = (RY * sum_C_L + GY * sum_C_C + BY * sum_C_R) / (
                    (RX + RY + RZ) * sum_C_L + (GX + GY + GZ) * sum_C_C + (BX + BY + BZ) * sum_C_R)

            Gu_C = 4 * Gx_C / (-2 * Gx_C + 12 * Gy_C + 3)
            Gv_C = 9 * Gy_C / (-2 * Gx_C + 12 * Gy_C + 3)

            # # # 计算侧视角R颜色 @uv坐标系
            Gx_RGB = (RX * sum_LR_L + GX * sum_LR_C + BX * sum_LR_R) / (
                    (RX + RY + RZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (BX + BY + BZ) * sum_LR_R)
            Gy_RGB = (RY * sum_LR_L + GY * sum_LR_C + BY * sum_LR_R) / (
                    (RX + RY + RZ) * sum_LR_L + (GX + GY + GZ) * sum_LR_C + (BX + BY + BZ) * sum_LR_R)

            Gu_RGB = 4 * Gx_RGB / (-2 * Gx_RGB + 12 * Gy_RGB + 3)
            Gv_RGB = 9 * Gy_RGB / (-2 * Gy_RGB + 12 * Gy_RGB + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_SPR_R_RGB = (((Gu_RGB - Gu_C) ** 2 + (Gv_RGB - Gv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis18 = pd.DataFrame(JNCD_COA_SPR_R_RGB, columns=['右视角，G画面，B串入'], index=['右侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis18)
        
        elif pixel == 3 and case == 7:  # # # 第19种情况 COA-SPR结构，左视角，B点亮，混入了G
            # # # 计算正视角R颜色 @uv坐标系
            Bx_C = (GX * sum_C_L + BX * sum_C_C + GX * sum_C_R) / (
                    (GX + GY + GZ) * sum_C_L + (BX + BY + BZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)
            By_C = (GY * sum_C_L + BY * sum_C_C + GY * sum_C_R) / (
                    (GX + GY + GZ) * sum_C_L + (BX + BY + BZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)

            Bu_C = 4 * Bx_C / (-2 * Bx_C + 12 * By_C + 3)
            Bv_C = 9 * By_C / (-2 * Bx_C + 12 * By_C + 3)

            # # # 计算侧视角R颜色 @uv坐标系
            Bx_GBG = (GX * sum_LR_L + BX * sum_LR_C + GX * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (BX + BY + BZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)
            By_GBG = (GY * sum_LR_L + BY * sum_LR_C + GY * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (BX + BY + BZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)

            Bu_GBG = 4 * Bx_GBG / (-2 * Bx_GBG + 12 * By_GBG + 3)
            Bv_GBG = 9 * By_GBG / (-2 * By_GBG + 12 * By_GBG + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_SPR_L_GBG = (((Bu_GBG - Bu_C) ** 2 + (Bv_GBG - Bv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis19 = pd.DataFrame(JNCD_COA_SPR_L_GBG, columns=['左视角，B画面，G串入'], index=['左侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis19)

        elif pixel == 3 and case == 8:  # # # 第20种情况 COA-SPR结构，右视角，B点亮，混入了G
            # # # 计算正视角R颜色 @uv坐标系
            Bx_C = (GX * sum_C_L + BX * sum_C_C + GX * sum_C_R) / (
                    (GX + GY + GZ) * sum_C_L + (BX + BY + BZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)
            By_C = (GY * sum_C_L + BY * sum_C_C + GY * sum_C_R) / (
                    (GX + GY + GZ) * sum_C_L + (BX + BY + BZ) * sum_C_C + (GX + GY + GZ) * sum_C_R)

            Bu_C = 4 * Bx_C / (-2 * Bx_C + 12 * By_C + 3)
            Bv_C = 9 * By_C / (-2 * Bx_C + 12 * By_C + 3)

            # # # 计算侧视角R颜色 @uv坐标系
            Bx_GBG = (GX * sum_LR_L + BX * sum_LR_C + GX * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (BX + BY + BZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)
            By_GBG = (GY * sum_LR_L + BY * sum_LR_C + GY * sum_LR_R) / (
                    (GX + GY + GZ) * sum_LR_L + (BX + BY + BZ) * sum_LR_C + (GX + GY + GZ) * sum_LR_R)

            Bu_GBG = 4 * Bx_GBG / (-2 * Bx_GBG + 12 * By_GBG + 3)
            Bv_GBG = 9 * By_GBG / (-2 * By_GBG + 12 * By_GBG + 3)

            # # # 计算串色JNCD计算
            JNCD_COA_SPR_R_GBG = (((Bu_GBG - Bu_C) ** 2 + (Bv_GBG - Bv_C) ** 2) ** 0.5) / 0.004
            JNCD_dis20 = pd.DataFrame(JNCD_COA_SPR_R_GBG, columns=['右视角，B画面，G串入'], index=['右侧视角'])
            # 设置显示
            with bz5_5:
                st.write(' ')
                st.write(' ')
                st.write(':green[计算完成，请及时保存结果！]')
            bz5_6, bz5_7 = st.columns([1, 25])
            with bz5_7:
                st.write(JNCD_dis20)
    # except AttributeError:
    #     with bz5_5:
    #         st.write(' ')
    #         st.write(' ')
    #         st.write(':red[请确认所有项目已填写完成1!]')
    # except ValueError:
    #     with bz5_5:
    #         st.write(' ')
    #         st.write(' ')
    #         st.write(':red[请确认所有项目已填写完成2!]')
    except NameError:
        with bz5_5:
            st.write(' ')
            st.write(' ')
            st.write(':red[请确认加载的Tehcwiz仿真数据以及BLU和RGB光谱!]')
    # except ZeroDivisionError:
    #     with bz5_5:
    #         st.write(' ')
    #         st.write(' ')
    #         st.write(':red[请检查<步骤2：仿真参数>是否正确!]')

# 编辑button - Final计算
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(14) > div.st-emotion-cache-vft1hk.e1f1d6gn3 > div > div > div > div > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px !important;
    width: 150px !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑techwiz数据加载button1
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(10) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div:nth-child(1) > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑techwiz数据加载button2
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(10) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > section > button
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
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(12) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div:nth-child(1) > div > section > button
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
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(12) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > section > button
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
