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
        new_content = user_name + '于' + date + '使用了《11-整数波长处理工具 (V1.0) - 1nm step》;  ' + '\n'

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
        new_content = user_name + '于' + date + '使用了《11-整数波长处理工具 (V1.0) - 5nm step》;  ' + '\n'

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
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div:nth-child(1) > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px !important;
    width: 160px !important;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px !important;
    width: 160px !important;
    }
    
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(4) > div.st-emotion-cache-1duevtu.e1f1d6gn3 > div > div > div > div > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    </style>
    ''',
    unsafe_allow_html=True
)
