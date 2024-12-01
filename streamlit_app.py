import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import streamlit as st
from scipy.integrate import quad

import pandas as pd
from io import BytesIO





#设置字体路径
from matplotlib import font_manager
font_path = 'SourceHanSansSC-Bold.otf'
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=font_path).get_name()
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题







# 设置字体为宋体
# plt.rcParams['font.sans-serif'] = ['SimHei']

# matplotlib.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题


# 标题和简介
st.title('热电模块性能计算-20241130-wjj')
st.write('这个应用程序允许用户输入温差电池的尺寸、温度以及物料属性，计算和展示热电模块的性能参数。')

# 显示公式

with st.expander("参考公式"):
    # Seebeck系数 (α)
    st.write("### Seebeck系数 (α)")
    st.latex(r'''
    a_n = -1.045 \times 10^{-11} T^3 + 9.337 \times 10^{-9} T^2 - 2.649 \times 10^{-6} T + 4.4603 \times 10^{-4}
    ''')
    st.latex(r'''
    a_p = -6.373 \times 10^{-12} T^3 + 3.59 \times 10^{-9} T^2 - 9.24 \times 10^{-8} T + 8.4605 \times 10^{-5}
    ''')

    # 电动势公式
    st.write("### 电动势公式")
    st.write("热电模块两端的电动势由 Seebeck 效应产生，其计算公式为：")
    st.latex(r'''
    \mathcal{E} = S \cdot \Delta T
    ''')
    st.write("其中：")
    st.latex(r'''
    \mathcal{E} \text{ ：是一对P、N温差电池的电动势，单位为伏特 (V)；}
    ''')
    st.latex(r'''
    S \text{ ：是总 Seebeck 系数，单位为伏特每开尔文 (V/K)；}
    ''')
    st.latex(r'''
    \Delta T \text{ ：是温差，单位为开尔文 (K)，计算为 } T_{\text{热端}} - T_{\text{冷端}}。
    ''')
    st.write("""
    当 \( S \) 随温度变化时，电动势可用积分形式计算：
    """)
    st.latex(r'''
    \mathcal{E} = \int_{T_{\text{冷端}}}^{T_{\text{热端}}} S(T) \, dT
    ''')
    st.write("""
    上述公式是更精确的计算方法，适用于复杂材料的性能评估。
    """)


    # 热导率 (λ)
    st.write("### 热导率 (λ)")
    st.latex(r'''
    \lambda_n = 2.36 \times 10^{-5} T^2 - 0.015 T + 3.806
    ''')
    st.latex(r'''
    \lambda_p = 3.2 \times 10^{-5} T^2 - 0.0216 T + 4.949
    ''')

    # 电阻率 (ρ)
    st.write("### 电阻率 (ρ)")
    st.latex(r'''
    \rho_n = -2.5786 \times 10^{-13} T^3 + 1.9767 \times 10^{-10} T^2 - 6.0208 \times 10^{-9} T + 5.7588 \times 10^{-7}
    ''')
    st.latex(r'''
    \rho_p = -7.9299 \times 10^{-13} T^3 + 8.6932 \times 10^{-10} T^2 - 2.506 \times 10^{-7} T + 2.8215 \times 10^{-5}
    ''')

    # ZT值公式
    st.write("### ZT值公式")
    st.latex(r'''
    ZT = \frac{S^2 \cdot T}{\lambda \cdot \rho}
    ''')
    st.write("""


    **物理模型简化**：
    通常在设计制造温差发电片时，P、N 电偶臂的高度一致，适当的 P、N 电偶臂截面面积比有利于提高 ZT值，即提高温差发电片整体性能。进一步假定 P、N 型电偶臂材料的热导率、电阻率相同,塞贝克系数的数值相等但是符号相反,最终简化为该方程

    其中：
    - \( S \) 为 Seebeck 系数；
    - \( T \) 为平均温度（当 ( S ) 随温度T变化时，ZT值可用积分形式计算）；
    - \( λ \) 为材料的热导率；
    - \( ρ \) 材料的电阻率。

    **ZT值的物理意义**：
    ZT 值越高，说明材料的热电转换效率越高，能更有效地将热能转化为电能。
    )

    其中：

    **普通材料**:ZT <1，效率较低，难以实际应用
            
    **高性能材料**:ZT≈2-3，适合用于热电发电或制冷设备
            
    **未来目标**:T>3，研究重点，用于高效能源转换

    """)

    # 功率公式
    st.write("### 功率公式")
    st.write("发电功率 \( P \) 的计算公式如下：")
    st.latex(r'''
    P = \frac{(S \cdot \Delta T)^2}{R}
    ''')
    st.write("""
    其中：
    - \( S \) 为 Seebeck 系数；
    - \( Δ T \) 为温差（热端温度与冷端温度之差）；
    - \( R \) 为总电阻，其计算如下：
    """)
    st.latex(r'''
    R = \frac{\rho \cdot L}{A}
    ''')
    st.write("""
    将 \( R \) 的表达式代入功率公式中，可以得到：
    """)
    st.latex(r'''
    P = \frac{(S \cdot \Delta T)^2 \cdot A}{\rho \cdot L}
    ''')
    st.write("""
    这个展开形式揭示了热电发电功率 \( P \) 不仅取决于塞贝克系数 \( S \) 和温差 \( Δ T \)，还受到热电材料的电阻率 \( ρ \)，电流路径的长度 \( L \) 和横截面积 \( A \) 的影响。通过调整这些几何和物理参数，可以优化装置的功率输出。

    **功率公式的物理意义**：用于计算热电模块的发电输出功率，结果以瓦特 (W) 为单位。这表明通过适当选择材料和设计几何尺寸，可以优化热电装置的功率输出，进而提高能量转换的效率。



    ### 最大发电功率
    最大发电功率 \( Pmax\) 出现在负载电阻 \( R负载 \) 等于内部电阻 \( R \) 时。其计算公式为：
    """)
    st.latex(r'''
    P_{max} = \frac{(S \cdot \Delta T)^2}{4R}
    ''')
    st.write("""
    在最大功率条件下：
    - 负载电阻 \( R负载 \) 应设置为与热电模块的内部电阻 \( R \) 相同。

    **最大功率的物理意义**：在阻抗匹配的条件下，热电模块可以达到最高的能量转换效率，此时的功率输出是理论上的最大值。这种设置在设计热电发电系统时至关重要，以确保最高的能效。
    """)


    st.write("""
    ### 最大功率电流
    最大电流I发生在负载电阻等于内部电阻。此时，电流的计算公式为：
    """)
    st.latex(r'''
    I_{\text{Pmax}} = \frac{S \cdot \Delta T}{2}
    ''')
    st.write("""
    **最大电流的物理意义**：最大电流表示热电模块在短路条件下能产生的最大电流值，这对于理解和测试模块的电气特性非常重要。

    ### 热端热流 \( Qh \)
    热端热流 \( Qh \) 是指从热源通过热电模块到冷端的热能传递。其计算公式依赖于多个因素，包括热电模块的热电性能参数和温差：
    """)
    st.latex(r'''
    Q_h = \alpha_{\text{总}} \cdot T_c \cdot I + K(T_h - T_c) + \frac{1}{2} I^2 R
    ''')
    st.write("""
    其中
    - \( K \) 为热电模块的热导率。
    - \( α总 \) 为N和P的温度区间平均Seebeck系数。

    **热流的物理意义**：热端热流量是评估热电模块热效率的关键参数，表明了热能从热源到冷端的流动效率。

    ### 转换效率 \( η \)
    转换效率 \( η \) 表示热能转换为电能的效率，计算公式为：
    """)
    st.latex(r'''
    \eta = \frac{P_{\text{out}}}{Q_h}
    ''')
    st.write("""
    **转换效率的物理意义**：转换效率是衡量热电模块性能的核心指标，高效率意味着更多的热能被有效转换为电能。
    """)



