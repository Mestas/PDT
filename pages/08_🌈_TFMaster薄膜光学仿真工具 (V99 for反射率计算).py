import glob
import os
import colour
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import tmm
from scipy.interpolate import interp1d
import time

from decimal import Decimal, getcontext
precision = 10

getcontext().prec = precision

st.set_page_config(
    page_title="Thin Film Master",
    page_icon="🌈",
    initial_sidebar_state="auto",
    layout="wide"
)

wl_min = 380.0
wl_max = 780.0
wl_pitch = 1.0
inc_angle = 0.0

inc_wl = 550.0
inc_angle_min = 0.0
inc_angle_max = 85.0
inc_angle_pitch = 1.0

# nlayers = 1

# nk_idx_subst = 0
nk_idx_film = 0

def order_n(i):
    return {1: "1st (top)", 2: "2nd", 3: "3rd"}.get(i) or "%dth" % i

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

@st.cache_data
def get_nk_list():
    """
    获取指定目录中的 nk 文件名列表
    Returns
    name_list : list of str
        文件名列表
    """
    nk_list = []  # 存储文件名的列表
    nk_dirs = "source/material/"  # 指定 nk 文件所在的目录
    files = os.listdir(nk_dirs)  # 列出目录中的所有文件和子目录
    nk_files = [f for f in files if os.path.isfile(os.path.join(nk_dirs, f))]  # 仅筛选出真正的文件

    for nk_file in nk_files:
        # 获取每个文件的基本名称，即去除扩展名的文件名
        basename = os.path.splitext(os.path.basename(nk_file))[0]
        nk_list.append(basename)  # 将文件的基本名称添加到列表中

    # 如果找不到 nk 数据，输出错误消息
    if len(nk_list) < 1:
        st.error('在 ' + nk_dirs + ' 中未找到 nk 数据')
        files_data = glob.glob("data")
        st.error('data 目录下的文件 =', files_data)
        files_nk = glob.glob("source/material/")
        st.error('material 目录下的文件 =', files_nk)

    nk_list.sort()  # 对文件名列表进行排序
    return nk_list
    
def get_blu_list():
    """
    获取指定目录中的blu文件名列表
    Returns
    blu_list : list of str
        文件名列表
    """
    blu_list = []  # 存储文件名的列表
    blu_dirs = "source/backlight/"  # 指定blu文件所在的目录
    files = os.listdir(blu_dirs)  # 列出目录中的所有文件和子目录
    blu_files = [f for f in files if os.path.isfile(os.path.join(blu_dirs, f))]  # 仅筛选出真正的文件

    for blu_file in blu_files:
        # 获取每个文件的基本名称，即去除扩展名的文件名
        basename = os.path.splitext(os.path.basename(blu_file))[0]
        blu_list.append(basename)  # 将文件的基本名称添加到列表中

    # 如果找不到blu数据，输出错误消息
    if len(blu_list) < 1:
        st.error('在 ' + blu_dirs + ' 中未找到backlight数据')
        files_data = glob.glob("data")
        st.error('data 目录下的文件 =', files_data)
        files_blu = glob.glob("source/backlight/")
        st.error('backlight 目录下的文件 =', files_blu)

    blu_list.sort()  # 对文件名列表进行排序
    return blu_list

def calc_nk_list(nk_fn_list, wl):
    """
    根据光学定数的函数列表和给定波长，返回薄膜的光学定数列表
    Parameters
    ----------
    nk_fn_list : list of fn(wl)
        光学定数的函数列表.
    wl : float
        波长（单位：纳米）.
    Returns
    -------
    nk_list : array of complex
        各层的光学定数.
    """
    nk_list = []
    for nk in nk_fn_list:
        nk_list.append(nk(wl))
    return nk_list

