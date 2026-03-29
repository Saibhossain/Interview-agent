import os
import io
import wave
import tempfile
from typing import Optional, Union


def _ensure_wav_file(audio_source: Union[str, bytes, bytearray, io.BytesIO]) -> str:
    """
    Normalize different audio inputs into a temporary WAV file path.

    Supported:
    - local file path
    - raw bytes
    - BytesIO
    """
    if isinstance(audio_source, str):
        if not os.path.exists(audio_source):
            raise FileNotFoundError(f"Audio file not found: {audio_source}")
        return audio_source

    if isinstance(audio_source, (bytes, bytearray)):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp.write(audio_source)
        tmp.flush()
        tmp.close()
        return tmp.name

    if isinstance(audio_source, io.BytesIO):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp.write(audio_source.getvalue())
        tmp.flush()
        tmp.close()
        return tmp.name

    raise ValueError("Unsupported audio source type.")


def speech_to_text(audio_source: Union[str, bytes, bytearray, io.BytesIO]) -> str:
    """
    Convert speech audio to text using SpeechRecognition.

    Accepts:
    - audio file path
    - audio bytes
    - BytesIO
    """
    try:
        import speech_recognition as sr
    except ImportError:
        raise ImportError(
            "speech_recognition is not installed. Run: pip install SpeechRecognition"
        )

    temp_path = _ensure_wav_file(audio_source)
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(temp_path) as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            return text.strip()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            raise RuntimeError(f"Speech recognition service error: {e}")

    finally:
        # Delete only temp files created from bytes/stream
        if not isinstance(audio_source, str) and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


def text_to_speech(text: str, output_path: Optional[str] = None) -> str:
    """
    Convert text to speech using pyttsx3 and save as WAV file.

    Returns the saved file path.
    """
    try:
        import pyttsx3
    except ImportError:
        raise ImportError("pyttsx3 is not installed. Run: pip install pyttsx3")

    if not text or not text.strip():
        raise ValueError("Text for TTS cannot be empty.")

    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)

    engine = pyttsx3.init()

    # Slightly more natural defaults
    rate = engine.getProperty("rate")
    engine.setProperty("rate", max(140, rate - 20))

    volume = engine.getProperty("volume")
    engine.setProperty("volume", min(1.0, volume))

    engine.save_to_file(text, output_path)
    engine.runAndWait()

    return output_path