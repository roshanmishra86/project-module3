import openai
import os
import json
import tiktoken
import time
from datetime import datetime

class ContentAnalyzer:
    def batch_analyze(self, docs, analysis_type="General Business", progress_callback=None):
        """
        Batch process multiple documents with progress tracking, rate limiting, and error handling.
        Args:
            docs (list of dict): Each dict should have at least 'id' and 'content' keys.
            analysis_type (str): Type of analysis to perform.
            progress_callback (callable): Function accepting (progress: float, status: str).
        Returns:
            list of dict: Each result includes 'id', 'timestamp', 'result', and 'error' if any.
        """
        results = []
        total = len(docs)
        for idx, doc in enumerate(docs):
            doc_id = doc.get('id', f'doc_{idx}')
            content = doc.get('content', '')
            timestamp = datetime.utcnow().isoformat()
            status = f"Analyzing {doc_id} ({idx+1}/{total})"
            if progress_callback:
                progress_callback(idx / total, status)
            try:
                analysis_result, input_tokens, output_tokens = self.analyze_content(content, analysis_type)
                result = {
                    'id': doc_id,
                    'timestamp': timestamp,
                    'result': analysis_result,
                    'input_tokens': input_tokens,
                    'output_tokens': output_tokens,
                    'error': None
                }
            except Exception as e:
                result = {
                    'id': doc_id,
                    'timestamp': timestamp,
                    'result': None,
                    'input_tokens': None,
                    'output_tokens': None,
                    'error': str(e)
                }
            results.append(result)
            time.sleep(0.5)  # Rate limiting
            if progress_callback:
                progress_callback((idx+1) / total, f"Completed {doc_id}")
        if progress_callback:
            progress_callback(1.0, "Batch analysis complete.")
        return results
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
            messages = [
                {
                    "role": "system",
                    "content": self.SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"Please perform a '{analysis_type}' analysis on the following content. Provide the output in a JSON object based on this template. Do not deviate from the structure:\n\n{json.dumps(template, indent=2)}\n\nContent to Analyze:\n---_BEGIN_CONTENT---_\n{text}\n---_END_CONTENT---"
                }
            ]
            
            # Calculate input tokens
            encoding = tiktoken.encoding_for_model("gpt-4o-mini")
            input_tokens_used = sum(len(encoding.encode(m["content"])) for m in messages)

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            analysis = json.loads(response.choices[0].message.content)
            
            # Calculate output tokens
            output_tokens_used = len(encoding.encode(response.choices[0].message.content))
            
            return analysis, input_tokens_used, output_tokens_used
        except openai.APIError as e:
            return {"error": f"OpenAI API error: {e}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}