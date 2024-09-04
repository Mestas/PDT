import streamlit as st
from shapely.geometry import Polygon

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>This tools can calculate the Color Gamut and Color Coverage</h4>", unsafe_allow_html=True)

# # # 工具名称、版本号
st.write("# Color Gamut Calculater #")
    
def calculate_overlap_area(triangle1, triangle2):
    # 创建Shapely的多边形对象
    polygon1 = Polygon(triangle1)
    polygon2 = Polygon(triangle2)

    # 计算两个多边形的重叠部分
    overlap = polygon1.intersection(polygon2)

    # 返回重叠部分的面积
    return overlap.area

# # # 设置步骤1
col1, col2 = st.columns([1, 2])
bz1_1, bz1_2, bz1_3, bz1_4 = st.columns([1, 2, 2, 8])
with col1:
    st.write(' ')
    st.write("<h6>step1: Input Sample Color Coordinate</h6>", unsafe_allow_html=True)
with bz1_2:
    Rx = st.number_input(label='**Rx**', format='%f', key='Rx')
    Gx = st.number_input(label='**Gx**', format='%f', key='Gx')
    Bx = st.number_input(label='**Bx**', format='%f', key='Bx')
with bz1_3:
    Ry = st.number_input(label='**Ry**', format='%f', key='Ry')
    Gy = st.number_input(label='**Gy**', format='%f', key='Gy')
    By = st.number_input(label='**By**', format='%f', key='By')

# # # 设置步骤2
col3, col4 = st.columns([1, 2])
bz2_1, bz2_2, bz2_3, bz2_4 = st.columns([1, 4, 2, 6])
bz2_11, bz2_12, bz2_13, bz2_14 = st.columns([1, 2, 2, 8])
with col3:
    st.write(' ')
    st.write("<h6>step2: Select Standard Color Coordinate</h6>", unsafe_allow_html=True)
with bz2_2:
    spMenu = ('sRGB', 'DCI-P3', 'Adobe', 'BT2020', 'NTSC')
    Standard_Color = st.selectbox('**Select Standard Color**', spMenu, key='Standard')
    if Standard_Color == spMenu[0]:
        Rx0 = 0.640
        Ry0 = 0.330
        Gx0 = 0.300
        Gy0 = 0.600
        Bx0 = 0.150
        By0 = 0.060
    elif Standard_Color == spMenu[1]:
        Rx0 = 0.680
        Ry0 = 0.320
        Gx0 = 0.265
        Gy0 = 0.690
        Bx0 = 0.150
        By0 = 0.060
    elif Standard_Color == spMenu[2]:
        Rx0 = 0.640
        Ry0 = 0.330
        Gx0 = 0.210
        Gy0 = 0.710
        Bx0 = 0.150
        By0 = 0.060
    elif Standard_Color == spMenu[3]:
        Rx0 = 0.708
        Ry0 = 0.292
        Gx0 = 0.170
        Gy0 = 0.797
        Bx0 = 0.131
        By0 = 0.046
    elif Standard_Color == spMenu[4]:
        Rx0 = 0.670
        Ry0 = 0.330
        Gx0 = 0.210
        Gy0 = 0.710
        Bx0 = 0.140
        By0 = 0.080

with bz2_12:
    Rx0 = st.number_input(label='**Rx**', value=Rx0, disabled=True, format='%f', key='Rx0')
    Gx0 = st.number_input(label='**Gx**', value=Gx0, disabled=True, format='%f', key='Gx0')
    Bx0 = st.number_input(label='**Bx**', value=Bx0, disabled=True, format='%f', key='Bx0')
with bz2_13:
    Ry0 = st.number_input(label='**Ry**', value=Ry0, disabled=True, format='%f', key='Ry0')
    Gy0 = st.number_input(label='**Gy**', value=Gy0, disabled=True, format='%f', key='Gy0')
    By0 = st.number_input(label='**By**', value=By0, disabled=True, format='%f', key='By0')

# # # 设置步骤3
col5, col6 = st.columns([1, 2])
bz3_1, bz3_2, bz3_3, bz3_4, bz3_5 = st.columns([1, 4, 4, 4, 1])
bz4_1, bz4_2, bz4_3, bz4_4, bz4_5 = st.columns([1, 4, 4, 4, 1])
with col5:
    st.write(' ')
    st.write("<h6>step3: Click to Calculate</h6>", unsafe_allow_html=True)