# 显示公式
st.write("""## 计算程序""")

# 定义函数用于计算材料属性
def calculate_coefficient(T, a, b, c, d):
    return a * T**3 + b * T**2 + c * T + d

# 定义物性计算公式
def lambda_func(T, a, b, c, d):
    return a * T**3 + b * T**2 + c * T + d

def rho_func(T, a, b, c, d):
    return a * T**3 + b * T**2 + c * T + d

def seebeck_func(T, a, b, c, d):
    return a * T**3 + b * T**2 + c * T + d

# 定义积分计算平均物性的函数
def calculate_average_property(func, T_c, T_h, coeffs):
    integral, error = quad(func, T_c, T_h, args=coeffs)
    average = integral / (T_h - T_c)
    return average


# N型和P型材料的物性参数系数
#coeffs_seebeck_n = (-1.045e-11, 9.337e-9, -2.649e-6, 4.4603e-4)
#coeffs_seebeck_p = (-6.373e-12, 3.59e-9, -9.24e-8, 8.4605e-5)
coeffs_seebeck_n = (1.82981e-12, -3.17605e-09, 1.33474e-06, 5.30108e-05)
coeffs_seebeck_p = (2.11554e-12, -3.62723e-09, 1.54490e-06, 2.09893e-05)



coeffs_lambda_n = (0, 2.36e-5, -0.015, 3.806)
coeffs_lambda_p = (0, 3.2e-5, -0.0216, 4.949)

