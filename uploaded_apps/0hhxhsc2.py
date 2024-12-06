import streamlit as st

import numpy as np

import matplotlib.pyplot as plt











def run():



    # 设置字体路径

    from matplotlib import font_manager

    font_path = 'SourceHanSansSC-Bold.otf'

    font_manager.fontManager.addfont(font_path)

    plt.rcParams['font.family'] = font_manager.FontProperties(fname=font_path).get_name()

    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题



    # 设置 Streamlit 页面标题

    st.title("椭圆平面螺旋图：原始曲线、O 点对称、-θ 反旋")



    # 几何理论公式

    st.markdown("### 几何理论公式")

    st.latex(r"r = 1 + k \cdot \theta \quad \text{（正旋半径公式）}")

    st.latex(r"r = 1 + k \cdot (-\theta) \quad \text{（-θ 反旋公式）}")

    st.latex(r"x = r \cdot a \cdot \cos(\theta)")

    st.latex(r"y = r \cdot b \cdot \sin(\theta)")



    # 参数输入控件

    st.sidebar.header("参数调整")

    b = st.sidebar.number_input("短半轴 b", min_value=-100.0, max_value=100.0, value=1.0, step=0.1)

    ab_ratio = st.sidebar.number_input("a/b 比例", min_value=-10.0, max_value=10.0, value=4.5, step=0.1)

    a = b * ab_ratio



    k = st.sidebar.number_input("螺旋扩展系数 k", min_value=-1.0, max_value=1.0, value=1.0, step=0.1)

    num_turns = st.sidebar.number_input("圈数", min_value=-100, max_value=100, value=8, step=1)



    # 添加图形控制开关

    st.sidebar.header("图形控制")

    show_original = st.sidebar.checkbox("显示原始曲线", value=True)

    show_symmetric = st.sidebar.checkbox("显示 O 点对称曲线", value=True)





    # 绘图函数

    def plot_ellipse_spiral(ax, a, b, k, num_turns, mode="original", label_prefix=""):

        """

        绘制椭圆平面螺旋图，包括原始曲线、O 点对称。

        """

        # 参数范围

        theta = np.linspace(0, num_turns * np.pi, 1000)



        # 螺旋半径公式

        if mode == "-theta":

            r = 1 + k * np.abs(theta) * (-1)

        else:

            r = 1 + k * theta



        # 计算坐标

        x = r * a * np.cos(theta)

        y = r * b * np.sin(theta)



        # 对称模式

        if mode == "symmetric":

            x = -x

            y = -y



        # 计算最外层的长半轴和短半轴

        max_r = max(r)

        outer_a = max_r * a

        outer_b = max_r * b



        # 显示详细信息

        if mode == "original":  # 避免重复打印

            st.markdown("## 比例计算")

            st.write(f"根据输入的短半轴 **b = {b:.2f}** 和比例 **a/b = {ab_ratio:.2f}**，计算得到：")

            st.write(f"- 长半轴 **a = {a:.2f}**")

            st.write(f"- 最外层长半轴 **{outer_a:.2f}**")

            st.write(f"- 最外层短半轴 **{outer_b:.2f}**")

            st.write(f"- 短半轴间距 **{outer_b/num_turns:.2f}**")



        # 绘制曲线

        ax.plot(x, y, label=f"{label_prefix}椭圆平面螺旋")





    # 创建图形

    fig, ax = plt.subplots(figsize=(8, 8))



    # 绘制曲线

    if show_original:

        plot_ellipse_spiral(ax, a, b, k, num_turns, mode="original", label_prefix="原始")



    if show_symmetric:

        plot_ellipse_spiral(ax, a, b, k, num_turns, mode="symmetric", label_prefix="O 点对称")



    # 设置图形属性

    ax.set_title("椭圆平面螺旋图", fontsize=16)

    ax.set_xlabel("x", fontsize=14)

    ax.set_ylabel("y", fontsize=14)

    ax.axis("equal")

    ax.grid(True)

    ax.legend()



    # 显示图形

    st.pyplot(fig)

