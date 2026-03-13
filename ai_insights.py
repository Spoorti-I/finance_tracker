"""
ai_insights.py — LLM-powered financial insights using Groq (FREE)
Get your free API key at: https://console.groq.com
"""

import os
import json
from groq import Groq


class FinanceAI:
    """Generates AI-driven insights from finance data using Groq (free LLM)."""

    MODEL = "llama-3.3-70b-versatile"  # Free model on Groq

    def __init__(self, api_key: str = None):
        key = api_key or os.getenv("GROQ_API_KEY")
        if not key:
            raise EnvironmentError("GROQ_API_KEY not set.")
        self.client = Groq(api_key=key)

    def get_insights(self, summary: dict, monthly: list) -> list:
        """Returns 4 plain-English insights about the user's finances."""
        prompt = f"""
You are a friendly, honest personal finance advisor.
Analyse this financial data and give exactly 4 short insights.
Each insight must be 1-2 sentences. Be specific, practical, and encouraging.
Use simple language no jargon. Respond ONLY as a valid JSON array of 4 strings.

DATA:
- Total Income:  Rs{summary['total_income']}
- Total Expense: Rs{summary['total_expense']}
- Balance:       Rs{summary['balance']}
- By Category:   {json.dumps(summary['by_category'])}
- Monthly Trend: {json.dumps(monthly)}

Example format:
["insight 1", "insight 2", "insight 3", "insight 4"]
"""
        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": "You are a concise personal finance advisor. Always respond in valid JSON only."},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0.7,
                max_tokens=500,
            )
            raw = response.choices[0].message.content.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()
            return json.loads(raw)
        except json.JSONDecodeError:
            return [response.choices[0].message.content]
        except Exception as e:
            return [f"Could not generate insights: {str(e)}"]

    def categorise_transaction(self, description: str) -> str:
        """Auto-suggests a spending category from a description."""
        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"Classify this into exactly one category from: "
                            f"Food, Transport, Rent, Utilities, Shopping, Health, "
                            f"Education, Entertainment, Other.\n"
                            f"Transaction: '{description}'\n"
                            f"Reply with just the category name. Nothing else."
                        ),
                    }
                ],
                max_tokens=10,
                temperature=0,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return "Other"

    def get_saving_tip(self, summary: dict) -> str:
        """Returns one specific saving tip based on top expense category."""
        if not summary["by_category"]:
            return ""
        expenses = [x for x in summary["by_category"] if x["type"] == "expense"]
        if not expenses:
            return ""
        top_cat = max(expenses, key=lambda x: x["total"])
        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"Give me one very specific, actionable tip to reduce spending on "
                            f"'{top_cat['category']}'. I spent Rs{top_cat['total']} on it. "
                            f"Keep it under 2 sentences. Be practical and friendly."
                        ),
                    }
                ],
                max_tokens=100,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return ""
