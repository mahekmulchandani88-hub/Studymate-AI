from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

prompt = "Explain what photosynthesis is in 3 simple sentences for a student."
prompt = "What is machine learning? Explain in 2 lines."
prompt = "Give me 5 tips to study better."
prompt = "What is the capital of France? Also tell me one fun fact about it."
print("Sending your question to AI...")
print("-" * 40)

response = client.chat.completions.create(
    model="openrouter/auto",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print("AI says:")
print(response.choices[0].message.content)
print("-" * 40)
print("It worked! You just talked to AI using Python.")