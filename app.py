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

col1, col2 = st.columns(2)

with col1:
    st.header("Input Content")
    content_input = st.text_area("Paste your content here", height=300)
    analyze_button = st.button("Analyze")

with col2:
    st.header("Analysis Results")
    if analyze_button:
        if content_input:
            with st.spinner("Analyzing content..."):
                analysis_result = analyzer.analyze_content(content_input)

                if "error" in analysis_result:
                    st.error(analysis_result["error"])
                else:
                    st.success("Analysis complete!")
                    st.write("**Summary:**", analysis_result.get("summary"))
                    st.write("**Sentiment:**", analysis_result.get("sentiment"))
                    st.write("**Key Points:**")
                    for point in analysis_result.get("key_points", []):
                        st.write(f"- {point}")

                    st.info("Estimated API Cost: $0.05")
        else:
            st.warning("Please paste some content to analyze.")