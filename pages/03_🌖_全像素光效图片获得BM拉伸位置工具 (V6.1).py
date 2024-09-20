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

import numpy as np
from scipy.stats import norm


# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具由Techwiz全像素光效图获得BM内缩距离</h4>", unsafe_allow_html=True)


# # # 工具名称、版本号
st.write("# 全像素光效图获得BM内缩距离工具 #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V1.0</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2023/12/18</h5>", unsafe_allow_html=True)


# # # 设置步骤1
st.write("<h6>步骤1：请上传Techwiz仿真的全像素图片</h6>", unsafe_allow_html=True)
# 上传图片，files为ByteIO的子类
col1, col2, col3 = st.columns([1, 20, 1])
with col2:
    file = st.file_uploader("请选择bmp图片文件", type=['bmp'], help="请选择bmp图片进行上传")
# fn = file.name
    if file is not None:
        img = Image.open(file)
        Pic_gray = img.convert("L")  # 将图片转换为灰阶
        pic_w, pic_h = Pic_gray.size

        if pic_h == 1056 and pic_w == 1936:
            st.write('图片读取成功')
        else:
            st.write('图片分辨率错误，请确认后重新上传！')
                
# # # 设置步骤2
st.write("<h6>步骤2：填写像素信息</h6>", unsafe_allow_html=True)
col21, col22, col23, col24, col25 = st.columns([1, 3, 1, 3, 10])
with col22:
    pixel_w = st.number_input(label='Pixel宽度', format='%f', key=2)  # 像素实际尺寸-X方向 -------
with col24:
    pixel_h = st.number_input(label='Pixel高度', format='%f', key=1)    # 像素实际尺寸-Y方向 -------

# # # 设置步骤3
st.write("<h6>步骤3：填写灰阶数 (同CAD中输入的灰阶数)</h6>", unsafe_allow_html=True)
col31, col32, col33, col34 = st.columns([1, 3, 3, 11])
with col32:
    L = int(st.number_input(label='灰阶过渡数', format='%f', key=3) + 1.0)  # 灰阶过渡数 -------

