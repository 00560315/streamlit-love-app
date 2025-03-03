import streamlit as st
import time
import random
from PIL import Image
from io import BytesIO
import base64
 
# ====================== 游戏配置 ======================
CHAPTERS = [
    {
        "id": "cafe",
        "title": "☕ 初遇咖啡馆",
        "bg_image": "cafe_bg.jpg",
        "scenes": [
            {
                "text": "阳光透过玻璃窗洒在她翻动的书页上，《小王子》的封面微微反光，你会：",
                "choices": [
                    {"text": "轻敲桌面：「我也喜欢那句关于驯养的话」", "effect": {"trust": 2}},
                    {"text": "画下她的侧影夹在书里", "effect": {"memory": "素描画像"}},
                    {"text": "请店员送上一杯卡布奇诺", "effect": {"charm": 1}}
                ]
            },
            {
                "text": "她注意到你的举动，睫毛轻颤投下阴影：「我们见过吗？」你会：",
                "choices": [
                    {"text": "「在某个平行宇宙肯定见过」", "effect": {"romance": 3}},
                    {"text": "「现在开始认识也不晚」", "effect": {"trust": 2}},
                    {"text": "展示手机里的共同歌单", "effect": {"charm": 2}}
                ]
            }
        ]
    },
    {
        "id": "rain",
        "title": "🌧️ 雨夜重逢",
        "bg_image": "rain_bg.jpg",
        "scenes": [
            {
                "text": "地铁站台灯光在雨幕中晕染，没带伞的她发梢滴着水珠，你会：",
                "choices": [
                    {"text": "把伞塞给她转身跑进雨中", "effect": {"memory": "雨中背影"}},
                    {"text": "轻拍她肩头：「要共享心跳频率吗？」", "effect": {"romance": 3}},
                    {"text": "默默撑开伞站在上风处挡雨", "effect": {"trust": 2}}
                ]
            }
        ]
    }
]
 
# ====================== 初始化游戏状态 ======================
if 'game' not in st.session_state:
    st.session_state.update({
        "current_chapter": 0,
        "current_scene": 0,
        "attributes": {"trust": 0, "charm": 0, "romance": 0},
        "memories": [],
        "achievements": [],
        "last_rerun": time.time()
    })
 
# ====================== 游戏样式 ======================
def load_css():
    st.markdown(f"""
    <style>
    /* 动态渐变背景 */
    @keyframes gradientBG {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    .chapter-title {{
        color: #ff69b4;
        text-shadow: 2px 2px 4px rgba(255,105,180,0.3);
        border-left: 5px solid #ff1493;
        padding-left: 1rem;
        animation: fadeIn 1s;
    }}
    .choice-btn {{
        transition: all 0.3s !important;
        border: 2px solid #ffb6c1 !important;
        margin: 10px 0 !important;
    }}
    .choice-btn:hover {{
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(255,105,180,0.3);
    }}
    </style>
    """, unsafe_allow_html=True)
 
# ====================== 游戏逻辑 ======================
def handle_choice(effect):
    # 更新属性
    for attr, value in effect.items():
        if attr in st.session_state.game["attributes"]:
            st.session_state.game["attributes"][attr] += value
        elif attr == "memory":
            st.session_state.game["memories"].append(value)
    
    # 推进剧情
    if st.session_state.game["current_scene"] < len(current_chapter["scenes"])-1:
        st.session_state.game["current_scene"] += 1
    else:
        if st.session_state.game["current_chapter"] < len(CHAPTERS)-1:
            st.session_state.game["current_chapter"] += 1
            st.session_state.game["current_scene"] = 0
        else:
            st.session_state.game["current_chapter"] = -1
    
    # 智能刷新（修复rerun问题）
    st.session_state.game["last_rerun"] = time.time()
 
# ====================== 游戏渲染 ======================
load_css()
 
# 侧边栏显示状态
with st.sidebar:
    st.header("📊 情感指数")
    st.write(f"💖 信任值: {st.session_state.game['attributes']['trust']}")
    st.write(f"✨ 魅力值: {st.session_state.game['attributes']['charm']}")
    st.write(f"🌹 浪漫值: {st.session_state.game['attributes']['romance']}")
    
    st.header("🏆 成就收藏")
    if "雨中背影" in st.session_state.game["memories"]:
        st.success("「雨幕中的骑士」成就已解锁")
 
# 主游戏界面
if st.session_state.game["current_chapter"] == -1:
    st.balloons()
    st.success("""
    🎉 故事仍在继续...
    点击右上角菜单「Rerun」重新开始
    """)
else:
    current_chapter = CHAPTERS[st.session_state.game["current_chapter"]]
    current_scene = current_chapter["scenes"][st.session_state.game["current_scene"]]
    
    # 动态加载背景
    try:
        bg = Image.open(f"images/{current_chapter['bg_image']}")
        buffered = BytesIO()
        bg.save(buffered, format="PNG")
        bg_base64 = base64.b64encode(buffered.getvalue()).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"背景加载失败: {str(e)}")
 
    # 剧情展示
    st.markdown(f'<div class="chapter-title">{current_chapter["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:1.2rem; margin:2rem 0;">{current_scene["text"]}</div>', unsafe_allow_html=True)
    
    # 选项按钮
    cols = st.columns(len(current_scene["choices"]))
    for idx, choice in enumerate(current_scene["choices"]):
        with cols[idx]:
            st.button(
                choice["text"],
                on_click=handle_choice,
                kwargs={"effect": choice["effect"]},
                key=f"choice_{idx}_{st.session_state.game['last_rerun']}",
                help="点击做出你的选择"
            )
