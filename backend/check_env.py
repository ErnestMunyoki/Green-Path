import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get key
key = os.getenv("OPENAI_API_KEY")
if key:
    print("OPENAI_API_KEY loaded:", key[:10] + "…")
else:
    print("OPENAI_API_KEY not found")
