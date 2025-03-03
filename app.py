import streamlit as st
 
# ============== 修复重点 ==============
# 1. 使用session_state持久化数据
# 2. 添加章节推进逻辑
# 3. 确保组件重新渲染
 
CHAPTERS = [
    {
        "title": "初遇咖啡馆",
        "scenes": [
            {
                "text": "周六下午的咖啡馆，你注意到邻座正在看《小王子》的她，你会：",
                "choices": [
                    {"text": "借书搭讪", "next": "response1"},
                    {"text": "偷偷画下她的侧影", "next": "response2"},
                    {"text": "请店员送咖啡", "next": "response3"}
                ]
            },
            {
                "id": "response1",
                "text": "她抬头微笑：「你也喜欢这句关于星星的描写吗？」你会说：",
                "choices": [
                    {"text": "「你的眼睛比星星更亮」", "end": "结局1"},
                    {"text": "「我在寻找我的玫瑰」", "end": "结局2"}
                ]
            }
        ]
    }
]
 
# 初始化会话状态
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        "current_chapter": 0,
        "current_scene": 0,
        "history": []
    }
 
def handle_choice(choice):
    # 记录选择历史
    st.session_state.game_state["history"].append(choice)
    
    # 推进剧情逻辑
    if "end" in choice:
        st.session_state.game_state["current_scene"] = -1
    else:
        st.session_state.game_state["current_scene"] += 1
    
    # 强制重新渲染
    st.experimental_rerun()
 
# 渲染当前场景
current_chapter = CHAPTERS[st.session_state.game_state["current_chapter"]]
current_scene = current_chapter["scenes"][st.session_state.game_state["current_scene"]]
 
st.header(current_chapter["title"])
st.write(current_scene["text"])
 
# 动态生成选项按钮
cols = st.columns(len(current_scene["choices"]))
for idx, choice in enumerate(current_scene["choices"]):
    with cols[idx]:
        st.button(
            choice["text"],
            on_click=handle_choice,
            args=(choice,),
            key=f"choice_{idx}"
        )
 
# 显示历史记录
st.sidebar.header("📜 选择历程")
for item in st.session_state.game_state["history"]:
    st.sidebar.write(f"→ {item['text']}")
 
# 结局处理
if st.session_state.game_state["current_scene"] == -1:
    st.balloons()
    st.success("""
    🎉 故事仍在继续...
    点击右上角菜单「Rerun」重新开始
    """)
