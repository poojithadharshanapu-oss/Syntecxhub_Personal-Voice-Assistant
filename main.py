import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import sounddevice as sd
from scipy.io.wavfile import write


# Text-to-speech setup
engine = pyttsx3.init()
engine.setProperty("rate", 170)


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def listen():

    duration = 5
    sample_rate = 44100

    print("Listening... Speak now")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write("voice.wav", sample_rate, audio)

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile("voice.wav") as source:
            audio_data = recognizer.record(source)

        command = recognizer.recognize_google(audio_data)

        print("You said:", command)

        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return ""

    except sr.RequestError:
        speak("Speech service is unavailable.")
        return ""



def execute_command(command):

    if "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")


    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")


    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)


    elif "notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")


    elif "calculator" in command:
        speak("Opening Calculator")
        os.system("calc")


    elif "exit" in command or "stop" in command:
        speak("Goodbye")
        exit()


    else:
        speak("Sorry, I cannot perform that command.")



# Starting assistant
speak("Hello, I am your personal voice assistant.")


while True:

    command = listen()

    if command:
        execute_command(command)