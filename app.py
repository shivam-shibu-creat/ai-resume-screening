import streamlit as st
import tempfile
import os

from resume_parser import extract_text_from_pdf
from matcher import calculate_score
from skills import SKILLS

st.title("AI Resume Screening App")

resume_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
jd_text = st.text_area("Paste Job Description here")

if st.button("Analyze Resume"):

    if resume_file is None:
        st.error("Beta resume upload hi nahi hua 😅")
        st.stop()

    if jd_text.strip() == "":
        st.error("Beta JD paste nahi ki 😅")
        st.stop()

    # 🔴 IMPORTANT DEBUG CHECK
    file_size = resume_file.size
    st.write("📄 Uploaded file size (bytes):", file_size)

    if file_size == 0:
        st.error("❌ Resume file 0 KB hai — ye PDF text wali nahi hai")
        st.stop()

    # 🔴 SAFE TEMP FILE WRITE
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(resume_file.getbuffer())
        tmp_path = tmp.name

    # 🔴 EXTRA SAFETY CHECK
    if os.path.getsize(tmp_path) == 0:
        st.error("❌ Temp file bhi empty ban rahi hai")
        st.stop()

    resume_text = extract_text_from_pdf(tmp_path)
    jd_lower = jd_text.lower()

    matched_skills = []
    for skill in SKILLS:
        if skill in resume_text and skill in jd_lower:
            matched_skills.append(skill)

    score = calculate_score(resume_text, jd_lower)

    st.success("Resume analyzed successfully 🎉")
    st.write("Match Score:", score, "%")
    st.write("Matched Skills:", matched_skills)