#coeffs_rho_n = (-2.5786e-13, 1.9767e-10, -6.0208e-9, 5.7588e-7)
#coeffs_rho_p = (-7.9299e-13, 8.6932e-10, -2.506e-7, 2.8215e-5)
coeffs_rho_n = (8.4476e-14, -1.7758e-10, 1.2524e-07, -1.4166e-05)
coeffs_rho_p = (7.7187e-14, -1.8061e-10, 1.4092e-07, -1.7761e-05)




# 初始化公式参数
#a_n, b_n, c_n, d_n = -1.045e-11, 9.337e-9, -2.649e-6, 4.4603e-4
#a_p, b_p, c_p, d_p = -6.373e-12, 3.59e-9, -9.24e-8, 8.4605e-5
a_n, b_n, c_n, d_n = 1.82981e-12, -3.17605e-09, 1.33474e-06, 5.30108e-05
a_p, b_p, c_p, d_p = 2.11554e-12, -3.62723e-09, 1.54490e-06, 2.09893e-05
lambda_a_n, lambda_b_n, lambda_c_n, lambda_d_n = 0, 2.36e-5, - 0.015, 3.806
lambda_a_p, lambda_b_p, lambda_c_p, lambda_d_p = 0, 3.2e-5, - 0.0216, 4.949

#rho_a_n, rho_b_n, rho_c_n, rho_d_n = -2.5786e-13, 1.9767e-10, -6.0208e-9, 5.7588e-7
#rho_a_p, rho_b_p, rho_c_p, rho_d_p = -7.9299e-13, 8.6932e-10, -2.506e-7, 2.8215e-5
rho_a_n, rho_b_n, rho_c_n, rho_d_n = 8.4476e-14, -1.7758e-10, 1.2524e-07, -1.4166e-05
rho_a_p, rho_b_p, rho_c_p, rho_d_p = 7.7187e-14, -1.8061e-10, 1.4092e-07, -1.7761e-05


# 用户输入温度

with st.expander("输入温度参数", expanded=True):
    col1, col2 = st.columns(2)
with col1:
    T_c = st.number_input('冷端温度 (K)', value=320.0,min_value=200.0, max_value=600.0, step=1.0, help="请输入冷端温度", format="%f")
with col2:
    T_h = st.number_input('热端温度 (K)', value=450.0,min_value=200.0, max_value=800.0, step=1.0, help="请输入热端温度", format="%f")
    T_avg = (T_h + T_c) / 2

    # 定义温度范围``
T_range = np.linspace(T_c, T_h, 30)

# 用户输入材料尺寸
with st.expander("输入材料尺寸"):
        col1, col2, col3 = st.columns(3)
with col1:
    L = st.number_input('长度 (m)', value=0.01,min_value=0.0, max_value=100000.0, step=0.001, format="%f")
with col2:
    W = st.number_input('宽度 (m)', value=0.01,min_value=0.0, max_value=100000.0, step=0.001,  format="%f")
with col3:
    H = st.number_input('P/N高度 (m)', value=0.002,min_value=0.0, max_value=100000.0, step=0.001,  format="%f")
    A = W * L  # 计算截面积

# 用户输入公式系数


# 自定义Seebeck系数公式

