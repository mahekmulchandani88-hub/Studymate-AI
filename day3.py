import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

st.title("StudyMate AI")
st.write("Your ultimate AI study companion!")

topic = st.text_input("Enter a topic to learn about:")
explain_clicked = st.button("Explain It")

if explain_clicked:
    with st.spinner("AI is thinking..."):
        prompt = f"Explain {topic} in simple language for a student in 3 sentences."
        response = client.chat.completions.create(
            model="openrouter/auto",
            messages=[{"role": "user", "content": prompt}]
        )
        st.write(response.choices[0].message.content)