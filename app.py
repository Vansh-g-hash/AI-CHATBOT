import streamlit as st
import openai
from datetime import datetime
from chatbot import Chatbot  # import your rule-based chatbot

# --- API Key setup ---
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Styling
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #e6e6e6;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1 {
    color: #f5f5f5;
}
.chat-container {
    max-height: 600px;
    overflow-y: auto;
    padding: 15px;
    background-color: #1c1f26;
    border-radius: 10px;
    margin-bottom: 20px;
}
.user-msg, .bot-msg {
    padding: 10px 15px;
    border-radius: 20px;
    margin-bottom: 10px;
    max-width: 75%;
    font-size: 16px;
    line-height: 1.4;
}
.user-msg {
    background-color: #2a9df4;
    color: white;
    margin-left: auto;
    text-align: right;
}
.bot-msg {
    background-color: #32363e;
    color: #ddd;
    margin-right: auto;
}
.timestamp {
    font-size: 12px;
    color: #888;
    margin-top: -8px;
    margin-bottom: 5px;
}
input, textarea {
    background-color: #22262e !important;
    color: #e6e6e6 !important;
}
.stButton > button {
    background-color: #2a9df4;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
    border: none;
    cursor: pointer;
}
.stButton > button:hover {
    background-color: #1c81d1;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 GPT-Powered AI Chatbot")

# --- Session state init ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, friendly AI assistant."}
    ]

# Rule-based chatbot instance
bot = Chatbot()

def display_chat():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages[1:]:  # skip system prompt
        if msg["role"] == "user":
            st.markdown(
                f'<div class="timestamp" style="text-align:right;">{msg.get("time","")}</div>',
                unsafe_allow_html=True
            )
            st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="timestamp">{msg.get("time","")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def chat_with_gpt(prompt):
    user_msg = {"role": "user", "content": prompt, "time": datetime.now().strftime("%H:%M:%S")}
    st.session_state.messages.append(user_msg)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # 🔥 updated model
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=500,
            temperature=0.7
        )
        answer = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        st.error(f"OpenAI API error: {e}")  # show error instead of silent fail
        answer = bot.get_response(prompt)

    bot_msg = {"role": "assistant", "content": answer, "time": datetime.now().strftime("%H:%M:%S")}
    st.session_state.messages.append(bot_msg)
    return answer

# --- UI ---
display_chat()
user_input = st.text_input("You:", placeholder="Ask me anything...", key="input")

if user_input:
    with st.spinner("AI is thinking..."):
        chat_with_gpt(user_input)
    st.rerun()

if st.button("Clear Chat"):
    st.session_state.messages = [{"role": "system", "content": "You are a helpful, friendly AI assistant."}]
    st.rerun()
