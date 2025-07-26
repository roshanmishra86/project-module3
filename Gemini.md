# Project: Enterprise Content Analysis Platform

## File Structure

- `app.py`: The main Streamlit application.
- `content_analyzer.py`: Module for handling content analysis with OpenAI.
- `document_processor.py`: Module for processing uploaded documents.
- `cost_tracker.py`: Module for tracking API usage and costs.
- `requirements.txt`: Project dependencies.
- `.env.example`: Example for environment variables.
- `README.md`: Project overview.

## Setup Instructions (for user)

1.  **Create and activate virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```
2.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```
3.  **Configure API Key:**
    - Create a `.env` file from the `.env.example`.
    - Add your OpenAI API key to the `.env` file.
4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## Streamlit Application (`app.py`)

The main application is built with Streamlit and provides a user-friendly interface for the content analysis platform.

### Features

-   **Professional Title:** The application is titled "Enterprise Content Analysis Platform".
-   **Analysis Type Selection:** A dropdown menu allows users to select the type of analysis to perform (e.g., General Business, Competitive Intelligence, Customer Feedback).
-   **Content Input:** A file uploader allows users to upload one or more text, PDF, or DOCX files for analysis.
-   **File Information Display:** After uploading, the application displays file type, size, and token count for each document.
-   **Cost Estimation:** The estimated cost of the API call is shown for each uploaded file before analysis.
-   **Cost Tracking Metrics:** Daily and monthly API usage and remaining budget are displayed in the sidebar.
-   **Batch Analysis:** The "Analyze Content" button triggers batch processing for all uploaded files. Progress is shown using `st.progress()` and status updates. Each file is processed with a 0.5s delay between API calls, and errors for individual files do not stop the batch.
-   **Formatted Results:** The analysis results for each file are displayed in a clear and organized format tailored to the chosen analysis type.
-   **Error Handling:** Proper error handling is implemented for unsupported file types or processing issues. If a file fails, its error is shown but other files continue.
-   **Layout:** The application is organized with configuration options (analysis type, file uploader) at the top, followed by the detailed results for each analyzed file.

## ContentAnalyzer Class

The `ContentAnalyzer` class in `content_analyzer.py` connects to the OpenAI API to analyze text, supporting both single and batch processing.

### Methods

- `analyze_content(text, analysis_type)`: Sends the input text to GPT-4o-mini for analysis and returns a dictionary with structured results (see below).
- `batch_analyze(docs, analysis_type, progress_callback=None)`: Processes a list of documents in batch mode with:
  - Progress tracking (calls `progress_callback(progress, status)` if provided)
  - 0.5 second rate limiting between requests
  - Graceful error handling (continues if one document fails)
  - Returns a list of results, each with `id`, `timestamp`, `result`, and `error` (if any)

#### Output Structure (for each document)
  - `content_classification`:
    - `type`: e.g., Financial Report, Customer Feedback, News Article
    - `industry`: e.g., Technology, Healthcare, Finance
    - `quality_score`: Rate from 1-10 (1=Poor, 10=Excellent)
  - `key_insights`: A list of 3-5 findings with impact levels (High, Medium, Low).
  - `sentiment_analysis`:
    - `overall_sentiment`: Positive, Neutral, or Negative
    - `confidence_score`: Score from 0.0 to 1.0
  - `strategic_implications`:
    - `opportunities`: A list of opportunities.
    - `risks`: A list of risks.
  - `action_items`: A list of action items with priorities (High, Medium, Low).
  - `executive_summary`: A concise, high-level summary for a C-suite audience.
  - `id`: Document identifier
  - `timestamp`: UTC ISO timestamp of analysis
  - `error`: Error message if analysis failed, else `None`

## DocumentProcessor Class

The `DocumentProcessor` class in `document_processor.py` handles file processing.

### Methods

- `process(file_path)`:
  - Handles PDF, DOCX, and TXT files.
  - Extracts and cleans text from each format.
  - Optimizes content length to reduce API costs (max 3000 tokens).
  - Uses tiktoken to count tokens accurately.
  - Returns document metadata (type, size, token count).

## CostTracker Class

The `CostTracker` class in `cost_tracker.py` tracks daily and monthly API usage and calculates costs.

### Methods

- `record_usage(input_tokens, output_tokens)`: Records the API usage and calculates the cost.
- `get_daily_usage()`: Returns the total cost for the current day.
- `get_monthly_usage()`: Returns the total cost for the current month.
- `can_afford(estimated_cost)`: Checks if the estimated cost is within the daily and monthly budget limits.
- `get_remaining_budget()`: Returns the remaining daily and monthly budget.