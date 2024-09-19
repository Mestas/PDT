import os
import streamlit as st
import pandas as pd

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具确认是否存在网站使用者.txt</h4>", unsafe_allow_html=True)


# # # 工具名称、版本号
st.write("# 内部测试用 #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：Vbeta</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2999/12/31</h5>", unsafe_allow_html=True)

def write_txt(new_content):
    import requests
    import json
    import base64
    from hashlib import sha1

    # 从 Streamlit Secret 获取 GitHub PAT
    github_pat = st.secrets['github_token']

    # GitHub 仓库信息
    owner = 'Mestas'  # 仓库所有者
    repo = 'PDT'  # 仓库名称
    branch = 'main'  # 分支名称
    filepath = 'users/网站使用者.txt'  # 文件路径

    # # 文件内容
    # content = '测试数据'

    # 计算内容的 SHA1 哈希值
    encoded_content = new_content.encode('utf-8')
    content_sha1 = sha1(encoded_content).hexdigest()

    # 将内容转换为 Base64 编码
    encoded_content_base64 = base64.b64encode(encoded_content).decode('utf-8')

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
        existing_content = base64.b64decode(file_data['content'])
        # 将新内容追加到现有内容
        updated_content = existing_content + new_content.encode('utf-8')
        # 计算更新后内容的 SHA1 哈希值
        content_sha1 = sha1(updated_content).hexdigest()
    else:
        # 如果文件不存在，就创建新文件
        updated_content = new_content.encode('utf-8')
        content_sha1 = sha1(updated_content).hexdigest()

    # 构建请求体
    data = {
        "message": "Update file via Streamlit",
        "content": encoded_content_base64,
        "branch": branch,
        "sha": file_data['sha'] if response.status_code == 200 else None  # 如果文件不存在，这将被忽略
    }

    # 发送请求以更新文件内容
    response = requests.put(api_url, headers=headers, data=json.dumps(data))

    # 检查响应状态
    if response.status_code == 200:
        # 请求成功，显示成功信息
        st.success('File updated successfully on GitHub!')
    else:
        # 请求失败，显示错误信息
        st.error(f'Error: {response.status_code}')
        st.write(response.text)

def read_txt():
    import requests
    import base64

    # GitHub 仓库信息
    owner = 'Mestas'  # 仓库所有者
    repo = 'PDT'  # 仓库名称
    branch = 'main'  # 分支名称
    filepath = 'users/网站使用者.txt'  # 文件路径

    # GitHub API URL
    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{filepath}'

    # 设置请求头
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    # 发送请求以获取文件内容
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        file_data = response.json()
        # 解码 Base64 内容
        file_content = base64.b64decode(file_data['content']).decode('utf-8')
        print(file_content)
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

    return file_content

write = st.button('点击计算', key='pushbutton1')
if write is True:
    try:
        word = '使用了CA410数据处理工'
        write_txt(word)
        st.write('写入成功')
    except Exception as e:
        # st.error(f"无法写入文件: {e}")
        st.write('写入失败')


read = st.button('点击读取', key='pushbutton2')
if read is True:
    try:
        txtcontent = read_txt()
        st.write(txtcontent)

    except Exception as e:
        # st.error(f"无法读取文件: {e}")
        st.write('读取失败')

# check = st.button('点击查看', key='pushbutton3')
# if check is True:
#     try:
#         files_and_dirs = os.listdir('.')
#         for item in files_and_dirs:
#             st.write(item)
#     except Exception as e:
#         # st.error(f"无法读取文件: {e}")
#         st.write('读取失败')

