import json
import requests
import time

API_KEY = "AIzaSyBoLwUnBbEro4lmnNLoUp7KUrIYQ8jQbzQ"  
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
GEMINI_API_PREDICT_URL = f"{GEMINI_API_URL}?key={API_KEY}"


class EcotrackAIService:
    
    @staticmethod
    def _make_api_call(payload):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    GEMINI_API_PREDICT_URL,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(payload),
                    timeout=30
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  
                else:
                    return {"error": f"Failed to connect to AI service: {e}"}
            except Exception as e:
                return {"error": f"An unexpected error occurred: {e}"}
        return {"error": "API call exhausted all retries."}

    @staticmethod
    def get_insights(emissions_data):
        data_string = json.dumps(emissions_data, indent=2)
        system_instruction = (
            "You are EcoBot, a friendly and motivational sustainability assistant. "
            "Analyze the provided weekly emissions data. Identify the highest and lowest emission days "
            "and activities. Provide a concise, single-paragraph summary (under 80 words) "
            "and offer one actionable, encouraging tip for the user to reduce their carbon footprint next week."
        )
        user_query = f"Analyze the following weekly CO2 emissions data (in kg) and activity log:\n\n{data_string}"
        payload = {
            "contents": [{"parts": [{"text": user_query}]}],
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "tools": [{"google_search": {}}]
        }
        result = EcotrackAIService._make_api_call(payload)
        if "error" in result:
            return None, result["error"]
        try:
            insight_text = result['candidates'][0]['content']['parts'][0]['text']
            return insight_text, None
        except (KeyError, IndexError) as e:
            return None, f"Could not parse AI response structure for insights: {e}"

    @staticmethod
    def predict_next_7_days(emissions_data):
        data_string = json.dumps(emissions_data, indent=2)
        system_instruction = (
            "Based on the provided weekly CO2 emission history, predict the CO2 emission (in kg, as a float, rounded to one decimal place) "
            "for the next 7 consecutive days. Do not include any textual explanation, introduction, or conclusion outside of the JSON block."
        )
        user_query = f"Predict the next 7 days of emissions (in kg) based on this history:\n\n{data_string}"
        prediction_schema = {
            "type": "OBJECT",
            "properties": {
                "total_predicted_emissions": {
                    "type": "NUMBER",
                    "description": "The sum of all seven daily predictions, rounded to one decimal place."
                },
                "daily_predictions": {
                    "type": "ARRAY",
                    "description": "A list of predicted emissions for 7 days.",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "day": {"type": "STRING", "description": "Generic day label (e.g., Day 1, Day 2, etc.)"},
                            "emission": {"type": "NUMBER", "description": "Predicted CO2 emission in kg, rounded to one decimal place."}
                        },
                        "required": ["day", "emission"]
                    }
                }
            },
            "required": ["total_predicted_emissions", "daily_predictions"]
        }
        payload = {
            "contents": [{"parts": [{"text": user_query}]}],
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": prediction_schema
            }
        }
        result = EcotrackAIService._make_api_call(payload)
        if "error" in result:
            return result
        try:
            json_string = result['candidates'][0]['content']['parts'][0]['text']
            return json.loads(json_string)
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            return {"error": f"Could not parse or decode structured AI response: {e}"}
