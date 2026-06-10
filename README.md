# 📚 StudyMate AI

> Your personal AI-powered study companion

🔗 **Live Demo:** [Click here to try](https://studymate-ai-wammmz9fpbwhmqqqtgrhz8.streamlit.app)  
🐙 **GitHub:** [mahekmulchandani88-hub/Studymate-AI](https://github.com/mahekmulchandani88-hub/Studymate-AI)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **PDF Chat** | Upload any PDF and ask questions — AI answers from your document |
| 🎥 **YouTube Summarizer** | Paste any YouTube link and get instant bullet point summary |
| 🗒️ **Notes Generator** | Auto-generate structured revision notes from any PDF |
| 🃏 **Flashcard Generator** | Create Q&A flashcards from your study material |
| ❓ **Quiz Generator** | Generate MCQ quiz with instant scoring from any PDF |
| 💡 **Topic Explainer** | Explain any topic in different styles and difficulty levels |
| 🧠 **Mind Map** | Visual concept breakdown of any topic with subtopics |

---

## 🛠️ Tech Stack

- **Python** — Core language
- **Streamlit** — Web UI framework
- **OpenRouter API** — Free open source AI models (Llama 3)
- **PyPDF2** — PDF text extraction
- **YouTube Transcript API** — Fetch video transcripts
- **python-dotenv** — Secure API key management

---

## 💡 Key Concepts

- **RAG (Retrieval Augmented Generation)** — PDF text injected into prompts so AI answers from your document
- **Prompt Engineering** — Different prompts for notes, flashcards, quiz, explanation
- **Session State** — Maintains quiz data between Streamlit reruns
- **API Integration** — Connects to OpenRouter to access open source LLMs

---

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/mahekmulchandani88-hub/Studymate-AI.git
cd Studymate-AI
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create `.env` file**
```
OPENROUTER_API_KEY=your_key_here
```
Get a free API key at [openrouter.ai](https://openrouter.ai)

**4. Run the app**
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
Studymate-AI/
├── app.py              # Main app — all 7 features
├── requirements.txt    # Python dependencies
├── .streamlit/
│   └── config.toml     # Dark theme config
└── .env                # API keys (not uploaded)
```

---

*Built with ❤️ using Python and Streamlit*