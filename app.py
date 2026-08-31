import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY was not found in the .env file.")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)

# Create chat session with instructions
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="""
You are a helpful AI chatbot.

IMPORTANT:
- Remember and use the previous messages in the conversation.
- Understand follow-up questions based on the previous conversation.
- Resolve words such as "it", "its", "they", "them", "this", "that", and "those"
  using the previous conversation whenever possible.
- Do not ask the user to clarify something if the previous conversation already
  provides enough information.
- Give clear, accurate and helpful answers.
"""
    )
)

print("================================")
print("       GEMINI AI CHATBOT")
print("================================")
print("Type 'exit' to stop the chatbot.\n")

while True:
    user_message = input("You: ")

    if user_message.lower() == "exit":
        print("Chatbot: Goodbye! 👋")
        break

    try:
        response = chat.send_message(user_message)
        print("Chatbot:", response.text)
        print()

    except Exception as e:
        print("Chatbot: Sorry, something went wrong.")
        print("Error:", e)
        print()
