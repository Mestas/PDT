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

try:
    os.makedirs('users', exist_ok=True)
    fp_save = 'users/网站使用者.txt'
    mode = 'a'
    with open(fp_save, mode) as f:
        f.write('使用了CA410数据处理工具' + '\n')
except Exception as e:
    st.error(f"无法写入文件: {e}")
