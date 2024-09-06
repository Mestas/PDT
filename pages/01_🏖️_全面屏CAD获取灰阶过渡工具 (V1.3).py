import streamlit as st
import ezdxf
from tempfile import NamedTemporaryFile
from shapely.geometry import Polygon, Point
import pandas as pd
import numpy as np
import os
import cv2
import time
import zipfile
from io import BytesIO

st.set_page_config(
    initial_sidebar_state="auto",
    layout="centered"
)

# # # 侧边栏设置
st.sidebar.write("<h4 style='color: blue;'>本工具可以将异形产品CAD图纸转换为灰阶过渡CSV文件</h4>", unsafe_allow_html=True)

# # # 工具名称、版本号
st.write("# 灰阶过渡处理工具 (V1.3) #")
col1, col2 = st.columns([2, 1])
with col2:
    st.write("<h5 style='color: blue;'>版本号：V1.3</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>发布时间：2024/09/06</h5>", unsafe_allow_html=True)

# # # 设置步骤1
st.write()
st.write("<h6>步骤1: 请加载DXF文件</h6>", unsafe_allow_html=True)
col11, col12 = st.columns([1, 20])
with col12:
    st.write('<span style="color: blue; font-size: 16px">DXF文件要求: <br>1. 文件类型为DXF, 支持版本R12, R2000, R2004, R2007, R2010, R2013 and R2018  <br>2. DXF文件需解密后上传  <br>3. Panel图纸若不带孔: 按照AA, Dummy1, Dummy2三个图层; <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Panel图纸若带孔: 需在上述图层再增加Hole_AA, Hole_Dummy1, Hole_Dummy2三个图层  <br>4. DXF文件中的图形为闭合的多段线, 圆弧线需要转换成多段线, 孔为圆形  <br>5. DXF文件的单位为mm, 确保图形为正确的尺寸', unsafe_allow_html=True)

with col12:
    dxf_file = st.file_uploader("请选择DXF文件", type=['DXF'], help="请选择dxf文件进行上传")
    if dxf_file is not None:
    # 将上传的文件保存到临时文件
        with NamedTemporaryFile(delete=False) as temp:
            temp.write(dxf_file.getvalue())
            temp.seek(0)  # 重置文件指针到文件开始，以便读取文件
            # 读取dxf文件
            try:
                doc = ezdxf.readfile(temp.name)
            except OSError:
                st.write(':red[DXF文件未解密, 请解密后重新上传]')

# # # 设置步骤2
st.write("<h6>步骤2: 请输入像素尺寸和是否带孔</h6>", unsafe_allow_html=True)
col21, col22, col23, col24, col25 = st.columns([1, 3, 1, 3, 10])
with col22:
    pix_x0 = st.number_input(label='Pixel宽度(um)', format='%f', key='pixel_x')
    pix_x = pix_x0 / 1000
with col24:
    pix_y0 = st.number_input(label='Pixel高度(um)', format='%f', key='pixel_y')
    pix_y = pix_y0 / 1000

# # # 设置步骤3
st.write("<h6>步骤3: 请确认产品是否带孔</h6>", unsafe_allow_html=True)
col111, col222, col333 = st.columns([1, 4, 15])
with col222:
    my_hole = st.radio('是否带孔', ('不带孔', '带孔'), label_visibility='collapsed')
    if my_hole == '不带孔':
        hole = 0
    else:
        hole = 1

# # # 设置步骤4
st.write("<h6>步骤4: 请输入灰阶过渡数</h6>", unsafe_allow_html=True)
col2_1, col2_2, col2_3 = st.columns([1, 3, 14])
with col2_2:    
    Gray0 = st.number_input(label='过渡灰阶数', format='%f', key='Gray')
    Gray = int(Gray0)
with col2_3:

    st.write('<span style="color: blue; font-size: 16px">39代表透过率精度2.5%, 59代表透过率精度1.67%, 79代表透过率精度1.25%  <br>全灰阶建议填写199, 代表透过率精度0.5%  <br>450 ~ 350PPI用39灰阶, 350 ~ 250PPI用59灰阶, 150 ~ 250PPI用79灰阶', unsafe_allow_html=True)

