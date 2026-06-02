import os
from google import genai

# Using your verified working token format
MY_KEY = "paste_API_key_here"

print("📡 Attempting connection to Gemini...")
client = genai.Client(api_key=MY_KEY)

try:
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents='Hello world',
    )
    print("🟢 SUCCESS! Your AI Studio Key is active.")
    print(f"🤖 Gemini Response: {response.text}")

except Exception as e:
    print("🔴 CONNECTION FAILED.")
    print(f"Error Details: {e}")