# # # 设置步骤4，设置点击按钮，并进入Main code
st.write("<h6>步骤4：点击按钮获取数据</h6>", unsafe_allow_html=True)
bz41, bz42, bz43 = st.columns([1, 6, 15])
bz44, bz45, bz46 = st.columns([1, 11, 10])
with bz42:
    calc = st.button('***点击计算***', key=4)
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
    new_content = user_name + '于' + date + '使用了《03-全像素光效图片获得BM拉伸位置工具 (V6.1)》;  ' + '\n'

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
        # # 从techwiz图片中找到Pixel边界
        for iu in range(120, 530):
            if Pic_gray.getpixel((850, iu)) == 255 and Pic_gray.getpixel((850, iu + 1)) == 0:
                u = iu + 1
        for id in range(590, 1000):
            if Pic_gray.getpixel((850, id)) == 0 and Pic_gray.getpixel((850, id + 1)) == 255:
                d = id
        for jl in range(600, 850):
            if Pic_gray.getpixel((jl, u)) == 255 and Pic_gray.getpixel((jl + 1, u)) == 0:
                l = jl + 1
        for jr in range(850, 1200):
            if Pic_gray.getpixel((jr, u)) == 0 and Pic_gray.getpixel((jr + 1, u)) == 255:
                r = jr

        # # 提取后的Pixel灰阶信息
        gray_imgs = Pic_gray.crop((l, u, r + 1, d + 1))
        # 获取所有像素的灰阶数值
        w, h = gray_imgs.size
        Pixel_gray = np.zeros((h, w))
        for i in range(h):
            for j in range(w):
                Pixel_gray[i, j] = gray_imgs.getpixel((j, i))
        Pixel_trans = (Pixel_gray / 255) ** 2.2  # 将图片灰阶转换为透过率
        # st.write(Pixel_gray)
        c_h = math.ceil(h / 2)  # Pixel像素行中心点
        c_w = math.ceil(w / 2)  # Pixel像素列中心点
        ave_h = pixel_h / h  # 每个图片像素所代表实际pixel的尺寸-Y方向
        ave_w = pixel_w / w  # 每个图片像素所代表实际pixel的尺寸-X方向

        # # 创建M行N列数组AA_BM，第一行为开口区最上方BM行数，第二行为开口区最下方BM行数
        M = 2
        N = w
        AA_BM = [None] * M
        for i in range(len(AA_BM)):
            AA_BM[i] = [0] * N

        for i in range(h - 1):
            for j in range(w):
                if Pixel_gray[i, j] < 10 and Pixel_gray[i + 1, j] > 10:
                    AA_BM[0][j] = i + 1
                elif Pixel_gray[i, j] > 10 and Pixel_gray[i + 1, j] < 10:
                    AA_BM[1][j] = i + 1
        # # 将数组中为0的数据用255替换，以便找到真正的Top BM最小pixel数量
        for i in range(M):
            for j in range(N):
                if AA_BM[i][j] == 0 or AA_BM[i][j] == 1:
                    AA_BM[i][j] = int(c_h)
        # # 找到pixel开口top(min_aa)和bottom(max_aa)位置
        AA_BM = [i for j in AA_BM for i in j]

        min_aa = min(AA_BM)
        max_aa = max(AA_BM)

        # # 开口区中心行数为aa_c_h
        aa_h = max_aa - min_aa
        aa_c_h = math.ceil(aa_h / 2)

        # # 将开口区从Pixel中截取出来，生成数组AA_gray和AA_trans
        # 首先创建空AA_gray和AA_trans数组，size为aa_h行*w列
        AA_gray = [None] * aa_h
        for i in range(len(AA_gray)):
            AA_gray[i] = [0] * w

        AA_trans = [None] * aa_h
        for i in range(len(AA_trans)):
            AA_trans[i] = [0] * w

        for i in range(aa_h):
            for j in range(w):
                AA_gray[i][j] = Pixel_gray[i + min_aa][j]
                AA_trans[i][j] = Pixel_trans[i + min_aa][j]

        # # 以下为计算各行透过率累加结果，最终输出各行透过率关系trans_h
        sum_h = []
        for i in range(aa_c_h):
            sum_h.append([-1 for x in range(aa_c_h)])
            # 判断中心点为偶数行，第一行的为0，其余数据为分别进行上下单行累加
            if divmod(aa_h, 2)[1] == 0 and i == 0:
                sum_h[i] = 0
                sum_hh = np.array(sum_h)
            elif divmod(aa_h, 2)[1] == 0 and i > 0:
                sum_h[i] = sum(AA_trans[aa_c_h - i] + AA_trans[aa_c_h - 1 + i])
                sum_hh = np.array(sum_h)
            # 判断中心点为奇数行，第一行的为中心点所在行，其余数据为分别行进行上下单行累加
            elif divmod(aa_h, 2)[1] != 0 and i == 0:
                sum_h[i] = sum(AA_trans[aa_c_h - 1])
                sum_hh = np.array(sum_h)
            elif divmod(aa_h, 2) != 0 and i > 0:
                sum_h[i] = sum(AA_trans[aa_c_h - 1 - i] + AA_trans[aa_c_h - 1 + i])
                sum_hh = np.array(sum_h)
        # print(sum_hh)
        # # 将上下单行累加的进行复加，获得行数与透过率对应阵列trans_h
        trans_h1 = 0
        trans_hh = []
        for i in range(aa_c_h):
            trans_hh.append([-1 for x in range(aa_c_h)])
            trans_h1 += sum_hh[i]
            # print(trans_h1)
            trans_hh[i] = trans_h1

        trans_hhh = []
        for i in range(aa_c_h):
            trans_hhh.append([-1 for x in range(aa_c_h)])
            trans_hhh[i] = trans_hh[i] / trans_hh[aa_c_h - 1]

        # 将像素数和透过率对应起来，最终生成trans_h矩阵
        df1 = pd.DataFrame(trans_hhh)
        trans_hdf = df1.stack()
        trans_hdf1 = trans_hdf.values

        M = aa_c_h
        N = 2
        trans_h = [None] * M
        for i in range(len(trans_h)):
            trans_h[i] = [0] * N
        for i in range(aa_c_h):
            trans_h[i][0] = i
            trans_h[i][1] = trans_hdf1[i]

        # # 输出全灰阶 + 全灰阶BM拉伸情况
        M = 256
        N = 7
        G2BM = [None] * M
        for i in range(len(G2BM)):
            G2BM[i] = [0] * N

        for i in range(256):
            G2BM[i][0] = i
            G2BM[i][1] = (i / 255) ** 2.2

        # print(aa_c_h)
        for i in range(256):
            for j in range(aa_c_h):
                if G2BM[i][1] > trans_h[j][1] and G2BM[i][1] < trans_h[j + 1][1]:
                    G2BM[i][3] = trans_h[j][1]  # 透过率夹在中间的值
                    G2BM[i][4] = trans_h[j][0]  # 透过率对应的BM从中心到上端像素数量

        G2BM[255][2] = 0  # 设置0灰阶对应透过率
        G2BM[255][3] = 1  # 设置255灰阶对应透过率
        G2BM[255][4] = aa_c_h

        # # 设置BM拉伸距离，显示在G2BM[i][5]位置
        for i in range(256):
            for j in range(aa_c_h):
                if G2BM[i][1] > trans_h[j][1] and G2BM[i][1] < trans_h[j + 1][1]:
                    if divmod(aa_c_h, 2)[1] != 0 and G2BM[i][
                        4] == 0:  # 若开口区为奇数行，那么trans_h[0] 代表的是最中间的那一行，若考虑拉伸的话，需要 中间行/2
                        G2BM[i][2] = (aa_c_h - 0.5 - (
                                    (G2BM[i][1] - G2BM[i][3]) / (trans_h[j + 1][1] - trans_h[j][1])) / 2) * ave_h
                        G2BM[i][5] = (G2BM[i][1] - G2BM[i][3]) / (trans_h[j + 1][1] - trans_h[j][1]) * ave_h
                    elif divmod(aa_c_h, 2)[1] != 0 and G2BM[i][
                        4] != 0:  # 若开口区为奇数行，那么trans_h[0] 代表的是最中间的那一行，若考虑拉伸的话，需要 中间行/2
                        G2BM[i][2] = (aa_c_h - 0.5 - (
                                    (G2BM[i][1] - G2BM[i][3]) / (trans_h[j + 1][1] - trans_h[j][1]) + G2BM[i][
                                4] + 0.5)) * ave_h
                        G2BM[i][5] = (((G2BM[i][1] - G2BM[i][3]) / (trans_h[j + 1][1] - trans_h[j][1]) + G2BM[i][
                            4]) * 2 + 1) * ave_h
                        G2BM[255][5] = aa_h * ave_h
                    elif divmod(aa_c_h, 2)[1] == 0:
                        G2BM[i][2] = (aa_c_h - (
                                    (G2BM[i][1] - G2BM[i][3]) / (trans_h[j + 1][1] - trans_h[j][1]) + G2BM[i][
                                4])) * ave_h
                        G2BM[i][5] = ((G2BM[i][1] - G2BM[i][3]) / (trans_h[j + 1][1] - trans_h[j][1]) + G2BM[i][
                            4]) * 2 * ave_h

        # # 设置将Space < 4um的做成正方形，显示在G2BM[i][6]位置
        for i in range(256):
            for j in range(aa_c_h):
                if G2BM[i][5] < 4:
                    G2BM[i][6] = (G2BM[i][3] * trans_hh[aa_c_h - 1]) ** 0.5 * ave_h

        # # 定义灰阶对应BM拉伸的对应矩阵Final
        X = 256  # 定义Final总行数
        Y = 2  # 定义Final总列数
        Final_List = [None] * X
        for i in range(len(Final_List)):
            Final_List[i] = [0] * Y

        for i in range(256):
            Final_List[i][0] = i
            if G2BM[i][5] > 4:
                Final_List[i][1] = round(G2BM[i][2], 2)
            else:
                Final_List[i][1] = round(G2BM[i][6], 2)

        # # 设置最终数据
        f_h = L  # 定义Final总行数
        f_l = 3  # 定义Final总列数
        Final = [None] * f_h
        for i in range(len(Final)):
            Final[i] = [0] * f_l

        Final[0][0] = str('gray')
        Final[0][1] = str('up neisuo')
        Final[0][2] = str('down neisuo')

        trans_step = 1 / L
        for i in range(1, L):
            Final[i][0] = round((i * trans_step) ** (1 / 2.2) * 255)
            Final[i][1] = Final_List[Final[i][0]][1]
            Final[i][2] = Final[i][1]

        # # 设置显示
        col51, col52, col53, col54, col55, col56, col57, col58, col59 = st.columns([1, 18, 1, 8, 0.5, 8, 0.5, 8, 1])
        # 显示最终数据
        df2 = pd.DataFrame(Final)
        with col52:
            st.write("<h7>最终数据</h7>", unsafe_allow_html=True)
            st.write(df2)
        # 显示整个Pixel图片
        with col54:
            st.write("<h7>像素图</h7>", unsafe_allow_html=True)
            st.image(Pixel_gray, clamp=True)
        # 显示BM拉伸后的Pixel图片
        Final_BM = np.zeros((h, w))
        Final_BM[0:int(h/3), :] = 0
        Final_BM[int(h/3):int(2*h/3)] = Pixel_gray[int(h/3):int(2*h/3)]
        Final_BM[int(2*h/3):h+1, :] = 0
        with col56:
            st.write("<h7>BM遮挡图</h7>", unsafe_allow_html=True)
            st.image(Final_BM, clamp=True)
        # 显示仅Pixel开口区图片
        Pic_AR = Pixel_gray[min_aa:max_aa, :]
        with col58:
            st.write("<h7>像素开口区</h7>", unsafe_allow_html=True)
            st.image(Pic_AR, clamp=True)

    except AttributeError:
        with bz43:
            st.write(' ')
            st.write(' ')
            st.write(':red[请确认所有项目已填写完成1!]')
    # except ValueError:
    #     with bz43:
    #         st.write(' ')
    #         st.write(' ')
    #         st.write(':red[请确认所有项目已填写完成2!]')
    except NameError:
        with bz43:
            st.write(' ')
            st.write(' ')
            st.write(':red[请加载Techwiz图片!]')
    # except ZeroDivisionError:
    #     with bz43:
    #         st.write(' ')
    #         st.write(' ')
    #         st.write(':red[请检查<步骤2：仿真参数>是否正确!]')

# 编辑button - Final计算
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(10) > div.st-emotion-cache-17xod8c.e1f1d6gn3 > div > div > div > div > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px !important;
    width: 150px !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑bmp图片上传按钮
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(4) > div.st-emotion-cache-ulq27u.e1f1d6gn3 > div > div > div > div > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(4) > div.st-emotion-cache-ulq27u.e1f1d6gn3 > div > div > div > div > div > section > button
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