with st.expander("输入Seebeck系数公式参数（拟合温度：200~600K）"):
    st.write("#### N型材料Seebeck系数公式系数")    
    st.markdown("多项式拟合：[拟合](https://demo2.yunser.com/math/fitted_curve/)") 

    st.latex(r'''
    a_n = -1.045 \times 10^{-11} T^3 + 9.337 \times 10^{-9} T^2 - 2.649 \times 10^{-6} T + 4.4603 \times 10^{-4}
    ''')

    def calculate_step(value):
        # 保证步长为浮点类型，并且是value的10%
        return abs(float(value)) * 0.1 if value != 0 else 0.1

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        a_n = st.number_input('a_n', value=float(a_n), step=calculate_step(a_n), format="%e", min_value=float(-1e10), max_value=float(1e10))
    with col2:
        b_n = st.number_input('b_n', value=float(b_n), step=calculate_step(b_n), format="%e", min_value=float(-1e10), max_value=float(1e10))
    with col3:
        c_n = st.number_input('c_n', value=float(c_n), step=calculate_step(c_n), format="%e", min_value=float(-1e10), max_value=float(1e10))
    with col4:
        d_n = st.number_input('d_n', value=float(d_n), step=calculate_step(d_n), format="%e", min_value=float(-1e10), max_value=float(1e10))


    st.write("#### P型材料Seebeck系数公式系数")
    st.latex(r'''
    a_p = -6.373 \times 10^{-12} T^3 + 3.59 \times 10^{-9} T^2 - 9.24 \times 10^{-8} T + 8.4605 \times 10^{-5}
    ''')
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        a_p = st.number_input('a_p', value=a_p, format="%e")
    with col6:
        b_p = st.number_input('b_p', value=b_p, format="%e")
    with col7:
        c_p = st.number_input('c_p', value=c_p, format="%e")
    with col8:
        d_p = st.number_input('d_p', value=d_p, format="%e")


# 计算Seebeck数据
    alpha_n_values = calculate_coefficient(T_range, a_n, b_n, c_n, d_n)
    alpha_p_values = calculate_coefficient(T_range, a_p, b_p, c_p, d_p)

# 输出Seebeck数据图表


        # 假设 T_range, alpha_n_values, alpha_p_values 是已经定义好的数据列表
        # 创建 DataFrame
    data = pd.DataFrame({
        '温度 (K)': T_range,
        'N型 α (V/K)': alpha_n_values,
        'P型 α (V/K)': alpha_p_values
    })

    # 创建图表
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(T_range, alpha_n_values, label=r'N型 α', color='blue')
    ax.plot(T_range, alpha_p_values, label=r'P型 α', color='red')
    ax.set_xlabel(u'温度 (K)')
    ax.set_ylabel(u'Seebeck 系数 (V/K)')
    ax.set_title('Seebeck 系数随温度变化')
    ax.legend()
    st.pyplot(fig)

    # 将 DataFrame 转换为 CSV 并创建下载链接
    def convert_df_to_csv(df):
        output = BytesIO()
        df.to_csv(output, index=False, encoding='utf-8-sig')  # 使用utf-8-sig ，确保index=False除非你想要行号编码
        output.seek(0)
        return output

    csv = convert_df_to_csv(data)

    st.download_button(
        label="下载 Seebeck 数据",
        data=csv,
        file_name='seebeck_data.csv',
        mime='text/csv',
    )



# 自定义电阻率公式
with st.expander("输入电阻率公式系数（拟合温度：200~600K）"):
    st.write("#### N型材料电阻率公式系数")
    
    st.latex(r'''
    \rho_n = -2.5786 \times 10^{-13} T^3 + 1.9767 \times 10^{-10} T^2 - 6.0208 \times 10^{-9} T + 5.7588 \times 10^{-7}
    ''')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        rho_a_n = st.number_input('ρ_a_n', value=rho_a_n, format="%e")
    with col2:
        rho_b_n = st.number_input('ρ_b_n', value=rho_b_n, format="%e")
    with col3:
        rho_c_n = st.number_input('ρ_c_n', value=rho_c_n, format="%e")
    with col4:
        rho_d_n = st.number_input('ρ_d_n', value=rho_d_n, format="%e")

    st.write("#### P型材料电阻率公式系数")
    st.latex(r'''
    \rho_p = -7.9299 \times 10^{-13} T^3 + 8.6932 \times 10^{-10} T^2 - 2.506 \times 10^{-7} T + 2.8215 \times 10^{-5}
    ''')
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        rho_a_p = st.number_input('ρ_a_p', value=rho_a_p, format="%e")
    with col6:
        rho_b_p = st.number_input('ρ_b_p', value=rho_b_p, format="%e")
    with col7:
        rho_c_p = st.number_input('ρ_c_p', value=rho_c_p, format="%e")
    with col8:
        rho_d_p = st.number_input('ρ_d_p', value=rho_d_p, format="%e")


# 计算电阻率数据
    rho_n_values = calculate_coefficient(T_range, rho_a_n, rho_b_n, rho_c_n, rho_d_n)
    rho_p_values = calculate_coefficient(T_range, rho_a_p, rho_b_p, rho_c_p, rho_d_p)

