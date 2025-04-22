import os
import random
import webbrowser
import requests
import pygame
import speech_recognition as sr
import pyttsx3

from langchain.agents import Tool, initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Recognizer and mic
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Music setup
music_dir = "D:\\Music"
if not os.path.exists(music_dir):
    os.makedirs(music_dir)

songs = [file for file in os.listdir(music_dir) if file.endswith(".mp3")]
song_index = 0
history_stack = []
pygame.mixer.init()

# Joke memory
last_joke = None

def tell_online_joke(_):
    global last_joke
    try:
        while True:
            res = requests.get("https://official-joke-api.appspot.com/jokes/random")
            if res.status_code == 200:
                joke = res.json()
                full_joke = f"{joke['setup']} ... {joke['punchline']}"
                if full_joke != last_joke:
                    last_joke = full_joke
                    return full_joke
            else:
                return "Couldn't fetch a joke right now."
    except Exception as e:
        return f"Error fetching joke: {str(e)}"

def next_joke(_):
    return tell_online_joke(None)

# Music control
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

# Open web tools
def open_google(_): webbrowser.open("https://www.google.com"); return "Opening Google."
def open_youtube(_): webbrowser.open("https://www.youtube.com"); return "Opening YouTube."
def open_youtube_music(_): webbrowser.open("https://music.youtube.com"); return "Opening YouTube Music."
def open_jiosaavn(_): webbrowser.open("https://www.jiosaavn.com"); return "Opening JioSaavn."

# File download (PDF/PPT)
def download_file(command):
    words = command.split()
    for word in words:
        if word.startswith("http"):
            url = word
            break
    else:
        return "Please provide a valid URL to download from."

    filename = url.split("/")[-1]
    if not filename.endswith((".ppt", ".pptx", ".pdf")):
        return "Only PPT and PDF files are supported."

    try:
        download_folder = "C:\\Users\\Sutiksh\\Downloads"
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        download_path = os.path.join(download_folder, filename)

        response = requests.get(url)
        with open(download_path, "wb") as f:
            f.write(response.content)
        return f"Downloaded {filename} to Downloads folder."
    except Exception as e:
        return f"Failed to download: {str(e)}"

# Tools for LangChain Agent
tools = [
    Tool(name="Play System Music", func=lambda x: play_music(), description="Plays a music file."),
    Tool(name="Next Music", func=lambda x: next_music(), description="Plays the next music file."),
    Tool(name="Previous Music", func=lambda x: previous_music(), description="Plays the previous music file."),
    Tool(name="Stop Music", func=lambda x: stop_music(), description="Stops the current music."),
    Tool(name="Open Google", func=open_google, description="Opens Google in a web browser."),
    Tool(name="Open YouTube", func=open_youtube, description="Opens YouTube in a web browser."),
    Tool(name="Open YouTube Music", func=open_youtube_music, description="Opens YouTube Music in a web browser."),
    Tool(name="Open JioSaavn", func=open_jiosaavn, description="Opens JioSaavn for music streaming."),
    Tool(name="Tell Joke", func=tell_online_joke, description="Tells a random joke from the internet."),
    Tool(name="Next Joke", func=next_joke, description="Tells another joke from the internet."),
    Tool(name="Download File", func=download_file, description="Downloads a PPT or PDF file from a URL.")
]

# LangChain Agent setup
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model="gpt-4o-mini")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True, memory=memory, handle_parsing_errors=True
)

# Speech listening
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

# Start assistant
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
