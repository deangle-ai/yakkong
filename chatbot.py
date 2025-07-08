import streamlit as st
import openai
import os
from dotenv import load_dotenv
import gpts_prompt
import time

load_dotenv()

# --- OpenAI API KEY ---
openai.api_key = os.getenv("OPENAI_API_KEY")

st.markdown(
    """
    <style>
    .chat-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #2A6B35; /* 부드러운 초록 */
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .chat-info {
        background-color: #E6F2E6;
        border-left: 6px solid #57A05A;
        padding: 1.2rem 1.8rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        font-size: 1.15rem;
        color: #3B6B35;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 2px 6px rgb(90 145 90 / 0.2);
    }
    .user-msg {
        background-color: #C9E6C9;
        color: #1E3F20;
        border-radius: 18px 18px 6px 18px;
        padding: 1rem 1.2rem;
        margin: 0.6rem 0;
        max-width: 65%;
        align-self: flex-end;
        font-size: 1.05rem;
        text-align: right;
        margin-left: auto;
        margin-right: 0;
        box-shadow: 0 4px 12px rgb(140 190 140 / 0.3);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.4;
        word-break: break-word;
        width: fit-content;
        white-space: pre-wrap;
    }
    .bot-msg {
        background-color: #F3FAF2;
        color: #2F553F;
        border-radius: 18px 18px 18px 6px;
        padding: 1rem 1.2rem;
        margin: 0.6rem 0;
        max-width: 65%;
        align-self: flex-start;
        font-size: 1.05rem;
        text-align: left;
        margin-right: auto;
        margin-left: 0;
        box-shadow: 0 4px 12px rgb(170 210 170 / 0.3);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.4;
        word-break: break-word;
        width: fit-content;
        white-space: pre-wrap;
    }
    .input-area {
        display: flex;
        gap: 0.7rem;
        margin-top: 1.2rem;
    }
    input[type="text"] {
        width: 100%;
        box-sizing: border-box;
        padding: 12px 16px;
        border-radius: 30px;
        border: 2px solid #57A05A;
        background-color: #FBFFFB;
        font-size: 1.1rem;
        outline: none;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    input[type="text"]:focus {
        border-color: #3E8E41;
        box-shadow: 0 0 8px 2px rgba(59, 132, 63, 0.4);
    }
    button {
        background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.6rem 1.6rem;
        font-size: 1.1rem;
        cursor: pointer;
        transition: background 0.4s ease;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 4px 8px rgba(56, 142, 60, 0.4);
    }
    button:hover {
        background: linear-gradient(135deg, #3E8E41 0%, #2E6B31 100%);
        box-shadow: 0 6px 12px rgba(46, 107, 49, 0.6);
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown('<div class="chat-title">🫛 건강 상담사 약콩이</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-info">이 챗봇은 건강 관련 궁금증을 친절하게 상담해주는 AI입니다. 건강, 생활습관, 영양 등에 대해 무엇이든 물어보세요!</div>', unsafe_allow_html=True)

SYSTEM_PROMPT = gpts_prompt.SYSTEM_PROMPT

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# --- 대화 내용 출력 (system prompt는 제외) ---
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg"><b>사용자:</b> {msg["content"]}</div>', unsafe_allow_html=True)
        time.sleep(0.2)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="bot-msg"><b>챗봇:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# --- 챗봇 답변 생성 및 한 줄씩 출력 ---
if len(st.session_state.messages) > 1 and st.session_state.messages[-1]["role"] == "user":
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages,
        max_tokens=512,
        temperature=0.7,
    )
    bot_reply = response.choices[0].message.content.strip()
    time.sleep(0.5)
    placeholder = st.empty()
    lines = bot_reply.split('\n')
    displayed = ""
    for line in lines:
        if line.strip() == "":
            continue
        displayed += line + "\n"
        placeholder.markdown(f'<div class="bot-msg"><b>챗봇:</b> {displayed}</div>', unsafe_allow_html=True)
        time.sleep(0.25)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.rerun()

# --- 입력 폼: 항상 하단에 위치 ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="질문을 입력해 주세요...", key="input")
    submitted = st.form_submit_button("전송")

if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    del st.session_state["input"]
    st.rerun()
