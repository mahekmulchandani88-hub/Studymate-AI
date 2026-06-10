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

st.title("StudyMate AI - Youtube Summary")
st.write("Upload a youtube video and gets its summary!")
youtube_link = st.text_input("Paste YouTube link:")
summarize_clicked = st.button("Summarize")
if summarize_clicked and youtube_link:
    if "v=" in youtube_link:
        video_id = youtube_link.split("v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_link:
        video_id = youtube_link.split("youtu.be/")[1].split("?")[0]
    else:
        st.error("Invalid YouTube link. Please paste a proper YouTube URL.")
        st.stop()
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    full_text = " ".join([item.text for item in transcript])

    prompt = f"""Summarize this YouTube video transcript for a student.
Give a 5 bullet point summary and 3 key takeaways.

Transcript:
{full_text[:4000]}"""

    with st.spinner("AI is thinking..."):
        response = client.chat.completions.create(
            model="openrouter/auto",
            messages=[{"role": "user", "content": prompt}]
        )
        st.write(response.choices[0].message.content)