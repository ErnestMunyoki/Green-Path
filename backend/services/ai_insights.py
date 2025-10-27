import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Google Generative AI client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class AIInsightsService:
    @staticmethod
    def generate_insight(activity_name: str, distance_km: float = 0, vehicle_type: str = "other"):
        """
        Generate sustainability insights for a given activity using Google Gemini AI.
        Returns a dictionary with keys: activity, emission, problem, recommendation, solution
        """

        prompt = f"""
        You are a sustainability assistant.

        Return a JSON object exactly like this (and nothing else):

        {{
            "emission": 0.0,
            "problem": "",
            "recommendation": "",
            "solution": ""
        }}

        Activity: {activity_name}
        Distance: {distance_km} km
        Vehicle Type: {vehicle_type}
        """

        for attempt in range(2):
            try:
                # Use the latest Gemini model
                model = genai.GenerativeModel("models/gemini-2.5-flash")
                response = model.generate_content(prompt)
                ai_text = response.text.strip()

                # Remove markdown code blocks if present
                ai_text_clean = re.sub(r"^```json|```$", "", ai_text.strip(), flags=re.MULTILINE).strip()

                # Parse JSON
                data = json.loads(ai_text_clean)

                return {
                    "activity": activity_name,
                    "emission": float(data.get("emission", 0.0)),
                    "problem": data.get("problem", ""),
                    "recommendation": data.get("recommendation", ""),
                    "solution": data.get("solution", "")
                }

            except (json.JSONDecodeError, KeyError, ValueError):
                # Retry once
                if attempt == 0:
                    continue

                # Fallback parsing for emission
                emission_match = re.search(r"(\d+(\.\d+)?)\s*kg", ai_text)
                emission_value = float(emission_match.group(1)) if emission_match else 0.0
                return {
                    "activity": activity_name,
                    "emission": emission_value,
                    "problem": ai_text,
                    "recommendation": "Follow the advice above.",
                    "solution": "Keep improving your sustainability habits!"
                }

            except Exception as e:
                # Catch-all fallback
                print("⚠️ Gemini error:", e)
                return {
                    "activity": activity_name,
                    "emission": 0.0,
                    "problem": "Could not generate AI insight.",
                    "recommendation": "Try again later.",
                    "solution": "AI service temporarily unavailable."
                }