def make_nk_fn(nk_name_list=[]):
    """
    创建各层的光学定数函数列表
    Parameters
    ----------
    nk_name_list : list of string
        光学定数名的列表.
    Returns
    -------
    nk_fn_list : list of fn(wl)
        各层的光学定数函数列表.
    """
    nk_path = "source/material/"  # nk 文件的路径
    nk_fn_list = []

    # 遍历光学定数名列表
    for idx, nk_name in enumerate(nk_name_list):
        # 如果 nk_name 是复数、浮点数或整数
        if isinstance(nk_name, complex) or isinstance(nk_name, float) or isinstance(nk_name, int):
            nk = complex(nk_name)
            nk_fn = lambda wavelength: nk
        # 如果 nk_name 是字符串且为数字
        elif isinstance(nk_name, str) and str(nk_name).isnumeric():
            nk = float(nk_name)
            nk_fn = lambda wavelength: nk
        else:
            # 构造 nk 文件路径
            fname_path = nk_path + nk_name + '.txt'

            # 如果文件存在
            if os.path.isfile(fname_path):
                # 读取文件数据
                nk_mat = np.loadtxt(fname_path, comments=';', encoding="utf-8_sig")
                w_mat = nk_mat[:, 0]
                n_mat = np.array(nk_mat[:, 1] + nk_mat[:, 2] * 1j)
                # 使用线性插值创建光学定数函数
                nk_fn = interp1d(w_mat, n_mat, kind='linear', fill_value='extrapolate')
            else:
                try:
                    # 尝试将字符串转换为复数
                    nk = complex(nk_name)
                except ValueError:
                    # 如果转换失败，默认使用复数 1.0
                    nk = complex(1.0)
                nk_fn = lambda wavelength: nk
        # 将光学定数函数添加到列表中
        nk_fn_list.append(nk_fn)
    return nk_fn_list

def calc_reflectance(wl_ar, nk_fn_list, d_list, inc_angle=0.0):
    """
    计算光学薄膜的反射率

    Parameters
    ----------
    wl_ar : array of float
        波长（单位：纳米）.
    nk_fn_list : list of fn(wl)
        光学定数函数的列表.
    d_list : array of float
        各层的膜厚（单位：纳米）.
        单层膜: [np.inf, 300, np.inf]  # 第一个元素是介质
    inc_angle : float, optional
        入射角（单位：度）. 默认值是 0.0.

    Returns
    -------
    Rp_ar : array of float
        Rp.
    Rs_ar : array of float
        Rs.
    """
    Rp_ar = np.empty(len(wl_ar), dtype=float)
    Rs_ar = np.empty(len(wl_ar), dtype=float)
    inc_angle_rad = float(inc_angle / 180.0 * np.pi)

    for idx, wl in enumerate(wl_ar):
        n_list = calc_nk_list(nk_fn_list, float(wl))
        Rp_ar[idx] = tmm.inc_tmm('p', n_list, d_list, c_list, inc_angle_rad, float(wl))['R']
        # Rp_ar[idx] = tmm.coh_tmm('p', n_list, d_list, inc_angle_rad, float(wl))['R']
        if inc_angle < 0.01:
            Rs_ar[idx] = Rp_ar[idx]
        else:
            Rs_ar[idx] = tmm.inc_tmm('s', n_list, d_list, c_list, inc_angle_rad, float(wl))['R']
    return Rp_ar, Rs_ar

def calc_transmittance(wl_ar, nk_fn_list, d_list, inc_angle=0.0):
    """
    计算光学薄膜的透射率

    Parameters
    ----------
    wl_ar : array of float
        波长（单位：纳米）.
    nk_fn_list : list of fn(wl)
        光学定数函数的列表.
    d_list : array of float
        各层的膜厚（单位：纳米）.
        单层膜: [np.inf, 300, np.inf]  # 第一个元素是介质
    inc_angle : float, optional
        入射角（单位：度）. 默认是 0.0.

    Returns
    -------
    Tp_ar : array of float
        Tp.
    Ts_ar : array of float
        Ts.
    """
    Tp_ar = np.empty(len(wl_ar), dtype=float)
    Ts_ar = np.empty(len(wl_ar), dtype=float)
    inc_angle_rad = float(inc_angle / 180.0 * np.pi)

    for idx, wl in enumerate(wl_ar):
        n_list = calc_nk_list(nk_fn_list, float(wl))
        Tp_ar[idx] = tmm.inc_tmm('p', n_list, d_list, c_list, inc_angle_rad, float(wl))['T']
        if inc_angle < 0.01:
            Ts_ar[idx] = Tp_ar[idx]
        else:
            Ts_ar[idx] = tmm.inc_tmm('s', n_list, d_list, c_list, inc_angle_rad, float(wl))['T']
    return (Tp_ar, Ts_ar)

