import streamlit as st
import base64
import os
import time
from io import BytesIO
from PIL import Image
 
# ====================== 调试模式开关 ======================
DEBUG_MODE = False  # 部署时设置为False即可隐藏调试信息
 
def debug_info():
    if DEBUG_MODE:
        st.write("当前工作目录:", os.getcwd())
        st.write("images文件夹内容:", os.listdir("images"))
 
# ====================== 核心配置 ======================
def set_photo_background():
    try:
        img = Image.open("images/couple_bg.jpg")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"背景图加载失败: {str(e)}")
        debug_info()  # 仅在出错时显示调试信息
 
# ====================== 主程序 ======================
set_photo_background()
 
with st.container():
    # 添加半透明遮罩层
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.85);
        padding: 30px;
        border-radius: 15px;
        margin: 50px auto;
        max-width: 80%;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    ">
    """, unsafe_allow_html=True)
    
    # 主内容
    st.markdown("""
    <div style="text-align: center; color: #ff1493; font-size: 20px;">
        🎉 宝宝快看！我熬夜做的小程序真的跑起来啦！<br>
        虽然它不会修图不会点外卖，<br>
        但每次刷新都能看到你的照片在对我笑~<br>
        第一个成功必须和你分享！
    </div>
    """, unsafe_allow_html=True)
    
    # 互动按钮（带调试入口）
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🎈 点击领取奖励"):
            st.balloons()
            st.success("""
            🎁 奖励已到账：
            1. 奶茶续杯券x3  
            2. 专属按摩服务x1小时  
            3. 男朋友夸夸卡（无限次使用）
            """)
    with col2:
        if st.button("🛠️ 开发者模式", help="点击显示调试信息"):
            debug_info()
 
# 确保部署时隐藏调试按钮
if not DEBUG_MODE:
    st.markdown("""
    <style>
    /* 隐藏开发者按钮 */
    div[data-testid="stVerticalBlock"] > div:nth-child(2) {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
