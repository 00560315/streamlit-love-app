import streamlit as st
import time
 
# ============== 游戏配置 ==============
CHAPTERS = [
    {
        "title": "初遇咖啡馆",
        "scenes": [
            {
                "text": "周六下午的咖啡馆，你注意到邻座正在看《小王子》的她，你会：",
                "choices": [
                    {"text": "借书搭讪：「我也喜欢这句星星发亮是为了让每个人有一天都能找到自己的星星」", "score": 3},
                    {"text": "偷偷画下她的侧影夹在书里", "score": 2},
                    {"text": "请店员送她一杯卡布奇诺", "score": 1}
                ]
            },
            {
                "text": "她注意到你的举动，微笑着询问缘由，你回应：",
                "choices": [
                    {"text": "「你的眼睛比小王子的玫瑰更动人」", "emotion": 5},
                    {"text": "「这本书记录了我的童年幻想」", "emotion": 3},
                    {"text": "「要一起拼个桌吗？」", "emotion": 2}
                ]
            }
        ]
    },
    {
        "title": "雨夜重逢",
        "scenes": [
            {
                "text": "三个月后的雨夜，地铁站偶遇没带伞的她，你会：",
                "choices": [
                    {"text": "把伞塞给她转身跑进雨中", "memory": "雨中背影"},
                    {"text": "提议共享一把伞步行送她", "memory": "伞下心跳"},
                    {"text": "打车送她并悄悄付了车费", "memory": "车窗雾气"}
                ]
            }
        ]
    }
]
 
# ============== 游戏状态管理 ==============
if "chapter" not in st.session_state:
    st.session_state.update({
        "chapter_index": 0,
        "scene_index": 0,
        "memories": [],
        "emotion_score": 0,
        "last_choice": None
    })
 
# ============== 游戏样式 ==============
st.markdown("""
<style>
/* 章节标题动画 */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.chapter-title {
    animation: fadeInUp 1s ease;
    color: #ff69b4;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    border-left: 5px solid #ff1493;
    padding-left: 20px;
}
/* 选择按钮特效 */
.stButton > button {
    transition: all 0.3s !important;
    border: 2px solid #ffb6c1 !important;
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(255,105,180,0.3);
}
/* 记忆卡片 */
.memory-card {
    background: rgba(255,255,255,0.9);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 3px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)
 
# ============== 游戏逻辑 ==============
def make_choice(choice_data):
    """处理玩家选择"""
    # 记录情感分数
    if "emotion" in choice_data:
        st.session_state.emotion_score += choice_data["emotion"]
    # 收集记忆碎片
    if "memory" in choice_data:
        st.session_state.memories.append(choice_data["memory"])
    # 推进剧情
    if st.session_state.scene_index < len(CHAPTERS[st.session_state.chapter_index]["scenes"]) - 1:
        st.session_state.scene_index += 1
    else:
        if st.session_state.chapter_index < len(CHAPTERS) - 1:
            st.session_state.chapter_index += 1
            st.session_state.scene_index = 0
        else:
            st.session_state.chapter_index = -1  # 标记游戏结束
 
# ============== 游戏渲染 ==============
# 侧边栏显示记忆碎片
with st.sidebar:
    st.header("💌 记忆收藏馆")
    if st.session_state.memories:
        for memo in set(st.session_state.memories):
            st.markdown(f'<div class="memory-card">📜 {memo}</div>', unsafe_allow_html=True)
    else:
        st.write("暂时还没有收集到记忆碎片...")
 
# 主游戏界面
if st.session_state.chapter_index == -1:
    st.balloons()
    st.markdown(f"""
    <div style="text-align:center; padding:50px;">
        <h1>🎉 故事仍在继续...</h1>
        <h3>情感温度计：{st.session_state.emotion_score}°</h3>
        <p>你们共同创造了 {len(set(st.session_state.memories))} 个独特回忆</p>
        <button onclick="window.location.reload()" style="
            background: #ff69b4;
            color: white;
            border: none;
            padding: 10px 30px;
            border-radius: 25px;
            margin-top: 20px;
        ">重新开始</button>
    </div>
    """, unsafe_allow_html=True)
else:
    current_chapter = CHAPTERS[st.session_state.chapter_index]
    current_scene = current_chapter["scenes"][st.session_state.scene_index]
    
    # 章节标题
    st.markdown(f'<h1 class="chapter-title">{current_chapter["title"]}</h1>', unsafe_allow_html=True)
    
    # 情景描述
    st.markdown(f'<div style="font-size:18px; margin:30px 0;">{current_scene["text"]}</div>', unsafe_allow_html=True)
    
    # 选项按钮
    cols = st.columns(len(current_scene["choices"]))
    for idx, choice in enumerate(current_scene["choices"]):
        with cols[idx]:
            st.button(
                choice["text"],
                on_click=make_choice,
                args=(choice,),
                key=f"choice_{idx}",
                help="点击做出你的选择" if "memory" in choice else None
            )
