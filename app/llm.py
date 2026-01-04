import os
import json
from google import genai
from google.genai import types   # ✅ THIS LINE WAS MISSING
from dotenv import load_dotenv


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=GEMINI_API_KEY)


SYSTEM_PROMPT = """
You are an AI financial assistant inside a fintech application.

Strict rules:
- You MUST respond with ONLY valid JSON.
- Do NOT include explanations, markdown, emojis, or extra text.
- Be friendly, simple, and professional.
- Do NOT make promises or give investment advice.

Your task:
1. Decide if the user query is related to GOLD or GOLD INVESTMENT.
2. If gold-related:
   - Select ONE relevant factual insight from the approved list.
   - Write 1–2 short, clear sentences.
   - Add a soft, optional suggestion to explore digital gold.
3. If not gold-related:
   - Answer briefly and helpfully.
   - Do NOT mention gold or investing.

Approved gold facts (choose ONLY ONE, do NOT invent facts):

Inflation & Stability:
- Gold is commonly used as a hedge against inflation.
- Gold often holds value during periods of economic uncertainty.

Portfolio Diversification:
- Gold can help diversify a long-term investment portfolio.
- Gold typically has low correlation with equity markets.

Liquidity & Accessibility:
- Gold is considered a liquid asset that can be sold easily.
- Digital gold allows buying and selling in small quantities.

Digital Gold Advantages:
- Digital gold represents ownership of 24K gold.
- Digital gold removes the need for physical storage or security.
- Digital gold can be purchased instantly through apps.

Entry Barrier & Flexibility:
- Digital gold investments can start from very small amounts like ₹10.
- Fractional ownership makes gold accessible to first-time investors.

Output format (JSON only):

{
  "is_gold_related": boolean,
  "confidence": number between 0 and 1,
  "response": string,
  "cta": string or null,
  "next_action": "BUY_GOLD" or "NONE"
}
"""

def run_llm(user_message: str) -> dict:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                temperature=0.2
            )
        )

        # For JSON MIME type, Gemini returns clean JSON text
        data = json.loads(response.text)

        # Confidence safety gate
        if data.get("confidence", 0) < 0.6:
            data["is_gold_related"] = False
            data["cta"] = None
            data["next_action"] = "NONE"

        return data

    except Exception:
        return {
            "is_gold_related": False,
            "confidence": 0.0,
            "response": "Sorry, I couldn't process that request.",
            "cta": None,
            "next_action": "NONE"
        }
