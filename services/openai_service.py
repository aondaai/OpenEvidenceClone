import os
import json
import logging
from typing import Dict, Any
from openai import OpenAI

class OpenAIService:
    """Service for OpenAI integration for medical content processing"""
    
    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            logging.warning("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key) if api_key else None
    
    def generate_medical_summary(self, content: str, query_context: str = "") -> str:
        """
        Generate a medical summary of content relevant to the query
        
        Args:
            content: Medical content to summarize
            query_context: Original search query for context
            
        Returns:
            Medical summary with key clinical points
        """
        try:
            if not self.client:
                return "Summary unavailable - OpenAI service not configured"
            
            context_prompt = f" in relation to the medical query about '{query_context}'" if query_context else ""
            
            prompt = f"""As a medical AI assistant, provide a concise clinical summary of the following medical content{context_prompt}.

Focus on:
- Key clinical findings and evidence
- Diagnostic criteria or treatment recommendations
- Level of evidence and study quality
- Clinical relevance for healthcare professionals
- Any important contraindications or warnings

Medical content:
{content[:3000]}

Provide a clear, professional summary in 2-3 paragraphs suitable for healthcare professionals."""

            # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical AI assistant helping healthcare professionals understand clinical evidence. Provide accurate, evidence-based summaries."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            content = response.choices[0].message.content or "Summary unavailable"
            return content.strip() if isinstance(content, str) else "Summary unavailable"
            
        except Exception as e:
            logging.error(f"OpenAI summarization error: {str(e)}")
            return "Summary unavailable due to processing error"
    
    def assess_medical_credibility(self, source_info: Dict[str, Any]) -> str:
        """
        Assess the credibility of a medical source
        
        Args:
            source_info: Dictionary containing source information
            
        Returns:
            Credibility assessment string
        """
        try:
            if not self.client:
                return "Credibility assessment unavailable"
            
            url = source_info.get('url', '')
            title = source_info.get('title', '')
            source_type = source_info.get('source_type', '')
            
            prompt = f"""Assess the medical credibility of this source for healthcare professionals:

Title: {title}
URL: {url}
Source Type: {source_type}

Provide a credibility assessment considering:
- Source reputation in medical field
- Peer-review status
- Editorial standards
- Evidence level

Respond with JSON in this format:
{{"credibility_level": "High/Medium/Low", "confidence": 0.85, "reasoning": "Brief explanation"}}"""

            # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical information specialist assessing source credibility for healthcare professionals."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=200,
                temperature=0.2
            )
            
            content = response.choices[0].message.content
            if not content:
                return "Credibility assessment unavailable"
            result = json.loads(content)
            credibility_level = result.get('credibility_level', 'Unknown')
            confidence = result.get('confidence', 0.5)
            
            return f"{credibility_level} ({confidence:.1%} confidence)"
            
        except Exception as e:
            logging.error(f"OpenAI credibility assessment error: {str(e)}")
            return "Credibility assessment unavailable"
    
    def generate_clinical_questions(self, topic: str) -> list:
        """
        Generate relevant clinical questions for a medical topic
        
        Args:
            topic: Medical topic or condition
            
        Returns:
            List of relevant clinical questions
        """
        try:
            if not self.client:
                return []
            
            prompt = f"""Generate 5 relevant clinical questions that healthcare professionals commonly ask about {topic}.

Focus on:
- Diagnostic approaches
- Treatment options
- Risk factors
- Prognosis
- Management guidelines

Return only the questions, one per line."""

            # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical educator helping healthcare professionals formulate clinical questions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,
                temperature=0.4
            )
            
            content = response.choices[0].message.content
            if not content:
                return []
            questions = content.strip().split('\n')
            return [q.strip('- ').strip() for q in questions if q.strip()]
            
        except Exception as e:
            logging.error(f"OpenAI question generation error: {str(e)}")
            return []
