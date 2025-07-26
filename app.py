import streamlit as st
from content_analyzer import ContentAnalyzer
from document_processor import DocumentProcessor
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()

st.set_page_config(layout="wide")
st.title("Enterprise Content Analysis Platform")

# Initialize the ContentAnalyzer and DocumentProcessor
try:
    analyzer = ContentAnalyzer()
    doc_processor = DocumentProcessor()
except ValueError as e:
    st.error(e)
    st.stop()

col1, col2 = st.columns([0.6, 0.4])
with col1:
    st.header("Upload Content for Analysis")
    analysis_type = st.selectbox(
        "Select Analysis Type",
        options=list(analyzer.ANALYSIS_TEMPLATES.keys())
    )
with col2:
    st.header("Configuration")
    uploaded_files = st.file_uploader(
        "Choose one or more files (.txt, .pdf, .docx)",
        type=["txt", "pdf", "docx"],
        accept_multiple_files=True
    )

if st.button("Analyze Content"):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.markdown(f"---")
            st.header(f"Analysis for: `{uploaded_file.name}` (`{analysis_type}`)")

            # Save uploaded file to a temporary location for DocumentProcessor
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            try:
                processed_doc = doc_processor.process(tmp_file_path)
                content_input = processed_doc["content"]
                st.info(f"Processed {uploaded_file.name}: Type={processed_doc['file_type']}, Size={processed_doc['size_bytes']} bytes, Tokens={processed_doc['token_count']}")

                with st.spinner(f"Performing '{analysis_type}' analysis on {uploaded_file.name}..."):
                    analysis_result = analyzer.analyze_content(content_input, analysis_type)

                    if "error" in analysis_result:
                        st.error(analysis_result["error"])
                    else:
                        st.success(f"Analysis complete for {uploaded_file.name}!")

                        if analysis_type == "General Business":
                            st.subheader("Executive Summary")
                            st.write(analysis_result.get("executive_summary", "Not available."))

                            st.subheader("Content Classification")
                            classification = analysis_result.get("content_classification", {})
                            st.table(classification)

                            st.subheader("Key Insights")
                            insights = analysis_result.get("key_insights", [])
                            st.table(insights)

                            st.subheader("Sentiment Analysis")
                            sentiment = analysis_result.get("sentiment_analysis", {})
                            st.table(sentiment)

                            st.subheader("Strategic Implications")
                            implications = analysis_result.get("strategic_implications", {})
                            st.write("**Opportunities:**")
                            st.json(implications.get("opportunities", []))
                            st.write("**Risks:**")
                            st.json(implications.get("risks", []))

                            st.subheader("Action Items")
                            actions = analysis_result.get("action_items", [])
                            st.table(actions)

                        elif analysis_type == "Competitive Intelligence":
                            st.subheader("Executive Summary")
                            st.write(analysis_result.get("executive_summary", "Not available."))

                            st.subheader("Competitor Profile")
                            profile = analysis_result.get("competitor_profile", {})
                            st.table(profile)

                            st.subheader("Key Findings")
                            findings = analysis_result.get("key_findings", [])
                            st.table(findings)

                            st.subheader("Strategic Analysis")
                            strategic_analysis = analysis_result.get("strategic_analysis", {})
                            st.write("**Opportunities:**")
                            st.table(strategic_analysis.get("opportunities", []))
                            st.write("**Threats:**")
                            st.table(strategic_analysis.get("threats", []))

                            st.subheader("Recommendations")
                            recommendations = analysis_result.get("recommendations", [])
                            st.table(recommendations)

                        elif analysis_type == "Customer Feedback":
                            st.subheader("Executive Summary")
                            st.write(analysis_result.get("executive_summary", "Not available."))

                            st.subheader("Feedback Classification")
                            classification = analysis_result.get("feedback_classification", {})
                            st.table(classification)

                            st.subheader("Sentiment Analysis")
                            sentiment = analysis_result.get("sentiment_analysis", {})
                            st.table(sentiment)

                            st.subheader("Key Themes")
                            themes = analysis_result.get("key_themes", [])
                            st.table(themes)

                            st.subheader("Actionable Insights")
                            insights = analysis_result.get("actionable_insights", [])
                            st.table(insights)
            finally:
                # Clean up the temporary file
                os.unlink(tmp_file_path)
    else:
        st.warning("Please upload at least one file to analyze.")
