import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("No API key found. Please add GOOGLE_API_KEY=your_key to .env file.")
    exit()

# Configure Gemini
genai.configure(api_key=api_key)

# Use Gemini model
model = genai.GenerativeModel("models/gemini-2.5-flash")

prompt = """
Estimate CO₂ emissions for driving 10 km using a petrol car.
Return a JSON response like this:
{
  "emission": 0.0,
  "problem": "",
  "recommendation": "",
  "solution": ""
}
"""

try:
    response = model.generate_content(prompt)
    print("✅ Gemini Response:")
    print(response.text)
except Exception as e:
    print("❌ Gemini Error:", e)
