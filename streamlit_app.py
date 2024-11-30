import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import streamlit as st


# 设置字体为宋体
matplotlib.rcParams['font.sans-serif'] = ['SimSun']  # 中文宋体
matplotlib.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题


# 标题和简介
st.title('热电模块性能计算-20241130-wjj')
st.write('这个应用程序允许用户输入温差电池的尺寸、温度以及物料属性，计算和展示热电模块的性能参数。')

# 显示公式
st.write("""## 参考公式""")

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
- \( △T \) 为温差（热端温度与冷端温度之差）；
- \( R \) 为总电阻。

**功率公式的物理意义**：用于计算热电模块的发电输出功率，结果以瓦特 (W) 为单位。
""")

# 显示公式
st.write("""## 参考公式""")

# 定义函数用于计算材料属性
def calculate_coefficient(T, a, b, c, d):
    return a * T**3 + b * T**2 + c * T + d

# 定义温度范围
T_range = np.linspace(200, 600, 400)

# 初始化公式参数
a_n, b_n, c_n, d_n = -1.045e-11, 9.337e-9, -2.649e-6, 4.4603e-4
a_p, b_p, c_p, d_p = -6.373e-12, 3.59e-9, -9.24e-8, 8.4605e-5
rho_a_n, rho_b_n, rho_c_n, rho_d_n = -2.5786e-13, 1.9767e-10, -6.0208e-9, 5.7588e-7
rho_a_p, rho_b_p, rho_c_p, rho_d_p = -7.9299e-13, 8.6932e-10, -2.506e-7, 2.8215e-5
lambda_a_n, lambda_b_n, lambda_c_n, lambda_d_n = 0, 2.36e-5, - 0.015, 3.806
lambda_a_p, lambda_b_p, lambda_c_p, lambda_d_p = 0, 3.2e-5, - 0.0216, 4.949

# 用户输入温度
with st.expander("输入温度参数", expanded=True):
    T_h = st.number_input('热端温度 (K)', value=373.0, format="%f")
    T_c = st.number_input('冷端温度 (K)', value=273.0, format="%f")
    T_avg = (T_h + T_c) / 2

# 用户输入材料尺寸
with st.expander("输入材料尺寸"):
    L = st.number_input('长度 (m)', value=0.01, format="%f")
    W = st.number_input('宽度 (m)', value=0.01, format="%f")
    H = st.number_input('高度 (m) [注意：高度为P和N型材料或的高度]', value=0.002, format="%f")
    A = W * L  # 计算截面积

# 用户输入公式系数
with st.expander("输入公式参数"):
    st.write("#### N型材料Seebeck系数公式系数")
    col1, col2 = st.columns(2)
    with col1:
        a_n = st.number_input('a_n', value=a_n, format="%e")
        b_n = st.number_input('b_n', value=b_n, format="%e")
    with col2:
        c_n = st.number_input('c_n', value=c_n, format="%e")
        d_n = st.number_input('d_n', value=d_n, format="%e")

    st.write("#### P型材料Seebeck系数公式系数")
    col3, col4 = st.columns(2)
    with col3:
        a_p = st.number_input('a_p', value=a_p, format="%e")
        b_p = st.number_input('b_p', value=b_p, format="%e")
    with col4:
        c_p = st.number_input('c_p', value=c_p, format="%e")
        d_p = st.number_input('d_p', value=d_p, format="%e")

# 自定义电阻率公式
with st.expander("输入电阻率公式系数（可选）"):
    st.write("#### N型材料电阻率公式系数")
    rho_a_n = st.number_input('ρ_a_n', value=rho_a_n, format="%e")
    rho_b_n = st.number_input('ρ_b_n', value=rho_b_n, format="%e")
    rho_c_n = st.number_input('ρ_c_n', value=rho_c_n, format="%e")
    rho_d_n = st.number_input('ρ_d_n', value=rho_d_n, format="%e")

    st.write("#### P型材料电阻率公式系数")
    rho_a_p = st.number_input('ρ_a_p', value=rho_a_p, format="%e")
    rho_b_p = st.number_input('ρ_b_p', value=rho_b_p, format="%e")
    rho_c_p = st.number_input('ρ_c_p', value=rho_c_p, format="%e")
    rho_d_p = st.number_input('ρ_d_p', value=rho_d_p, format="%e")

