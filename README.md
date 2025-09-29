# VoiceMirrorLLM
VoiceMirrorLLM – Real-time AI-powered voice translation and dubbing agent.  It is an experimental project that captures your voice, transcribes it using Whisper, translates the text (placeholder for now), and plays it back using Text-to-Speech (TTS).  

This version is optimized for development on **Chromebook (Debian ARM64 via Crostini)**.  
It is not focused on speed, but on having a stable end-to-end prototype.

---

## 🚀 Features

- 🎤 Record audio from the microphone (`--mic`)
- 📂 Process audio files directly (`--file sample.wav`)
- 📝 Transcribe speech to text (Whisper tiny)
- 🌍 Simple translation placeholder (prep for LLM integration)
- 🔊 Text-to-Speech playback (gTTS, local audio output)

---

## 📦 Installation (Chromebook / Debian ARM64)

1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/VoiceMirrorLLM.git
   cd VoiceMirrorLLM
