import streamlit as st

import numpy as np

import matplotlib.pyplot as plt

from skimage import io, color, filters, measure

from io import BytesIO

import pdfkit





def run():









    # 标题和介绍

    st.title("热致变色液晶温度图像处理系统")

    st.write("扩展功能包括非线性校准、伪彩色显示、区域选择与分析、生成报告以及背景隐藏。")



    # 上传图像

    uploaded_file = st.file_uploader("上传图像文件 (支持 TIFF/PNG/JPEG)", type=["tif", "png", "jpg"])



    # 校准模型参数设置

    st.sidebar.title("校准参数")

    model_type = st.sidebar.radio("选择校准模型", ("线性", "非线性"))

    if model_type == "线性":

        a = st.sidebar.number_input("线性系数 (a)", value=0.05, format="%.5f")

        b = st.sidebar.number_input("截距 (b)", value=20.0, format="%.2f")

    else:

        st.sidebar.write("输入非线性系数 (支持二次模型 T = a*G^2 + b*G + c)：")

        a = st.sidebar.number_input("二次项系数 (a)", value=0.001, format="%.5f")

        b = st.sidebar.number_input("一次项系数 (b)", value=0.05, format="%.5f")

        c = st.sidebar.number_input("常数项 (c)", value=20.0, format="%.2f")



    # 伪彩色选择

    colormap = st.sidebar.selectbox("选择伪彩色", ["hot", "cool", "viridis", "plasma", "inferno"])



    # 温度范围设置

    min_temp = st.sidebar.number_input("温度最小值", value=20.0, format="%.2f")

    max_temp = st.sidebar.number_input("温度最大值", value=80.0, format="%.2f")



    # 上传图像处理

    if uploaded_file:

        # 加载图像

        image = io.imread(uploaded_file)

        st.image(image, caption="原始图像", use_container_width=True)



        # 检查是否为 RGB 图像

        if len(image.shape) == 3 and image.shape[2] == 3:

            # 提取绿色通道

            green_channel = image[:, :, 1]



            # 背景隐藏处理（基于阈值）

            st.sidebar.write("背景隐藏阈值")

            threshold = st.sidebar.slider("设定绿色通道强度阈值", 0, 255, 30)

            mask = green_channel > threshold

            filtered_channel = green_channel * mask



            # 显示绿色通道（处理后）

            st.write("绿色通道 (处理后)：")

            fig, ax = plt.subplots()

            ax.imshow(filtered_channel, cmap="gray")

            ax.axis("off")

            st.pyplot(fig)



            # 温度计算

            if model_type == "线性":

                temperature_map = a * filtered_channel + b

            else:

                temperature_map = a * (filtered_channel ** 2) + b * filtered_channel + c



            # 温度范围限制

            temperature_map = np.clip(temperature_map, min_temp, max_temp)



            # 显示伪彩色温度图

            st.write("伪彩色温度分布图：")

            fig, ax = plt.subplots()

            cax = ax.imshow(temperature_map, cmap=colormap, origin="upper")

            fig.colorbar(cax, ax=ax, label="Temperature (°C)")

            st.pyplot(fig)



            # 区域选择与分析

            st.write("区域选择与分析：")

            region_stats = st.checkbox("启用区域分析")

            if region_stats:

                labels = measure.label(mask, connectivity=2)

                regions = measure.regionprops(labels, intensity_image=temperature_map)



                for i, region in enumerate(regions, start=1):

                    st.write(f"区域 {i}:")

                    st.write(f"- 平均温度: {region.mean_intensity:.2f} °C")

                    st.write(f"- 最大温度: {region.max_intensity:.2f} °C")

                    st.write(f"- 面积: {region.area} 像素")





    from fpdf import FPDF



    if st.button("生成报告"):

        st.write("生成 PDF 报告中...")



        # 创建 PDF 实例

        pdf = FPDF()

        pdf.add_page()



        # 加载 Noto Sans 字体

        pdf.add_font('NotoSans', '', 'NotoSans-Regular.ttf', uni=True)

        pdf.set_font('NotoSans', size=12)



        # 添加标题

        pdf.set_font('NotoSans', size=16)  # 无需指定加粗样式

        pdf.cell(200, 10, txt="温度图像处理报告", ln=True, align="C")





        # 添加模型信息

        pdf.set_font('NotoSans', size=12)

        pdf.ln(10)  # 空行

        pdf.cell(200, 10, txt=f"校准模型: {model_type}", ln=True)

        if model_type == "线性":

            pdf.cell(200, 10, txt=f"线性参数: a={a}, b={b}", ln=True)

        else:

            pdf.cell(200, 10, txt=f"非线性参数: a={a}, b={b}, c={c}", ln=True)

        pdf.cell(200, 10, txt=f"温度范围: {min_temp}°C - {max_temp}°C", ln=True)



        # 添加区域分析结果

        if region_stats:

            pdf.ln(10)

            pdf.set_font('NotoSans', style="B", size=14)

            pdf.cell(200, 10, txt="区域分析结果:", ln=True)

            pdf.set_font('NotoSans', size=12)

            for i, region in enumerate(regions, start=1):

                pdf.ln(5)  # 区域间距

                pdf.cell(200, 10, txt=f"区域 {i}:", ln=True)

                pdf.cell(200, 10, txt=f"- 平均温度: {region.mean_intensity:.2f} °C", ln=True)

                pdf.cell(200, 10, txt=f"- 最大温度: {region.max_intensity:.2f} °C", ln=True)

                pdf.cell(200, 10, txt=f"- 面积: {region.area} 像素", ln=True)



        # 保存 PDF

        pdf_output_path = "temperature_report.pdf"

        pdf.output(pdf_output_path)



        # 提供下载

        with open(pdf_output_path, "rb") as pdf_file:

            st.download_button(

                label="下载 PDF 报告",

                data=pdf_file,

                file_name="temperature_report.pdf",

                mime="application/pdf",

            )

