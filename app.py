import streamlit as st
import os

def cleanup_temp_data():
    for folder in ["uploads", "outputs"]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

# Cleanup when app starts (fresh session)
cleanup_temp_data()


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="University Result Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# GLOBAL STYLING
# --------------------------------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        color: #b0b0b0;
        margin-bottom: 3rem;
    }

    .feature-card {
        background-color: #161b22;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 25px;
        height: 100%;
    }

    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .feature-text {
        color: #c9d1d9;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .hint {
        margin-top: 3rem;
        color: #9da5b4;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# MAIN CONTENT
# --------------------------------------------------

st.markdown(
    """
    <div style="text-align:center;">
        <div class="hero-title">🎓 University Result Analyzer</div>
        <div class="hero-subtitle">
            A smart system to upload, process, analyze, and understand university examination results
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# FEATURES
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📤 Upload Result PDFs</div>
        <div class="feature-text">
            Upload official university result PDFs.  
            The system automatically extracts and structures student data.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📊 Analyze Results</div>
        <div class="feature-text">
            Generate department-wise CSVs, performance summaries, and clean visual insights.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🤖 AI Result Assistant</div>
        <div class="feature-text">
            Ask questions, generate charts, and get insights using the integrated AI chatbot.
        </div>
    </div>
    """, unsafe_allow_html=True)

# HINT
st.markdown("""
<div class="hint">
👉 Use the <b>sidebar navigation</b> to start by uploading result PDFs or exploring analysis.
</div>
""", unsafe_allow_html=True)
