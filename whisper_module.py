import whisper
import os
import imageio_ffmpeg

# Get FFmpeg automatically
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

# Add FFmpeg to PATH
os.environ["PATH"] = (
    os.path.dirname(ffmpeg_path)
    + os.pathsep
    + os.environ["PATH"]
)

# Load multilingual Whisper model
model = whisper.load_model("base")


def speech_to_text(audio_file):

    result = model.transcribe(
        audio_file,
        task="transcribe",
        fp16=False
    )

    text = result["text"].strip()
    language = result.get("language", "unknown")

    return text, language


if __name__ == "__main__":

    print("Whisper is ready!")

    audio_file = "test.wav"

    if os.path.exists(audio_file):

        text, language = speech_to_text(audio_file)

        print("Detected Language:", language)
        print("Transcribed Text:", text)

    else:

        print("test.wav not found.")
        print("Please record an audio file first.")