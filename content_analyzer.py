import openai
import os
import json

class ContentAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        openai.api_key = self.api_key

    def analyze_content(self, text: str) -> str:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content analyst. Analyze the following text and provide a JSON object with three keys: 'summary', 'sentiment' (which can be 'positive', 'neutral', or 'negative'), and 'key_points' (a list of three strings)."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                response_format={"type": "json_object"}
            )
            analysis = json.loads(response.choices[0].message.content)
            return analysis
        except openai.APIError as e:
            return {"error": f"OpenAI API error: {e}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}