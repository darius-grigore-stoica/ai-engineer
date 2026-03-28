import os
from pydantic import BaseModel # type: ignore
from google import genai
from dotenv import load_dotenv # type: ignore

load_dotenv()

class CodeReview(BaseModel):
    summary: str
    suggestions: list[str]
    critical_bugs: bool

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_INSTRUCTIONS = """
You are a Principal Software Engineer at a top-tier tech company. 
Your goal is to provide concise, brutal, but helpful code reviews.
Focus on:
1. Security vulnerabilities (OWASP Top 10).
2. Performance bottlenecks (Big O complexity).
3. Readability and Maintainability.
Always return valid JSON.
"""

def get_code_review(diff_text: str) -> CodeReview:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Review this diff: {diff_text}",
        config={
            'system_instruction': SYSTEM_INSTRUCTIONS,
            'response_mime_type': 'application/json',
            'response_schema': CodeReview,
        }
    )
    return response.parsed