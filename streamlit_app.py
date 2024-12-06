import streamlit as st
# 确保 set_page_config 是第一个 Streamlit 命令
st.set_page_config(page_title="WJJ 应用集合", layout="wide")

from streamlit_option_menu import option_menu
import json
import os
import shutil
from datetime import datetime
import random
import string
import base64
import importlib.util
import sys
from typing import Dict, List, Optional

# 配置常量
CONFIG_FILE = "apps_config.json"
BACKUP_DIR = "backups"
UPLOAD_DIR = "uploaded_apps"
DEFAULT_CONFIG = {
    "apps": [],
    "categories": [
        {"id": "default", "name": "默认分组", "icon": "folder"},
        {"id": "analysis", "name": "数据分析", "icon": "graph-up"},
        {"id": "tools", "name": "工具集合", "icon": "tools"},
        {"id": "simulation", "name": "仿真模拟", "icon": "pc-display"},
    ]
}
ICON_LIST = [
    "https://img.icons8.com/color/48/000000/bar-chart.png",
    "https://img.icons8.com/color/48/000000/data-configuration.png",
    "https://img.icons8.com/ios-filled/50/000000/electricity.png",
    "https://img.icons8.com/color/48/000000/python.png",
    "https://img.icons8.com/color/48/000000/code.png"
]

