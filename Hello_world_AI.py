import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_KEY")

if not api_key:
    print("Error: API key not found. Check .env file")
else:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model = 'gemini-flash-latest',
        contents= "Write a haiku about coding."
    )
    print(response.text)