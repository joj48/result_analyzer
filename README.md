# 🎓 KTU Result Analyzer

A **Streamlit-based web application** designed to analyze **Kerala Technological University (KTU)** examination result PDFs.  
The system extracts department-wise results, performs analysis, and provides an **AI-powered assistant** for querying insights — all while maintaining **data privacy** through session-based processing.

---

## 🚀 Features

- 📄 Upload official KTU result PDFs
- 🏫 Automatic department detection
- 📊 Session-based result analysis (no stale data)
- 🤖 AI chatbot for result-related queries
- 📝 Issue / error reporting module with attachments
- 🔐 Privacy-aware design (temporary data only)
- 🔄 Auto-redirect to result page after processing

---

## 🧠 Application Flow

1. **Upload PDF**  
   Upload the official KTU result PDF.

2. **Process Results**  
   Select a department (or all departments) and process results.

3. **Result Analysis**  
   View the processed result for the current session only.

4. **AI Assistant**  
   Ask questions, generate insights, and visualize data.

5. **Report Issues**  
   Users can report errors with description and supporting files.

> ⚠️ All uploaded PDFs and generated results are **temporary** and are automatically cleared on reload or new upload.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: MongoDB (for processed result storage)
- **AI**: Google Gemini API
- **Visualization**: Pandas, Plotly
- **Version Control**: Git & GitHub

---

## ▶️ How to Run the Project

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/akhilabusalih/KTU_Result-Analyzer.git
cd KTU_Result-Analyzer
```
### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Configure Environment Variables
Create a **.env** or **Api.env** file and add:
```bash
GEMINI_API_KEY=your_api_key_here
```
### 4️⃣ Run the Application
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```bash
KTU_Result-Analyzer/
│
├── app.py                  # Main landing page
├── pages/
│   ├── 1-upload.py         # Upload & processing
│   ├── 2-result.py         # Result analysis (session-based)
│   ├── 3-chatbot.py        # AI assistant
│   └── 4-report.py         # Issue reporting module
│
├── core.py                 # Core PDF parsing & logic
├── db.py                   # MongoDB integration
├── requirements.txt
└── README.md
```
---
## 🔐 Data Privacy & Design Decisions
- **Uploaded PDFs and generated CSVs are temporary**
- **Data is cleared on:**
  - Page reload 
  - New upload
  - Application restart
- **No student data is stored permanently without explicit intent**

This ensures ethical handling of academic data.

---
## 🏷️ Versioning
- **v0.8-session-based-flow**

    Introduced session-based processing, auto-cleanup, guided UX, and stable result flow.

---
## 📌 Note
### This project is intended for academic and educational purposes.