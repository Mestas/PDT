import streamlit as st
from shapely.geometry import Polygon

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>This tools can calculate the Color Gamut and Color Coverage</h4>", unsafe_allow_html=True)

# # # 工具名称、版本号
st.write("# Color Gamut Calculater #")
    
def calculate_overlap_area(triangle1, triangle2):
    # 创建Shapely的多边形对象
    polygon1 = Polygon(triangle1)
    polygon2 = Polygon(triangle2)

    # 计算两个多边形的重叠部分
    overlap = polygon1.intersection(polygon2)

    # 返回重叠部分的面积
    return overlap.area

# # # 设置步骤1
col1, col2 = st.columns([1, 2])
bz1_1, bz1_2, bz1_3, bz1_4 = st.columns([1, 2, 2, 8])
with col1:
    st.write(' ')
    st.write("<h6>step1: Input Sample Color Coordinate</h6>", unsafe_allow_html=True)
with bz1_2:
    Rx = st.number_input(label='**Rx**', format='%f', key='Rx')
    Gx = st.number_input(label='**Gx**', format='%f', key='Gx')
    Bx = st.number_input(label='**Bx**', format='%f', key='Bx')
with bz1_3:
    Ry = st.number_input(label='**Ry**', format='%f', key='Ry')
    Gy = st.number_input(label='**Gy**', format='%f', key='Gy')
    By = st.number_input(label='**By**', format='%f', key='By')

# # # 设置步骤2
col3, col4 = st.columns([1, 2])
bz2_1, bz2_2, bz2_3, bz2_4 = st.columns([1, 4, 2, 6])
bz2_11, bz2_12, bz2_13, bz2_14 = st.columns([1, 2, 2, 8])
with col3:
    st.write(' ')
    st.write("<h6>step2: Select Standard Color Coordinate</h6>", unsafe_allow_html=True)
with bz2_2:
    spMenu = ('sRGB', 'DCI-P3', 'Adobe', 'BT2020', 'NTSC')
    Standard_Color = st.selectbox('**Select Standard Color**', spMenu, key='Standard')
    if Standard_Color == spMenu[0]:
        Rx0 = 0.640
        Ry0 = 0.330
        Gx0 = 0.300
        Gy0 = 0.600
        Bx0 = 0.150
        By0 = 0.060
    elif Standard_Color == spMenu[1]:
        Rx0 = 0.680
        Ry0 = 0.320
        Gx0 = 0.265
        Gy0 = 0.690
        Bx0 = 0.150
        By0 = 0.060
    elif Standard_Color == spMenu[2]:
        Rx0 = 0.640
        Ry0 = 0.330
        Gx0 = 0.210
        Gy0 = 0.710
        Bx0 = 0.150
        By0 = 0.060
    elif Standard_Color == spMenu[3]:
        Rx0 = 0.708
        Ry0 = 0.292
        Gx0 = 0.170
        Gy0 = 0.797
        Bx0 = 0.131
        By0 = 0.046
    elif Standard_Color == spMenu[4]:
        Rx0 = 0.670
        Ry0 = 0.330
        Gx0 = 0.210
        Gy0 = 0.710
        Bx0 = 0.140
        By0 = 0.080

with bz2_12:
    Rx0 = st.number_input(label='**Rx**', value=Rx0, disabled=True, format='%f', key='Rx0')
    Gx0 = st.number_input(label='**Gx**', value=Gx0, disabled=True, format='%f', key='Gx0')
    Bx0 = st.number_input(label='**Bx**', value=Bx0, disabled=True, format='%f', key='Bx0')
with bz2_13:
    Ry0 = st.number_input(label='**Ry**', value=Ry0, disabled=True, format='%f', key='Ry0')
    Gy0 = st.number_input(label='**Gy**', value=Gy0, disabled=True, format='%f', key='Gy0')
    By0 = st.number_input(label='**By**', value=By0, disabled=True, format='%f', key='By0')

# # # 设置步骤3
col5, col6 = st.columns([1, 2])
bz3_1, bz3_2, bz3_3, bz3_4, bz3_5 = st.columns([1, 4, 4, 4, 1])
bz4_1, bz4_2, bz4_3, bz4_4, bz4_5 = st.columns([1, 4, 4, 4, 1])
with col5:
    st.write(' ')
    st.write("<h6>step3: Click to Calculate</h6>", unsafe_allow_html=True)