def generate_layer_combinations(layer_ranges):
    combinations = [[]]
    for layer_range in layer_ranges:
        start, end, step = layer_range["start"], layer_range["end"], layer_range["step"]
        # print(end)
        if step != 0:
            values = []
            cur_value = Decimal(0.0)
            cur_value += Decimal(start)
            while cur_value <= Decimal(end) + Decimal(1.0 / (precision * 10)):
                values.append(cur_value)
                cur_value += Decimal(step)
            # values = np.arange(start, end, step)
        # 0116：添加判断条件，对于step = 0的layer默认start值
        else:
            values = [Decimal(start)]
        new_combinations = []

        for value in values:
            for combination in combinations:
                new_combinations.append(combination + [value])
        combinations = new_combinations

    return combinations


# # # # # # # # # # 页面设计 # # # # # # # # # # # # # # 

# # # 工具名称、版本号
st.write("# Thin Film Master #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V99</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2025/03/18</h5>", unsafe_allow_html=True)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具可以计算多层薄膜堆叠的反射和透射光学</h4>", unsafe_allow_html=True)

# # # 步骤1
st.write("<h6>步骤1：请进行仿真模式设置</h6>", unsafe_allow_html=True)
bz1_1, bz1_2, bz1_3 = st.columns([1, 8, 20])
bz1_11, bz1_12, bz1_13 = st.columns([1, 15, 13])
bz1_21, bz1_22, bz1_23 = st.columns([1, 15, 13])
with bz1_2:
    # 选择仿真模式（Wavelength Scan 或 Angle Scan）
    calc_mode_menu = ['Wavelength Scan', 'Angle Scan']
    calc_mode = st.radio("---Scan Mode", calc_mode_menu)

# 如果是波长扫描模式
if calc_mode == 'Wavelength Scan':
    # 选择波长范围
    with bz1_12:
        spMenu = ('Visible Light[380-780nm]', 'UV Light[200-400nm]', 'IR Light[700-1000nm]', 'All Wavelength[200-1000nm]', 'Customization')
        wl_option = st.selectbox('---Wavelength Range', spMenu, key='Wavelength range')
        if wl_option == spMenu[0]:
            wl_min = 380.0
            wl_max = 780.0
            # wl_pitch = 1.0
        elif wl_option == spMenu[1]:
            wl_min = 200.0
            wl_max = 400.0
            # wl_pitch = 0.5
        elif wl_option == spMenu[2]:
            wl_min = 700.0
            wl_max = 1000.0
            # wl_pitch = 2.0
        elif wl_option == spMenu[3]:
            wl_min = 200.0
            wl_max = 1000.0
            # wl_pitch = 1.0
        # 如果选择了自定义波长范围
        else:
            with bz1_12:
                wl_range = st.slider('---Wavelength Range Setting', min_value=200.0, max_value=1000.0, value=(wl_min, wl_max),
                                        step=20.0, format='%.0f')
    with bz1_12:
        wl_pitch = st.number_input('---Wavelength Step[nm]', min_value=0, max_value=1000,
                                    value=1, step=1)
    # 输入入射角
    with bz1_12:
        inc_angle = st.number_input('---Incident Light Angle[deg]', value=0.0, format='%f')
elif calc_mode == 'Angle Scan':
    # 如果是角度扫描模式，输入波长
    with bz1_12:
        inc_wl = st.number_input('---Wavelength[nm]', min_value=0.0, max_value=1000.0, value=inc_wl, step=0.1,
                                    format='%3.1f')
        # 输入入射角度范围
        inc_angle_range = st.slider('---Incident Angle Range Setting[deg]', min_value=0.0, max_value=89.9,
                                            value=(inc_angle_min, inc_angle_max), step=1.0, format='%.0f')
        if inc_angle_range:
            inc_angle_min = inc_angle_range[0]
            inc_angle_max = inc_angle_range[1]
        inc_angle_pitch = st.number_input('---Angle Step[deg]', min_value=0.01, max_value=15.0,
                                                value=inc_angle_pitch, step=0.01, format='%3.2f')
        inc_angle = np.arange(inc_angle_min, inc_angle_max + inc_angle_pitch, inc_angle_pitch)

        st.write(':red[该功能尚未完成，请期待]')

# 获取backlight文件列表
blu_namelist = get_blu_list()
if len(blu_namelist) < 1:
    st.error('backlight list not find')

# 上传BLU光谱
with bz1_22:
    blu_name = st.selectbox('---请选择光源', blu_namelist, key='backlight')
    blu_path = 'source/backlight/' + blu_name + '.txt'
    
