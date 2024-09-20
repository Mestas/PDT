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
    new_content = user_name + '于' + date + '使用了《14-图片信息获取工具 (V1.0) - 图片转Trans》;  ' + '\n'

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

elif cal_button_csv:
    start_time = time.time()
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
    new_content = user_name + '于' + date + '使用了《14-图片信息获取工具 (V1.0) - 图片转CSV》;  ' + '\n'

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

elif cal_button_base64:
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
    new_content = user_name + '于' + date + '使用了《14-图片信息获取工具 (V1.0) - 图片转base64》;  ' + '\n'

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

# 编辑计算按钮底色
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(5) > div.st-emotion-cache-1l269bu.e1f1d6gn3 > div > div > div > div:nth-child(1) > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px;
    width: 150px;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(5) > div.st-emotion-cache-1l269bu.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px;
    width: 150px;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(5) > div.st-emotion-cache-1l269bu.e1f1d6gn3 > div > div > div > div:nth-child(3) > div > button
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
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(4) > div > section > button
    {
    background-color: rgb(220, 240, 220);
    text = "点击加载";
    }
    </style>
    ''',
    unsafe_allow_html=True
)
