import streamlit as st

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
#     st.write("<h4 style='color: blue;'>作者：陈延青</h4>", unsafe_allow_html=True)

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
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-vk3wp9.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3
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
namelist = ['cyan', '刘晓辉', '刘瑞超', '任静峰', '陈凯', '李泽亮', '吴兆君', '李小艳', '张小凤', '纪浩晨', '许曦', '佟洁', '栗晓亚', '梁鹏', '王宁', '李忻放', '赵云鹭', '张海漠', '刘晓那', '李岩锋', '胡倩语', '李慧田']
if btn is True:
    if p > 0 and name in namelist:
        load_name = str(name + ' 登录成功，欢迎使用')

        with col16:
            st.write(f"<span style='color: blue;'>{load_name}</span>", unsafe_allow_html=True)
        
        # 将name信息保存到session状态中
        st.session_state['user_name'] = name  # 将用户输入存储在会话状态中

        # 将登录者信息保存到《网站使用者.txt》文件中
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
        new_content = name + '于' + date + '进行了登录;  ' + '\n'

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

        # 设置引导栏
        st.write("### 👈 请在左侧边栏点击想要使用的工具 ###")

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
        # 设置按钮底色
        st.markdown(
            '''
            <style>
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div.st-emotion-cache-ndxjbj.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > button
            {
                 background-color: rgb(220, 240, 220);
                 height: 60px;
                 width: 120px;
            }
            </style>
            ''',
            unsafe_allow_html=True
        )

        # 设置侧边栏隐藏
        st.markdown(
            '''
            <style>
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-vk3wp9.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3
            {
            visibility: visible !important;
            }
            </style>
            ''',
            unsafe_allow_html=True
        )
        
    elif p > 0 and name not in namelist:
        with col26:
            st.write('请联系作者，注册后使用')
    elif p == 0:
        with col26:
            st.write('请输入姓名，登录后使用')

# # # 增加cyan账户权限
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

if name == 'cyan':
    st.write(file_content)
else:
    st.write(' ')
# 设置按钮底色
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div.st-emotion-cache-ndxjbj.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > button
    {
         background-color: rgb(220, 240, 220);
         height: 60px;
         width: 120px;
    }
    </style>
    ''',
    unsafe_allow_html=True
)
# 设置名字输入栏底色
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