# 选择入射、出射介质
with bz1_22:
    inputMenu = ('Air', 'B20_Glass_Wizus')
    input_name = st.selectbox('---请选择入射介质', inputMenu, key='入射介质')
    if input_name == inputMenu[0]:
        input_para = 0
    else:
        input_para = 1

with bz1_22:
    outputMenu = ('Air', 'B20_Glass_Wizus')
    output_name = st.selectbox('---请选择出射介质', outputMenu, key='出射介质')
    if output_name == outputMenu[0]:
        output_para = 0
    else:
        output_para = 1
        
# # # 步骤2
st.write("<h6>步骤2：请设置膜层结构</h6>", unsafe_allow_html=True)

bz2_1, bz2_2, bz2_3 = st.columns([1, 8, 20])
bz2_11, bz2_12, bz2_13, bz2_14, bz2_15, bz2_16, bz2_17, bz2_18, bz2_19, bz2_20 = st.columns([1.5, 5, 1, 5, 1, 3, 1, 3, 1, 3])
bz2_21, bz2_22, bz2_23 = st.columns([1, 8, 20])
# 获取折射率文件列表
nk_namelist = get_nk_list()
if len(nk_namelist) < 1:
    st.error('nk list not find')

# 初始化折射率和薄膜厚度列表
nk_name_list = []
d_list_min = []
d_list_max = []
step_list = []  # 设置step仿真上下限
c_list = []  # 设置干涉非干涉

# # #导入txt文件
with bz2_2:
    file_all_stack = st.file_uploader('---请加载膜层堆叠txt文件', type=['txt'])

    if file_all_stack is not None:
        # 使用pandas的read_csv函数读取BLU数据，并将BLU数据按照wl_ar进行波长step选择
        stack_data = pd.read_csv(file_all_stack, header=None, sep="\t", skip_blank_lines=True)

        # #展平模块，去掉list嵌套
        def flatten_list(nested_list):
            result = []
            for element in nested_list:
                if isinstance(element, list):  # 如果是列表，则递归展平
                    result.extend(flatten_list(element))
                else:
                    result.append(element)  # 否则直接添加到结果列表
            return result

# # # 步骤3
st.write("<h6>步骤3：点击计算</h6>", unsafe_allow_html=True)

bz3_1, bz3_2, bz3_3 = st.columns([1, 8, 20])
bz3_11, bz3_12, bz3_13 = st.columns([1, 20, 1])
with bz3_2:
    cal_button_clicked_ref = st.button('***点击计算反射***', key='cal_button_ref')
with bz3_2:
    cal_button_clicked_trans = st.button('***点击计算透射率***', key='cal_button_trans')
    
