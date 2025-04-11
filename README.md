
# AIVoiceAssistant

# Voice Assistant using Python, LangChain, and OpenAI

This project is a voice-activated assistant built with Python. It uses speech recognition, AI-powered responses with OpenAI's GPT-4o via LangChain, and includes media controls, browser automation, and more.

## Features

- 🎤 Voice Recognition via microphone
- 💬 Conversational AI using GPT-4o (LangChain)
- 🔊 Text-to-Speech with `pyttsx3`
- 🎵 Music Controls (Play, Next, Previous, Stop)
- 🌐 Opens common websites like Google, YouTube, YouTube Music, and JioSaavn
- 😂 Tells random jokes
- 🧠 Maintains conversation memory

## Requirements

- Python 3.8+
- Microphone and speaker support
- `.env` file with your OpenAI API key

### Example `.env` File

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Installation

1. Clone the repository or copy the code.
2. Create and activate a Python virtual environment (optional but recommended).
3. Install dependencies:

```bash
pip install -r requirements.txt
```

Or manually install the following libraries:

```bash
pip install langchain langchain_openai langchain_community openai pygame SpeechRecognition pyttsx3 python-dotenv
```

4. Place some `.mp3` music files in `D:\Music` (or update the path in the script).

5. Run the script:

```bash
python voice_assistant.py
```

## Voice Commands

Try saying things like:

- "Play music"
- "Stop music"
- "Next music"
- "Tell me a joke"
- "Open Google"
- "Open YouTube Music"
- "Goodbye"
