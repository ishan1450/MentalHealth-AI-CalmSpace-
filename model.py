import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# Set up the client for Groq
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",  # GROQ's OpenAI-compatible endpoint
)

def generate_response(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  
        messages = prompt,
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()
