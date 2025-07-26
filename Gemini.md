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

## ContentAnalyzer Class

The `ContentAnalyzer` class in `content_analyzer.py` connects to the OpenAI API to analyze text.

### Methods

- `analyze_content(text)`: Sends the input text to GPT-4o-mini for analysis and returns a dictionary with the following information:
    - `summary`: A brief summary of the text.
    - `sentiment`: The sentiment of the text (positive, neutral, or negative).
    - `key_points`: A list of three key points from the text.