import os
import whisper
import imageio_ffmpeg

# Make FFmpeg available to Whisper
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
os.environ["PATH"] = (
    os.path.dirname(ffmpeg_path)
    + os.pathsep
    + os.environ["PATH"]
)

print("Loading Whisper...")
model = whisper.load_model("base")

print("Transcribing...")
result = model.transcribe(
    "test.wav",
    task="transcribe"
)

print("\nDetected language:", result["language"])
print("Text:", result["text"])