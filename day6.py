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

st.title("StudyMate AI - PDF tools")
st.write("Upload a PDF and get notes or flashcards!")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # read the pdf
    reader = PyPDF2.PdfReader(uploaded_file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()

    st.success(f"PDF loaded! {len(reader.pages)} pages found.")
    col1,col2=st.columns(2)
    with col1:
        notes_clicked=st.button("Generate notes")
    with col2:
        flashcard_clicked=st.button("Generate Flashcard")    



    #user_question = st.text_input("Ask a question about your PDF:")
    #ask_clicked = st.button("Ask AI")

    if notes_clicked:
        prompt = f"""Create well-structured study notes from this document.
Format with clear headings and key points.
Make it easy for a student to revise from.

Document:
{pdf_text[:4000]}"""

        with st.spinner("Generating notes..."):
            response = client.chat.completions.create(
                model="openrouter/auto",
                messages=[{"role": "user", "content": prompt}]
            )
            st.write(response.choices[0].message.content)

    if flashcard_clicked:
        prompt = f"""Create 8 flashcards from this document.
Use exactly this format for each card:
Q: question here
A: answer here

Document:
{pdf_text[:4000]}"""

        with st.spinner("Generating flashcards..."):
            response = client.chat.completions.create(
                model="openrouter/auto",
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = response.choices[0].message.content
            cards = response_text.split("Q:")
            for card in cards[1:]:
                parts = card.split("A:")
                question = parts[0].strip()
                answer = parts[1].strip() if len(parts) > 1 else ""
                with st.expander(f"❓ {question}"):
                    st.write(f"**Answer:** {answer}")