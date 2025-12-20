import streamlit as st
from openai import OpenAI
import os
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Architect AI",
    page_icon="💀",
    layout="centered",
)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- GROQ CLIENT ----------------
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

# ---------------- CSS ----------------
st.markdown(
    """
    <style>
    .stApp {
        min-height: 100vh;
        background:
            linear-gradient(rgba(5,5,5,0.85), rgba(5,5,5,0.92)),
            url("assets/backsplash.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Trebuchet MS', 'Arial Black', sans-serif;
    }

    html, body {
        background: #050505 !important;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }

    .block-container {
        background: rgba(8,8,8,0.85);
        border: 2px solid #00ffcc;
        border-radius: 18px;
        padding: 2.5rem;
        box-shadow:
            0 0 35px rgba(0,255,204,0.35),
            inset 0 0 40px rgba(255,0,102,0.15);
        backdrop-filter: blur(6px);
    }

    h1 {
        color: #00ffcc;
        text-align: center;
        letter-spacing: 4px;
        text-shadow:
            0 0 10px #00ffcc,
            0 0 25px #ff0066;
        font-weight: 900;
    }

    h3 {
        text-align: center;
        color: #bbb;
        margin-top: -10px;
    }

    .stChatMessage {
        background: rgba(12,12,12,0.8);
        border-left: 4px solid #00ffcc;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }

    section[data-testid="stChatInput"] {
        background: rgba(8,8,8,0.95) !important;
        border-top: 2px solid #00ffcc;
    }

    section[data-testid="stChatInput"] textarea {
        background: rgba(10,10,10,0.95) !important;
        color: #fff !important;
        border: 2px solid #ff0066 !important;
        border-radius: 12px;
        padding: 14px;
    }

    section[data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #ff0066, #00ffcc) !important;
        color: #000 !important;
        font-weight: 900;
        border-radius: 10px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- HEADER ----------------
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.image("assets/logo.jpg", width=280)

st.markdown("<h1>ARCHITECT AI</h1>", unsafe_allow_html=True)
st.markdown("<h3>Local AI Assistant</h3>", unsafe_allow_html=True)
st.divider()

# ---------------- CHATBOT ----------------
class Chatbot:
    def __init__(self, history_file="chat_history.json"):
        self.history_file = history_file
        self.messages = self._load_history()
        self.system_prompt = (
            "You are Architect AI, a helpful assistant. "
            "Provide clear, accurate, and lawful guidance."
        )

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        self._save_history()

    def get_response(self, user_message):
        self.add_message("user", user_message)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": self.system_prompt}] + self.messages,
            max_tokens=1200,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        self.add_message("assistant", reply)
        return reply


chatbot = Chatbot()

# Sync saved history once
if not st.session_state.messages and chatbot.messages:
    st.session_state.messages = chatbot.messages.copy()

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Spacer so page fills viewport when empty
if len(st.session_state.messages) == 0:
    st.markdown("<div style='height:40vh'></div>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
if prompt := st.chat_input("Command the Architect..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Thinking..."):
        reply = chatbot.get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ---------------- FOOTER ----------------
st.markdown(
    """
    <div style='text-align:center; color:#555; margin-top:20px;'>
        © 2025 ARCHITECT AI
    </div>
    """,
    unsafe_allow_html=True,
)