# # # 设置步骤5
st.write("<h6>步骤5: 点击按钮生成灰阶过渡CSV文件</h6>", unsafe_allow_html=True)
# 功能模块1 - 判断透过率精度
def check_trans(calc_tr):
    # 根据输入的灰阶过渡灰阶精度，生成透过率T_list
    tr_acc = 1 / (Gray + 1)
    T_list = []
    for i in range(Gray + 2):
        Tr = i * tr_acc
        T_list.append(Tr)
    for i in range(len(T_list)):
        if T_list[i] - tr_acc / 2 < calc_tr <= T_list[i] + tr_acc / 2:
            trans = T_list[i]
    return trans

# 功能模块2 - 生成pixel阵列pixel_array
def pixel_array(x0, y0, xmax, ymax, entity_polygon):
    rows = int((ymax - y0) / pix_y)
    columns = int((xmax - x0) / pix_x)
    Gray_Mapping = []
    for row in range(rows):
        for col in range(columns):
            c1 = (x0 + col * pix_x, y0 + row * pix_y)
            c2 = (c1[0], c1[1] + pix_y)
            c3 = (c1[0] + pix_x, c2[1])
            c4 = (c1[0] + pix_x, c1[1])
            # 创建多段线实体来表示矩形
            rectangle = [(c1[0], c1[1]), (c2[0], c2[1]), (c3[0], c3[1]), (c4[0], c4[1]), (c1[0], c1[1])]
            pix_polygon = Polygon(rectangle)
            calc_AR = pix_polygon.intersection(entity_polygon).area / pix_x / pix_y
            calc_trans = check_trans(calc_AR)
            calc_Gray = round(calc_trans ** (1 / 2.2) * 255)
            Gray_Mapping.append(calc_Gray)
    return Gray_Mapping

