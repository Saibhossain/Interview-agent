import os
from services.speech_service import speech_to_text, text_to_speech


def test_tts():
    print("=== Testing text_to_speech ===")
    sample_text = "Hello, this is a test of the speech service."
    output_file = "test_output.wav"

    try:
        result = text_to_speech(sample_text, output_file)
        print("TTS success.")
        print("Saved audio file:", result)
        print("File exists:", os.path.exists(result))
    except Exception as e:
        print("TTS failed:", e)


def test_stt():
    print("\n=== Testing speech_to_text ===")
    audio_file = "test_output.wav"   # reuse the file created by TTS

    try:
        if not os.path.exists(audio_file):
            print("Audio file not found. Run TTS test first.")
            return

        text = speech_to_text(audio_file)
        print("STT success.")
        print("Transcribed text:", repr(text))
    except Exception as e:
        print("STT failed:", e)


if __name__ == "__main__":
    test_tts()
    test_stt()