# 输出电阻率数据图表
    # 电阻率数据图表
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(T_range, rho_n_values, label=r'N型 ρ', color='orange')
    ax.plot(T_range, rho_p_values, label=r'P型 ρ', color='brown')
    ax.set_xlabel(u'温度 (K)')
    ax.set_ylabel(u'电阻率 (Ω·m)')
    ax.set_title('电阻率随温度变化')
    ax.legend()
    st.pyplot(fig)

    # 将电阻率数据转换为 DataFrame
    data_resistivity = pd.DataFrame({
        '温度 (K)': T_range,
        'N型 ρ (Ω·m)': rho_n_values,
        'P型 ρ (Ω·m)': rho_p_values
    })

    # 转换 DataFrame 为 CSV
    def convert_df_to_csv(df):
        output = BytesIO()
        df.to_csv(output, index=False, encoding='utf-8-sig')  # 确保 UTF-8 编码解决中文问题
        output.seek(0)
        return output

    csv_resistivity = convert_df_to_csv(data_resistivity)

    # 添加下载按钮
    st.download_button(
        label="下载电阻率数据",
        data=csv_resistivity,
        file_name='resistivity_data.csv',
        mime='text/csv',
    )


# 自定义导热率公式
with st.expander("输入导热率公式系数（拟合温度：200~600K）"):
    st.write("#### N型材料导热率公式系数")
    st.latex(r'''
    \lambda_n = 2.36 \times 10^{-5} T^2 - 0.015 T + 3.806
    ''')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        lambda_a_n = st.number_input('ρ_a_n', value=lambda_a_n, format="%e")
    with col2:
        lambda_b_n = st.number_input('ρ_b_n', value=lambda_b_n, format="%e")
    with col3:
        lambda_c_n = st.number_input('ρ_c_n', value=lambda_c_n, format="%e")
    with col4:
        lambda_d_n = st.number_input('ρ_d_n', value=lambda_d_n, format="%e")

    st.write("#### P型材料导热率公式系数")
    st.latex(r'''
    \lambda_p = 3.2 \times 10^{-5} T^2 - 0.0216 T + 4.949
    ''')

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        lambda_a_p = st.number_input('ρ_a_p', value=lambda_a_p, format="%e")
    with col6:
        lambda_b_p = st.number_input('ρ_b_p', value=lambda_b_p, format="%e")
    with col7:
        lambda_c_p = st.number_input('ρ_c_p', value=lambda_c_p, format="%e")
    with col8:
        lambda_d_p = st.number_input('ρ_d_p', value=lambda_d_p, format="%e")
# 计算导热率数据
    lambda_n_values = calculate_coefficient(T_range, lambda_a_n, lambda_b_n, lambda_c_n, lambda_d_n)
    lambda_p_values = calculate_coefficient(T_range, lambda_a_p, lambda_b_p, lambda_c_p, lambda_d_p)
# 输出导热率数据图表
    # 输出导热率数据图表
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(T_range, lambda_n_values, label=r'N型 λ', color='green')
    ax.plot(T_range, lambda_p_values, label=r'P型 λ', color='purple')
    ax.set_xlabel(u'温度 (K)')
    ax.set_ylabel(u'热导率 (W/m·K)')
    ax.set_title('热导率随温度变化')
    ax.legend()
    st.pyplot(fig)

    # 将导热率数据转换为 DataFrame
    data_conductivity = pd.DataFrame({
        '温度 (K)': T_range,
        'N型 λ (W/m·K)': lambda_n_values,
        'P型 λ (W/m·K)': lambda_p_values
    })

    # 转换 DataFrame 为 CSV
    def convert_df_to_csv(df):
        output = BytesIO()
        df.to_csv(output, index=False, encoding='utf-8-sig')  # 确保 UTF-8 编码解决中文问题
        output.seek(0)
        return output

    csv_conductivity = convert_df_to_csv(data_conductivity)

    # 添加下载按钮
    st.download_button(
        label="下载热导率数据",
        data=csv_conductivity,
        file_name='conductivity_data.csv',
        mime='text/csv',
    )



