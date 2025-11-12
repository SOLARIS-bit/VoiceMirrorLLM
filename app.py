import gradio as gr
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os

# Charger le modèle Whisper (base pour plus de précision)
print("🔄 Loading Whisper model...")
model = whisper.load_model("base")
print("✅ Model loaded!")

def translate_audio(audio, target_lang="en"):
    """Transcrit, traduit et retourne texte + audio."""
    if audio is None:
        return "No audio provided", None

    # Transcription Whisper
    result = model.transcribe(audio)
    text = result["text"]

    # Traduction
    try:
        translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        translated = f"[Translation failed: {e}]"

    # TTS (optionnel)
    try:
        tts = gTTS(translated, lang=target_lang)
        tts.save("translated.mp3")
        audio_out = "translated.mp3"
    except Exception as e:
        print("TTS error:", e)
        audio_out = None

    return f"🗣️ Original: {text}\n🌍 Translated ({target_lang}): {translated}", audio_out


# Interface Gradio
iface = gr.Interface(
    fn=translate_audio,
    inputs=[
        gr.Audio(type="filepath", label="🎤 Speak or upload audio"),
        gr.Textbox(value="en", label="🌍 Target language (e.g., en, fr, es, de)")
    ],
    outputs=[
        gr.Textbox(label="📝 Transcription + Translation"),
        gr.Audio(label="🔊 Translated Speech")
    ],
    title="🎙️ VoiceMirrorLLM — Real-time Translator",
    description="Speak or upload an audio file, and get an instant translation with voice playback."
)
