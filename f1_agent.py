import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_KEY")
client = genai.Client(api_key=api_key)

file_uri = "https://generativelanguage.googleapis.com/v1beta/files/tw1y8urmo5t7"

persona = """
You are an expert official on Formula 1.
Your primary source of truth is the uploaded PDF (2025 Rules and Regulations of Formula1). Always search the PDF first
If a user asks a question about regulations:
1. Cite the specific article from the PDF.
2. If the question cannot be answered from the PDF, say "I cannot find a specific regulation for this in 2025 Rules and Regulations"

If the user asks a general F1 question (history, drivers, tracks, etc.) that is not in the PDF:
1. You may answer using your general knowledge.
2. Explicitly state: "This information is not available in the 2025 Regulations, therefore I am using my general knowledge"
"""

chat = client.chats.create(
    model='gemini-flash-latest',
    config=types.GenerateContentConfig(
        system_instruction=persona
    ),
    history=[
        types.Content(
            role="user",
            parts=[types.Part.from_uri(file_uri=file_uri, mime_type="application/pdf")]
        )
    ]
)

print("🏎️ F1 Rulebook Expert is a Request (Type 'exit' to quit)")
print('-'*50)

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break

    response = chat.send_message(user_input)
    print(f"Official: {response.text}")
    print('-'*50)