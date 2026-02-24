import streamlit as st
import os
import uuid
import pandas as pd
from db import save_structured_records_to_mongodb


from core import (
    get_available_departments,
    extract_raw_lines_for_dept,
    create_matrix_data
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Upload Result PDF",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("## 📄 Upload University Result PDF")
st.caption("Upload the official university result PDF to start processing")

#---------------------WARNING-------------------------#

st.warning(
    "⚠️ Uploaded PDFs and generated results are temporary.\n\n"
    "Your data will be **permanently deleted** if you:\n"
    "- Reload the page\n"
    "- Upload a new PDF\n"
    "- Close the browser window"
)


#---------------UI STYLING----------------------------#

st.markdown("""
<style>
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2.5rem;
        max-width: 900px;
    }

    .hint {
        color: #9da5b4;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    .step-card {
        background-color: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 18px;
        height: 100%;
    }

    .step-title {
        font-weight: 600;
        margin-bottom: 6px;
    }

    .step-text {
        color: #c9d1d9;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- PATHS ---------------- #

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- SESSION STATE ---------------- #

st.session_state.setdefault("pdf_path", None)
st.session_state.setdefault("departments", [])

# ---------------- FILE UPLOAD ---------------- #

st.markdown(
    "<div class='hint'>Only official university result PDFs are supported.</div>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload Result PDF",
    type=["pdf"],
    help="Upload only official university-issued result PDFs"
)


if uploaded_file:

    # 🔥 New upload = new session → clean old files
    for folder in ["uploads", "outputs"]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))

    # 🔥 Clear previous result data (NEW SESSION)
    st.session_state.pop("current_df", None)
    st.session_state.pop("current_department", None)

    file_id = uuid.uuid4().hex
    pdf_name = f"{file_id}_{uploaded_file.name}"
    pdf_path = os.path.join(UPLOAD_DIR, pdf_name)

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ PDF uploaded successfully")
    st.caption("Departments will be detected automatically. Choose what to process below.")

    st.session_state.pdf_path = pdf_path


    # -------- PARSE IMMEDIATELY TO FIND DEPARTMENTS -------- #
    with st.status("🔄 Scanning departments in PDF...", expanded=True):
        departments = get_available_departments(pdf_path)

    if not departments:
        st.error("No departments found in the uploaded PDF")
    else:
        st.session_state.departments = departments

# ---------------- DEPARTMENT DROPDOWN ---------------- #

if st.session_state.departments:
    options = ["ALL DEPARTMENTS"] + st.session_state.departments

    selected_option = st.selectbox(
        "Select Department to Process",
        options
    )
    st.divider()

    if st.button("Process Result"):
        with st.status("🔄 Processing Result...", expanded=True):

            processed_files = []

            # -------- ALL DEPARTMENTS -------- #
            if selected_option == "ALL DEPARTMENTS":
                for dept in st.session_state.departments:
                    raw_data = extract_raw_lines_for_dept(
                        st.session_state.pdf_path,
                        dept
                    )
                    headers, matrix_data = create_matrix_data(raw_data)

                    if not matrix_data:
                        continue

                    rows = []

                    for student in matrix_data:

                        row = {
                            "Register No": student["reg_no"]
                        }

                        for subject, info in student["subjects"].items():
                            row[subject] = info["grade"]

                        rows.append(row)

                    df = pd.DataFrame(rows)

                    output_file = dept.replace(" ", "_") + ".csv"
                    output_path = os.path.join(OUTPUT_DIR, output_file)
                    df.to_csv(output_path, index=False)

                    # Save to MongoDB
                    save_structured_records_to_mongodb(matrix_data, dept)

                    processed_files.append(output_file)
                    # Update session with latest processed department
                    st.session_state["current_department"] = dept
                    st.session_state["current_df"] = df


            # -------- SINGLE DEPARTMENT -------- #
            else:
                raw_data = extract_raw_lines_for_dept(
                    st.session_state.pdf_path,
                    selected_option
                )
                headers, matrix_data = create_matrix_data(raw_data)

                if matrix_data:
                    rows = []

                    for student in matrix_data:

                        row = {
                            "Register No": student["reg_no"]
                        }

                        for subject, info in student["subjects"].items():
                            row[subject] = info["grade"]

                        rows.append(row)

                    df = pd.DataFrame(rows)

                    output_file = selected_option.replace(" ", "_") + ".csv"
                    output_path = os.path.join(OUTPUT_DIR, output_file)
                    df.to_csv(output_path, index=False)

                    # Save to MongoDB
                    save_structured_records_to_mongodb(matrix_data, selected_option)

                    processed_files.append(output_file)
                    # -------- STORE CURRENT SESSION DATA -------- #
                    st.session_state["current_department"] = selected_option
                    st.session_state["current_df"] = df

        # ---------------- RESULT FEEDBACK ---------------- #

        if processed_files:
            st.success("✅ Processing completed successfully")

            st.caption("Redirecting to Result Analysis page...")

            # Small delay so user sees success message
            import time

            time.sleep(1)

            # 🔥 Auto-redirect to Result page
            st.switch_page("pages/2-result.py")
