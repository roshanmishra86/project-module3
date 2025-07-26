import streamlit as st
from content_analyzer import ContentAnalyzer
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(layout="wide")
st.title("Enterprise Content Analysis Platform")

# Initialize the ContentAnalyzer
try:
    analyzer = ContentAnalyzer()
except ValueError as e:
    st.error(e)
    st.stop()

st.header("Upload Content for Analysis")
uploaded_files = st.file_uploader(
    "Choose one or more files (.txt)",
    type=["txt"],
    accept_multiple_files=True
)

if st.button("Analyze Content"):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.markdown(f"---")
            st.header(f"Analysis for: `{uploaded_file.name}`")

            content_input = uploaded_file.getvalue().decode("utf-8")

            with st.spinner(f"Performing advanced analysis on {uploaded_file.name}..._"):
                analysis_result = analyzer.analyze_content(content_input)

                if "error" in analysis_result:
                    st.error(analysis_result["error"])
                else:
                    st.success(f"Analysis complete for {uploaded_file.name}!")

                    col1, col2 = st.columns(2)

                    with col1:
                        # Display Executive Summary First
                        st.subheader("Executive Summary")
                        st.write(analysis_result.get("executive_summary", "Not available."))

                        # Strategic Implications
                        st.subheader("Strategic Implications")
                        implications = analysis_result.get("strategic_implications", {})
                        st.markdown("**Opportunities:**")
                        for opp in implications.get("opportunities", []):
                            st.markdown(f"- {opp}")
                        st.markdown("**Risks:**")
                        for risk in implications.get("risks", []):
                            st.markdown(f"- {risk}")

                    with col2:
                        # Content Classification and Sentiment
                        st.subheader("Content Classification & Sentiment")
                        classification = analysis_result.get("content_classification", {})
                        sentiment = analysis_result.get("sentiment_analysis", {})
                        st.metric("Content Type", classification.get("type", "N/A"))
                        st.metric("Industry", classification.get("industry", "N/A"))
                        st.metric("Quality Score", f'{classification.get("quality_score", "N/A")}/10')
                        st.metric("Overall Sentiment", f'{sentiment.get("overall_sentiment", "N/A")} (Confidence: {sentiment.get("confidence_score", "N/A")})')

                    # Key Insights
                    st.subheader("Key Insights")
                    for insight in analysis_result.get("key_insights", []):
                        st.markdown(f'- **{insight.get("finding", "N/A")}** (Impact: {insight.get("impact_level", "N/A")})')

                    # Action Items
                    st.subheader("Recommended Action Items")
                    for action in analysis_result.get("action_items", []):
                        st.markdown(f'- **{action.get("item", "N/A")}** (Priority: {action.get("priority", "N/A")})')

                    st.info("Estimated API Cost: $0.05")  # Placeholder
    else:
        st.warning("Please upload at least one file to analyze.")