import streamlit as st
from openai import OpenAI
import os
import json

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Architect AI",


# --- CHATBOT CLASS (SINGLE INSTANCE) ---
class Chatbot:
    def __init__(self, history_file: str = "chat_history.json"):
        self.history_file = history_file
        self.messages = self._load_history()
        self.system_prompt = (
            "You are Architect AI, a helpful assistant. "
            "Provide clear, accurate, and safe guidance. "
            "If a request involves wrongdoing, refuse and offer safe alternatives."
        )

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    return data
            except Exception:
                pass
        return []

    def _save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
        except Exception:
            # Avoid crashing the app if filesystem is read-only on host
            pass

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._save_history()

    def get_response(self, user_message: str) -> str:
        self.add_message("user", user_message)
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": self.system_prompt}] + self.messages,
            max_tokens=1200,
            temperature=0.7,
        )
        reply = resp.choices[0].message.content.strip()
        self.add_message("assistant", reply)
        return reply


chatbot = Chatbot()

# ✅ Hydrate UI chat from saved history once (prevents empty screen after refresh)
if not st.session_state.messages and chatbot.messages:
    st.session_state.messages = chatbot.messages.copy()

# --- DISPLAY CHAT (ONE LOOP, chat_message API) ---
for msg in st.session_state.messages:
    role = msg.get("role", "assistant")
    content = msg.get("content", "")
    with st.chat_message(role):
        st.markdown(content)

# --- INPUT (ONE INPUT) ---
if prompt := st.chat_input("Message ARCHITECT AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Responding..."):
        reply = chatbot.get_response(prompt)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# --- FOOTER ---
st.markdown(
    """
    <div style='text-align:center; color:#555; margin-top:20px;'>
        © 2025 ARCHITECT AI — All Rights Reserved
    </div>
    """,
    unsafe_allow_html=True,
)
)





