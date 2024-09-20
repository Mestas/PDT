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
    calc = st.button("***点击计算***")
if calc is True:
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
    new_content = user_name + '于' + date + '使用了《09-CA410数据处理工具 (V1.0)》;  ' + '\n'

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

# 编辑点击计算按钮
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(5) > div.st-emotion-cache-1l269bu.e1f1d6gn3 > div > div > div > div > div > button
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
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(4) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    </style>
    ''',
    unsafe_allow_html=True
)