# 自定义CSS样式
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .app-card {
        padding: 1rem;
        border-radius: 10px;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .category-section {
        margin-top: 2rem;
        padding: 1rem;
        border-radius: 10px;
        background: #f8f9fa;
    }
    .search-box {
        padding: 0.5rem;
        margin-bottom: 1rem;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .nav-category {
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        background: #f1f3f5;
    }
</style>
""", unsafe_allow_html=True)

class AppManager:
    def __init__(self):
        self.apps_config = self.load_apps_config()
        self.initialize_if_empty()

    def generate_random_id(self) -> str:
        """生成随机应用ID"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

    def generate_random_title(self) -> str:
        """生成随机应用标题"""
        prefixes = ["智能", "自动化", "高效", "创新", "专业"]
        suffixes = ["分析工具", "处理系统", "管理器", "辅助工具", "控制台"]
        return f"{random.choice(prefixes)}{random.choice(suffixes)}"

    def generate_random_description(self) -> str:
        """生成随机应用描述"""
        features = ["高效", "智能", "便捷", "专业", "创新"]
        functions = ["数据分析", "流程管理", "自动化处理", "性能优化", "系统控制"]
        benefits = ["提高效率", "节省时间", "优化性能", "降低成本", "提升体验"]
        return f"这是一个{random.choice(features)}的{random.choice(functions)}工具，能够{random.choice(benefits)}。"

    def load_module(self, app_id: str, code: str) -> Optional[object]:
        """加载Python模块"""
        try:
            spec = importlib.util.spec_from_loader(
                app_id,
                loader=None,
                origin=os.path.join(UPLOAD_DIR, f"{app_id}.py")
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[app_id] = module
            exec(code, module.__dict__)
            return module
        except Exception as e:
            st.error(f"加载模块失败: {str(e)}")
            return None

    def delete_app(self, app_id: str) -> bool:
        """删除应用及其相关文件"""
        try:
            # 删除应用文件
            app_file = os.path.join(UPLOAD_DIR, f"{app_id}.py")
            if os.path.exists(app_file):
                os.remove(app_file)
            
            # 从配置中移除应用
            self.apps_config["apps"] = [
                app for app in self.apps_config["apps"] 
                if app["id"] != app_id
            ]
            
            # 从系统模块中移除
            if app_id in sys.modules:
                del sys.modules[app_id]
            
            self.save_apps_config()
            return True
        except Exception as e:
            st.error(f"删除应用失败: {str(e)}")
            return False

    def initialize_if_empty(self):
        """初始化配置文件如果它是空的或损坏的"""
        if not self.apps_config or "apps" not in self.apps_config or "categories" not in self.apps_config:
            self.reset_to_factory()

    def reset_to_factory(self):
        """重置为出厂设置"""
        try:
            # 清除上传的应用
            if os.path.exists(UPLOAD_DIR):
                shutil.rmtree(UPLOAD_DIR)
            os.makedirs(UPLOAD_DIR)

            # 重置配置文件
            self.apps_config = DEFAULT_CONFIG.copy()
            self.save_apps_config()
            return True
        except Exception as e:
            st.error(f"重置失败: {str(e)}")
            return False

    def load_apps_config(self) -> Dict:
        """加载应用配置"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"加载配置文件失败: {str(e)}")
        return DEFAULT_CONFIG.copy()

    def save_apps_config(self) -> bool:
        """保存应用配置"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.apps_config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            st.error(f"保存配置文件失败: {str(e)}")
            return False

    def get_apps_by_category(self, category_id: str) -> List[Dict]:
        """获取指定分类的应用列表"""
        return [app for app in self.apps_config["apps"] if app.get("category", "default") == category_id]

    def render_app_card(self, app: Dict, run_callback):
        """渲染应用卡片"""
        with st.container():
            card_html = f'''
            <div class="app-card" onclick="/">
                <div style="display: flex; align-items: center;">
                    <img src="{app['icon']}" style="width: 40px; height: 40px; margin-right: 15px;">
                    <div>
                        <h3 style="margin: 0;">{app['title']}</h3>
                        <p style="margin: 5px 0 0 0; color: #666;">{app['description']}</p>
                    </div>
                </div>
            </div>
            '''
            if st.markdown(card_html, unsafe_allow_html=True):
                run_callback(app["id"])

    def render_app_details_compact(self):
        """渲染应用详情列表"""
        st.markdown("## 📱 应用列表")
        
        # 搜索框
        search_query = st.text_input("🔍 搜索应用", key="search_apps")
        
        # 按分类显示应用
        for category in self.apps_config["categories"]:
            apps_in_category = self.get_apps_by_category(category["id"])
            
            # 如果有搜索查询，过滤应用
            if search_query:
                apps_in_category = [
                    app for app in apps_in_category
                    if search_query.lower() in app["title"].lower() or 
                       search_query.lower() in app["description"].lower()
                ]
            
            if apps_in_category:
                with st.container():
                    st.markdown(f"### {category['name']}")
                    for app in apps_in_category:
                        self.render_app_card(app, self.run_app)

    def render_navigation(self):
        """渲染导航栏"""
        with st.sidebar:
            # 搜索框
            search_query = st.text_input("🔍 搜索", key="search_nav")
            
            menu_items = ["主页", "设置"]
            icons = ["house", "gear"]
            
            # 按分类组织应用
            for category in self.apps_config["categories"]:
                apps_in_category = self.get_apps_by_category(category["id"])
                
                # 搜索过滤
                if search_query:
                    apps_in_category = [
                        app for app in apps_in_category
                        if search_query.lower() in app["title"].lower()
                    ]
                
                if apps_in_category:
                    st.markdown(f"### {category['name']}")
                    for app in apps_in_category:
                        menu_items.append(app["title"])
                        icons.append(category["icon"])
            
            selected = option_menu(
                "导航菜单",
                menu_items,
                icons=icons,
                menu_icon="menu-button",
                default_index=0,
            )
            
            return selected

    def render_settings(self):
        """渲染设置界面"""
        st.markdown("## ⚙️ 系统设置")
        
        tabs = st.tabs(["📱 应用管理", "📂 分类管理", "💾 备份管理", "⬆️ 上传新应用", "🔄 系统重置"])

        # 应用管理标签页
        with tabs[0]:
            self.render_app_management()

        # 分类管理标签页
        with tabs[1]:
            self.render_category_management()

        # 备份管理标签页
        with tabs[2]:
            self.render_backup_management()

        # 上传新应用标签页
        with tabs[3]:
            self.render_upload_form()

        # 系统重置标签页
        with tabs[4]:
            self.render_system_reset()

    def render_system_reset(self):
        """渲染系统重置界面"""
        st.markdown("### 🔄 系统重置")
        st.warning("⚠️ 警告：重置系统将删除所有应用和配置，恢复到初始状态！")
        
        if st.button("重置系统", key="reset_system"):
            if self.reset_to_factory():
                st.success("✅ 系统已重置！")
                st.experimental_rerun()

    def render_category_management(self):
        """渲染分类管理界面"""
        st.markdown("### 📂 分类管理")
        
        # 显示现有分类
        for category in self.apps_config["categories"]:
            with st.expander(f"{category['name']}"):
                new_name = st.text_input("分类名称", category["name"], key=f"cat_name_{category['id']}")
                new_icon = st.text_input("分类图标", category["icon"], key=f"cat_icon_{category['id']}")
                
                if st.button("更新", key=f"update_cat_{category['id']}"):
                    category.update({
                        "name": new_name,
                        "icon": new_icon
                    })
                    self.save_apps_config()
                    st.success("✅ 更新成功！")
                    st.experimental_rerun()
        
        # 添加新分类
        st.markdown("#### 添加新分类")
        new_cat_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        new_cat_name = st.text_input("分类名称", key="new_cat_name")
        new_cat_icon = st.text_input("分类图标", key="new_cat_icon")
        
        if st.button("添加分类"):
            self.apps_config["categories"].append({
                "id": new_cat_id,
                "name": new_cat_name,
                "icon": new_cat_icon
            })
            self.save_apps_config()
            st.success("✅ 添加成功！")
            st.experimental_rerun()

    def render_app_management(self):
        """渲染应用管理界面"""
        st.markdown("### 📱 应用管理")
        
        # 按分类显示应用
        for category in self.apps_config["categories"]:
            apps_in_category = self.get_apps_by_category(category["id"])
            if apps_in_category:
                st.markdown(f"#### {category['name']}")
                for app in apps_in_category:
                    with st.expander(f"{app['title']}"):
                        new_title = st.text_input("应用标题", app["title"], key=f"title_{app['id']}")
                        new_desc = st.text_area("应用描述", app["description"], key=f"desc_{app['id']}")
                        new_icon = st.selectbox("图标", ICON_LIST, 
                                              index=ICON_LIST.index(app["icon"]) if app["icon"] in ICON_LIST else 0,
                                              key=f"icon_{app['id']}")
                        new_category = st.selectbox("分类", 
                                                  [cat["id"] for cat in self.apps_config["categories"]],
                                                  index=[cat["id"] for cat in self.apps_config["categories"]].index(app.get("category", "default")),
                                                  format_func=lambda x: next((cat["name"] for cat in self.apps_config["categories"] if cat["id"] == x), x),
                                                  key=f"cat_{app['id']}")
                        
                        code_file = os.path.join(UPLOAD_DIR, f"{app['id']}.py")
                        try:
                            with open(code_file, 'r', encoding='utf-8') as f:
                                current_code = f.read()
                        except Exception:
                            current_code = app.get("code", "")
                        
                        new_code = st.text_area("应用代码", current_code, height=200, key=f"code_{app['id']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("更新", key=f"update_{app['id']}"):
                                try:
                                    app.update({
                                        "title": new_title,
                                        "description": new_desc,
                                        "icon": new_icon,
                                        "category": new_category,
                                        "code": new_code
                                    })
                                    
                                    with open(code_file, 'w', encoding='utf-8') as f:
                                        f.write(new_code)
                                    
                                    self.save_apps_config()
                                    st.success("✅ 更新成功！")
                                    st.experimental_rerun()
                                except Exception as e:
                                    st.error(f"更新失败: {str(e)}")
                        
                        with col2:
                            if st.button("删除", key=f"delete_{app['id']}", type="primary"):
                                if self.delete_app(app["id"]):
                                    st.success("✅ 删除成功！")
                                    st.experimental_rerun()

    def render_backup_management(self):
        """渲染备份管理界面"""
        st.markdown("### 💾 备份管理")
        
        # 创建备份部分
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.container():
                st.markdown("#### 📦 创建备份")
                backup_name = st.text_input("备份名称（可选）", placeholder="留空将使用时间戳")
                if st.button("创建新备份", use_container_width=True):
                    backup_path, success = self.create_backup(backup_name)
                    if success:
                        st.success(f"✅ 备份创建成功！\n位置：{backup_path}")
        
        with col2:
            with st.container():
                st.markdown("#### ♻️ 恢复备份")
                backup_dirs = self.get_available_backups()
                if backup_dirs:
                    selected_backup = st.selectbox(
                        "选择要恢复的备份",
                        backup_dirs,
                        format_func=lambda x: x.split('_')[-1] if '_' in x else x
                    )
                    
                    if st.button("恢复选中的备份", use_container_width=True):
                        confirm = st.checkbox("确认恢复? 这将覆盖当前的所有设置和应用")
                        if confirm and self.restore_backup(os.path.join(BACKUP_DIR, selected_backup)):
                            st.success("✅ 备份恢复成功！")
                            st.experimental_rerun()
                else:
                    st.info("📝 暂无可用的备份")
        
        # 备份列表和管理
        st.markdown("#### 🗂️ 备份列表")
        backup_dirs = self.get_available_backups()
        if backup_dirs:
            for backup_dir in backup_dirs:
                with st.expander(f"备份: {backup_dir}"):
                    backup_path = os.path.join(BACKUP_DIR, backup_dir)
                    backup_time = os.path.getctime(backup_path)
                    st.text(f"创建时间: {datetime.fromtimestamp(backup_time).strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("删除备份", key=f"delete_backup_{backup_dir}"):
                            try:
                                shutil.rmtree(backup_path)
                                st.success("✅ 备份删除成功！")
                                st.experimental_rerun()
                            except Exception as e:
                                st.error(f"删除备份失败: {str(e)}")
                    with col2:
                        if st.button("导出备份", key=f"export_backup_{backup_dir}"):
                            try:
                                zip_path = shutil.make_archive(
                                    backup_path,
                                    'zip',
                                    backup_path
                                )
                                with open(zip_path, 'rb') as f:
                                    st.download_button(
                                        label="下载备份文件",
                                        data=f.read(),
                                        file_name=f"{backup_dir}.zip",
                                        mime="application/zip",
                                        key=f"download_{backup_dir}"
                                    )
                            except Exception as e:
                                st.error(f"导出备份失败: {str(e)}")

    def create_backup(self, backup_name: str = None) -> tuple[Optional[str], bool]:
        """创建备份"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(
                BACKUP_DIR,
                f"backup_{backup_name}_{timestamp}" if backup_name else f"backup_{timestamp}"
            )
            os.makedirs(backup_path, exist_ok=True)
            
            # 备份配置文件
            if os.path.exists(CONFIG_FILE):
                shutil.copy2(CONFIG_FILE, backup_path)
            
            # 备份上传的应用
            if os.path.exists(UPLOAD_DIR):
                shutil.copytree(
                    UPLOAD_DIR,
                    os.path.join(backup_path, "uploaded_apps"),
                    dirs_exist_ok=True
                )
            
            return backup_path, True
        except Exception as e:
            st.error(f"创建备份失败: {str(e)}")
            return None, False

    def get_available_backups(self) -> List[str]:
        """获取可用的备份列表"""
        try:
            return [d for d in os.listdir(BACKUP_DIR)
                   if os.path.isdir(os.path.join(BACKUP_DIR, d)) and d.startswith("backup_")]
        except Exception:
            return []

    def restore_backup(self, backup_dir: str) -> bool:
        """恢复备份"""
        try:
            # 恢复配置文件
            backup_config_path = os.path.join(backup_dir, CONFIG_FILE)
            if os.path.exists(backup_config_path):
                shutil.copy2(backup_config_path, ".")
            else:
                raise FileNotFoundError(f"备份中缺少配置文件: {backup_config_path}")

            # 恢复上传的应用
            uploaded_apps_backup = os.path.join(backup_dir, "uploaded_apps")
            if os.path.exists(uploaded_apps_backup):
                if os.path.exists(UPLOAD_DIR):
                    shutil.rmtree(UPLOAD_DIR)
                shutil.copytree(uploaded_apps_backup, UPLOAD_DIR)
            else:
                raise FileNotFoundError(f"备份中缺少上传的应用目录: {uploaded_apps_backup}")

            # 重新加载配置
            self.apps_config = self.load_apps_config()
            return True
        except Exception as e:
            st.error(f"恢复备份失败: {str(e)}")
            return False


    def render_upload_form(self):
        """渲染上传表单"""
        st.markdown("### ⬆️ 上传新应用")
        
        # 生成随机默认值
        default_id = self.generate_random_id()
        default_title = self.generate_random_title()
        default_description = self.generate_random_description()
        default_icon = random.choice(ICON_LIST)
        
        # 上传方式选择
        upload_method = st.radio("选择上传方式", ["上传文件", "直接编写代码"])
        
        # 基本信息（使用列布局）
        col1, col2 = st.columns(2)
        with col1:
            new_app_id = st.text_input("应用ID", value=default_id, help="留空将自动生成")
            new_app_title = st.text_input("应用标题", value=default_title, help="留空将自动生成")
        with col2:
            new_app_icon = st.selectbox("应用图标", ICON_LIST, index=ICON_LIST.index(default_icon))
            new_app_category = st.selectbox(
                "应用分类",
                [cat["id"] for cat in self.apps_config["categories"]],
                format_func=lambda x: next((cat["name"] for cat in self.apps_config["categories"] if cat["id"] == x), x)
            )
        
        new_app_desc = st.text_area("应用描述", value=default_description, help="留空将自动生成")
        
        # 代码输入
        code_content = None
        if upload_method == "上传文件":
            uploaded_file = st.file_uploader("上传应用代码文件(.py)", type=['py'])
            if uploaded_file:
                code_content = uploaded_file.getvalue().decode('utf-8')
        else:
            code_content = st.text_area("直接编写代码", height=300)
        
        # 提交按钮
        if st.button("📤 提交应用", use_container_width=True):
            if self.upload_new_app(
                new_app_id, new_app_title, new_app_desc,
                new_app_icon, new_app_category, code_content
            ):
                st.success("✅ 新应用上传成功！")
                st.experimental_rerun()

    def upload_new_app(self, app_id: str, title: str, description: str,
                      icon: str, category: str, code_content: str) -> bool:
        """上传新应用"""
        try:
            if not code_content:
                st.warning("请提供应用代码！")
                return False
            
            # 使用默认值或用户输入
            final_app_id = app_id or self.generate_random_id()
            final_title = title or self.generate_random_title()
            final_description = description or self.generate_random_description()
            
            # 保存代码文件
            file_path = os.path.join(UPLOAD_DIR, f"{final_app_id}.py")
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(code_content)
            
            # 更新配置
            self.apps_config["apps"].append({
                "id": final_app_id,
                "title": final_title,
                "description": final_description,
                "icon": icon,
                "category": category,
                "module": final_app_id,
                "code": code_content
            })
            
            self.save_apps_config()
            return True
        except Exception as e:
            st.error(f"上传应用失败: {str(e)}")
            return False

    def run_app(self, app_id: str):
        """运行指定的应用"""
        try:
            app = next((app for app in self.apps_config["apps"] if app["id"] == app_id), None)
            if not app:
                st.error("找不到指定的应用")
                return

            code_file = os.path.join(UPLOAD_DIR, f"{app['id']}.py")
            if os.path.exists(code_file):
                with open(code_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                module = self.load_module(app["id"], code)
                if module and hasattr(module, 'run'):
                    module.run()
                else:
                    st.error("应用代码中未找到 run() 函数")
            else:
                st.error(f"无法找到应用代码文件：{code_file}")
        except Exception as e:
            st.error(f"运行应用时出错：{str(e)}")

def main():
    """主程序入口"""
    # 初始化应用管理器
    app_manager = AppManager()
    
    # 显示标题
    st.title("🚀 WJJ 应用集合")
    
    # 初始化session state
    if "selected_app" not in st.session_state:
        st.session_state.selected_app = "home"
    
    # 导航栏选择
    selected = app_manager.render_navigation()
    
    if selected == "主页":
        st.session_state.selected_app = "home"
    elif selected == "设置":
        st.session_state.selected_app = "settings"
    else:
        for app in app_manager.apps_config["apps"]:
            if app["title"] == selected:
                st.session_state.selected_app = app["id"]
    
    # 加载页面
    if st.session_state.selected_app == "home":
        app_manager.render_app_details_compact()
    elif st.session_state.selected_app == "settings":
        app_manager.render_settings()
    else:
        app_manager.run_app(st.session_state.selected_app)

if __name__ == "__main__":
    main()