# 点击button计算色域
with bz3_2:
    cal_color_gamut = st.button('***Calc Color Gamut***', key='color gamut')

# # # main code
if cal_color_gamut:
    # 输入两个三角形的顶点坐标
    triangle1 = [(Rx, Ry), (Gx, Gy), (Bx, By)]
    triangle2 = [(Rx0, Ry0), (Gx0, Gy0), (Bx0, By0)]
    # 计算重叠面积
    area_overlap = calculate_overlap_area(triangle1, triangle2)
    # 计算标准色的面积
    area_standard_color = (Rx0 * Gy0 + Gx0 * By0 + Bx0 * Ry0 - Ry0 * Gx0 - Gy0 * Bx0 - By0 * Rx0) * 0.5

    # 计算评估颜色的色域及覆盖率
    color_gamut = (Rx * Gy + Gx * By + Bx * Ry - Ry * Gx - Gy * Bx - By * Rx) * 0.5 / 0.1582
    standard_gamut = (Rx0 * Gy0 + Gx0 * By0 + Bx0 * Ry0 - Ry0 * Gx0 - Gy0 * Bx0 - By0 * Rx0) * 0.5 / 0.1582
    color_coverage = area_overlap / area_standard_color

    # 显示结果
    str_color_gamut = str(str(round(color_gamut * 100, 2)) + '%')
    str_color_coverage = str(str(round(color_coverage * 100, 2)) + '%')
    str_standard_gamut = str(str(round(standard_gamut * 100, 2)) + '%')
    
    with bz4_2:
        st.text_input(label='**Sample Color Gamut(NTSC)**', value=str_color_gamut, key='color_gamut')
    with bz4_3:
        st.text_input(label='**Standard Color Gamut(NTSC)**', value=str_standard_gamut, key='standard_gamut')
    with bz4_4:
        st.text_input(label='**Sample Color Coverage**', value=str_color_coverage, key='color_coverage')

# 编辑Standard color selectbox
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(5) > div.st-emotion-cache-14nh3c1.e1f1d6gn3 > div > div > div > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    height: 40px !important;
    width: 200px !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑Calc_color_Gamut button
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(8) > div:nth-child(2) > div > div > div > div > div > button
    {
    background-color: rgb(220, 240, 220);
    height: 60px !important;
    width: 200px !important;
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

# 设置input和output的背景
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div:nth-child(2) > div > div > div > div:nth-child(1) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div:nth-child(3) > div > div > div > div:nth-child(1) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div:nth-child(2) > div > div > div > div:nth-child(2) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div:nth-child(3) > div > div > div > div:nth-child(2) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div:nth-child(2) > div > div > div > div:nth-child(3) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(3) > div:nth-child(3) > div > div > div > div:nth-child(3) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }

    
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div:nth-child(2) > div > div > div > div:nth-child(1) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div:nth-child(3) > div > div > div > div:nth-child(1) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div:nth-child(2) > div > div > div > div:nth-child(2) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div:nth-child(3) > div > div > div > div:nth-child(2) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div:nth-child(2) > div > div > div > div:nth-child(3) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(6) > div:nth-child(3) > div > div > div > div:nth-child(3) > div > div > div > div
    {
    background-color: rgb(220, 240, 220);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(9) > div:nth-child(2) > div > div > div > div > div > div.st-ae.st-af.st-ag.st-ah.st-bx.st-by.st-bz.st-c0.st-am.st-an.st-ao.st-ap.st-aq.st-ar.st-as.st-at.st-au.st-bu.st-bv.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7.st-b8.st-b9 > div
    {
    background-color: rgb(200, 240, 240);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(9) > div:nth-child(3) > div > div > div > div > div > div.st-ae.st-af.st-ag.st-ah.st-bx.st-by.st-bz.st-c0.st-am.st-an.st-ao.st-ap.st-aq.st-ar.st-as.st-at.st-au.st-bu.st-bv.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7.st-b8.st-b9 > div
    {
    background-color: rgb(200, 240, 240);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(9) > div:nth-child(4) > div > div > div > div > div > div.st-ae.st-af.st-ag.st-ah.st-bx.st-by.st-bz.st-c0.st-am.st-an.st-ao.st-ap.st-aq.st-ar.st-as.st-at.st-au.st-bu.st-bv.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7.st-b8.st-b9 > div
    {
    background-color: rgb(200, 240, 240);
    }
    </style>
    ''',
    unsafe_allow_html=True
)