# 按钮1 - 生成AA区CSV及图片
col51, col52, col53, col54, col55, col56, col57, col58, col59 = st.columns([1, 5, 1, 5, 1, 5, 1, 4, 1])
col511, col521, col531 = st.columns([1, 20, 1])
with col52:
    btn_AA_csv = st.button('***生成AA区CSV数据***')
    if btn_AA_csv is True:  
        try:
            start_time = time.time()
            # 创建工作区
            msp = doc.modelspace()
            if hole == 0:
                # 根据layer name读取图形
                AA = msp.query('*[layer=="AA"]').first
                # 获取每个多段线图形的坐标
                AA_xy = [(point[0], point[1]) for point in AA]
                # 将每个多段线图形转换为polygon
                AA_polygon = Polygon(AA_xy)
            else:
                # 根据layer name读取图形
                AA = msp.query('*[layer=="AA"]').first
                Hole_AA = msp.query('*[layer=="Hole_AA"]').first

                # 获取每个多段线图形的坐标
                AA_xy = [(point[0], point[1]) for point in AA]
                Hole_AA_pos = Hole_AA.dxf.center
                Hole_AA_xy = Point(Hole_AA_pos.x, Hole_AA_pos.y)
                Hole_AA_rad = Hole_AA.dxf.radius

                # 将每个多段线图形转换为polygon
                AA_polygon0 = Polygon(AA_xy)
                Hole_AA_polygon = Hole_AA_xy.buffer(Hole_AA_rad, resolution=512)

                # 获取带孔的polygon
                AA_polygon = AA_polygon0.difference(Hole_AA_polygon)

            # 获取每个多段线图形的最小xy坐标和最大xy坐标
            AA_x0 = float('inf')
            AA_y0 = float('inf')
            AA_xmax = float('-inf')
            AA_ymax = float('-inf')

            for point in AA:  # 遍历多段线中的每个顶点。
                x, y, *_ = point  # 从顶点中解包x和y坐标，*_表示忽略其他可能存在的值（如z坐标、起始宽度、结束宽度和凸度）。
                if x < AA_x0:
                    AA_x0 = x
                if y < AA_y0:
                    AA_y0 = y
                if x > AA_xmax:
                    AA_xmax = x
                if y > AA_ymax:
                    AA_ymax = y

            # # # 输入灰阶精度，并生成透过率T_list
            tr_acc = 1 / (Gray + 1)
            T_list = []
            for i in range(Gray + 2):
                Tr = i * tr_acc
                T_list.append(Tr)

            # # # 获取布满AA区时的开口率信息
            AA_area = pixel_array(AA_x0, AA_y0, AA_xmax, AA_ymax, AA_polygon)
            sublist_size1 = int((AA_xmax - AA_x0) / pix_x)
            AA_area_list0 = [AA_area[i:i + sublist_size1] for i in range(0, len(AA_area), sublist_size1)]
            AA_area_list = list(reversed(AA_area_list0))
            AA_DF = pd.DataFrame(AA_area_list)

            end_time = time.time()
            dis_time = round(end_time - start_time, 2)

            str0 = '下表为AA区灰阶过渡数据；' + '数据生成时间：<span style="color: #11CC11; font-weight: bold;">' + str(dis_time) + '</span>s'
            # 显示CSV数据
            with col521:
                st.write(str0, unsafe_allow_html=True)
            with col521:
                st.write(AA_DF)

            # # # 获取AA区灰阶过渡图片信息
            M_AA0 = np.array(AA_area_list)
            M_AA = np.int16(M_AA0)
            aa_h = M_AA.shape[0]
            aa_l = M_AA.shape[1]

            M_Al = np.ones((aa_h, aa_l), dtype=np.int16) * 255
            M_Alpha = M_Al - M_AA
            ZZ = np.zeros((aa_h, aa_l), dtype=np.int16)
            ONE = np.ones((aa_h, aa_l), dtype=np.int16) * 255

            AA_B1 = cv2.merge([ZZ, ZZ, M_AA])
            AA_B2 = cv2.merge([ZZ, ZZ, ONE, M_Alpha])

            AA_G1 = cv2.merge([ZZ, M_AA, ZZ])
            AA_G2 = cv2.merge([ZZ, ONE, ZZ, M_Alpha])

            AA_R1 = cv2.merge([M_AA, ZZ, ZZ])
            AA_R2 = cv2.merge([ONE, ZZ, ZZ, M_Alpha])

            AA_W1 = cv2.merge([M_AA, M_AA, M_AA])
            AA_W2 = cv2.merge([ZZ, ZZ, ZZ, M_Alpha])

            pics = [AA_R1, AA_R2, AA_G1, AA_G2, AA_B1, AA_B2, AA_W1, AA_W2]

            # 创建ZIP文件
            zip_file = BytesIO()
            with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                for i, img_array in enumerate(pics):
                    img = cv2.imencode('.png', img_array)[1]
                    zip_info = zipfile.ZipInfo(f'image_{i}.png')
                    zf.writestr(zip_info, img.tobytes())

            zip_file.seek(0)  # 移动到ZIP文件的开头

            with col58:
                btn_download_pic = st.download_button(
                    label="下载AA区灰阶过渡图片",
                    data=zip_file.getvalue(),
                    file_name="AA区灰阶过渡图片.zip",
                    mime="application/zip",
                )

            # 清理：删除临时文件
            os.unlink(temp.name)
            
        except NameError:
            st.write(':red[DXF文件未上传或DXF文件未解密, 请确认后重新上传]')
        except TypeError:
            st.write(':red[DXF文件未包含正确图层, 请确认后重新上传]')
        except AttributeError:
            st.write(':red[DXF图层不正确, 请确认后重新上传]')
        except OverflowError:
            st.write(':red[未输入Pixel信息, 请输入后再生成]')

