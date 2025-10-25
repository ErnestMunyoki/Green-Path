import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class AIInsightsService:
    @staticmethod
    def generate_insight(activity_name: str, distance_km=0, vehicle_type="other"):
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

        for attempt in range(2):  # Retry once if parsing fails
            try:
                # ✅ Correct model name and version
                model = genai.GenerativeModel("models/gemini-2.5-flash")

                # Generate the AI insight
                response = model.generate_content(prompt)
                ai_text = response.text.strip()

                # Remove any Markdown code fences (```json ... ```)
                ai_text_clean = re.sub(r"^```json|```$", "", ai_text.strip(), flags=re.MULTILINE).strip()

                # Parse JSON from AI output
                data = json.loads(ai_text_clean)

                return {
                    "activity": activity_name,
                    "emission": float(data.get("emission", 0.0)),
                    "problem": data.get("problem", ""),
                    "recommendation": data.get("recommendation", ""),
                    "solution": data.get("solution", "")
                }

            except (json.JSONDecodeError, KeyError, ValueError):
                # Try to recover if JSON was malformed
                if attempt == 0:
                    continue  # Retry once

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
                # Catch any API or network errors
                print("⚠️ Gemini error:", e)
                return {
                    "activity": activity_name,
                    "emission": 0.0,
                    "problem": "Could not generate AI insight.",
                    "recommendation": "Try again later.",
                    "solution": "AI service temporarily unavailable."
                }
