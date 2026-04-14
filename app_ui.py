import streamlit as st
import os
import re
from faster_whisper import WhisperModel
from moviepy import VideoFileClip
import ollama
import time
import random

# -----------------------------
# UI Title
# -----------------------------
st.title("🎬 AI Video Summarizer")
st.write("Upload a video and get a smart summary using AI")

# -----------------------------
# Upload video
# -----------------------------
uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

# -----------------------------
# Extract Audio
# -----------------------------
def extract_audio(video_path, audio_path="audio.wav"):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, fps=16000)
    return audio_path

# -----------------------------
# Speech to Text
# -----------------------------
def speech_to_text(audio_path):
    model = WhisperModel("base", compute_type="int8")
    segments, _ = model.transcribe(audio_path)
    return " ".join([segment.text for segment in segments])

# -----------------------------
# Clean Text
# -----------------------------
def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9., ]', '', text)
    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if len(s.split()) > 6]
    return ". ".join(sentences[:12])

# -----------------------------
# Summarize (Ollama)
# -----------------------------
def summarize_text(text):
    prompt = f"""
Summarize the following text clearly in 2-3 sentences.

Important:
- Correct any obvious transcription errors (especially numbers like salaries).
- Ensure realistic values (e.g., 5-8 lakhs, 10-12 lakhs).
- Focus on the main idea and insights.

Text:
{text}
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']

# -----------------------------
# Main Button Logic
# -----------------------------
if uploaded_file is not None:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ Video uploaded!")
    st.video(uploaded_file)

    if st.button("🚀 Generate Summary"):

        progress = st.progress(0)
        status = st.empty()

        messages = [
            "🔊 Listening to your video...",
            "🧠 Understanding the content...",
            "✍️ Writing smart summary...",
            "🚀 Almost done..."
        ]

        # Step 1
        status.text(messages[0])
        audio = extract_audio("temp_video.mp4")
        progress.progress(25)

        # Step 2
        status.text(messages[1])
        transcript = speech_to_text(audio)
        progress.progress(50)

        # Step 3
        status.text(messages[2])
        cleaned = clean_text(transcript)
        summary = summarize_text(cleaned)
        progress.progress(75)

        # Step 4
        status.text(messages[3])
        time.sleep(1)
        progress.progress(100)

        status.text("✅ Done!")
        time.sleep(1)

        progress.empty()
        status.empty()
       
        st.subheader("📄 AI Summary")

        fun_messages = [
            "🤖 AI did its magic!",
            "⚡ That was fast, right?",
            "🧠 Brain power delivered!",
            "🎯 Summary ready, boss!",
            "🚀 Mission accomplished!",
            "✨ Here's your smart summary!",
            "🔥 AI cooked this perfectly!"
        ]

        fun_msg = random.choice(fun_messages)

        st.success(fun_msg + "\n\n" + summary)