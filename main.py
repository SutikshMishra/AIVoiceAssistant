import os
import time
import random
import webbrowser
import pygame
import speech_recognition as sr
import pyttsx3  # For speaking

from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Load .env for API keys
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Text-to-speech engine setup
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Speaking speed

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Setup recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Music setup
music_dir = "D:\Music"
if not os.path.exists(music_dir):
    os.makedirs(music_dir)

songs = [file for file in os.listdir(music_dir) if file.endswith(".mp3")]
song_index = 0
history_stack = []
pygame.mixer.init()

# Jokes list
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? Because it had too many problems.",
    "Why do cows wear bells? Because their horns don't work!",
    "What did the computer do at lunchtime? Had a byte!"
]

# Music control functions
def play_music():
    global song_index
    if not songs:
        return "No songs found in the folder."
    song = os.path.join(music_dir, songs[song_index])
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    return f"Playing: {songs[song_index]}"

def next_music():
    global song_index
    if not songs:
        return "No songs found."
    history_stack.append(song_index)
    song_index = (song_index + 1) % len(songs)
    return play_music()

def previous_music():
    global song_index
    if history_stack:
        song_index = history_stack.pop()
        return play_music()
    else:
        return "No previous song in history."

def stop_music():
    pygame.mixer.music.stop()
    return "Music stopped."

# Browser-based actions
def open_google(_): webbrowser.open("https://www.google.com"); return "Opening Google."
def open_youtube(_): webbrowser.open("https://www.youtube.com"); return "Opening YouTube."
def open_youtube_music(_): webbrowser.open("https://music.youtube.com"); return "Opening YouTube Music."
def open_jiosaavn(_): webbrowser.open("https://www.jiosaavn.com"); return "Opening JioSaavn."
def tell_joke(_): return random.choice(jokes)

# LangChain tools
tools = [
    Tool(name="Play System Music", func=lambda x: play_music(), description="Plays a music file."),
    Tool(name="Next Music", func=lambda x: next_music(), description="Plays the next music file."),
    Tool(name="Previous Music", func=lambda x: previous_music(), description="Plays the previous music file."),
    Tool(name="Stop Music", func=lambda x: stop_music(), description="Stops the current music."),
    Tool(name="Open Google", func=open_google, description="Opens Google in a web browser."),
    Tool(name="Open YouTube", func=open_youtube, description="Opens YouTube in a web browser."),
    Tool(name="Open YouTube Music", func=open_youtube_music, description="Opens YouTube Music in a web browser."),
    Tool(name="Open JioSaavn", func=open_jiosaavn, description="Opens JioSaavn for music streaming."),
    Tool(name="Tell Joke", func=tell_joke, description="Tells a random joke to the user.")
]

# Agent setup
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model="gpt-4o-mini")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = initialize_agent(
    tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True, memory=memory, handle_parsing_errors=True
)

def listen_command():
    with mic as source:
        print("Adjusting for background noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "I didn't catch that."
    except sr.RequestError:
        return "Speech Recognition error."

# Assistant starts
speak("Hello, I am your voice assistant. How can I help you today?")

while True:
    command = listen_command().lower()
    print("User said:", command)

    if any(phrase in command for phrase in ["exit", "quit", "goodbye", "stop exit"]):
        speak("Goodbye! Have a great day.")
        break

    try:
        response = agent.run(command)
        speak(response)
    except Exception as e:
        speak("Something went wrong.")
        print("Error:", e)
