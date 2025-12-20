import streamlit as st
from openai import OpenAI
import os
import json
from datetime import datetime

# --- PAGE CONFIG (WIDE REQUIRED FOR FULL-WIDTH BANNER) ---
st.set_page_config(
    page_title="Architect AI",
    page_icon="assets/icon.jpg",
    layout="wide",
)

# --- SESSION STATE INIT (CRITICAL FIX) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- GROQ CLIENT ---
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# --- CUSTOM CSS ---
st.markdown(
    """
    <style>

    /* FULL BACKGROUND */
    .stApp {
        background: url("assets/backsplash.jpg") no-repeat center center fixed;
        background-size: cover;
        font-family: 'Trebuchet MS', 'Arial Black', sans-serif;
    }

    /* REMOVE TOP PADDING FOR BANNER */
    header, footer { visibility: hidden; }
    .block-container {
        padding-top: 0rem;
        background: rgba(5,5,5,0.82);
        border: 2px solid #00ffcc;
        border-radius: 20px;
        padding: 3rem;
        margin-top: 1rem;
        box-shadow:
            0 0 35px rgba(0,255,204,0.45),
            inset 0 0 25px rgba(255,0,102,0.25);
        backdrop-filter: blur(6px);
        max-width: 1100px;
    }

    /* FULL-WIDTH LOGO BANNER */
    .banner {
        width: 100vw;
        margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        margin-bottom: 30px;
    }

    .banner img {
        width: 100%;
        height: auto;
        display: block;
        filter:
            drop-shadow(0 0 30px #00ffcc)
            drop-shadow(0 0 50px #ff0066);
    }

    /* TITLES */
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
        color: #ccc;
        letter-spacing: 1px;
        margin-top: -10px;
    }

    /* CHAT INPUT */
    .stChatInput textarea {
        background: rgba(10,10,10,0.95);
        color: #fff;
        border: 2px solid #ff0066;
        border-radius: 10px;
        box-shadow: inset 0 0 15px rgba(255,0,102,0.4);
    }

    /* CHAT MESSAGES */
    .stChatMessage {
        background: rgba(12,12,12,0.8);
        border-left: 4px solid #00ffcc;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #ff0066, #00ffcc);
        color: #000;
        font-weight: 900;
        border-radius: 12px;
        height: 3.2em;
        box-shadow: 0 0 25px rgba(0,255,204,0.6);
        border: none;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #ff3388, #33ffee);
        box-shadow: 0 0 40px rgba(255,0,102,0.9);
        transform: scale(1.03);
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# --- FULL-WIDTH LOGO BANNER ---
st.markdown(
    """
    <div class="banner">
        <img src="assets/logo.jpg">
    </div>
    """,
    unsafe_allow_html=True,
)

# --- TITLES ---
st.markdown("<h1>ARCHITECT AI</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3>Unrestricted Local Genius • Synthetic Systems • Precision Output</h3>",
    unsafe_allow_html=True
)

st.divider()

# --- CHATBOT CLASS (UNCHANGED LOGIC) ---
class Chatbot:
    def __init__(self):
        self.history_file = "chat_history.json"
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.messages = json.load(f)
        else:
            self.messages = []

        self.system_prompt = """You are Architect AI..."""  # unchanged

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        self.save_history()

    def get_response(self, user_message):
        self.add_message("user", user_message)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": self.system_prompt}] + self.messages,
            max_tokens=3000,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        self.add_message("assistant", reply)
        return reply

    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, indent=2, ensure_ascii=False)

chatbot = Chatbot()

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- INPUT ---
if prompt := st.chat_input("Message ARCHITECT AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("ARCHITECT is responding..."):
        reply = chatbot.get_response(prompt)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# --- FOOTER ---
st.markdown(
    """
    <div style='text-align:center; color:#555; margin-top:60px;'>
        © 2025 ARCHITECT AI
    </div>
    """,
    unsafe_allow_html=True,
)

