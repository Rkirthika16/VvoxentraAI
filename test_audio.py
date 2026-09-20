import streamlit as st
from audio_recorder_streamlit import audio_recorder

st.title("🎙️ VoxenAI Voice Test")

audio = audio_recorder(
    text="🎙️ Record",
    recording_color="#ff0000",
    neutral_color="#333333"
)

if audio:
    st.success("Recording received!")
    st.audio(audio, format="audio/wav")

    with open("test.wav", "wb") as f:
        f.write(audio)

    st.write("Audio saved as test.wav")