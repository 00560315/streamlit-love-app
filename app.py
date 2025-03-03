import streamlit as st
import os
 
# 打印当前工作目录和文件列表
st.write("当前工作目录:", os.getcwd())
st.write("images文件夹是否存在:", os.path.exists("images"))
st.write("图片文件是否存在:", os.path.exists("images/couple_bg.jpg"))
import streamlit as st
import base64
import time
from io import BytesIO
from PIL import Image
 
# ====================== 核心配置 ======================
def set_photo_background():
    try:
        # 从images文件夹加载背景图
        img = Image.open("images/couple_bg.jpg")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # 设置全屏背景
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
        }}
        .content-box {{
            background: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 15px;
            margin: 50px auto;
            max-width: 80%;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .love-text {{
            font-size: 20px;
            line-height: 1.8;
            color: #ff1493;
            text-align: center;
        }}
        </style>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"背景图加载失败，请检查路径: {str(e)}")
 
# ====================== 主程序 ======================
set_photo_background()
 
with st.container():
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
    # 直白情话
    st.markdown("""
    <div class="love-text">
    🎉 宝宝快看！我熬夜做的小程序真的跑起来啦！<br>
    虽然它不会修图不会点外卖，<br>
    但每次刷新都能看到你的照片在对我笑~<br>
    第一个成功必须和你分享！
    </div>
    """, unsafe_allow_html=True)
    
    # 互动按钮
    if st.button("🎈 点击领取奖励"):
        st.balloons()
        st.success("""
        🎁 奖励已到账：
        1. 奶茶续杯券x3  
        2. 专属按摩服务x1小时  
        3. 男朋友夸夸卡（无限次使用）
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)  
