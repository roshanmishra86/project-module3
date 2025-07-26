import streamlit as st
from content_analyzer import analyze_content
from dotenv import load_dotenv
import os

load_dotenv()

st.title("Enterprise Content Analysis Platform")

uploaded_file = st.file_uploader("Upload a business document", type=["txt", "md"])

if uploaded_file is not None:
    with st.spinner("Analyzing document..."):
        content = uploaded_file.read().decode("utf-8")
        analysis_result = analyze_content(content)
        st.subheader("Analysis Result")
        st.write(analysis_result)