# 显示计算结果
with st.expander("计算结果", expanded=True):














    # 计算N型材料的平均物性值
    avg_lambda_n = calculate_average_property(lambda_func, T_c, T_h, coeffs_lambda_n)
    avg_rho_n = calculate_average_property(rho_func, T_c, T_h, coeffs_rho_n)
    avg_seebeck_n = calculate_average_property(seebeck_func, T_c, T_h, coeffs_seebeck_n)

    # 计算P型材料的平均物性值
    avg_lambda_p = calculate_average_property(lambda_func, T_c, T_h, coeffs_lambda_p)
    avg_rho_p = calculate_average_property(rho_func, T_c, T_h, coeffs_rho_p)
    avg_seebeck_p = calculate_average_property(seebeck_func, T_c, T_h, coeffs_seebeck_p)

    
    S_total = abs(avg_seebeck_n) + abs(avg_seebeck_p)
    lambda_total = avg_lambda_p  + avg_lambda_n
    rho_total = avg_rho_n  + avg_rho_p
    R_n = avg_rho_n * (H / A)
    R_p = avg_rho_p * (H / A)
    R_total = R_n + R_p
    Delta_T = T_h - T_c
    P = (S_total * Delta_T)**2 / R_total  
    U = (P * R_total)**0.5
    ZT = (S_total**2 * T_avg) / ((lambda_total) * rho_total)

    # 计算最大功率下的电流
    I_max_power = U/(2* R_total)


    # 计算最大功率
    P_max = (S_total * Delta_T)**2 / (4 * rho_total)

    # 计算热端热流 Q_h

        # 计算各部分热流
    Q_Seebeck = S_total * I_max_power * T_avg
    Q_conductive = lambda_total * (T_h - T_c)
    Q_joule = 0.5 * I_max_power**2 * R_total

        # 总热流
    Q_h = Q_Seebeck + Q_conductive + Q_joule


    
    # 计算最大功率转换效率
    eta = P_max / Q_h

    # 计算电流密度
    J = I_max_power / A  # 电流密度, 单位: 安培/平方米




 





# 5. 扩展数据（动态加载更多）
with st.expander("计算结果"):

    # 标题
    st.title("计算结果展示")

    # 1. 基础物性值
    st.subheader("基础物性值")
    cols1 = st.columns(3)
    cols1[0].metric(label="N型材料平均Seebeck系数", value=f"{avg_seebeck_n:.3e} V/K")
    cols1[1].metric(label="P型材料平均Seebeck系数", value=f"{avg_seebeck_p:.3e} V/K")
    cols1[2].metric(label="总平均Seebeck系数", value=f"{S_total:.3e} V/K")

    cols2 = st.columns(2)
    cols2[0].metric(label="N型材料平均导热率", value=f"{avg_lambda_n:.3f} W/m·K")
    cols2[1].metric(label="P型材料平均导热率", value=f"{avg_lambda_p:.3f} W/m·K")

    cols3 = st.columns(2)
    cols3[0].metric(label="N型材料平均电阻率", value=f"{avg_rho_n:.3e} Ω·m")
    cols3[1].metric(label="P型材料平均电阻率", value=f"{avg_rho_p:.3e} Ω·m")

    st.metric(label="总电阻", value=f"{R_total:.3e} Ω")

    # 2. 电性能指标
    st.subheader("电性能指标")
    cols4 = st.columns(3)
    cols4[0].metric(label="温度区间平均ZT值", value=f"{ZT:.3f}")
    cols4[1].metric(label="总电压", value=f"{U:.3f} V")
    cols4[2].metric(label="电流密度", value=f"{J/1e6:.3f} A/mm²")

    cols5 = st.columns(2)
    cols5[0].metric(label="最大功率下的电流", value=f"{I_max_power:.3f} A")
    cols5[1].metric(label="最大输出电功率", value=f"{P_max:.3f} W")

    # 3. 热流计算
    st.subheader("最大功率下的热流")
    st.latex(r'''
    Q_h = \alpha_{\text{总}} \cdot T_c \cdot I + K(T_h - T_c) + \frac{1}{2} I^2 R
    ''')

    cols6 = st.columns(4)
    cols6[0].metric(label="Seebeck效应产生的热", value=f"{Q_Seebeck:.3f} W")
    cols6[1].metric(label="热导损失的热流", value=f"{Q_conductive:.3f} W")
    cols6[2].metric(label="焦耳热产生的热", value=f"{Q_joule:.3f} W")
    cols6[3].metric(label="总热流", value=f"{Q_h:.3f} W")

    # 4. 转换效率
    st.subheader("最大功率转换效率")
    st.metric(label="效率", value=f"{eta * 100:.3f}%")



