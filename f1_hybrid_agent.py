import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from duckduckgo_search import DDGS
import time

load_dotenv()

# Organ 1: Access API key
api_key = os.getenv("GEMINI_KEY")
client = genai.Client(api_key=api_key)

# Provide reference to the uploaded file
file_uri = "https://generativelanguage.googleapis.com/v1beta/files/tw1y8urmo5t7"

# Organ 2: Tools for the model to search the web (duckduckgo)
def search_internet(query: str):
    print(f"\n 🔎 Searching for {query} ...")
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=3))
    except Exception as e:
        return f"Error searching: {e}"

# Organ 3: Prompt to provide specific context to the model    
hybrid_persona = """
You are an F1 Team Principal AI.
1. You have access to the 2025 Sporting Regulations PDF. Always site Article number for rule questions.
2. You have access to a Search tool. Use it when the user asks questions about anything that is not covered in the PDF.
"""

# Organ 4: the model
chat = client.chats.create(
    model="gemini-flash-latest",
    config=types.GenerateContentConfig(
        tools=[search_internet],
        system_instruction=hybrid_persona,
        response_modalities=["TEXT"]
    ),
    history=[
        types.Content(
            role="user",
            parts=[types.Part.from_uri(file_uri=file_uri, mime_type="application/pdf")]
        ),
        types.Content(
            role="model",
            parts=[types.Part(text="Understood. I have the regulations and I am ready to search for live data.")]
        )
    ]
)

# Organ 5: Flow control and error handling
print(" 🏎️ Team Principal is online (type 'exit' or 'quit' to quit) ")
print("-"*50)

while True:
    user_input = input("You: ")
    if user_input in ["exit", "quit"]:
        break

    try:
        response = chat.send_message(user_input)
        if response.text:
            print(f"Principal: {response.text}")
        else:
            print("Principal: (No response, check logs)")

    except ClientError as e:
        print("Limit reached, cooling down for 30 seconds ...")
        time.sleep(35)
        print("Ready to go again")
    except Exception as e:
        print(f"Unexpected error occured: {e}")

    print("-"*50)