# ******************** # 计算反射部分 @Wavelength Scan
if cal_button_clicked_ref:
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
    new_content = user_name + '于' + date + '使用了《08-TFMaster薄膜光学仿真工具 (V99.2) - 反射部分》;  ' + '\n'

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

    # # # # # # # # # # # # 分隔符，以上为保存使用者信息 # # # # # # # # # # # #
    # # # # # # # # # # # # 分隔符，以下为正式代码 # # # # # # # # # # # #
    
    try:
        # 根据用户输入生成波长数组
        wl_ar = np.arange(wl_min, wl_max + wl_pitch, wl_pitch, dtype=float)

        # 使用pandas的read_csv函数读取BLU数据，并将BLU数据按照wl_ar进行波长step选择
        illuminant_data = pd.read_csv(blu_path, header=None, sep="\t", skip_blank_lines=True)
        illuminant_data = np.float64(illuminant_data)
        wavelengths = pd.Series(illuminant_data[:, 0])
        intensities = pd.Series(illuminant_data[:, 1])

        # 创建一个 DataFrame，使用波长列作为索引
        selected_blu = pd.DataFrame({'Wavelength': wavelengths, 'Column1': intensities})
        # 选择需要的行，假设您希望筛选波长在某个范围内的数据
        selected_blu = selected_blu[selected_blu['Wavelength'].isin(wl_ar)]
        sblu = selected_blu.values

        # 将 DataFrame 转换为 MultiSpectralDistributions 类型
        illuminant_array_ref = colour.SpectralDistribution(sblu[:, 1], name='BLU Spectrum')
        illuminant_array_ref.wavelengths = wl_ar

        # #确认上传的txt文件中，一共多少组膜堆
        stack_num = int(stack_data.shape[1] / 2)
        # 初始化一个空的 DataFrame，用于存储所有 f_Ref_Meta 的结果
        results_ref = []
        
        for k in range(stack_num):
            nk_name_list0 = []
            if input_para == 0:
                nk_name_list0.append('Air')
            else:
                nk_name_list0.append('B20_Glass_Wizus')
            
            insert_nk_name = stack_data[k * 2].dropna().tolist()
            nk_name_list0.append(insert_nk_name)

            if output_para == 0:
                nk_name_list0.append('Air')
            else:
                nk_name_list0.append('B20_Glass_Wizus')
            
            nk_name_list = flatten_list(nk_name_list0)
        
            d_list_min0 = []
            d_list_min0.append('inf')
            insert_d_list_min = stack_data[k * 2 + 1].dropna().tolist()
            d_list_min0.append(insert_d_list_min)
            d_list_min0.append('inf')
            d_list_min = flatten_list(d_list_min0)

            d_list_max0 = []
            d_list_max0.append('inf')
            insert_d_list_max = stack_data[k * 2 + 1].dropna().tolist()
            d_list_max0.append(insert_d_list_max)
            d_list_max0.append('inf')
            d_list_max = flatten_list(d_list_max0)

            num_step_list = len(stack_data[k * 2].dropna())
            step_list = [0.0] * num_step_list

            c_list = [''] * (num_step_list + 2)
            for i in range(num_step_list + 2):
                if d_list_min[i] == 'inf' or d_list_min[i] > 100000:
                    c_list[i] = 'i'
                else:
                    c_list[i] = 'c'

            # # # # # # # 计算折射率函数列表nk_fn_list
            nk_fn_list = make_nk_fn(nk_name_list)
                
            # # # # # # # 计算厚度列表d_lists
            step_layers = []
            for i in range(0, len(step_list)):
                step_layers.append({'start': d_list_min[i + 1], 'end': d_list_max[i + 1], 'step': step_list[i]})
            # print(step_layers)

            combinations = generate_layer_combinations(step_layers)

            d_lists = []
            for i in range(len(combinations)):
                d = [np.inf]
                for j in range(1, len(nk_name_list) - 1):
                    if step_list[j - 1] != 0:
                        d.append(combinations[i][j - 1])
                    else:
                        d.append(d_list_min[j])
                d.append(np.inf)
                d_lists.append(d)

            # 计算所有split的反射率Wx, Wy数据
            #设置输出文件
            nlayers = len(step_list)
            m = len(d_lists) + 1
            n = int(8 + nlayers + (wl_max - wl_min) / wl_pitch) # NO. / 入射介质 / 薄膜膜层 / 出射介质 / Wx / Wy / WY / 380~780光谱(81 or 401组)
            final = np.empty((m, n), dtype=object)

            final[0, 0]="No."
            final[0, 1]="入射介质" + nk_name_list[0]
            for i in range(nlayers):
                final[0, i + 2] = nk_name_list[i + 1]
            final[0, nlayers + 2] = "出射介质" + nk_name_list[len(nk_name_list) - 1]
            final[0, nlayers + 3] = "Wx"
            final[0, nlayers + 4] = "Wy"
            final[0, nlayers + 5] = "WY"
            final[0, nlayers + 6] = "400~700nm平均值"
            for i in range(int((wl_max - wl_min) / wl_pitch + 1)):
                final[0, i + nlayers + 7] = 380 + i * wl_pitch
            
            for ind, d_list in enumerate(d_lists):  
                # 计算得到反射率光谱sd_R
                Rp, Rs = calc_reflectance(wl_ar, nk_fn_list, d_list, inc_angle)
                R = (Rp + Rs) / 2

                spectrum_R = colour.SpectralDistribution(R, name='Sample R')
                spectrum_R.wavelengths = wl_ar

                # 加载CMF，并进行波长step筛选
                fp_CMF = 'source/CMF.txt'
                CMF0 = pd.read_csv(fp_CMF, header=None, sep="\t", skip_blank_lines=True)
                CMF1 = np.float64(CMF0)
                wavelengths_cmfs = np.arange(380, 780 + 1, 1)
                values_cmfs = CMF1[:, 0:3]
                # 创建一个 DataFrame，使用波长step列作为索引
                selected_rows = pd.DataFrame(
                    {'Wavelength': wavelengths_cmfs, 'Column1': values_cmfs[:, 0], 'Column2': values_cmfs[:, 1],
                    'Column3': values_cmfs[:, 2]})
                # 选择需要的行，假设您希望筛选波长在某个范围内的数据
                selected_rows = selected_rows[selected_rows['Wavelength'].isin(wl_ar)]
                # 将 DataFrame 转换为 MultiSpectralDistributions 类型
                CMF = colour.MultiSpectralDistributions(
                    {wavelength: [row['Column1'], row['Column2'], row['Column3']] for wavelength, row in
                    selected_rows.set_index('Wavelength').iterrows()}
                )

                # # 计算生成WX, WY, WZ
                XYZ_R = colour.sd_to_XYZ(spectrum_R, CMF, illuminant_array_ref)
                WX = XYZ_R[0]
                WY = XYZ_R[1]
                WZ = XYZ_R[2]

                # 计算白点色坐标Wx，Wy
                Wx = WX / (WX + WY + WZ)
                Wy = WY / (WX + WY + WZ)
                f_Wx = "{:.4f}".format(Wx)
                f_Wy = "{:.4f}".format(Wy)
                f_WY = "{:.4f}".format(WY)

                # 计算400~700nm反射率平均值
                Ref_Meta = np.mean(R[int((400 - wl_min) / wl_pitch):int((700 - wl_min) / wl_pitch + 1)])
                f_Ref_Meta = "{:.6f}".format(Ref_Meta)
                # 将 f_Ref_Meta 添加到结果列表中
                results_ref.append({'Index': '膜堆' + str(k + 1), 'f_Ref_Meta': f_Ref_Meta})

                # 设置final数据
                final[ind + 1, 0] = ind + 1
                for i in range(len(nk_name_list)):
                    final[ind + 1, i + 1] = d_list[i]

                g = len(nk_name_list)
                final[ind + 1, g + 1] = f_Wx
                final[ind + 1, g + 2] = f_Wy
                final[ind + 1, g + 3] = f_WY
                final[ind + 1, g + 4] = f_Ref_Meta

                for i in range(int((wl_max - wl_min) / wl_pitch + 1)):
                    final[ind + 1, g + 5 + i] = R[i]

            with bz3_12:
                st.write(' **反射数据 - 膜堆** ' + str(k + 1))
                st.write(final)
            # 将结果列表转换为 DataFrame
            f_Ref_Meta_df = pd.DataFrame(results_ref)
        with bz3_12:
            st.write(f_Ref_Meta_df)

    except ValueError:
        bz5_3, bz5_4, bz5_5 = st.columns([1, 3, 5])
        with bz5_4:
            st.write(':red[请加载BLU光谱txt文件!]')
            
