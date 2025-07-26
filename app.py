import streamlit as st
from content_analyzer import ContentAnalyzer
from dotenv import load_dotenv
import os

load_dotenv()

st.title("Enterprise Content Analysis Platform")

# Initialize the ContentAnalyzer
try:
    analyzer = ContentAnalyzer()
except ValueError as e:
    st.error(e)
    st.stop()

uploaded_file = st.file_uploader("Upload a business document", type=["txt", "md"])

if uploaded_file is not None:
    with st.spinner("Analyzing document..."):
        content = uploaded_file.read().decode("utf-8")
        analysis_result = analyzer.analyze_content(content)

        st.subheader("Analysis Result")
        if "error" in analysis_result:
            st.error(analysis_result["error"])
        else:
            st.write("**Summary:**", analysis_result.get("summary"))
            st.write("**Sentiment:**", analysis_result.get("sentiment"))
            st.write("**Key Points:**")
            for point in analysis_result.get("key_points", []):
                st.write(f"- {point}")
