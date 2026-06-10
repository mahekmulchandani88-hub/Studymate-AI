from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# ─────────────────────────────────────────
# HELPER FUNCTION - ask_ai()
# We put the AI call inside a function so
# we can reuse it easily anywhere
# ─────────────────────────────────────────
def ask_ai(prompt):
    response = client.chat.completions.create(
        model="openrouter/auto",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# ─────────────────────────────────────────
# PART 1 - Different prompt styles
# Same topic, different instructions = different output
# ─────────────────────────────────────────
topic = "black holes"

print("=" * 50)
print("PART 1: Same topic, different prompts")
print("=" * 50)

# Prompt style 1 - Simple explanation
prompt1 = f"Explain {topic} in 2 simple sentences for a beginner."
print("\n[Simple explanation]")
print(ask_ai(prompt1))

# Prompt style 2 - Bullet points
prompt2 = f"Give me 5 key facts about {topic} in bullet points."
print("\n[Bullet points]")
print(ask_ai(prompt2))

# Prompt style 3 - Quiz question
prompt3 = f"Create 1 quiz question with 4 options (A B C D) about {topic}. Mark the correct answer."
print("\n[Quiz question]")
print(ask_ai(prompt3))


# ─────────────────────────────────────────
# PART 2 - User types their own question
# input() waits for the user to type something
# ─────────────────────────────────────────
print("\n" + "=" * 50)
print("PART 2: Ask your own question")
print("=" * 50)

user_question = input("\nType any topic or question: ")

# We build a prompt using what the user typed
# This is called "prompt engineering"
my_prompt = f"Explain '{user_question}' in simple language for a student. Keep it under 5 lines."

print("\nAI says:")
print("-" * 40)
print(ask_ai(my_prompt))
print("-" * 40)


# ─────────────────────────────────────────
# PART 3 - User picks what kind of answer
# ─────────────────────────────────────────
print("\n" + "=" * 50)
print("PART 3: Choose your answer style")
print("=" * 50)

topic2 = input("\nEnter a topic: ")
print("What kind of answer do you want?")
print("1. Simple explanation")
print("2. Bullet point summary")
print("3. Quiz question")

choice = input("Enter 1, 2 or 3: ")

if choice == "1":
    prompt = f"Explain {topic2} simply in 3 sentences for a beginner student."
elif choice == "2":
    prompt = f"Summarize {topic2} in 5 bullet points."
elif choice == "3":
    prompt = f"Create 1 MCQ quiz question with 4 options about {topic2}. Mark the correct answer."
else:
    prompt = f"Tell me something interesting about {topic2}."

print("\nAI says:")
print("-" * 40)
print(ask_ai(prompt))
print("-" * 40)
print("\nDay 2 complete! You now understand prompt engineering.")