# ******************** # 计算透射部分 @Wavelength Scan
if cal_button_clicked_trans:
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
    new_content = user_name + '于' + date + '使用了《08-TFMaster薄膜光学仿真工具 (V99.2) - 透射部分》;  ' + '\n'

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

    # # # # # # # # # # # # 分隔符，以上为保存使用者信息 # # # # # # # # # # # #
    # # # # # # # # # # # # 分隔符，以下为正式代码 # # # # # # # # # # # #
    
    try:
        # 根据用户输入生成波长数组
        wl_ar = np.arange(wl_min, wl_max + wl_pitch, wl_pitch, dtype=float)

        # 使用pandas的read_csv函数读取BLU数据，并将BLU数据按照wl_ar进行波长step选择
        illuminant_data = pd.read_csv(blu_path, header=None, sep="\t", skip_blank_lines=True)
        illuminant_data = np.float64(illuminant_data)
        wavelengths = pd.Series(illuminant_data[:, 0])
        intensities = pd.Series(illuminant_data[:, 1])

        # 创建一个 DataFrame，使用波长列作为索引
        selected_blu = pd.DataFrame({'Wavelength': wavelengths, 'Column1': intensities})
        # 选择需要的行，假设您希望筛选波长在某个范围内的数据
        selected_blu = selected_blu[selected_blu['Wavelength'].isin(wl_ar)]
        sblu = selected_blu.values

        # 将 DataFrame 转换为 MultiSpectralDistributions 类型
        illuminant_array_ref = colour.SpectralDistribution(sblu[:, 1], name='BLU Spectrum')
        illuminant_array_ref.wavelengths = wl_ar

        # #确认上传的txt文件中，一共多少组膜堆
        stack_num = int(stack_data.shape[1] / 2)
        
        # 初始化一个空的 DataFrame，用于存储所有 f_Trans_Meta 的结果
        results_trans = []

        for k in range(stack_num):
            nk_name_list0 = []
            if input_para == 0:
                nk_name_list0.append('Air')
            else:
                nk_name_list0.append('B20_Glass_Wizus')
            
            insert_nk_name = stack_data[k * 2].dropna().tolist()
            nk_name_list0.append(insert_nk_name)

            if output_para == 0:
                nk_name_list0.append('Air')
            else:
                nk_name_list0.append('B20_Glass_Wizus')
            
            nk_name_list = flatten_list(nk_name_list0)
        
            d_list_min0 = []
            d_list_min0.append('inf')
            insert_d_list_min = stack_data[k * 2 + 1].dropna().tolist()
            d_list_min0.append(insert_d_list_min)
            d_list_min0.append('inf')
            d_list_min = flatten_list(d_list_min0)

            d_list_max0 = []
            d_list_max0.append('inf')
            insert_d_list_max = stack_data[k * 2 + 1].dropna().tolist()
            d_list_max0.append(insert_d_list_max)
            d_list_max0.append('inf')
            d_list_max = flatten_list(d_list_max0)

            num_step_list = len(stack_data[k * 2].dropna())
            step_list = [0.0] * num_step_list

            c_list = [''] * (num_step_list + 2)
            for i in range(num_step_list + 2):
                if d_list_min[i] == 'inf' or d_list_min[i] > 100000:
                    c_list[i] = 'i'
                else:
                    c_list[i] = 'c'

            # # # # # # # 计算折射率函数列表nk_fn_list
            nk_fn_list = make_nk_fn(nk_name_list)
                
            # # # # # # # 计算厚度列表d_lists
            step_layers = []
            for i in range(0, len(step_list)):
                step_layers.append({'start': d_list_min[i + 1], 'end': d_list_max[i + 1], 'step': step_list[i]})
            # print(step_layers)

            combinations = generate_layer_combinations(step_layers)

            d_lists = []
            for i in range(len(combinations)):
                d = [np.inf]
                for j in range(1, len(nk_name_list) - 1):
                    if step_list[j - 1] != 0:
                        d.append(combinations[i][j - 1])
                    else:
                        d.append(d_list_min[j])
                d.append(np.inf)
                d_lists.append(d)

            # 计算所有split的反射率Wx, Wy数据
            #设置输出文件
            nlayers = len(step_list)
            m = len(d_lists) + 1
            n = int(8 + nlayers + (wl_max - wl_min) / wl_pitch) # NO. / 入射介质 / 薄膜膜层 / 出射介质 / Wx / Wy / WY / 380~780光谱(81 or 401组)
            final = np.empty((m, n), dtype=object)

            final[0, 0]="No."
            final[0, 1]="入射介质" + nk_name_list[0]
            for i in range(nlayers):
                final[0, i + 2] = nk_name_list[i + 1]
            final[0, nlayers + 2] = "出射介质" + nk_name_list[len(nk_name_list) - 1]
            final[0, nlayers + 3] = "Wx"
            final[0, nlayers + 4] = "Wy"
            final[0, nlayers + 5] = "WY"
            final[0, nlayers + 6] = "400~700nm平均值"
            for i in range(int((wl_max - wl_min) / wl_pitch + 1)):
                final[0, i + nlayers + 7] = 380 + i * wl_pitch

            for ind, d_list in enumerate(d_lists):
                # 使用提供的函数计算透射系数
                Tp, Ts = calc_transmittance(wl_ar, nk_fn_list, d_list, inc_angle)
                T = (Tp + Ts) / 2

                spectrum_T = colour.SpectralDistribution(T, name='Sample T')
                spectrum_T.wavelengths = wl_ar

                # 加载CMF，并进行波长step筛选
                fp_CMF = 'D:/python_work/project/1_PDT_Local/source/CMF.txt'
                CMF0 = pd.read_csv(fp_CMF, header=None, sep="\t", skip_blank_lines=True)
                CMF1 = np.float64(CMF0)
                wavelengths_cmfs = np.arange(380, 780 + 1, 1)
                values_cmfs = CMF1[:, 0:3]
                # 创建一个 DataFrame，使用波长step列作为索引
                selected_rows = pd.DataFrame(
                    {'Wavelength': wavelengths_cmfs, 'Column1': values_cmfs[:, 0], 'Column2': values_cmfs[:, 1],
                    'Column3': values_cmfs[:, 2]})
                # 选择需要的行，假设您希望筛选波长在某个范围内的数据
                selected_rows = selected_rows[selected_rows['Wavelength'].isin(wl_ar)]
                # 将 DataFrame 转换为 MultiSpectralDistributions 类型
                CMF = colour.MultiSpectralDistributions(
                    {wavelength: [row['Column1'], row['Column2'], row['Column3']] for wavelength, row in
                    selected_rows.set_index('Wavelength').iterrows()}
                )

                # 计算Wx，Wy和Y值
                XYZ_T = colour.sd_to_XYZ(spectrum_T, CMF, illuminant_array_ref)
                WX = XYZ_T[0]
                WY = XYZ_T[1]
                WZ = XYZ_T[2]

                # 计算白点色坐标Wx，Wy
                Wx = WX / (WX + WY + WZ)
                Wy = WY / (WX + WY + WZ)
                f_Wx = "{:.4f}".format(Wx)
                f_Wy = "{:.4f}".format(Wy)
                f_WY = "{:.4f}".format(WY)

                # 计算400~700nm透过率平均值
                Trans_Meta = np.mean(T[int((400 - wl_min) / wl_pitch):int((700 - wl_min) / wl_pitch + 1)])
                f_Trans_Meta = "{:.6f}".format(Trans_Meta)
                # 将 f_Ref_Meta 添加到结果列表中
                results_trans.append({'Index': '膜堆' + str(k + 1), 'f_Trans_Meta': f_Trans_Meta})

                # 设置final数据
                final[ind + 1, 0] = ind + 1
                for i in range(len(nk_name_list)):
                    final[ind + 1, i + 1] = d_list[i]

                g = len(nk_name_list)
                final[ind + 1, g + 1] = f_Wx
                final[ind + 1, g + 2] = f_Wy
                final[ind + 1, g + 3] = f_WY
                final[ind + 1, g + 4] = f_Trans_Meta

                for i in range(int((wl_max - wl_min) / wl_pitch + 1)):
                    final[ind + 1, g + 5 + i] = T[i]

            with bz3_12:
                st.write(' **透射数据 - 膜堆** ' + str(k + 1))
                st.write(final)
            # 将结果列表转换为 DataFrame
            f_Trans_Meta_df = pd.DataFrame(results_trans)
            # print(f_Ref_Meta_df)
        with bz3_12:
            st.write(f_Trans_Meta_df)
            
    except ValueError:
        bz5_3, bz5_4, bz5_5 = st.columns([1, 3, 5])
        with bz5_4:
            st.write(':red[请加载BLU光谱txt文件!]')


