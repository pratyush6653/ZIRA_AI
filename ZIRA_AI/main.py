import datetime
import os
import webbrowser

import pyttsx3
import pywhatkit
import requests
import speech_recognition
import wikipedia
from bs4 import BeautifulSoup

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

engine.setProperty('rate', 140)

# Define headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Hi, good morning!")
    elif 12 <= hour < 18:
        speak("Hi, good afternoon!")
    else:
        speak("Hi, good evening!")
    speak("I am Zira... your A.I Assistance. Please tell me how may I help you")


def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        s = "Say that again please...."
        print("Say that again please....")
        speak(s)
        return "none"
    return query


def weather(city):
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',
        headers=headers)
    print("Searching...\n")
    soup = BeautifulSoup(res.text, 'html.parser')

    try:
        location = soup.select('#wob_loc')[0].getText().strip()
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        weather = soup.select('#wob_tm')[0].getText().strip()

        print(location)
        print(time)
        print(info)
        print(weather + "°C")

        speak(location)
        speak(time)
        speak(info)
        speak(weather + "degree Centigrade")
    except Exception as e:
        print("Error fetching weather information:", str(e))
        speak("Sorry, I couldn't fetch the weather information at the moment.")


if __name__ == '__main__':
    wishMe()
    stop_listening = False
    while not stop_listening:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('searching Wikipedia....')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        elif 'youtube' in query:
            speak("Sure, what you want to search on youtube?")
            data_query = takeCommand()
            speak(f"Searching for {data_query} on YouTube.")
            pywhatkit.playonyt(data_query)
        elif 'google' in query:
            webbrowser.open_new_tab("google.com")
        elif 'gmail' in query:
            webbrowser.open_new_tab("https://mail.google.com/mail/u/0/#inbox")
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'open code' in query:
            codePath = "C:\\Users\\cprat\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            speak("opening vs Code")
            os.startfile(codePath)
        elif 'stop' in query:
            speak("Byeee  Byeee. See you soon!")
            stop_listening = True
        elif "weather" in query:
            speak("Please provide name of the City")
            city = takeCommand()
            city = city + " weather"
            weather(city)
            speak("Have a Nice Day :)")
