import streamlit as st
from db import get_db, get_collection_name
import pandas as pd
from cgpa import update_all_cgpa
from config import CREDIT_COLLECTION
import os
import matplotlib.pyplot as plt
import numpy as np


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Result Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------
st.markdown("## 📊 Result Analysis")

# --------------------------------------------------
# SESSION VALIDATION
# --------------------------------------------------
if "current_df" not in st.session_state or "current_department" not in st.session_state:
    st.warning("No result data available.")
    st.info("Please upload and process a result PDF first.")
    st.stop()

df = st.session_state["current_df"]
department = st.session_state["current_department"]
db = get_db()
collection_name = get_collection_name(department)

update_all_cgpa(
    db,
    collection_name,
    CREDIT_COLLECTION
)
# ---------------------------------------
# FETCH CGPA FROM DB AND ADD TO DF
# ---------------------------------------

collection = db[collection_name]

cgpa_map = {
    student["reg_no"]: student.get("CGPA", 0)
    for student in collection.find({}, {"reg_no": 1, "CGPA": 1})
}

df["CGPA"] = df["Register No"].map(cgpa_map)

# ---------------------------------------
# UPDATE CSV FILE WITH CGPA COLUMN
# ---------------------------------------

output_file = department.replace(" ", "_") + ".csv"
output_path = os.path.join("outputs", output_file)

df.to_csv(output_path, index=False)

# --------------------------------------------------
# BASIC METRICS
# --------------------------------------------------
total_students = len(df)
total_subjects = len([col for col in df.columns if col not in ["Register No", "CGPA"]]) # excluding Register No

subjects = [col for col in df.columns if col not in ["Register No", "CGPA"]]

#------------------PERFORMANCE ANALYSIS---------------------
st.markdown("## 📘 Performance Analysis of All Students")

analysis_rows = []

for subject in subjects:

    total = len(df)

    pass_count = df[df[subject] != "F"].shape[0]
    fail_count = df[df[subject] == "F"].shape[0]

    pass_percent = round((pass_count / total) * 100, 2)

    grade_counts = df[subject].value_counts().to_dict()

    row = {
        "Subject": subject,
        "Pass %": pass_percent,
        "Pass Count": pass_count,
        "Fail Count": fail_count,
        "S": grade_counts.get("S", 0),
        "A+": grade_counts.get("A+", 0),
        "A": grade_counts.get("A", 0),
        "B+": grade_counts.get("B+", 0),
        "B": grade_counts.get("B", 0),
        "C+": grade_counts.get("C+", 0),
        "C": grade_counts.get("C", 0),
        "D": grade_counts.get("D", 0),
        "P": grade_counts.get("P", 0),
        "F": grade_counts.get("F", 0)
    }

    analysis_rows.append(row)

analysis_df = pd.DataFrame(analysis_rows)
st.dataframe(analysis_df, use_container_width=True)

# --------------------------------------------------
# PASS vs FAIL CHART (COMPACT)
# --------------------------------------------------

st.markdown("### 📊 Pass vs Fail Comparison")

subjects_chart = analysis_df["Subject"]
pass_counts = analysis_df["Pass Count"]
fail_counts = analysis_df["Fail Count"]

fig = plt.figure(figsize=(10, 4))  # compact height

x = np.arange(len(subjects_chart))
width = 0.35

plt.bar(x - width/2, pass_counts, width)
plt.bar(x + width/2, fail_counts, width)

plt.xticks(x, subjects_chart, rotation=45, fontsize=8)
plt.yticks(fontsize=8)
plt.xlabel("Subject", fontsize=9)
plt.ylabel("Count", fontsize=9)
plt.title("Pass vs Fail Count per Subject", fontsize=10)

plt.legend(["Pass", "Fail"], fontsize=8, loc="upper right")

plt.tight_layout()

st.pyplot(fig)

# --------------------------------------------------
# GRADE DISTRIBUTION CHART (COMPACT)
# --------------------------------------------------

st.markdown("### 🎯 Grade Distribution")

grade_columns = ["S", "A+", "A", "B+", "B", "C+", "C", "D", "P", "F"]

