import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
import pandas as pd
import plotly.express as px
import pypdf
import re

# --------------------------------------------------
# 1. PAGE CONFIG (SAFE IN MULTI-PAGE APP)
# --------------------------------------------------
st.set_page_config(
    page_title="Gemini Ultra Chat",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2. CUSTOM CSS (THEME-CONSISTENT)
# --------------------------------------------------
st.markdown("""
<style>
    /* Layout spacing */
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2.5rem;
    }

    /* Chat message base */
    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 10px;
        border: 1px solid rgba(255,255,255,0.08);
        background-color: rgba(255,255,255,0.03);
    }

    /* User message */
    [data-testid="stChatMessage"][aria-label="user"] {
        background-color: rgba(255,255,255,0.05);
    }

    /* Assistant message */
    [data-testid="stChatMessage"][aria-label="assistant"] {
        background-color: rgba(255,255,255,0.025);
    }

    /* Chat input box */
    textarea {
        background-color: rgba(255,255,255,0.04) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
    }

    /* Buttons */
    button {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3. API SETUP
# --------------------------------------------------
load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    load_dotenv("Api.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API Key not found. Configure GEMINI_API_KEY.")
    st.stop()

client = genai.Client(api_key=api_key)

# --------------------------------------------------
# 4. FETCH ALL MODELS
# --------------------------------------------------
@st.cache_data
def get_all_models():
    try:
        models = client.models.list()
        model_names = [m.name for m in models]
        model_names.sort(reverse=True)
        return model_names, None
    except Exception as e:
        return ["gemini-2.0-flash", "gemini-1.5-pro"], str(e)

available_models, fetch_error = get_all_models()

# --------------------------------------------------
# 5. SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ Configuration")

    if fetch_error:
        st.error(fetch_error)

    selected_model = st.selectbox(
        "Select Model",
        available_models,
        index=0,
        label_visibility="collapsed"
    )

    clean_name = selected_model.replace("models/", "")
    st.caption(f"Active: `{clean_name}`")

    st.markdown("---")
    st.markdown("#### 📂 Knowledge Base")

    uploaded_file = st.file_uploader(
        "Upload Context (PDF/TXT)",
        type=["pdf", "txt"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.success(f"Linked: {uploaded_file.name}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    with col2:
        st.download_button(
            "💾 Save",
            data=str(st.session_state.get("messages", "")),
            file_name="chat_history.json",
            use_container_width=True
        )

# --------------------------------------------------
# 6. CORE LOGIC
# --------------------------------------------------
SYS_PROMPT = """
You are a professional AI assistant.
1. IMAGE: If asked to generate/draw, start with "GENERATE_IMAGE:".
2. DATA: If asked for a chart, return Plotly code inside ```python``` blocks.
3. TONE: Be concise and professional.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

def extract_text(file):
    try:
        if file.type == "application/pdf":
            reader = pypdf.PdfReader(file)
            return "".join(p.extract_text() or "" for p in reader.pages)
        return file.getvalue().decode("utf-8")
    except:
        return ""

def exec_code(code):
    try:
        match = re.search(r"```python(.*?)```", code, re.DOTALL)
        if match:
            env = {"pd": pd, "px": px}
            exec(match.group(1), {}, env)
            return env.get("fig")
    except:
        return None

# --------------------------------------------------
# 7. MAIN UI
# --------------------------------------------------
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding-top:50px;">
        <h1>Gemini Ultra Chat</h1>
        <p>Connected to multiple Gemini models</p>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"], width=400)
        elif msg["type"] == "plot":
            fig = exec_code(f"```python\n{msg['code']}\n```")
            if fig:
                st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# 8. INPUT HANDLER
# --------------------------------------------------
if prompt := st.chat_input("Type your request here..."):
    st.session_state.messages.append(
        {"role": "user", "type": "text", "content": prompt}
    )

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Connecting to model...")

        try:
            context = ""
            if uploaded_file:
                context = extract_text(uploaded_file)

            history = "\n".join(
                f"{m['role'].upper()}: {m['content']}"
                for m in st.session_state.messages
                if m["type"] == "text"
            )

            full_input = f"{SYS_PROMPT}\n{history}\n{context}\nUSER: {prompt}"

            response = client.models.generate_content(
                model=selected_model,
                contents=full_input
            )

            text = response.text

            if "GENERATE_IMAGE:" in text:
                img_prompt = text.replace("GENERATE_IMAGE:", "").strip()
                url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}"
                st.image(url, width=400)
                st.session_state.messages.append(
                    {"role": "assistant", "type": "image", "content": url}
                )

            elif "```python" in text:
                fig = exec_code(text)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                code = re.search(r"```python(.*?)```", text, re.DOTALL).group(1)
                st.session_state.messages.append(
                    {"role": "assistant", "type": "plot", "code": code}
                )

            else:
                placeholder.markdown(text)
                st.session_state.messages.append(
                    {"role": "assistant", "type": "text", "content": text}
                )

        except Exception as e:
            placeholder.error(f"Error: {e}")
