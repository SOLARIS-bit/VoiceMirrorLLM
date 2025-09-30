import argparse
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import os
from deep_translator import GoogleTranslator
from gtts import gTTS

def record_audio(filename="input.wav", duration=5, fs=16000):
    """Enregistre depuis le micro et sauvegarde en WAV."""
    print(f"Recording for {duration} seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    # Normaliser le volume
    audio = audio / np.max(np.abs(audio))
    audio = (audio * 32767).astype(np.int16)
    write(filename, fs, audio)
    print(f"Saved recording to {filename}")
    return filename

def transcribe_audio(filename, model):
    """Transcrit l'audio avec Whisper."""
    print(f"Transcribing {filename}...")
    result = model.transcribe(filename)
    text = result["text"]
    print("Transcribed text:", text)
    return text

def translate_text(text, target_lang="en"):
    """Traduit automatiquement le texte avec Google Translate (deep-translator)."""
    try:
        translator = GoogleTranslator(source="auto", target=target_lang)
        translated_text = translator.translate(text)
        print(f"Translated text ({target_lang}): {translated_text}")
        return translated_text
    except Exception as e:
        print("Translation failed:", e)
        return f"[Untranslated] {text}"

def tts_playback(text, lang="en", filename="output.mp3"):
    """TTS avec gTTS (Google)."""
    try:
        tts = gTTS(text, lang=lang)
        tts.save(filename)
        song = AudioSegment.from_mp3(filename)
        play(song)
        os.remove(filename)
    except Exception as e:
        print("TTS failed:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VoiceMirrorLLM Prototype")
    parser.add_argument("--mic", action="store_true", help="Use microphone input")
    parser.add_argument("--file", type=str, help="Path to audio file (.wav)")
    parser.add_argument("--duration", type=int, default=5, help="Recording duration in seconds")
    parser.add_argument("--model", type=str, default="tiny", help="Whisper model to use (tiny, tiny.en, base, small, medium, large)")
    parser.add_argument("--lang", type=str, default="en", help="Target language for translation and TTS (default: en)")
    args = parser.parse_args()

    # Charger Whisper une seule fois
    print(f"Loading Whisper model '{args.model}'...")
    model = whisper.load_model(args.model)
    print("Model loaded!")

    if args.mic:
        wav_file = record_audio(duration=args.duration)
    elif args.file:
        wav_file = args.file
    else:
        print("❌ Please specify --mic or --file <path>")
        exit(1)

    text = transcribe_audio(wav_file, model)
    translated = translate_text(text, target_lang=args.lang)
    tts_playback(translated, lang=args.lang)
    print("Done ✅")

