import streamlit as st
from audio_recorder_streamlit import audio_recorder

st.set_page_config(
    page_title="VoxenAI Voice Test",
    page_icon="🎙️"
)

st.title("🎙️ VoxenAI Voice Test")

st.write("Tamil 🇮🇳 / English Voice Recording")

audio = audio_recorder(
    text="🎙️ Record Voice",
    recording_color="#ff4b4b",
    neutral_color="#333333"
)

if audio:

    st.success("✅ Voice recorded successfully!")

    st.audio(
        audio,
        format="audio/wav"
    )

    with open("test.wav", "wb") as file:
        file.write(audio)

    st.success("✅ test.wav saved successfully!")

    st.info(
        "Now run: python whisper_module.py"
    )