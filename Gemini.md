# Project: Enterprise Content Analysis Platform

## File Structure

- `app.py`: The main Streamlit application.
- `content_analyzer.py`: Module for handling content analysis with OpenAI.
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
-   **Content Input:** A file uploader allows users to upload one or more text files for analysis.
-   **Analysis Trigger:** An "Analyze" button initiates the content analysis process for the uploaded files.
-   **Formatted Results:** The analysis results for each file are displayed in a clear and organized format.
-   **Cost Estimation:** The estimated cost of the API call is shown after each analysis.
-   **Layout:** The application displays an uploader at the top. After analysis, results for each file are displayed in a two-column format.

## ContentAnalyzer Class

The `ContentAnalyzer` class in `content_analyzer.py` connects to the OpenAI API to analyze text.

### Methods

- `analyze_content(text)`: Sends the input text to GPT-4o-mini for analysis and returns a dictionary with the following information:
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
