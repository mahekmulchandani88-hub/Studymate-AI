from youtube_transcript_api import YouTubeTranscriptApi
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

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="wide"
)

# ── LANDING PAGE ──────────────────────────────
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; font-size:3.5rem;'>📚 StudyMate AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.2rem; color:gray;'>Your personal AI-powered study companion</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    #col1, col2, col3, col4 = st.columns(4)
    #col1.metric("Features", "6")
    #col2.metric("PDF Support", "✅")
    #col3.metric("YouTube", "✅")
    #col4.metric("100% Free", "✅")

    #st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🚀 Let's Get Started", use_container_width=True):
            st.session_state.started = True
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    st.markdown("<h3 style='text-align:center;'>Everything you need to study smarter</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📄 **PDF Chat**\n\nUpload any PDF and ask questions. AI answers based on your document.")
    with col2:
        st.info("🎥 **YouTube Summarizer**\n\nPaste any YouTube link and get a bullet point summary instantly.")
    with col3:
        st.info("🗒️ **Smart Notes**\n\nAuto-generate structured revision notes from any PDF in seconds.")

    st.markdown("<br>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.success("🃏 **Flashcards**\n\nGenerate Q&A flashcards from your study material instantly.")
    with col5:
        st.success("❓ **Quiz Generator**\n\nCreate MCQ quizzes with scoring from any uploaded PDF.")
    with col6:
        st.success("🧠 **Mind Map**\n\nVisual concept breakdown of any topic with subtopics.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    st.markdown("<h3 style='text-align:center;'>How it works</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.warning("**Step 1 — Upload** 📤\n\nUpload your PDF or paste a YouTube link")
    with col2:
        st.warning("**Step 2 — Choose** 🎯\n\nPick what you want — notes, quiz, flashcards or summary")
    with col3:
        st.warning("**Step 3 — Learn** 🎓\n\nGet instant AI-powered study material")

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<p style='text-align:center; color:gray;'>Built with Python · Streamlit · Open Source AI</p>", unsafe_allow_html=True)
    st.stop()

# ── SIDEBAR ───────────────────────────────────
with st.sidebar:
    st.markdown("# 📚 StudyMate AI")
    st.markdown("*Your AI study companion*")
    st.divider()
    st.markdown("**✨ Features**")
    st.markdown("📄 PDF Chat")
    st.markdown("🎥 YouTube Summary")
    st.markdown("🗒️ Notes & Flashcards")
    st.markdown("❓ Quiz Generator")
    st.markdown("💡 Topic Explainer")
    st.markdown("🧠 Mind Map")
    st.divider()
    st.markdown("*Built with Python + Streamlit*")
    st.markdown("*Powered by Open Source AI*")
    if st.button("🏠 Back to Home"):
        st.session_state.started = False
        st.rerun()

# ── TABS ──────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 PDF Chat",
    "🎥 YouTube Summarizer",
    "🗒️ Notes & Flashcards",
    "❓ Quiz",
    "💡 Topic Explainer",
    "🧠 Mind Map"
])

# ── TAB 1 - PDF CHAT ──────────────────────────
with tab1:
    
    st.title("📄 PDF Chat")
    st.write("Upload a PDF and ask questions about it!")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf", key="pdf_chat")

    if uploaded_file is not None:
        reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()
        st.success(f"✅ PDF loaded! {len(reader.pages)} pages found.")

        user_question = st.text_input("Ask a question about your PDF:")
        ask_clicked = st.button("🤖 Ask AI", key="ask_pdf")

        if ask_clicked and user_question:
            prompt = f"""You are a study assistant.
Use the following document to answer the question.

Document:
{pdf_text[:4000]}

Question: {user_question}

Answer clearly and simply for a student."""

            with st.spinner("AI is thinking..."):
                response = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.divider()
                st.subheader("💬 Answer")
                st.write(response.choices[0].message.content)

# ── TAB 2 - YOUTUBE ───────────────────────────
with tab2:
    
    st.title("🎥 YouTube Summarizer")
    st.write("Paste any YouTube link and get an instant AI summary!")

    youtube_link = st.text_input("Paste YouTube link:")
    summarize_clicked = st.button("▶️ Summarize Video", key="summarize_yt")

    if summarize_clicked and youtube_link:
        if "v=" in youtube_link:
            video_id = youtube_link.split("v=")[1].split("&")[0]
        elif "youtu.be/" in youtube_link:
            video_id = youtube_link.split("youtu.be/")[1].split("?")[0]
        else:
            st.error("❌ Invalid YouTube link. Please paste a proper YouTube URL.")
            st.stop()

        try:
            ytt_api = YouTubeTranscriptApi()
            transcript = ytt_api.fetch(video_id)
            full_text = " ".join([item.text for item in transcript])

            prompt = f"""Summarize this YouTube video transcript for a student.
Give a 5 bullet point summary and 3 key takeaways.

Transcript:
{full_text[:4000]}"""

            with st.spinner("Summarizing video..."):
                response = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.divider()
                st.subheader("📋 Summary")
                st.write(response.choices[0].message.content)
        except Exception as e:
            st.error("❌ Could not fetch transcript. Try a different video.")

