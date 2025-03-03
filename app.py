import streamlit as st
import base64
from io import BytesIO
import time
from PIL import Image
 
# ====================== 核心代码 ======================
def set_photo_background(image_path):
    # 将图片转换为Base64
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    # 设置全屏背景图
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
    }}
    
    /* 半透明遮罩层 */
    .content-box {{
        background: rgba(255, 255, 255, 0.9);
        padding: 30px;
        border-radius: 15px;
        margin: 50px auto;
        max-width: 80%;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }}
    
    /* 加大字体并添加行间距 */
    .love-text {{
        font-size: 20px !important;
        line-height: 1.8;
        color: #ff1493;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)
 
# ====================== 主程序 ======================
try:
    set_photo_background("couple_bg.jpg")
except:
    st.error("请将背景图片命名为couple_bg.jpg并放在代码目录")
 
# 自定义情话（支持换行）
quotes = [
    """宝宝快看！我熬夜做的小程序真的跑起来啦！<br>
    虽然它不会修图不会点外卖，<br>
    但每次刷新都能看到你的照片在对我笑~<br>
    第一个成功必须和你分享！"""
]
 
with st.container():
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
    # 显示情话（带表情符号动画）
    st.markdown(f"""
    <div class="love-text">
    🎉 {quotes[0]}
    </div>
    """, unsafe_allow_html=True)
    
    # 添加动态庆祝效果
    if st.button("🎈 点击庆祝"):
        st.balloons()
        st.success("庆祝模式已激活！奖励系统加载中...")
        time.sleep(1)
        st.markdown("""
        <div style="text-align:center; margin-top:20px;">
            🎁 奖励清单：<br>
            1. 奶茶续杯券x3<br>
            2. 专属按摩服务x1小时<br>
            3. 男朋友夸夸卡（无限次使用）
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
