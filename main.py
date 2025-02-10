import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import datetime


def say(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    """Listen to the user's voice input."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception as e:
            print("Error:", e)
            return "None"


if __name__ == '__main__':
    print("PyCharm")
    say("Hello, I am your A.I. assistant.")

    while True:
        query = takeCommand()

        # Open websites
        sites = [["youtube", "https://www.youtube.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])

        # Play music
        if "open music" in query:
            music_path = r"D:\Music\01 - Abhi Toh Party Shuru Hui Hai - DownloadMing.SE.mp3"  # Use raw string for paths
            if os.path.exists(music_path):
                say("Playing music...")
                os.startfile(music_path)  # Opens the file in the default music player
            else:
                say("Sorry, I cannot find the music file.")
                print("Music file not found at:", music_path)

        # Tell the time
        if "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            second = datetime.datetime.now().strftime("%S")
            say(f"The time is {hour} bajke {minute} minutes {second} seconds")
            print(f"The time is {hour}:{minute}:{second}")

        # Exit command
        if "exit" in query or "quit" in query:
            say("Goodbye!")
            break
