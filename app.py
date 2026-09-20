import os
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import whisper
import imageio_ffmpeg

from nlp_module import preprocess_text
from classifier import classify_complaint


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="VoxenAI",
    page_icon="🤖",
    layout="wide"
)


# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f4f7fb;
}

.header {
    background: linear-gradient(135deg, #123c69, #1f6aa5);
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
}

.header h1 {
    font-size: 42px;
    margin: 0;
}

.header p {
    font-size: 17px;
}

.section {
    background: white;
    padding: 25px;
    border-radius: 16px;
    margin-bottom: 20px;
    border: 1px solid #e1e5eb;
}

.section-title {
    color: #123c69;
    font-size: 25px;
    font-weight: 700;
    margin-bottom: 15px;
}

.footer {
    text-align: center;
    color: #777;
    padding: 30px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# FFMPEG
# ==========================================================

try:
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    os.environ["PATH"] = (
        os.path.dirname(ffmpeg_path)
        + os.pathsep
        + os.environ["PATH"]
    )

except Exception as e:
    st.error("FFmpeg runtime could not be loaded.")
    st.exception(e)


# ==========================================================
# WHISPER
# ==========================================================

@st.cache_resource
def load_whisper_model():

    return whisper.load_model("base")


# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div class="header">

<h1>🤖 VoxenAI</h1>

<p>AI-Powered Citizen Complaint Management System</p>

<p>🇮🇳 Tamil &nbsp; | &nbsp; 🇬🇧 English &nbsp; | &nbsp; 🎙️ Voice AI</p>

</div>
""", unsafe_allow_html=True)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("🤖 VoxenAI")

    page = st.radio(
        "Navigation",
        [
            "📝 Submit Complaint",
            "📊 Admin Dashboard"
        ]
    )

    st.divider()

    st.write("### Languages")

    st.write("🇮🇳 Tamil")
    st.write("🇬🇧 English")
    st.write("🔤 Tanglish")

    st.divider()

    st.caption(
        "Offline-first prototype"
    )


# ==========================================================
# SUBMIT COMPLAINT
# ==========================================================

if page == "📝 Submit Complaint":

    st.markdown(
        '<div class="section-title">🎙️ Voice Complaint</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Speak your complaint in Tamil or English."
    )

    # ------------------------------------------------------
    # LANGUAGE
    # ------------------------------------------------------

    language_option = st.selectbox(
        "🌐 Language",
        [
            "Auto Detect",
            "Tamil",
            "English"
        ]
    )

    # ------------------------------------------------------
    # RECORD
    # ------------------------------------------------------

    audio = audio_recorder(
        text="🎙️ Record Complaint",
        recording_color="#d62828",
        neutral_color="#123c69",
        icon_size="2x"
    )

    if audio:

        st.audio(
            audio,
            format="audio/wav"
        )

        with open(
            "complaint.wav",
            "wb"
        ) as f:

            f.write(audio)

        st.success(
            "✅ Voice recorded successfully!"
        )

        # --------------------------------------------------
        # TRANSCRIBE
        # --------------------------------------------------

        if st.button(
            "🧠 Convert Voice to Text",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Whisper AI is processing..."
                ):

                    model = load_whisper_model()

                    result = model.transcribe(
                        "complaint.wav",
                        task="transcribe",
                        fp16=False
                    )

                text = result["text"].strip()

                detected_language = result.get(
                    "language",
                    "unknown"
                )

                st.session_state["complaint"] = text
                st.session_state["language"] = detected_language

                st.success(
                    "✅ Voice converted successfully!"
                )

                if detected_language == "ta":

                    lang_name = "Tamil 🇮🇳"

                elif detected_language == "en":

                    lang_name = "English 🇬🇧"

                else:

                    lang_name = detected_language

                st.info(
                    f"🌐 Detected Language: {lang_name}"
                )

            except Exception as e:

                st.error(
                    "❌ Voice processing failed."
                )

                st.exception(e)


    # ======================================================
    # COMPLAINT TEXT
    # ======================================================

    st.divider()

    st.markdown(
        '<div class="section-title">📝 Complaint Details</div>',
        unsafe_allow_html=True
    )

    complaint = st.text_area(
        "Complaint",
        value=st.session_state.get(
            "complaint",
            ""
        ),
        height=150,
        placeholder=(
            "தமிழில்:\n"
            "எங்கள் பகுதியில் குடிநீர் வரவில்லை\n\n"
            "English:\n"
            "There is no water supply in our area."
        )
    )

    # ======================================================
    # LOCATION
    # ======================================================

    location = st.text_input(
        "📍 Location",
        placeholder="Village / Street / Area"
    )


    # ======================================================
    # ANALYZE
    # ======================================================

    if st.button(
        "🤖 Analyze Complaint",
        use_container_width=True
    ):

        if not complaint.strip():

            st.warning(
                "Please record or enter a complaint."
            )

        else:

            try:

                processed_text = preprocess_text(
                    complaint
                )

                category = classify_complaint(
                    processed_text
                )

                # Prototype priority
                urgent_words = [
                    "emergency",
                    "danger",
                    "accident",
                    "urgent",
                    "அவசரம்",
                    "ஆபத்து"
                ]

                if any(
                    word in complaint.lower()
                    for word in urgent_words
                ):

                    priority = "High 🔴"

                else:

                    priority = "Medium 🟡"


                # ------------------------------------------
                # RESULT
                # ------------------------------------------

                st.divider()

                st.markdown(
                    '<div class="section-title">🧠 AI Analysis</div>',
                    unsafe_allow_html=True
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Category",
                        category
                    )

                with col2:

                    st.metric(
                        "Priority",
                        priority
                    )

                with col3:

                    detected = st.session_state.get(
                        "language",
                        ""
                    )

                    if detected == "ta":

                        lang = "Tamil 🇮🇳"

                    elif detected == "en":

                        lang = "English 🇬🇧"

                    else:

                        lang = language_option

                    st.metric(
                        "Language",
                        lang
                    )


                st.success(
                    "✅ Complaint analyzed successfully!"
                )


                # ------------------------------------------
                # LOCATION
                # ------------------------------------------

                st.write("### 📍 Location")

                if location:

                    st.write(location)

                else:

                    st.warning(
                        "Location not provided."
                    )


                # ------------------------------------------
                # SUBMIT
                # ------------------------------------------

                if st.button(
                    "📤 Submit Complaint",
                    use_container_width=True
                ):

                    complaint_id = (
                        "VOX-"
                        + st.session_state.get(
                            "language",
                            "XX"
                        )
                        + "-"
                        + str(
                            abs(
                                hash(complaint)
                            )
                        )[:8]
                    )

                    st.success(
                        f"Complaint submitted! "
                        f"ID: {complaint_id}"
                    )

            except Exception as e:

                st.error(
                    "❌ AI classification failed."
                )

                st.exception(e)


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

else:

    st.markdown(
        '<div class="section-title">📊 Admin Dashboard</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Complaints",
            0
        )

    with col2:
        st.metric(
            "Pending",
            0
        )

    with col3:
        st.metric(
            "In Progress",
            0
        )

    with col4:
        st.metric(
            "Resolved",
            0
        )

    st.divider()

    st.info(
        "PostgreSQL and authorized government "
        "login will be connected in the next phase."
    )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""
<div class="footer">

<b>🤖 VoxenAI</b><br>

AI-Based Citizen Complaint Management System<br>

🇮🇳 Tamil | 🇬🇧 English | 🎙️ Voice AI<br><br>

Prototype — Not an official government service

</div>
""", unsafe_allow_html=True)