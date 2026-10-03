"""Speech-to-text utilities for recording and Whisper transcription."""

import os
import tempfile
import wave
from openai import OpenAI


def transcribe_audio(file_path: str) -> str:
    """Transcribe an audio file with OpenAI Whisper and return plain text."""
    client = OpenAI()
    with open(file_path, "rb") as audio_file:
        resp = client.audio.transcriptions.create(
            model=os.getenv("WHISPER_MODEL", "whisper-1"),
            file=audio_file,
        )
    return (getattr(resp, "text", "") or "").strip()


def record_audio(duration: int = 5) -> str:
    """Record audio to a temporary WAV file, or ask for a file path fallback."""
    try:
        import sounddevice as sd
    except Exception:
        path = input("sounddevice not available. Enter audio file path: ").strip()
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Audio file not found: {path}")
        return path

    sample_rate = 16000
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes((recording * 32767).astype("int16").tobytes())
        return tmp.name
