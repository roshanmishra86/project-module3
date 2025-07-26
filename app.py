import streamlit as st
from content_analyzer import ContentAnalyzer
from document_processor import DocumentProcessor
from cost_tracker import CostTracker
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()


try:
    import pandas as pd
except ImportError:
    import streamlit as st
    st.error("pandas is required for the dashboard. Please install it with 'pip install pandas'.")
    st.stop()
import tempfile
import os

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

with st.sidebar:
    st.header("API Usage Budget")
    daily_remaining, monthly_remaining = cost_tracker.get_remaining_budget()
    st.metric(label="Daily Remaining", value=f"${daily_remaining:.2f}")
    st.metric(label="Monthly Remaining", value=f"${monthly_remaining:.2f}")

st.header("Analytics Dashboard")

tab1, tab2 = st.tabs(["Single Analysis", "Batch Processing"])

with tab1:
    st.subheader("Single Document Analysis")
    analysis_type = st.selectbox(
        "Select Analysis Type",
        options=list(analyzer.ANALYSIS_TEMPLATES.keys()),
        key="single_analysis_type"
    )
    uploaded_file = st.file_uploader("Upload a document for analysis", type=["txt", "pdf", "docx"], key="single")
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        doc_content = doc_processor.extract_content(tmp_path)
        doc = {"id": uploaded_file.name, "content": doc_content}
        with st.spinner("Analyzing document..."):
            result = analyzer.batch_analyze([doc], analysis_type=analysis_type)[0]
        # Extract columns for DataFrame
        r = result.get("result", {})
        # Map fields based on analysis_type
        if analysis_type == "General Business":
            doc_type = r.get("content_classification", {}).get("type", "-")
            sentiment = r.get("sentiment_analysis", {}).get("overall_sentiment", "-")
            business_impact = r.get("strategic_implications", {}).get("opportunities", ["-"])
            business_impact = ", ".join(business_impact) if isinstance(business_impact, list) else business_impact
            confidence = r.get("sentiment_analysis", {}).get("confidence_score", "-")
        elif analysis_type == "Competitive Intelligence":
            doc_type = r.get("competitor_profile", {}).get("market_position", "-")
            sentiment = "-"
            business_impact = r.get("strategic_analysis", {}).get("opportunities", ["-"])
            business_impact = ", ".join(business_impact) if isinstance(business_impact, list) else business_impact
            confidence = "-"
        elif analysis_type == "Customer Feedback":
            doc_type = r.get("feedback_classification", {}).get("feedback_type", "-")
            sentiment = r.get("sentiment_analysis", {}).get("overall_sentiment", "-")
            business_impact = r.get("actionable_insights", [{}])[0].get("insight", "-") if r.get("actionable_insights") else "-"
            confidence = r.get("sentiment_analysis", {}).get("confidence_score", "-")
        else:
            doc_type = sentiment = business_impact = confidence = "-"
        # Cost calculation
        input_tokens = result.get("input_tokens", 0)
        output_tokens = result.get("output_tokens", 0)
        cost = cost_tracker._calculate_cost(input_tokens, output_tokens)
        df = pd.DataFrame([{
            "Document": result.get("id"),
            "Type": doc_type,
            "Sentiment": sentiment,
            "Business Impact": business_impact,
            "Confidence": confidence,
            "Cost": cost
        }])
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, f"single_analysis_{uploaded_file.name}.csv", "text/csv")
        st.metric("Total Cost", f"${cost:.4f}")
        try:
            conf_val = float(confidence)
        except Exception:
            conf_val = 0.0
        st.metric("Average Confidence", f"{conf_val:.2f}")
        os.unlink(tmp_path)

with tab2:
    st.subheader("Batch Document Processing")
    analysis_type = st.selectbox(
        "Select Analysis Type",
        options=list(analyzer.ANALYSIS_TEMPLATES.keys()),
        key="batch_analysis_type"
    )
    uploaded_files = st.file_uploader("Upload multiple documents", type=["txt", "pdf", "docx"], accept_multiple_files=True, key="batch")
    if uploaded_files:
        docs = []
        temp_paths = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            doc_content = doc_processor.extract_content(tmp_path)
            docs.append({"id": uploaded_file.name, "content": doc_content})
            temp_paths.append(tmp_path)
        with st.spinner("Analyzing batch documents..."):
            results = analyzer.batch_analyze(docs, analysis_type=analysis_type)
        rows = []
        total_cost = 0.0
        confidences = []
        for result in results:
            r = result.get("result", {})
            # Map fields based on analysis_type
            if analysis_type == "General Business":
                doc_type = r.get("content_classification", {}).get("type", "-")
                sentiment = r.get("sentiment_analysis", {}).get("overall_sentiment", "-")
                business_impact = r.get("strategic_implications", {}).get("opportunities", ["-"])
                business_impact = ", ".join(business_impact) if isinstance(business_impact, list) else business_impact
                confidence = r.get("sentiment_analysis", {}).get("confidence_score", "-")
            elif analysis_type == "Competitive Intelligence":
                doc_type = r.get("competitor_profile", {}).get("market_position", "-")
                sentiment = "-"
                business_impact = r.get("strategic_analysis", {}).get("opportunities", ["-"])
                business_impact = ", ".join(business_impact) if isinstance(business_impact, list) else business_impact
                confidence = "-"
            elif analysis_type == "Customer Feedback":
                doc_type = r.get("feedback_classification", {}).get("feedback_type", "-")
                sentiment = r.get("sentiment_analysis", {}).get("overall_sentiment", "-")
                business_impact = r.get("actionable_insights", [{}])[0].get("insight", "-") if r.get("actionable_insights") else "-"
                confidence = r.get("sentiment_analysis", {}).get("confidence_score", "-")
            else:
                doc_type = sentiment = business_impact = confidence = "-"
            input_tokens = result.get("input_tokens", 0)
            output_tokens = result.get("output_tokens", 0)
            cost = cost_tracker._calculate_cost(input_tokens, output_tokens)
            total_cost += cost
            try:
                conf_val = float(confidence)
                confidences.append(conf_val)
            except Exception:
                pass
            rows.append({
                "Document": result.get("id"),
                "Type": doc_type,
                "Sentiment": sentiment,
                "Business Impact": business_impact,
                "Confidence": confidence,
                "Cost": cost
            })
        df = pd.DataFrame(rows)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "batch_analysis_results.csv", "text/csv")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Cost", f"${total_cost:.2f}")
        with col2:
            avg_conf = sum(confidences)/len(confidences) if confidences else 0.0
            st.metric("Average Confidence", f"{avg_conf:.2f}")
        for p in temp_paths:
            os.unlink(p)