# 点击button计算色域
with bz3_2:
    cal_color_gamut = st.button('***Calc Color Gamut***', key='color gamut')

# # # main code
if cal_color_gamut:
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
    new_content = user_name + '于' + date + '使用了《12-Color Gamut计算工具 (V1.0)》;  ' + '\n'

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

    # 输入两个三角形的顶点坐标
    triangle1 = [(Rx, Ry), (Gx, Gy), (Bx, By)]
    triangle2 = [(Rx0, Ry0), (Gx0, Gy0), (Bx0, By0)]
    # 计算重叠面积
    area_overlap = calculate_overlap_area(triangle1, triangle2)
    # 计算标准色的面积
    area_standard_color = (Rx0 * Gy0 + Gx0 * By0 + Bx0 * Ry0 - Ry0 * Gx0 - Gy0 * Bx0 - By0 * Rx0) * 0.5

    # 计算评估颜色的色域及覆盖率
    color_gamut = (Rx * Gy + Gx * By + Bx * Ry - Ry * Gx - Gy * Bx - By * Rx) * 0.5 / 0.1582
    standard_gamut = (Rx0 * Gy0 + Gx0 * By0 + Bx0 * Ry0 - Ry0 * Gx0 - Gy0 * Bx0 - By0 * Rx0) * 0.5 / 0.1582
    color_coverage = area_overlap / area_standard_color

    # 显示结果
    str_color_gamut = str(str(round(color_gamut * 100, 2)) + '%')
    str_color_coverage = str(str(round(color_coverage * 100, 2)) + '%')
    str_standard_gamut = str(str(round(standard_gamut * 100, 2)) + '%')
    
    with bz4_2:
        st.text_input(label='**Sample Color Gamut(NTSC)**', value=str_color_gamut, key='color_gamut')
    with bz4_3:
        st.text_input(label='**Standard Color Gamut(NTSC)**', value=str_standard_gamut, key='standard_gamut')
    with bz4_4:
        st.text_input(label='**Sample Color Coverage**', value=str_color_coverage, key='color_coverage')

# 编辑Standard color selectbox
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(5) > div.st-emotion-cache-14nh3c1.e1f1d6gn3 > div > div > div > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    height: 40px !important;
    width: 200px !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑Calc_color_Gamut button
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(8) > div:nth-child(2) > div > div > div > div > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 60px !important;
    width: 200px !important;
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

# 设置input和output的背景
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div:nth-child(2) > div > div > div > div:nth-child(1) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div:nth-child(3) > div > div > div > div:nth-child(1) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div:nth-child(2) > div > div > div > div:nth-child(2) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div:nth-child(3) > div > div > div > div:nth-child(2) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div:nth-child(2) > div > div > div > div:nth-child(3) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div:nth-child(3) > div > div > div > div:nth-child(3) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }

    
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div:nth-child(2) > div > div > div > div:nth-child(1) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div:nth-child(3) > div > div > div > div:nth-child(1) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div:nth-child(2) > div > div > div > div:nth-child(2) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div:nth-child(3) > div > div > div > div:nth-child(2) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div:nth-child(2) > div > div > div > div:nth-child(3) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div:nth-child(3) > div > div > div > div:nth-child(3) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(9) > div:nth-child(2) > div > div > div > div > div > div.st-ae.st-af.st-ag.st-ah.st-ai.st-aj.st-ak.st-al.st-am.st-an.st-ao.st-ap.st-aq.st-ar.st-as.st-at.st-au.st-av.st-aw.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7.st-b8.st-b9 > div
    {
    background-color: rgb(200, 240, 240);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(9) > div:nth-child(3) > div > div > div > div > div > div.st-ae.st-af.st-ag.st-ah.st-ai.st-aj.st-ak.st-al.st-am.st-an.st-ao.st-ap.st-aq.st-ar.st-as.st-at.st-au.st-av.st-aw.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7.st-b8.st-b9 > div
    {
    background-color: rgb(200, 240, 240);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(9) > div:nth-child(4) > div > div > div > div > div > div.st-ae.st-af.st-ag.st-ah.st-ai.st-aj.st-ak.st-al.st-am.st-an.st-ao.st-ap.st-aq.st-ar.st-as.st-at.st-au.st-av.st-aw.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7.st-b8.st-b9 > div
    {
    background-color: rgb(200, 240, 240);
    }
    </style>
    ''',
    unsafe_allow_html=True
)