# ── TAB 3 - NOTES & FLASHCARDS ────────────────
with tab3:
   
    st.title("🗒️ Notes & Flashcards")
    st.write("Upload a PDF and get notes or flashcards!")

    uploaded_file3 = st.file_uploader("Upload a PDF", type="pdf", key="pdf_tools")

    if uploaded_file3 is not None:
        reader = PyPDF2.PdfReader(uploaded_file3)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()
        st.success(f"✅ PDF loaded! {len(reader.pages)} pages found.")

        col1, col2 = st.columns(2)
        with col1:
            notes_clicked = st.button("📝 Generate Notes", key="notes_btn", use_container_width=True)
        with col2:
            cards_clicked = st.button("🃏 Generate Flashcards", key="cards_btn", use_container_width=True)

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
                st.divider()
                st.subheader("📝 Study Notes")
                st.write(response.choices[0].message.content)

        if cards_clicked:
            prompt = f"""Create 8 flashcards from this document.
Use exactly this format:
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
                st.divider()
                st.subheader("🃏 Flashcards — click to reveal answer")
                cards = response_text.split("Q:")
                for card in cards[1:]:
                    parts = card.split("A:")
                    question = parts[0].strip()
                    answer = parts[1].strip() if len(parts) > 1 else ""
                    with st.expander(f"❓ {question}"):
                        st.success(f"✅ **Answer:** {answer}")

# ── TAB 4 - QUIZ ──────────────────────────────
with tab4:
    
    st.title("❓ Quiz Generator")
    st.write("Upload a PDF and test your knowledge!")

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    uploaded_file4 = st.file_uploader("Upload a PDF", type="pdf", key="pdf_quiz")

    if uploaded_file4 is not None:
        reader = PyPDF2.PdfReader(uploaded_file4)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()
        st.success(f"✅ PDF loaded! {len(reader.pages)} pages found.")

        if st.button("🎯 Generate Quiz", key="gen_quiz", use_container_width=True):
            prompt = f"""Create 5 multiple choice questions from this document.
Use EXACTLY this format:

Q1: Question here?
A) option one
B) option two
C) option three
D) option four
Answer: A

Document:
{pdf_text[:4000]}"""

            with st.spinner("Generating quiz..."):
                response = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=[{"role": "user", "content": prompt}]
                )
                quiz_text = response.choices[0].message.content

            questions = []
            blocks = quiz_text.split("Q")
            for block in blocks[1:]:
                lines = block.strip().split("\n")
                lines = [l for l in lines if l.strip()]
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

        if st.session_state.quiz_data:
            st.divider()
            st.subheader("📝 Answer all questions then submit:")
            for i, q in enumerate(st.session_state.quiz_data):
                st.info(f"**Q{i+1}: {q['question']}**")
                options_list = [f"{k}) {v}" for k, v in q['options'].items()]
                answer = st.radio("", options_list, key=f"q{i}")
                st.session_state.user_answers[i] = answer[0]
                st.write("")

            if st.button("✅ Submit Quiz", key="submit_quiz", use_container_width=True):
                score = 0
                st.divider()
                st.subheader("📊 Results")
                for i, q in enumerate(st.session_state.quiz_data):
                    if st.session_state.user_answers.get(i) == q['correct']:
                        score += 1
                        st.success(f"Q{i+1}: ✅ Correct!")
                    else:
                        st.error(f"Q{i+1}: ❌ Wrong! Correct answer was {q['correct']}")
                st.divider()
                total = len(st.session_state.quiz_data)
                col1, col2 = st.columns(2)
                col1.metric("Your Score", f"{score} / {total}")
                col2.metric("Percentage", f"{int(score/total*100)}%")
                if score == total:
                    st.balloons()
                    st.success("🏆 Perfect score! Outstanding!")
                elif score >= total * 0.6:
                    st.success("💪 Good job! Keep studying.")
                else:
                    st.warning("📚 Keep practicing! You'll get better.")

# ── TAB 5 - TOPIC EXPLAINER ───────────────────
with tab5:
    #col1, col2, col3 = st.columns(3)
    #col1.metric("Input", "Any Topic")
    #col2.metric("Styles", "4 Options")
    #col3.metric("Levels", "3 Options")
    #st.divider()
    st.title("💡 Topic Explainer")
    st.write("Type any topic and get a clear explanation!")

    topic = st.text_input("Enter a topic:", key="explain_topic_input",
                          placeholder="e.g. Machine Learning, Photosynthesis, Gravity...")

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("How do you want it explained?", [
            "Simple (like I'm 10 years old)",
            "Detailed (in depth explanation)",
            "Analogy (using a real life example)",
            "Bullet Points (key facts only)"
        ])
    with col2:
        level = st.selectbox("Your level:", [
            "School student",
            "College student",
            "Professional"
        ])

    explain_clicked = st.button("💡 Explain It", key="explain_btn", use_container_width=True)

    if explain_clicked and topic:
        prompt = f"""Explain the topic '{topic}' to a {level}.
