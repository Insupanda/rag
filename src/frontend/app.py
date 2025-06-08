import streamlit as st

# ─── 세션 상태 초기화 ───
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Simple Chat Demo", layout="centered")
st.title("🗨️ Insupanda Simple Chat Demo")

with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    user_text = col1.text_area(
        label="메시지를 입력하세요:",
        key="input_box",
        placeholder="메시지를 입력하세요.",
        label_visibility="collapsed",
        height=100,
    )
    clear_button = col2.form_submit_button("Clear")
    submit = col2.form_submit_button("전송")
    module1_test = st.form_submit_button("외상후 스트레스 장애(PTSD)를 보장하는 보험은?")
    module2_test = st.form_submit_button("현대해상의 기본플랜 보험료를 알려줘?")

if module1_test:
    user_text = "외상후 스트레스 장애(PTSD)를 보장하는 보험은?"
    st.session_state.chat_history.append(("User", user_text))
    # Bot 응답(여기서는 단순 에코)
    bot_reply = f"Echo: {user_text}"
    st.session_state.chat_history.append(("Bot", bot_reply))

if module2_test:
    user_text = "현대해상의 기본플랜 보험료를 알려줘?"
    st.session_state.chat_history.append(("User", user_text))
    # Bot 응답(여기서는 단순 에코)
    bot_reply = f"Echo: {user_text}"
    st.session_state.chat_history.append(("Bot", bot_reply))

if clear_button:
    st.session_state.chat_history = []

if submit and user_text:
    # User 메시지 추가
    st.session_state.chat_history.append(("User", user_text))
    # Bot 응답(여기서는 단순 에코)
    bot_reply = f"Echo: {user_text}"
    st.session_state.chat_history.append(("Bot", bot_reply))

for role, msg in st.session_state.chat_history:
    if role == "User":
        st.markdown(f"<div style='text-align: right; color: white;'>👤 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; color: green;'>🤖 {msg}</div>", unsafe_allow_html=True)
