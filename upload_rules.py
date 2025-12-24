import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_KEY")
client = genai.Client(api_key=api_key)

file_name = "rules.pdf"

print(f"Uploading {file_name} to Gemini")
try:
    rule_book = client.files.upload(file=file_name)
    print("Success! File uploaded")
    print(f"File name: {rule_book.name}")
    print(f"File URI: {rule_book.uri}")

except Exception as e:
    print(f"Error: {e}")