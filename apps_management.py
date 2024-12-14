import streamlit as st
import socket
import requests
import json
from datetime import datetime

def get_local_ip():
    try:
        # 获取本地主机名
        hostname = socket.gethostname()
        # 获取本地IP
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        return f"获取本地IP失败: {str(e)}"

def get_public_ip():
    try:
        # 使用公共API获取公网IP
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()['ip']
        return "获取公网IP失败"
    except Exception as e:
        return f"获取公网IP失败: {str(e)}"

def get_ip_info(ip):
    try:
        # 使用 ip-api.com 获取IP详细信息
        response = requests.get(f'http://ip-api.com/json/{ip}')
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

def main():
    st.set_page_config(page_title="服务器 IP 查看器", page_icon="🌐")
    
    st.title("服务器 IP 查看器 🖥️")
    
    # 添加刷新按钮
    if st.button("刷新数据 🔄"):
        st.experimental_rerun()
    
    # 显示当前时间
    st.write(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 创建两列布局
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("本地网络信息")
        local_ip = get_local_ip()
        st.info(f"本地 IP: {local_ip}")
        
        # 获取本地IP的详细信息
        local_ip_info = get_ip_info(local_ip)
        if local_ip_info and local_ip_info['status'] == 'success':
            st.json(local_ip_info)
    
    with col2:
        st.subheader("公网信息")
        public_ip = get_public_ip()
        st.info(f"公网 IP: {public_ip}")
        
        # 获取公网IP的详细信息
        public_ip_info = get_ip_info(public_ip)
        if public_ip_info and public_ip_info['status'] == 'success':
            st.json(public_ip_info)

    # 添加网络连接测试
    st.subheader("网络连接测试")
    if st.button("测试网络连接"):
        with st.spinner("正在测试..."):
            try:
                # 测试几个常用网站的连接
                sites = {
                    "百度": "www.baidu.com",
                    "谷歌": "www.google.com",
                    "GitHub": "github.com"
                }
                
                results = {}
                for name, site in sites.items():
                    try:
                        socket.create_connection((site, 80), timeout=3)
                        results[name] = "连接成功 ✅"
                    except:
                        results[name] = "连接失败 ❌"
                
                # 显示测试结果
                for name, result in results.items():
                    st.write(f"{name}: {result}")
            except Exception as e:
                st.error(f"测试过程中出现错误: {str(e)}")

if __name__ == "__main__":
    main()