# 编辑button - Final计算状态
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi2 > div > div > div > div:nth-child(13) > div.st-emotion-cache-12d0wtz.e1f1d6gn3 > div > div > div > div > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 70px !important;
    width: 150px !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑其他按钮
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi2 > div > div > div > div:nth-child(5) > div.st-emotion-cache-tqfcjc.e1f1d6gn3 > div > div > div > div:nth-child(1) > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi2 > div > div > div > div:nth-child(5) > div.st-emotion-cache-tqfcjc.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > div.st-emotion-cache-kskxxl.e116k4er3 > div.st-ae.st-af.st-ag.st-ah.st-bd.st-be.st-bf.st-bg.st-am.st-an.st-ao.st-ap.st-aq.st-ar.st-as.st-at.st-au.st-e7.st-e8.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7.st-b8.st-b9 > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi2 > div > div > div > div:nth-child(5) > div.st-emotion-cache-tqfcjc.e1f1d6gn3 > div > div > div > div:nth-child(3) > div > div.st-emotion-cache-kskxxl.e116k4er3 > div.st-ae.st-af.st-ag.st-ah.st-bd.st-be.st-bf.st-bg.st-am.st-an.st-ao.st-ap.st-aq.st-ar.st-as.st-at.st-au.st-e7.st-e8.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7.st-b8.st-b9 > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi2 > div > div > div > div:nth-child(6) > div.st-emotion-cache-tqfcjc.e1f1d6gn3 > div > div > div > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi2 > div > div > div > div:nth-child(6) > div.st-emotion-cache-tqfcjc.e1f1d6gn3 > div > div > div > div > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi2 > div > div > div > div:nth-child(8) > div.st-emotion-cache-12d0wtz.e1f1d6gn3 > div > div > div > div > div > section > button
    {
    background-color: rgb(220, 240, 220);
    }
    </style>
    ''',
    unsafe_allow_html=True
)
