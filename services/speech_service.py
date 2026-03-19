import os
from typing import Optional


def speech_to_text(audio_file_path: str) -> str:
    """
    Convert speech audio to text using SpeechRecognition.
    Supports WAV well. Other formats may need conversion first.
    """
    try:
        import speech_recognition as sr
    except ImportError:
        raise ImportError(
            "speech_recognition is not installed. Run: pip install SpeechRecognition"
        )

    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        raise RuntimeError(f"Speech recognition service error: {e}")


def text_to_speech(text: str, output_path: Optional[str] = None) -> str:
    """
    Convert text to speech using pyttsx3.
    Saves to file if output_path is provided.
    """
    try:
        import pyttsx3
    except ImportError:
        raise ImportError("pyttsx3 is not installed. Run: pip install pyttsx3")

    if not text or not text.strip():
        raise ValueError("Text for TTS cannot be empty.")

    engine = pyttsx3.init()

    # Slightly more natural defaults
    rate = engine.getProperty("rate")
    engine.setProperty("rate", max(140, rate - 20))

    volume = engine.getProperty("volume")
    engine.setProperty("volume", min(1.0, volume))

    if output_path:
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return output_path
    else:
        engine.say(text)
        engine.runAndWait()
        return "spoken"