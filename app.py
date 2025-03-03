import streamlit as st
import base64
import os
from io import BytesIO
from PIL import Image
 
# ====================== 核心配置 ======================
def set_photo_background():
    try:
        img = Image.open("images/couple_bg.jpg")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # 关键修复：添加内容容器层级保证可见性
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            position: relative;
            z-index: 0;
        }}
        .content-layer {{
            position: relative;
            z-index: 1;
        }}
        </style>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"背景图加载失败: {str(e)}")
 
# ====================== 主程序 ======================
set_photo_background()
 
# 添加内容层容器（关键！）
with st.container():
    st.markdown('<div class="content-layer">', unsafe_allow_html=True)
    
    # 半透明内容框
    with st.container():
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
        
        # 主标题
        st.markdown("""
        <h1 style="text-align:center; color:#ff1493;">
            🎉 给最可爱的你
        </h1>
        """, unsafe_allow_html=True)
        
        # 正文内容
        st.write("""
        <div style="text-align:center; font-size:18px;">
            这是我为你写的第一个小程序<br>
            虽然简单，但每一行代码都在说<br>
            「你是我最完美的算法」
        </div>
        """, unsafe_allow_html=True)
        
        # 互动按钮
        if st.button("✨ 点击解锁奖励", use_container_width=True):
            st.balloons()
            st.success("""
            **🎁 专属奖励已送达**
            - 奶茶无限续杯券
            - 男友按摩体验卡
            - 24小时待机服务
            """)
    
    st.markdown('</div>', unsafe_allow_html=True)  # 关键闭合标签
