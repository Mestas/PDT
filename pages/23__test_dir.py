import os
import streamlit as st

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
import requests

def get_github_user_info(token):
    url = "https://api.github.com/user"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

user_info = get_github_user_info(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)
st.write(user_info)

write = st.button('点击计算', key='pushbutton1')
if write is True:
    try:
        os.makedirs('users', exist_ok=True)
        fp_save = 'users/网站使用者.txt'
        mode = 'a'
        with open(fp_save, mode) as f:
            f.write('使用了CA410数据处理工具' + '\n')
        st.write('写入成功')
    except Exception as e:
        # st.error(f"无法写入文件: {e}")
        st.write('写入失败')

read = st.button('点击读取', key='pushbutton2')
if read is True:
    try:
        fname = 'users/网站使用者.txt'
        data = pd.read_csv(fname, header=None, sep="\t", skip_blank_lines=True)
        st.write(data)

    except Exception as e:
        # st.error(f"无法读取文件: {e}")
        st.write('读取失败')

check = st.button('点击查看', key='pushbutton3')
if check is True:
    try:
        files_and_dirs = os.listdir('.')
        for item in files_and_dirs:
            st.write(item)
    except Exception as e:
        # st.error(f"无法读取文件: {e}")
        st.write('读取失败')
