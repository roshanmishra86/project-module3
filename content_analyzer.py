import openai
import os
import json
import tiktoken

class ContentAnalyzer:
    SYSTEM_PROMPT = """You are a senior business analyst with 20 years of experience in distilling complex information into actionable insights for executive leadership. Your analysis is sharp, concise, and always aligned with strategic business objectives. You are thorough, detail-oriented, and your insights are trusted to drive major corporate decisions. When you analyze content, you must strictly adhere to the provided JSON template, ensuring every field is populated accurately and professionally."""

    ANALYSIS_TEMPLATE = {
        "content_classification": {
            "type": "e.g., Financial Report, Customer Feedback, News Article",
            "industry": "e.g., Technology, Healthcare, Finance",
            "quality_score": "Rate from 1-10 (1=Poor, 10=Excellent)"
        },
        "key_insights": [
            {
                "finding": "Insight 1",
                "impact_level": "High | Medium | Low"
            },
            {
                "finding": "Insight 2",
                "impact_level": "High | Medium | Low"
            },
            {
                "finding": "Insight 3",
                "impact_level": "High | Medium | Low"
            }
        ],
        "sentiment_analysis": {
            "overall_sentiment": "Positive | Neutral | Negative",
            "confidence_score": "Score from 0.0 to 1.0"
        },
        "strategic_implications": {
            "opportunities": ["Opportunity 1", "Opportunity 2"],
            "risks": ["Risk 1", "Risk 2"]
        },
        "action_items": [
            {
                "item": "Action Item 1",
                "priority": "High | Medium | Low"
            },
            {
                "item": "Action Item 2",
                "priority": "High | Medium | Low"
            }
        ],
        "executive_summary": "A concise, high-level summary for a C-suite audience."
    }

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
                        "content": self.SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": f"Please analyze the following content and provide the output in a JSON object based on this template. Do not deviate from the structure of this template:\n\n{json.dumps(self.ANALYSIS_TEMPLATE, indent=2)}\n\nContent to Analyze:\n---_BEGIN_CONTENT---_\n{truncated_text}\n---_END_CONTENT---"
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            analysis = json.loads(response.choices[0].message.content)
            return analysis
        except openai.APIError as e:
            return {"error": f"OpenAI API error: {e}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}
