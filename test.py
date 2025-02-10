from idlelib.editor import darwin

import speech_recognition as sr
import os
import pyttsx3
from openai import audio
from wikipedia import languages
import webbrowser
import openai
import datetime


def say(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Speak the given text
    engine.say(text)

    # Wait for the speech to complete
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, languages="en-in")
            print(f"User said = {query}")
            return query
        except Exception as e:
            return "Some Error Occured. Sorry from A.I."


if __name__ == '__main__':
    print('PyCharm')
    say("Hello, I am A.I.")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say("Opening {site[0]}....")
                webbrowser.open(site[1])
        if "open music" in query:
            musicPath = "D:\Music\01 - Abhi Toh Party Shuru Hui Hai - DownloadMing.SE.mp3"
            os.system(f"open {musicPath}")

        if "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Time is {hour} bajke {min} minutes")