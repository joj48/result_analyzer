import streamlit as st
import os
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Report an Issue",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# STYLING (CONSISTENT WITH APP)
# --------------------------------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2.5rem;
        max-width: 720px;
    }

    .hint {
        color: #9da5b4;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------
st.markdown("## 📝 Report an Issue")
st.markdown(
    "<div class='hint'>Use this form to report any errors or unexpected behavior you encountered.</div>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# REPORT FORM
# --------------------------------------------------
with st.form("issue_report_form", clear_on_submit=True):

    name = st.text_input("Your Name")

    email = st.text_input("Email / Contact Details")

    subject = st.selectbox(
        "Error Subject",
        [
            "Upload PDF Error",
            "Result Analysis Error",
            "Chatbot Error",
            "UI / Display Issue",
            "Performance Issue",
            "Other"
        ]
    )

    description = st.text_area(
        "Brief Description of the Issue",
        placeholder="Explain what happened, what you expected, and any error messages shown...",
        height=180
    )

    attachments = st.file_uploader(
        "Upload Supporting Image / Video (optional)",
        type=["png", "jpg", "jpeg", "mp4", "mov", "avi"],
        accept_multiple_files=True
    )

    submit = st.form_submit_button("📨 Submit Report")

# --------------------------------------------------
# SAVE REPORT
# --------------------------------------------------
if submit:
    if not name.strip() or not email.strip() or not description.strip():
        st.error("Please fill in all required fields (Name, Email, Description).")
    else:
        # Directories
        REPORT_DIR = "reports"
        ATTACH_DIR = os.path.join(REPORT_DIR, "attachments")

        os.makedirs(REPORT_DIR, exist_ok=True)
        os.makedirs(ATTACH_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_filename = f"report_{timestamp}.txt"
        report_path = os.path.join(REPORT_DIR, report_filename)

        # Handle attachments
        attachment_info = []
        if attachments:
            for file in attachments:
                file_path = os.path.join(ATTACH_DIR, f"{timestamp}_{file.name}")
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

                attachment_info.append(
                    f"- {file.name} | Type: {file.type} | Saved at: {file_path}"
                )

        # Prepare report content
        report_content = f"""
ISSUE REPORT
============

Time        : {datetime.now()}
Name        : {name}
Email       : {email}
Error Type  : {subject}

Description:
------------
{description}

Attachments:
------------
{chr(10).join(attachment_info) if attachment_info else "No attachments provided."}
        """.strip()

        # Write report file
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        st.success("✅ Your issue report has been submitted successfully.")
        st.caption("Thank you for helping us improve the system.")