Style: {style}

Give a clear engaging explanation.
End with 2-3 follow-up topics they should learn next."""

        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="openrouter/auto",
                messages=[{"role": "user", "content": prompt}]
            )
            st.divider()
            st.subheader(f"📖 {topic}")
            st.write(response.choices[0].message.content)

# ── TAB 6 - MIND MAP ──────────────────────────
with tab6:
    #col1, col2, col3 = st.columns(3)
    #col1.metric("Input", "Any Topic")
    #col2.metric("Output", "Visual Tree")
    #col3.metric("Depth", "2 Levels")
    #st.divider()
    st.title("🧠 Mind Map Generator")
    st.write("Type any topic and get a visual concept breakdown!")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Enter a topic:", key="mindmap_topic",
                              placeholder="e.g. Python, World War 2, Calculus...")
    with col2:
        depth = st.selectbox("Detail level:", [
            "Basic (5 main concepts)",
            "Detailed (10 concepts with subtopics)",
        ])

    map_clicked = st.button("🧠 Generate Mind Map", key="mindmap_btn", use_container_width=True)

    if map_clicked and topic:
        prompt = f"""Create a detailed mind map for the topic '{topic}'.
{depth}

Use EXACTLY this tree format with proper box structure:

╔══════════════════════════╗
║  🎯 {topic}              ║
╚══════════════════════════╝
         │
    ┌────┴────┐
    │         │
┌───▼───┐  ┌──▼────┐
│ Main 1│  │ Main 2│
└───┬───┘  └──┬────┘
    │          │
 ┌──▼──┐   ┌──▼──┐
 │Sub 1│   │Sub 2│
 └─────┘   └─────┘

But use text tree format like this instead:

🎯 {topic}
│
├── 📌 [Main Concept 1]
│   ├── ▸ [Sub point 1]
│   ├── ▸ [Sub point 2]
│   └── ▸ [Sub point 3]
│
├── 📌 [Main Concept 2]
│   ├── ▸ [Sub point 1]
│   ├── ▸ [Sub point 2]
│   └── ▸ [Sub point 3]
│
├── 📌 [Main Concept 3]
│   ├── ▸ [Sub point 1]
│   └── ▸ [Sub point 2]
│
└── 📌 [Main Concept 4]
    ├── ▸ [Sub point 1]
    └── ▸ [Sub point 2]

Make it educational and detailed for a student studying '{topic}'."""

        with st.spinner("Building mind map..."):
            response = client.chat.completions.create(
                model="openrouter/auto",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content

        st.divider()

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader(f"🧠 Mind Map: {topic}")
            lines = result.strip().split("\n")
            for line in lines:
                if "🎯" in line:
                    st.markdown(f"### {line.strip()}")
                elif "📌" in line:
                    st.markdown(f"**{line.strip()}**")
                elif "▸" in line:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;• {line.strip().replace('▸', '').strip()}", unsafe_allow_html=True)
                elif line.strip():
                    st.markdown(f"{line.strip()}")

        with col2:
            st.subheader("📚 Learn Next")
            followup_prompt = f"""List 6 related topics to learn after '{topic}'.
Format exactly like this:
1. Topic name — one line reason why
2. Topic name — one line reason why
...and so on"""
            with st.spinner("Finding related topics..."):
                followup = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=[{"role": "user", "content": followup_prompt}]
                )
                st.info(followup.choices[0].message.content)

        st.divider()
        st.subheader("💡 Quick Explanation")
        explain_prompt = f"Give a 3 sentence overview of '{topic}' for a student who just saw this mind map."
        with st.spinner("Generating overview..."):
            explain = client.chat.completions.create(
                model="openrouter/auto",
                messages=[{"role": "user", "content": explain_prompt}]
            )
            st.write(explain.choices[0].message.content)