with col54:
    btn_D1_cp = st.button('***生成Dummy1区CSV数据***')
    if btn_D1_cp is True:  
        try:
            start_time = time.time()
            # 创建工作区
            msp = doc.modelspace()
            if hole == 0:
                # 根据layer name读取图形
                Dummy1 = msp.query('*[layer=="Dummy1"]').first
                # 获取每个多段线图形的坐标
                D1_xy = [(point[0], point[1]) for point in Dummy1]
                # 将每个多段线图形转换为polygon
                D1_polygon = Polygon(D1_xy)
            else:
                # 根据layer name读取图形
                Dummy1 = msp.query('*[layer=="Dummy1"]').first
                Hole_Dummy1 = msp.query('*[layer=="Hole_Dummy1"]').first
                # 获取每个多段线图形的坐标
                D1_xy = [(point[0], point[1]) for point in Dummy1]
                Hole_Dummy1_pos = Hole_Dummy1.dxf.center
                Hole_Dummy1_xy = Point(Hole_Dummy1_pos.x, Hole_Dummy1_pos.y)
                Hole_Dummy1_rad = Hole_Dummy1.dxf.radius
                # 将每个多段线图形转换为polygon
                D1_polygon0 = Polygon(D1_xy)
                Hole_Dummy1_polygon = Hole_Dummy1_xy.buffer(Hole_Dummy1_rad, resolution=512)

                # 获取带孔的polygon
                D1_polygon = D1_polygon0.difference(Hole_Dummy1_polygon)

            # 获取每个多段线图形的最小xy坐标和最大xy坐标
            D1_x0 = float('inf')
            D1_y0 = float('inf')
            D1_xmax = float('-inf')
            D1_ymax = float('-inf')

            for point in Dummy1:  # 遍历多段线中的每个顶点。
                x, y, *_ = point  # 从顶点中解包x和y坐标，*_表示忽略其他可能存在的值（如z坐标、起始宽度、结束宽度和凸度）。
                if x < D1_x0:
                    D1_x0 = x
                if y < D1_y0:
                    D1_y0 = y
                if x > D1_xmax:
                    D1_xmax = x
                if y > D1_ymax:
                    D1_ymax = y

            # # # 输入灰阶精度，并生成透过率T_list
            tr_acc = 1 / (Gray + 1)
            T_list = []
            for i in range(Gray + 2):
                Tr = i * tr_acc
                T_list.append(Tr)

            # # # 布满Dummy1区时的面积获得
            D1_area = pixel_array(D1_x0, D1_y0, D1_xmax, D1_ymax, D1_polygon)
            sublist_size2 = int((D1_xmax - D1_x0) / pix_x)
            D1_area_list0 = [D1_area[i:i + sublist_size2] for i in range(0, len(D1_area), sublist_size2)]
            D1_area_list = list(reversed(D1_area_list0))
            D1_DF = pd.DataFrame(D1_area_list)

            end_time = time.time()
            dis_time = round(end_time - start_time, 2)
            str1 = '下表为Dummy1区灰阶过渡数据；' + '数据生成时间：<span style="color: #11CC11; font-weight: bold;">' + str(dis_time) + '</span>s'

            # 显示CSV数据
            with col521:
                st.write(str1, unsafe_allow_html=True)
            with col521:
                st.write(D1_DF)
            # 清理：删除临时文件
            os.unlink(temp.name)
            
        except NameError:
            st.write(':red[DXF文件未上传或DXF文件未解密, 请确认后重新上传]')
        except TypeError:
            st.write(':red[DXF文件未包含正确图层, 请确认后重新上传]')
        except AttributeError:
            st.write(':red[DXF图层不正确, 请确认后重新上传]')
        except OverflowError:
            st.write(':red[未输入Pixel信息, 请输入后再生成]') 

