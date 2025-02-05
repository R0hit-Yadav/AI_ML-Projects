import os
import yt_dlp
import subprocess
import streamlit as st
import ollama
import whisper # Import Whisper for transcription

# Streamlit UI
st.title("🎥 YouTube Video to Quiz Generator")
st.write("Enter a YouTube link to transcribe and generate a quiz.")

# Input for YouTube URL
youtube_url = st.text_input("Enter YouTube Video URL")

# Function to download audio
def download_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'video.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': r'C:/Users/Rohit/ffmpeg/bin'  # Provide the path to ffmpeg folder
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # Rename the extracted audio file
    for file in os.listdir():
        if file.endswith(".mp3"):
            return file
    return None

# Function to transcribe using Whisper (for speech-to-text)
def transcribe_audio(audio_file):
    st.write("🎤 Transcribing audio using Whisper...")

    # Load Whisper model
    model = whisper.load_model("base")  # You can choose "small", "medium", "large" for different accuracy/speed

    # Transcribe the audio
    result = model.transcribe(audio_file)
    
    transcript = result['text']
    return transcript

# Function to generate a quiz using Llama 3.2 via Ollama
def generate_quiz(transcript):
    st.write("🧠 Generating quiz questions...")

    response = ollama.chat(model="llama3.2", messages=[
        {"role": "system", "content": "Create 5 multiple-choice quiz questions from the following transcript."},
        {"role": "user", "content": transcript}
    ])

    quiz_text = response["message"]["content"]
    return quiz_text

# Process button
if st.button("Generate Quiz"):
    if youtube_url:
        st.write("🔄 Downloading audio...")
        audio_file = download_audio(youtube_url)
        
        if audio_file:
            transcript = transcribe_audio(audio_file)
            st.write("📝 Transcript:", transcript)

            quiz = generate_quiz(transcript)
            st.write("📚 Quiz Questions:")
            st.write(quiz)
        else:
            st.error("Failed to process the video.")
    else:
        st.warning("Please enter a valid YouTube URL.")
