import streamlit as st
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

st.title("StudyMate AI - PDF Chat")
st.write("Upload a PDF and ask questions about it!")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # read the pdf
    reader = PyPDF2.PdfReader(uploaded_file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()

    st.success(f"PDF loaded! {len(reader.pages)} pages found.")

    user_question = st.text_input("Ask a question about your PDF:")
    ask_clicked = st.button("Ask AI")

    if ask_clicked:
        prompt = f"""You are a study assistant.
Use the following document to answer the question.

Document:
{pdf_text}

Question: {user_question}

Answer clearly and simply for a student."""

        with st.spinner("AI is thinking..."):
            response = client.chat.completions.create(
                model="openrouter/auto",
                messages=[{"role": "user", "content": prompt}]
            )
            st.write(response.choices[0].message.content)