subjects_chart = analysis_df["Subject"]

fig2 = plt.figure(figsize=(10, 4))  # smaller height

bottom_values = np.zeros(len(subjects_chart))

for grade in grade_columns:
    values = analysis_df[grade]
    plt.bar(subjects_chart, values, bottom=bottom_values)
    bottom_values += values

plt.xticks(rotation=45, fontsize=8)
plt.yticks(fontsize=8)
plt.xlabel("Subject", fontsize=9)
plt.ylabel("Count", fontsize=9)
plt.title("Grade Distribution per Subject", fontsize=10)

# Smaller legend, placed below
plt.legend(
    grade_columns,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.25),
    ncol=5,
    fontsize=7
)

plt.tight_layout()

st.pyplot(fig2)


# --------------------------------------------------
# DISPLAY HEADER
# --------------------------------------------------
st.markdown(f"### 📄 {department}")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Students", total_students)

with col2:
    st.metric("Total Subjects", total_subjects)

# --------------------------------------------------
# RESULT PREVIEW
# --------------------------------------------------
st.markdown("### 🔍 Student Result Preview")
st.dataframe(df, use_container_width=True)

# --------------------------------------------------
# REGULAR STUDENTS FILTER
# --------------------------------------------------

regular_df = df[df["Register No"].str.contains("19")]

st.markdown("## 📗 Performance Analysis of  Students (2019)")

total_regular = len(regular_df)

failed_students = regular_df[
    (regular_df[subjects] == "F").any(axis=1)
]

total_failed = len(failed_students)
total_passed = total_regular - total_failed

pass_percent_regular = round((total_passed / total_regular) * 100, 2)

col1, col2, col3 = st.columns(3)

col1.metric("Total Regular Students", total_regular)
col2.metric("Total Failed (≥1 F)", total_failed)
col3.metric("Pass % (Regular)", f"{pass_percent_regular}%")

# --------------------------------------------------
# TOPPERS
# --------------------------------------------------


db = get_db()

collection = db[collection_name]

top_students  = list(
    collection.find().sort("CGPA", -1).limit(3)
)

st.markdown("## 🏆 Toppers ")

for student in top_students:
    st.write(f"{student['reg_no']} — CGPA: {student.get('CGPA', 0)}")


# --------------------------------------------------
# EXPORT OPTIONS
# --------------------------------------------------

st.markdown("## 📤 Export Report")

col1, col2 = st.columns(2)

with col1:
    if st.button("Export as Excel (.xlsx)"):

        from report_generator import generate_excel_report

        file_path = generate_excel_report(
            department,
            df,
            analysis_df,
            total_students
        )

        with open(file_path, "rb") as f:
            st.download_button(
                label="Download Excel",
                data=f,
                file_name=f"{department}_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

with col2:
    if st.button("Export as PDF (.pdf)"):

        from report_generator import generate_pdf_report

        file_path = generate_pdf_report(
            department,
            df,
            analysis_df,
            total_students
        )

        with open(file_path, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name=f"{department}_Report.pdf",
                mime="application/pdf"
            )


# --------------------------------------------------
# HANDLE EXPORT ACTION
# --------------------------------------------------

from report_generator import generate_excel_report, generate_pdf_report

if "export_type" in st.session_state:

    if st.session_state["export_type"] == "excel":
        file_path = generate_excel_report(
            department,
            df,
            analysis_df,
            total_students
        )
        st.success("Excel report generated!")
        with open(file_path, "rb") as f:
            st.download_button(
                label="Download Excel",
                data=f,
                file_name=f"{department}_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


    elif st.session_state["export_type"] == "pdf":
        file_path = generate_pdf_report(
            department,
            df,
            analysis_df,
            total_students
        )
        st.success("PDF report generated!")
        with open(file_path, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name=f"{department}_Report.pdf",
                mime="application/pdf"
            )

# --------------------------------------------------
# DATA LOSS WARNING
# --------------------------------------------------
st.warning(
    "⚠️ This result data is temporary. "
    "It will be cleared if you reload the page, close the browser, or start a new upload."
)
