import streamlit as st
import pandas as pd
import numpy as np
from binance.client import Client
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import json
import time

# 初始化Binance客户端
def init_client():
    api_key = "yP3j70Kp6DdP12ZYHPzz3kn7X2Mc2TYOLRgYxG2onlCodzqWnBZ1q1tONTifYBHL95"
    api_secret = "2BfmKSLHcEo7o7GKrfIZV1D1EtLmRU0w1pSgCt3DU86QfJShd44D32v1RxnqKgT988"
    return Client(api_key, api_secret)

# 主应用类
class OptionsManagementApp:
    def __init__(self):
        self.client = init_client()
        
    def run(self):
        st.title("加密货币期权管理系统")
        
        # 侧边栏设置
        st.sidebar.title("控制面板")
        menu = st.sidebar.selectbox(
            "选择功能",
            ["期权搜索与排序", "市场分析", "交易管理", "自动化策略", "风险管理", "历史记录"]
        )
        
        if menu == "期权搜索与排序":
            self.options_search_page()
        elif menu == "市场分析":
            self.market_analysis_page()
        elif menu == "交易管理":
            self.trading_management_page()
        elif menu == "自动化策略":
            self.automation_page()
        elif menu == "风险管理":
            self.risk_management_page()
        elif menu == "历史记录":
            self.history_page()

    def options_search_page(self):
        st.header("期权搜索与排序")
        
        # 搜索条件
        col1, col2, col3 = st.columns(3)
        with col1:
            symbol = st.selectbox("选择交易对", ["BTC/USDT", "ETH/USDT"])
        with col2:
            expiry_days = st.slider("到期天数", 0, 90, 30)
        with col3:
            sort_by = st.selectbox("排序依据", ["标记价格", "买价", "卖价", "成交量", "持仓量"])
            
        # 高级筛选
        with st.expander("高级筛选"):
            min_price = st.number_input("最低价格", 0.0)
            max_price = st.number_input("最高价格", 99999.0)
            option_type = st.multiselect("期权类型", ["看涨", "看跌"])
            
        # 获取并显示期权数据
        options_data = self.fetch_options_data(symbol, expiry_days)
        self.display_options_table(options_data, sort_by)
        
    def market_analysis_page(self):
        st.header("市场分析")
        
        # 市场概览
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("24h成交量", "$1.2M")
        with col2:
            st.metric("总持仓量", "$5.6M")
        with col3:
            st.metric("看涨/看跌比率", "1.2")
            
        # 价格趋势图
        st.subheader("价格趋势")
        self.plot_price_trend()
        
        # 波动率分析
        st.subheader("波动率分析")
        self.plot_volatility()
        
    def trading_management_page(self):
        st.header("交易管理")
        
        # 当前持仓
        st.subheader("当前持仓")
        positions = self.get_current_positions()
        st.dataframe(positions)
        
        # 交易下单
        st.subheader("新建交易")
        col1, col2 = st.columns(2)
        with col1:
            trade_type = st.selectbox("交易类型", ["买入看涨", "买入看跌", "卖出看涨", "卖出看跌"])
            quantity = st.number_input("数量", min_value=0.0)
        with col2:
            price = st.number_input("价格", min_value=0.0)
            st.button("下单")

    def automation_page(self):
        st.header("自动化策略")
        
        # 添加新策略
        st.subheader("创建新策略")
        strategy_name = st.text_input("策略名称")
        
        # 策略条件设置
        with st.expander("设置策略条件"):
            condition_type = st.selectbox("条件类型", ["价格触发", "时间触发", "波动率触发"])
            if condition_type == "价格触发":
                trigger_price = st.number_input("触发价格")
            elif condition_type == "时间触发":
                trigger_time = st.time_input("触发时间")
            
        # 策略动作设置
        with st.expander("设置策略动作"):
            action_type = st.selectbox("动作类型", ["市价买入", "限价买入", "市价卖出", "限价卖出"])
            action_quantity = st.number_input("交易数量")
            
        if st.button("保存策略"):
            st.success("策略已保存")
            
    def risk_management_page(self):
        st.header("风险管理")
        
        # 风险指标
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("当前风险度", "65%")
        with col2:
            st.metric("最大回撤", "-12%")
        with col3:
            st.metric("盈亏比", "1.5")
            
        # 持仓分析
        st.subheader("持仓分析")
        self.plot_position_analysis()
        
    def history_page(self):
        st.header("历史记录")
        
        # 时间范围选择
        date_range = st.date_input("选择时间范围", [])
        
        # 历史交易记录
        st.subheader("交易历史")
        history = self.get_trading_history()
        st.dataframe(history)
        
        # 盈亏分析
        st.subheader("盈亏分析")
        self.plot_pnl_analysis()

    # 辅助方法
    def fetch_options_data(self, symbol, expiry_days):
        # 模拟数据，实际应用中替换为真实API调用
        data = {
            "symbol": [symbol] * 10,
            "strike_price": np.random.uniform(10000, 50000, 10),
            "mark_price": np.random.uniform(100, 1000, 10),
            "bid": np.random.uniform(90, 950, 10),
            "ask": np.random.uniform(110, 1050, 10),
            "volume": np.random.randint(1, 1000, 10),
            "open_interest": np.random.randint(100, 10000, 10),
        }
        return pd.DataFrame(data)

    def display_options_table(self, df, sort_by):
        st.dataframe(df)

    def plot_price_trend(self):
        # 示例价格趋势图
        dates = pd.date_range(start="2024-01-01", periods=30)
        prices = np.random.normal(100, 10, 30).cumsum()
        fig = px.line(x=dates, y=prices)
        st.plotly_chart(fig)

    def plot_volatility(self):
        # 示例波动率图
        dates = pd.date_range(start="2024-01-01", periods=30)
        volatility = np.random.uniform(0.1, 0.4, 30)
        fig = px.line(x=dates, y=volatility)
        st.plotly_chart(fig)

    def get_current_positions(self):
        # 模拟当前持仓数据
        data = {
            "期权类型": ["看涨", "看跌"],
            "持仓量": [10, 5],
            "均价": [100, 200],
            "当前价值": [1050, 980],
            "盈亏": [50, -20]
        }
        return pd.DataFrame(data)

    def plot_position_analysis(self):
        # 示例持仓分析图
        labels = ['看涨期权', '看跌期权']
        values = [60, 40]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        st.plotly_chart(fig)

    def get_trading_history(self):
        # 模拟交易历史数据
        data = {
            "时间": pd.date_range(start="2024-01-01", periods=5),
            "类型": ["买入看涨", "卖出看跌", "买入看涨", "卖出看涨", "买入看跌"],
            "价格": [100, 200, 150, 180, 120],
            "数量": [1, 2, 1, 1, 3],
            "状态": ["已完成"] * 5
        }
        return pd.DataFrame(data)

    def plot_pnl_analysis(self):
        # 示例盈亏分析图
        dates = pd.date_range(start="2024-01-01", periods=30)
        pnl = np.random.normal(0, 100, 30).cumsum()
        fig = px.line(x=dates, y=pnl)
        st.plotly_chart(fig)

# 运行应用
if __name__ == "__main__":
    app = OptionsManagementApp()
    app.run()