with col56:
    btn_D2_cp = st.button('***生成Dummy2区CSV数据***')
    if btn_D2_cp is True:  
        try:
            start_time = time.time()
            # 创建工作区
            msp = doc.modelspace()
            if hole == 0:
                # 根据layer name读取图形
                Dummy2 = msp.query('*[layer=="Dummy2"]').first
                # 获取每个多段线图形的坐标
                D2_xy = [(point[0], point[1]) for point in Dummy2]
                # 将每个多段线图形转换为polygon
                D2_polygon = Polygon(D2_xy)
            else:
                # 根据layer name读取图形
                Dummy2 = msp.query('*[layer=="Dummy2"]').first
                Hole_Dummy2 = msp.query('*[layer=="Hole_Dummy2"]').first
                # 获取每个多段线图形的坐标
                D2_xy = [(point[0], point[1]) for point in Dummy2]
                Hole_Dummy2_pos = Hole_Dummy2.dxf.center
                Hole_Dummy2_xy = Point(Hole_Dummy2_pos.x, Hole_Dummy2_pos.y)
                Hole_Dummy2_rad = Hole_Dummy2.dxf.radius
                # 将每个多段线图形转换为polygon
                D2_polygon0 = Polygon(D2_xy)
                Hole_Dummy2_polygon = Hole_Dummy2_xy.buffer(Hole_Dummy2_rad, resolution=512)
                # 获取带孔的polygon
                D2_polygon = D2_polygon0.difference(Hole_Dummy2_polygon)

            # 获取每个多段线图形的最小xy坐标和最大xy坐标
            D2_x0 = float('inf')
            D2_y0 = float('inf')
            D2_xmax = float('-inf')
            D2_ymax = float('-inf')

            for point in Dummy2:  # 遍历多段线中的每个顶点。
                x, y, *_ = point  # 从顶点中解包x和y坐标，*_表示忽略其他可能存在的值（如z坐标、起始宽度、结束宽度和凸度）。
                if x < D2_x0:
                    D2_x0 = x
                if y < D2_y0:
                    D2_y0 = y
                if x > D2_xmax:
                    D2_xmax = x
                if y > D2_ymax:
                    D2_ymax = y

            # # # 输入灰阶精度，并生成透过率T_list
            tr_acc = 1 / (Gray + 1)
            T_list = []
            for i in range(Gray + 2):
                Tr = i * tr_acc
                T_list.append(Tr)

            # # # 布满Dummy2区时的面积获得
            D2_area = pixel_array(D2_x0, D2_y0, D2_xmax, D2_ymax, D2_polygon)
            sublist_size3 = int((D2_xmax - D2_x0) / pix_x)
            D2_area_list0 = [D2_area[i:i + sublist_size3] for i in range(0, len(D2_area), sublist_size3)]
            D2_area_list = list(reversed(D2_area_list0))
            D2_DF = pd.DataFrame(D2_area_list)

            end_time = time.time()
            dis_time = round(end_time - start_time, 2)
            str1 = '下表为Dummy2区灰阶过渡数据；' + '数据生成时间：<span style="color: #11CC11; font-weight: bold;">' + str(dis_time) + '</span>s'

            # 显示CSV数据
            with col521:
                st.write(str1, unsafe_allow_html=True)
            with col521:
                st.write(D2_DF)
            # 清理：删除临时文件
            os.unlink(temp.name)

        except NameError:
            st.write(':red[DXF文件未上传或DXF文件未解密, 请确认后重新上传]')
        except TypeError:
            st.write(':red[DXF文件未包含正确图层, 请确认后重新上传]')
        except AttributeError:
            st.write(':red[DXF图层不正确, 请确认后重新上传]')
        except OverflowError:
            st.write(':red[未输入Pixel信息, 请输入后再生成]') 

# 编辑点击计算按钮
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(12) > div:nth-child(2) > div > div > div > div > div > button
    {
        background-color: rgb(220, 240, 220);
        height: 70px;
        width: 150px;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(12) > div:nth-child(4) > div > div > div > div > div > button
    {
        background-color: rgb(220, 240, 220);
        height: 70px;
        width: 150px;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(12) > div:nth-child(6) > div > div > div > div > div > button
    {
        background-color: rgb(220, 240, 220);
        height: 70px;
        width: 150px;
    } 
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(12) > div:nth-child(8) > div > div > div > div > div > button
    {
        background-color: rgb(200, 250, 250);
        height: 60px;
        width: 120px;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# 编辑上传按钮底色
st.markdown(
    '''
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi3 > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi2 > div > div > div > div:nth-child(4) > div.st-emotion-cache-15qpf3q.e1f1d6gn3 > div > div > div > div:nth-child(2) > div > section > button
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
