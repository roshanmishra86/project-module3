import openai
import os
import json
import tiktoken

class ContentAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        openai.api_key = self.api_key
        self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")

    def _truncate_text(self, text: str, max_tokens: int = 120000) -> str:
        """Truncates the text to a maximum number of tokens."""
        tokens = self.encoding.encode(text)
        if len(tokens) > max_tokens:
            truncated_tokens = tokens[:max_tokens]
            return self.encoding.decode(truncated_tokens)
        return text

    def analyze_content(self, text: str) -> dict:
        try:
            truncated_text = self._truncate_text(text)
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content analyst. Analyze the following text and provide a JSON object with three keys: 'summary', 'sentiment' (which can be 'positive', 'neutral', or 'negative'), and 'key_points' (a list of three strings)."
                    },
                    {
                        "role": "user",
                        "content": truncated_text
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