import streamlit as st
from content_analyzer import ContentAnalyzer
from document_processor import DocumentProcessor
from cost_tracker import CostTracker
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()

st.set_page_config(layout="wide")
st.title("Enterprise Content Analysis Platform")

# Initialize the ContentAnalyzer, DocumentProcessor, and CostTracker
try:
    analyzer = ContentAnalyzer()
    doc_processor = DocumentProcessor()
    cost_tracker = CostTracker()
except ValueError as e:
    st.error(e)
    st.stop()

# Display budget in sidebar

with st.sidebar:
    st.header("API Usage Budget")
    daily_remaining, monthly_remaining = cost_tracker.get_remaining_budget()
    st.metric(label="Daily Remaining", value=f"${daily_remaining:.2f}")
    st.metric(label="Monthly Remaining", value=f"${monthly_remaining:.2f}")

    # Show file info, token count, and estimated cost for uploaded files
    if 'uploaded_files' in locals() and uploaded_files:
        st.header("Uploaded File(s) Info")
        for uploaded_file in uploaded_files:
            # Save uploaded file to a temporary location for DocumentProcessor
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            try:
                processed_doc = doc_processor.process(tmp_file_path)
                token_count = processed_doc["token_count"]
                file_type = processed_doc["file_type"]
                file_size = processed_doc["size_bytes"]
                estimated_cost = cost_tracker._calculate_cost(token_count, 500)
                st.write(f"**{uploaded_file.name}** ({file_type.upper()}, {file_size} bytes)")
                st.write(f"Token Count: {token_count}")
                st.write(f"Estimated Cost: ${estimated_cost:.4f}")
            except Exception as e:
                st.write(f"{uploaded_file.name}: Error reading file ({e})")
            finally:
                os.unlink(tmp_file_path)


# Ensure uploaded_files is always defined for sidebar use
uploaded_files = None
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
                token_count = processed_doc["token_count"]
                file_type = processed_doc["file_type"]
                file_size = processed_doc["size_bytes"]

                st.subheader(f"File: {uploaded_file.name}")
                st.write(f"**File Type:** {file_type.upper()}")
                st.write(f"**File Size:** {file_size} bytes")
                st.write(f"**Token Count (for analysis):** {token_count}")

                # Estimate cost and check budget before analysis
                # Assuming 500 output tokens for estimation for a rough estimate
                estimated_cost = cost_tracker._calculate_cost(token_count, 500)
                st.write(f"**Estimated Analysis Cost:** ${estimated_cost:.4f}")

                if not cost_tracker.can_afford(estimated_cost):
                    st.error(f"Analysis for {uploaded_file.name} would exceed budget. Estimated cost: ${estimated_cost:.2f}. Daily remaining: ${daily_remaining:.2f}, Monthly remaining: ${monthly_remaining:.2f}.")
                    os.unlink(tmp_file_path)
                    continue

                with st.spinner(f"Performing '{analysis_type}' analysis on {uploaded_file.name}..."):
                    analysis_result, input_tokens_used, output_tokens_used = analyzer.analyze_content(content_input, analysis_type)

                    if "error" in analysis_result:
                        st.error(analysis_result["error"])
                    else:
                        # Record actual usage after successful analysis
                        actual_cost = cost_tracker.record_usage(input_tokens_used, output_tokens_used)
                        st.success(f"Analysis complete for {uploaded_file.name}! Cost: ${actual_cost:.4f}")

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
            except ValueError as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred while processing {uploaded_file.name}: {e}")
            finally:
                # Clean up the temporary file
                os.unlink(tmp_file_path)
    else:
        st.warning("Please upload at least one file to analyze.")
