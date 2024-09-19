import os
import streamlit as st
import pandas as pd

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered",
)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具用来获取网站使用者.txt</h4>", unsafe_allow_html=True)


# # # 工具名称、版本号
st.write("# 网站使用者获取 #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V9999</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：9999/99/99</h5>", unsafe_allow_html=True)
    
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

    # 检查响应状态
    if response.status_code == 200:
        # 请求成功，显示成功信息
        print('File updated successfully on GitHub!')
    else:
        # 请求失败，显示错误信息
        print(f'Error: {response.status_code}')
        print(response.text)

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

# 输入用户名
col11, col12 = st.columns([2, 8])
with col11:
    name = st.text_input('请输入用户名后进行查看', key=1)
p = len(name)
namelist = ['administrator']

read = st.button('读取数据', key='pushbutton2')
if read is True:
    if p > 0 and name in namelist:
        try:
            txtcontent = read_txt()
            st.write(txtcontent)
    
        except Exception as e:
            # st.error(f"无法读取文件: {e}")
            st.write('读取失败')
    else:
        st.write("<h6 style='color: red;'>对不起，您无权限查看该文件内容！</h6>", unsafe_allow_html=True)
        
# if btn is True:
#     if p > 0 and name in namelist:
#         write = st.button('写入数据', key='pushbutton1')
#         if write is True:
#             try:
#                 word = '写入测试数据;  ' +'\n'
#                 write_txt(word)
#                 st.write('写入成功')
#             except Exception as e:
#                 # st.error(f"无法写入文件: {e}")
#                 st.write('写入失败')
        

# 设置按钮底色
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(4) > div > button
    {
        background-color: rgb(220, 240, 220);
        height: 60px;
        width: 120px;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div > button
    {
        background-color: rgb(220, 240, 220);
        height: 60px;
        width: 120px;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div.st-emotion-cache-ndxjbj.e1f1d6gn3 > div > div > div > div > div > div > div
    {
        background-color: rgb(220, 240, 220);
    }
    </style>
    ''',
    unsafe_allow_html=True
)