# 增加电池个数的展示
with st.expander("增加电池个数"):
    st.write("### 配置选项")
    SN = st.number_input('电池个数', value=1, min_value=1, max_value=100000, step=1)
    Q_joule_n = 0.5 * I_max_power**2 * SN * R_total
    P_max_n = (S_total * Delta_T)**2 / (4 * SN * rho_total)  # 重新计算最大功率
    Q_h_n = Q_h - Q_joule + Q_joule_n
    eta_n = P_max / Q_h_n
    st.write("### 计算影响")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label=f"{SN}个串联电池总电阻", value=f"{SN*1000*R_total:.2f} mmΩ")
    with col2:
        st.metric(label=f"{SN}个串联电池总电压", value=f"{SN*U:.3f} V")
    with col3:
        st.metric(label=f"{SN}个串联电池最大功率下的电流", value=f"{I_max_power:.1f} A")
    with col4:
        st.metric(label=f"{SN}个串联电池最大输出电功率", value=f"{P_max_n:.1f} W")
    st.write("### 热流分析")
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric(label="Seebeck效应热", value=f"{Q_Seebeck:.1f} W")
    with col6:
        st.metric(label="热导损失热流", value=f"{Q_conductive:.1f} W")
    with col7:
        st.metric(label="焦耳热产生的热", value=f"{Q_joule_n:.3f} W")
    with col8:
        st.metric(label=f"{SN}个电池的总热流", value=f"{Q_h_n:.1f} W")

# 变温度计算
# 变温度计算
# 变温度计算
# 变温度计算
# 变温度计算
# 变温度计算
# 变温度计算
# 变温度计算
# 变温度计算
# 变温度计算
# 变温度计算
# 变温度计算




# 计算ZT
def calculate_ZT(T_range, a_n, b_n, c_n, d_n, a_p, b_p, c_p, d_p, 
                 rho_a_n, rho_b_n, rho_c_n, rho_d_n, rho_a_p, rho_b_p, rho_c_p, rho_d_p, 
                 lambda_a_n, lambda_b_n, lambda_c_n, lambda_d_n, lambda_a_p, lambda_b_p, lambda_c_p, lambda_d_p):

    # 计算Seebeck系数（已有）


    # 计算电导率（已有）


    # 计算热导率（已有）


    # 计算ZT值
    ZT_n_values = (alpha_n_values**2 * T_range) / (lambda_n_values * rho_n_values)
    ZT_p_values = (alpha_p_values**2 * T_range) / (lambda_p_values * rho_p_values)

    # 总ZT值
    ZT_total_values = ZT_n_values + ZT_p_values

    return ZT_total_values

# 计算ZT并绘制图形
ZT_values = calculate_ZT(T_range, a_n, b_n, c_n, d_n, a_p, b_p, c_p, d_p, 
                         rho_a_n, rho_b_n, rho_c_n, rho_d_n, rho_a_p, rho_b_p, rho_c_p, rho_d_p, 
                         lambda_a_n, lambda_b_n, lambda_c_n, lambda_d_n, lambda_a_p, lambda_b_p, lambda_c_p, lambda_d_p)

