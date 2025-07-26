import openai
import os
import json

class ContentAnalyzer:
    SYSTEM_PROMPT = """You are a senior business analyst with 20 years of experience in distilling complex information into actionable insights for executive leadership. Your analysis is sharp, concise, and always aligned with strategic business objectives. You are thorough, detail-oriented, and your insights are trusted to drive major corporate decisions. When you analyze content, you must strictly adhere to the provided JSON template, ensuring every field is populated accurately and professionally."""

    ANALYSIS_TEMPLATES = {
        "General Business": {
            "content_classification": {
                "type": "e.g., Financial Report, Customer Feedback, News Article",
                "industry": "e.g., Technology, Healthcare, Finance",
                "quality_score": "Rate from 1-10 (1=Poor, 10=Excellent)"
            },
            "key_insights": [
                {"finding": "Insight 1", "impact_level": "High | Medium | Low"},
                {"finding": "Insight 2", "impact_level": "High | Medium | Low"},
                {"finding": "Insight 3", "impact_level": "High | Medium | Low"}
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
                {"item": "Action Item 1", "priority": "High | Medium | Low"},
                {"item": "Action Item 2", "priority": "High | Medium | Low"}
            ],
            "executive_summary": "A concise, high-level summary for a C-suite audience."
        },
        "Competitive Intelligence": {
            "competitor_profile": {
                "name": "Competitor Name",
                "market_position": "e.g., Leader, Challenger, Niche Player"
            },
            "key_findings": [
                {"finding": "Key competitive advantage or disadvantage", "threat_level": "High | Medium | Low"},
                {"finding": "Recent strategic move or announcement", "threat_level": "High | Medium | Low"}
            ],
            "strategic_analysis": {
                "opportunities": ["Market gap to exploit", "Area for differentiation"],
                "threats": ["Direct competitive threat", "Potential market disruption"]
            },
            "recommendations": [
                {"action": "Recommended action to counter competitor", "priority": "High | Medium | Low"}
            ],
            "executive_summary": "A summary of the competitive landscape and strategic recommendations."
        },
        "Customer Feedback": {
            "feedback_classification": {
                "product_service": "Product/Service Name",
                "feedback_type": "e.g., Bug Report, Feature Request, Usability Issue"
            },
            "sentiment_analysis": {
                "overall_sentiment": "Positive | Neutral | Negative",
                "confidence_score": "Score from 0.0 to 1.0"
            },
            "key_themes": [
                {"theme": "Recurring pain point or compliment", "frequency": "High | Medium | Low"},
                {"theme": "Suggestion for improvement", "frequency": "High | Medium | Low"}
            ],
            "actionable_insights": [
                {"insight": "Specific, actionable insight from feedback", "priority": "High | Medium | Low"},
                {"insight": "Product/service improvement opportunity", "priority": "High | Medium | Low"}
            ],
            "executive_summary": "A summary of customer sentiment, key issues, and recommended actions."
        }
    }

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        openai.api_key = self.api_key

    def analyze_content(self, text: str, analysis_type: str = "General Business") -> dict:
        if analysis_type not in self.ANALYSIS_TEMPLATES:
            raise ValueError(f"Invalid analysis type: {analysis_type}")

        template = self.ANALYSIS_TEMPLATES[analysis_type]

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": self.SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": f"Please perform a '{analysis_type}' analysis on the following content. Provide the output in a JSON object based on this template. Do not deviate from the structure:\n\n{json.dumps(template, indent=2)}\n\nContent to Analyze:\n---_BEGIN_CONTENT---_\n{text}\n---_END_CONTENT---"
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