# 计算数据
alpha_n_values = calculate_coefficient(T_range, a_n, b_n, c_n, d_n)
alpha_p_values = calculate_coefficient(T_range, a_p, b_p, c_p, d_p)
lambda_n_values = calculate_coefficient(T_range, lambda_a_n, lambda_b_n, lambda_c_n, lambda_d_n)
lambda_p_values = calculate_coefficient(T_range, lambda_a_p, lambda_b_p, lambda_c_p, lambda_d_p)
rho_n_values = calculate_coefficient(T_range, rho_a_n, rho_b_n, rho_c_n, rho_d_n)
rho_p_values = calculate_coefficient(T_range, rho_a_p, rho_b_p, rho_c_p, rho_d_p)

# Seebeck系数曲线模块
with st.expander("Seebeck 系数曲线", expanded=True):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(T_range, alpha_n_values, label=r'N型 α', color='blue')
    ax.plot(T_range, alpha_p_values, label=r'P型 α', color='red')
    ax.set_xlabel('温度 (K)')
    ax.set_ylabel('Seebeck 系数 (V/K)')
    ax.set_title('Seebeck 系数随温度变化')
    ax.legend()
    st.pyplot(fig)

# 热导率曲线模块
with st.expander("热导率曲线", expanded=False):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(T_range, lambda_n_values, label=r'N型 λ', color='green')
    ax.plot(T_range, lambda_p_values, label=r'P型 λ', color='purple')
    ax.set_xlabel('温度 (K)')
    ax.set_ylabel('热导率 (W/m·K)')
    ax.set_title('热导率随温度变化')
    ax.legend()
    st.pyplot(fig)

# 电阻率曲线模块
with st.expander("电阻率曲线", expanded=False):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(T_range, rho_n_values, label=r'N型 ρ', color='orange')
    ax.plot(T_range, rho_p_values, label=r'P型 ρ', color='brown')
    ax.set_xlabel('温度 (K)')
    ax.set_ylabel('电阻率 (Ω·m)')
    ax.set_title('电阻率随温度变化')
    ax.legend()
    st.pyplot(fig)

# 显示计算结果
with st.expander("计算结果", expanded=True):
    alpha_n = calculate_coefficient(T_avg, a_n, b_n, c_n, d_n)
    alpha_p = calculate_coefficient(T_avg, a_p, b_p, c_p, d_p)
    S_total = abs(alpha_n) + abs(alpha_p)

    rho_n = calculate_coefficient(T_avg, rho_a_n, rho_b_n, rho_c_n, rho_d_n)
    rho_p = calculate_coefficient(T_avg, rho_a_p, rho_b_p, rho_c_p, rho_d_p)
    lambda_n = calculate_coefficient(T_avg,lambda_a_n, lambda_b_n, lambda_c_n, lambda_d_n)
    lambda_p = calculate_coefficient(T_avg, lambda_a_p, lambda_b_p, lambda_c_p, lambda_d_p)
    lambda_total = lambda_n  + lambda_p
    rho_total = rho_n  + rho_p
    R_n = rho_n * (H / A)
    R_p = rho_p * (H / A)
    R_total = R_n + R_p
    Delta_T = T_h - T_c
    P = (S_total * Delta_T)**2 / R_total  
    U = (P * R_total)**0.5
    ZT = (S_total**2 * T_avg) / ((lambda_total) * rho_total)


    st.write("### 计算结果")
    st.metric(label="N型材料Seebeck系数", value=f"{alpha_n:.6f} V/K")
    st.metric(label="P型材料Seebeck系数", value=f"{alpha_p:.6f} V/K")
    st.metric(label="总Seebeck系数", value=f"{S_total:.6f} V/K")
    st.metric(label="N型材料电阻率", value=f"{rho_n:.6e} Ω·m")
    st.metric(label="P型材料电阻率", value=f"{rho_p:.6e} Ω·m")
    st.metric(label="总电阻", value=f"{R_total:.6f} Ω")
    st.metric(label="ZT值", value=f"{ZT:.6f} ")  
    st.metric(label="总电压", value=f"{U:.6f} V")    
    st.metric(label="发电功率", value=f"{P:.6f} W")
