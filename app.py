import streamlit as st
import time
import random
 
# ============== 游戏配置 ==============
GAME_TIME = 20  # 游戏时长(秒)
HEART_EMOJI = "💖"  # 可替换为其他表情
SCORE_FILE = "high_score.txt"  # 最高分记录文件
 
# ============== 初始化游戏数据 ==============
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_active" not in st.session_state:
    st.session_state.game_active = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
 
# ============== 游戏样式 ==============
st.markdown(f"""
<style>
/* 爱心点击动画 */
@keyframes heartBounce {{
    0% {{ transform: scale(1); }}
    50% {{ transform: scale(1.3); }}
    100% {{ transform: scale(1); }}
}}
/* 游戏标题 */
.title {{
    color: #ff69b4;
    text-shadow: 2px 2px 4px rgba(255,105,180,0.5);
    text-align: center;
}}
/* 得分板 */
.score {{
    background: rgba(255,255,255,0.9);
    border-radius: 10px;
    padding: 15px;
    margin: 20px auto;
    width: 200px;
    text-align: center;
}}
</style>
""", unsafe_allow_html=True)
 
# ============== 游戏逻辑 ==============
def update_score():
    """点击爱心增加分数"""
    st.session_state.score += random.randint(1,3)  # 随机加分
 
def get_high_score():
    """读取最高分"""
    try:
        with open(SCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0
 
def save_high_score(score):
    """保存最高分"""
    with open(SCORE_FILE, "w") as f:
        f.write(str(score))
 
# ============== 界面渲染 ==============
# 标题
st.markdown('<h1 class="title">❤️ 爱心大作战 ❤️</h1>', unsafe_allow_html=True)
 
# 游戏控制区
col1, col2, col3 = st.columns(3)
with col2:
    if not st.session_state.game_active:
        if st.button("🎮 开始游戏"):
            st.session_state.game_active = True
            st.session_state.score = 0
            st.session_state.start_time = time.time()
 
# 游戏主体
if st.session_state.game_active:
    # 倒计时计算
    elapsed = time.time() - st.session_state.start_time
    time_left = max(0, GAME_TIME - int(elapsed))
    
    # 结束检测
    if time_left == 0:
        st.session_state.game_active = False
        high_score = get_high_score()
        if st.session_state.score > high_score:
            save_high_score(st.session_state.score)
            st.balloons()
    
    # 游戏界面
    with st.container():
        # 得分和倒计时
        st.markdown(f"""
        <div class="score">
            <h3>剩余时间 ⏳: {time_left}s</h3>
            <h3>当前得分 ✨: {st.session_state.score}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 生成爱心按钮
        cols = st.columns(4)
        for col in cols:
            with col:
                st.button(
                    HEART_EMOJI,
                    on_click=update_score,
                    key=f"heart_{random.randint(0,1000)}",
                    use_container_width=True,
                    args=(),
                    kwargs={},
                )
 
# 最高分显示
if not st.session_state.game_active:
    high_score = get_high_score()
    st.markdown(f"""
    <div class="score">
        <h3>🏆 历史最高分: {high_score}</h3>
        <h4>点击开始挑战吧！</h4>
    </div>
    """, unsafe_allow_html=True)
