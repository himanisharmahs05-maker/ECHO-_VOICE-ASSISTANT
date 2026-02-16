import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import feedparser

# ---------------- SETTINGS ---------------- #

OPENAI_KEY = "YOUR_OPENAI_KEY"   # <-- replace with your key only here

# Initialize only once (important)
recognizer = sr.Recognizer()
engine = pyttsx3.init()
pygame.mixer.init()
client = OpenAI(api_key=OPENAI_KEY)


# ---------------- SPEAK FUNCTIONS ---------------- #

def speak_old(text):
    """Fallback offline TTS"""
    engine.say(text)
    engine.runAndWait()

def speak(text):
    """Google TTS voice output"""
    try:
        tts = gTTS(text)
        filename = "voice.mp3"
        tts.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove(filename)

    except Exception:
        speak_old(text)


# ---------------- AI RESPONSE ---------------- #

def aiProcess(command):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Echo, a smart short-answer AI assistant."},
            {"role": "user", "content": command}
        ]
    )
    return response.choices[0].message.content


# ---------------- COMMANDS HANDLER ---------------- #

def processCommand(c):

    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    elif c.startswith("play"):
        try:
            song = c.split("play")[1].strip()
            link = musicLibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")
        except:
            speak("Sorry, I couldn't find that song.")

    elif "news" in c:
        speak("Getting the latest headlines...")

        rss_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(rss_url)

        if len(feed.entries) == 0:
            speak("No news available right now.")
            return

        speak("Here are the top 5 news headlines.")
        for entry in feed.entries[:5]:
            speak(entry.title)

    else:
        reply = aiProcess(c)
        speak(reply)


# ---------------- MAIN LOOP ---------------- #

if __name__ == "__main__":
    speak("Echo is online. I'm listening.")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening for wake word...")

                try:
                    audio = recognizer.listen(source, timeout=6, phrase_time_limit=4)
                    word = recognizer.recognize_google(audio).lower()
                    print("You said:", word)
                except:
                    continue

                if "echo" in word:
                    speak("Yes?")
                    print("Waiting for command...")

                    try:
                        audio = recognizer.listen(source, timeout=7, phrase_time_limit=6)
                        command = recognizer.recognize_google(audio)
                        print("Command:", command)
                        processCommand(command)

                    except:
                        speak("I didn't catch that. Please repeat.")

        except Exception as e:
            print("Error:", e)
            speak("Something went wrong but I'm still running.")
