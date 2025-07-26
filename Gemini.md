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
-   **Content Input:** A text area is provided for users to paste the content they want to analyze.
-   **Analysis Trigger:** An "Analyze" button initiates the content analysis process.
-   **Formatted Results:** The analysis results (summary, sentiment, and key points) are displayed in a clear and organized format.
-   **Cost Estimation:** The estimated cost of the API call is shown after each analysis.
-   **Layout:** The application uses a two-column layout for a better user experience, separating the input and output sections.

## ContentAnalyzer Class

The `ContentAnalyzer` class in `content_analyzer.py` connects to the OpenAI API to analyze text.

### Methods

- `analyze_content(text)`: Sends the input text to GPT-4o-mini for analysis and returns a dictionary with the following information:
    - `summary`: A brief summary of the text.
    - `sentiment`: The sentiment of the text (positive, neutral, or negative).
    - `key_points`: A list of three key points from the text.