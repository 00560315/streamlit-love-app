import streamlit as st
import time
import random
 
# ============== 游戏配置 ==============
GAME_TIME = 45           # 总游戏时间
COMBO_BONUS = 5         # 连击加成
SPECIAL_HEART_INTERVAL = 8  # 特殊爱心出现间隔
PENALTY_PROB = 0.15     # 危险爱心出现概率
POWER_UP_TYPES = ["🕒 时间冻结", "💘 双倍心动", "🛡️ 爱心护盾"]
 
# ============== 游戏状态初始化 ==============
if "stage" not in st.session_state:
    st.session_state.update({
        "score": 0,
        "combo": 0,
        "game_active": False,
        "start_time": 0,
        "power_ups": {key: 0 for key in POWER_UP_TYPES},
        "shield_active": False,
        "time_frozen": False,
        "last_special": 0
    })
 
# ============== 游戏样式 ==============
st.markdown(f"""
<style>
/* 动态渐变背景 */
@keyframes gradientBG {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}
.game-container {{
    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    padding: 2rem;
    border-radius: 20px;
}}
/* 爱心动画 */
@keyframes heartPulse {{
    0% {{ transform: scale(0.9); opacity: 0.7; }}
    100% {{ transform: scale(1.2); opacity: 1; }}
}}
.heart-btn {{
    animation: heartPulse 0.8s ease-in-out infinite alternate;
    transition: all 0.3s !important;
}}
.danger {{
    animation: heartPulse 0.4s ease-in-out infinite alternate !important;
    background: rgba(255,0,0,0.2) !important;
}}
</style>
""", unsafe_allow_html=True)
 
# ============== 游戏逻辑 ==============
def handle_click(heart_type):
    """处理爱心点击"""
    if st.session_state.shield_active and heart_type == "💔":
        return
    
    if heart_type == "❤️":
        base = 2
        st.session_state.combo += 1
    elif heart_type == "💛":
        base = 3
        st.session_state.combo += 2
    elif heart_type == "💔":
        st.session_state.score = max(0, st.session_state.score - 15)
        st.session_state.combo = 0
        return
    elif heart_type == "💖":
        base = 5
        st.session_state.combo += 3
    
    # 连击加成
    combo_bonus = (st.session_state.combo // 5) * COMBO_BONUS
    st.session_state.score += base + combo_bonus
 
    # 随机获得道具
    if random.random() < 0.2:
        power = random.choice(POWER_UP_TYPES)
        st.session_state.power_ups[power] += 1
 
def use_power_up(power_type):
    """使用道具"""
    if st.session_state.power_ups[power_type] > 0:
        st.session_state.power_ups[power_type] -= 1
        if power_type == "🕒 时间冻结":
            st.session_state.time_frozen = True
        elif power_type == "💘 双倍心动":
            st.session_state.score += st.session_state.combo * 2
        elif power_type == "🛡️ 爱心护盾":
            st.session_state.shield_active = True
 
# ============== 界面渲染 ==============
with st.container():
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    
    # 游戏控制区
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 🎮 操作面板")
        if not st.session_state.game_active:
            if st.button("✨ 开始双人挑战", use_container_width=True):
                st.session_state.game_active = True
                st.session_state.start_time = time.time()
        
        # 道具使用区
        st.markdown("### 🎒 道具背包")
        for power in POWER_UP_TYPES:
            if st.button(f"{power} x{st.session_state.power_ups[power]}", 
                        help="点击使用", 
                        key=f"power_{power}",
                        on_click=use_power_up,
                        args=(power,)):
                pass
 
    # 游戏主界面
    with col2:
        if st.session_state.game_active:
            elapsed = time.time() - st.session_state.start_time
            time_left = max(0, GAME_TIME - int(elapsed))
            
            # 游戏结束检测
            if time_left <= 0 and not st.session_state.time_frozen:
                st.session_state.game_active = False
                st.balloons()
                st.session_state.time_frozen = False
                st.session_state.shield_active = False
            
            # 实时状态显示
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.9); padding:15px; border-radius:10px;">
                <h4>⏳ 剩余时间: {time_left}s</h4>
                <h4>✨ 当前得分: {st.session_state.score}</h4>
                <h4>⚡ 连击加成: x{(st.session_state.combo // 5) + 1}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # 动态生成爱心矩阵
            cols = st.columns(4)
            for idx, col in enumerate(cols):
                with col:
                    heart_type = "❤️"
                    # 特殊爱心逻辑
                    if time.time() - st.session_state.last_special > SPECIAL_HEART_INTERVAL:
                        heart_type = random.choice(["💖", "💛"])
                        st.session_state.last_special = time.time()
                    elif random.random() < PENALTY_PROB:
                        heart_type = "💔"
                    
                    st.button(heart_type, 
                            key=f"heart_{idx}_{time.time()}",
                            on_click=handle_click,
                            args=(heart_type,),
                            kwargs={},
                            help="小心红色爱心！",
                            use_container_width=True,
                            )
 
    st.markdown('</div>', unsafe_allow_html=True)