# 自定义导热率公式
with st.expander("温度曲线图"):
# 绘制ZT曲线图
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(T_range, ZT_values, label=r'ZT（P和N）', color='green')
    ax.set_xlabel(u'温度 (K)')
    ax.set_ylabel(u'ZT 值')
    ax.set_title('ZT 随温度变化')
    ax.legend()
    st.pyplot(fig)













    # 计算最大功率
    def calculate_max_power(S_total, Delta_T, rho_total):
        P_max = (S_total**2 * Delta_T**2) / (4 * rho_total)  # 最大功率公式
        return P_max

    # 计算热端总热流
    def calculate_total_heat_flow(S_total, I_max_power, T_avg, lambda_total, T_h, T_c, rho_total):
        Q_Seebeck = S_total * I_max_power * T_avg  # Seebeck效应产生的热流
        Q_conductive = lambda_total * (T_h - T_c)  # 热导产生的热流
        Q_joule = 0.5 * I_max_power**2 * rho_total  # 焦耳热产生的热流
        Q_h = Q_Seebeck + Q_conductive + Q_joule  # 总热流
        return Q_h, Q_Seebeck, Q_conductive, Q_joule

    # 计算最大效率
    def calculate_efficiency(P_max, Q_h):
        return P_max / Q_h  # 最大效率公式

    # 计算每个温度下的最大功率、最大效率、热流
    P_max_values = []
    efficiency_values = []
    Q_h_values = []
    Q_Seebeck_values = []
    Q_conductive_values = []
    Q_joule_values = []

    for T in T_range:
        # 计算当前温度下的各个值
        Delta_T = T - T_c  # 计算温差
        S_total = abs(calculate_coefficient(T, a_n, b_n, c_n, d_n)) + abs(calculate_coefficient(T, a_p, b_p, c_p, d_p))
        lambda_total = calculate_coefficient(T, lambda_a_n, lambda_b_n, lambda_c_n, lambda_d_n) + calculate_coefficient(T, lambda_a_p, lambda_b_p, lambda_c_p, lambda_d_p)
        rho_total = calculate_coefficient(T, rho_a_n, rho_b_n, rho_c_n, rho_d_n) + calculate_coefficient(T, rho_a_p, rho_b_p, rho_c_p, rho_d_p)
        
        # 计算最大功率
        P_max = calculate_max_power(S_total, Delta_T, rho_total)  # 使用当前温度和温差计算最大功率
        P_max_values.append(P_max)
        
        # 计算热流
        I_max_power = (S_total * Delta_T) / (2 * rho_total)
        Q_h, Q_Seebeck, Q_conductive, Q_joule = calculate_total_heat_flow(S_total, I_max_power, T, lambda_total, T, T_c, rho_total)
        Q_h_values.append(Q_h)
        Q_Seebeck_values.append(Q_Seebeck)
        Q_conductive_values.append(Q_conductive)
        Q_joule_values.append(Q_joule)

        # 计算效率
        eta2 = calculate_efficiency(P_max, Q_h)
        efficiency_values.append(eta2)

        



    # 计算电压
    def calculate_voltage(S_total, Delta_T, R_total):
        I = (S_total * Delta_T) / R_total  # 计算电流
        U = P_max / I  # 使用最大功率和电流计算电压
        return U

    # 计算每个温度下的电压
    voltage_values = []

    for T in T_range:
        Delta_T = T - T_c  # 计算温差
        S_total = abs(calculate_coefficient(T, a_n, b_n, c_n, d_n)) + abs(calculate_coefficient(T, a_p, b_p, c_p, d_p))
        lambda_total = calculate_coefficient(T, lambda_a_n, lambda_b_n, lambda_c_n, lambda_d_n) + calculate_coefficient(T, lambda_a_p, lambda_b_p, lambda_c_p, lambda_d_p)
        rho_total = calculate_coefficient(T, rho_a_n, rho_b_n, rho_c_n, rho_d_n) + calculate_coefficient(T, rho_a_p, rho_b_p, rho_c_p, rho_d_p)

        # 计算最大功率
        P_max = calculate_max_power(S_total, Delta_T, rho_total)

        # 计算电压
        voltage = calculate_voltage(S_total, Delta_T, rho_total)
        voltage_values.append(voltage)

    # 绘制电压关于温度的曲线
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(T_range, voltage_values, label='电压 U', color='purple')
    ax.set_xlabel(u'温度 (K)')
    ax.set_ylabel(u'电压 (V)')
    ax.set_title('电压随温度变化')
    ax.legend()
    st.pyplot(fig)













        


    # 绘制最大功率曲线
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(T_range, P_max_values, label='最大功率 P', color='blue')  # 使用普通文本而不是LaTeX
    ax.set_xlabel(u'温度 (K)')
    ax.set_ylabel(u'最大功率 (W)')
    ax.set_title('最大功率随温度变化')
    ax.legend()
    st.pyplot(fig)



    # 绘制热流曲线
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(T_range, Q_h_values, label='总热流 Qh', color='green')  # 使用普通文本而不是LaTeX
    ax.plot(T_range, Q_Seebeck_values, label='Seebeck效应热 QSeebeck', color='orange')  # 使用普通文本
    ax.plot(T_range, Q_conductive_values, label='热导损失热流 Qconductive', color='purple')  # 使用普通文本
    ax.plot(T_range, Q_joule_values, label='焦耳热 Qjoule', color='brown')  # 使用普通文本
    ax.set_xlabel(u'温度 (K)')
    ax.set_ylabel(u'热流 (W)')
    ax.set_title('不同热流随温度变化')
    ax.legend()
    st.pyplot(fig)


    # 绘制最大效率曲线
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(T_range, efficiency_values, label='最大效率 η', color='red')  # 使用普通文本而不是LaTeX
    ax.set_xlabel(u'温度 (K)')
    ax.set_ylabel(u'效率')
    ax.set_title('温度区间的最大效率')
    ax.legend()
    st.pyplot(fig)
















