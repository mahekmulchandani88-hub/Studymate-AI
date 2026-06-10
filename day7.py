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

st.set_page_config(page_title="StudyMate AI - Quiz", page_icon="❓")
st.title("StudyMate AI - Quiz Generator")
st.write("Upload a PDF and test your knowledge!")

# session_state stops quiz from disappearing when submit is clicked
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # read the pdf (same as day 4)
    reader = PyPDF2.PdfReader(uploaded_file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()
    st.success(f"PDF loaded! {len(reader.pages)} pages found.")

    generate_clicked = st.button("🧠 Generate Quiz")

    if generate_clicked:
        prompt = f"""Create 5 multiple choice questions from this document.
Use EXACTLY this format:

Q1: Question here?
A) option one
B) option two
C) option three
D) option four
Answer: A

Q2: Next question?
A) option one
B) option two
C) option three
D) option four
Answer: B

Document:
{pdf_text[:4000]}"""

        with st.spinner("Generating quiz..."):
            response = client.chat.completions.create(
                model="openrouter/auto",
                messages=[{"role": "user", "content": prompt}]
            )
            quiz_text = response.choices[0].message.content

        # parse the quiz text into list of questions
        questions = []
        blocks = quiz_text.split("Q")
        for block in blocks[1:]:
            lines = block.strip().split("\n")
            lines = [l for l in lines if l.strip()]  # remove empty lines
            if not lines:
                continue
            question = lines[0].split(":", 1)[1].strip() if ":" in lines[0] else lines[0]
            options = {}
            correct = ""
            for line in lines[1:]:
                line = line.strip()
                if line.startswith("A)"):
                    options["A"] = line[2:].strip()
                elif line.startswith("B)"):
                    options["B"] = line[2:].strip()
                elif line.startswith("C)"):
                    options["C"] = line[2:].strip()
                elif line.startswith("D)"):
                    options["D"] = line[2:].strip()
                elif line.startswith("Answer:"):
                    correct = line.split(":")[1].strip()
            if question and options:
                questions.append({
                    "question": question,
                    "options": options,
                    "correct": correct
                })

        st.session_state.quiz_data = questions
        st.session_state.user_answers = {}

    # show quiz if it exists
    if st.session_state.quiz_data:
        st.divider()
        st.subheader("📝 Answer the questions:")

        for i, q in enumerate(st.session_state.quiz_data):
            st.write(f"**Q{i+1}: {q['question']}**")
            options_list = [f"{k}) {v}" for k, v in q['options'].items()]
            answer = st.radio("Select answer:", options_list, key=f"q{i}")
            st.session_state.user_answers[i] = answer[0]  # store A/B/C/D
            st.write("")  # small gap between questions

        st.divider()
        submit_clicked = st.button("✅ Submit Quiz")

        if submit_clicked:
            score = 0
            for i, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state.user_answers.get(i)
                correct_ans = q['correct']
                if user_ans == correct_ans:
                    score += 1
                    st.success(f"Q{i+1}: ✅ Correct!")
                else:
                    st.error(f"Q{i+1}: ❌ Wrong! Correct answer was {correct_ans})")

            st.divider()
            total = len(st.session_state.quiz_data)
            st.subheader(f"🎯 Your Score: {score} / {total}")

            if score == total:
                st.balloons()
                st.success("Perfect score! Outstanding! 🏆")
            elif score >= total * 0.6:
                st.success("Good job! Keep studying! 💪")
            else:
                st.warning("Keep practicing! You'll get better! 📚")