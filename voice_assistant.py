import os
import vosk
import queue
import sounddevice as sd
import json
import pyttsx3
import webbrowser
import time
import psutil  
import pywhatkit  
import pyautogui  
import pyjokes  
import requests  
from datetime import datetime  
import threading  

# Initialize pyttsx3 engine globally
engine = pyttsx3.init()

def speak(text):
    if not engine._inLoop:
        engine.say(text)
        engine.runAndWait()
    else:
        engine.say(text)

# Load Vosk Model
model_path = r"C:\Users\Admin\Downloads\vosk-model-small-en-us-0.15"  
model = vosk.Model(model_path)

# Audio Input Setup
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

def recognize_speech():
    with sd.RawInputStream(samplerate=16000, blocksize=4000, dtype='int16',  
                           channels=1, callback=callback):
        print("Listening...")
        rec = vosk.KaldiRecognizer(model, 16000)
        last_speech_time = time.time()

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                command = result.get("text", "").lower().strip()
                
                if command:
                    print("You said:", command)
                    threading.Thread(target=execute_command, args=(command,)).start()
                    last_speech_time = time.time()

            if time.time() - last_speech_time > 15:  
                print("No speech detected. Restarting listening...")
                threading.Thread(target=speak, args=("Please repeat",)).start()
                last_speech_time = time.time()

def execute_command(command):
    if "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad.exe")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc.exe")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "shutdown" in command:
        speak("Shutting down")
        os.system("shutdown /s /t 10")

    elif "restart" in command:
        speak("Restarting your system")
        os.system("shutdown /r /t 10")

    elif "hello" in command:
        speak("Hello! How can I help you?")

    elif "quit" in command or "exit" in command:
        speak("Goodbye!")
        exit()

    elif "battery" in command:
        battery = psutil.sensors_battery()
        percent = battery.percent
        speak(f"Battery is at {percent} percent.")

    elif "time" in command:
        time_now = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time_now}")

    elif "date" in command:
        date_today = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today's date is {date_today}")

    elif "search" in command:
        query = command.replace("search", "").strip()
        url = f"https://www.google.com/search?q={query}"
        speak(f"Searching for {query}")
        webbrowser.open(url)

    elif "play music" in command:
        music_folder = "C:\\Users\\Admin\\Music\\"  
        os.startfile(music_folder)

    elif "send message" in command:
        speak("Whom should I send the message to?")
        number = input("Enter phone number: ")
        speak("What should I send?")
        message = input("Enter your message: ")
        pywhatkit.sendwhatmsg_instantly(number, message)
        speak("Message sent!")

    elif "type" in command:
        speak("What should I type?")
        text = input("Enter the text: ")
        pyautogui.write(text, interval=0.1)

    elif "weather" in command:
        city = "Coimbatore"  
        api_key = "c47c04f5ee446a66ddc6c88d89c5bbee"  
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        if "main" in response:
            temp = response["main"]["temp"]
            condition = response["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp} degrees Celsius with {condition}")
        else:
            speak("Could not fetch weather data. Please check API key.")

    elif "joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "note" in command:
        speak("What should I write?")
        note = input("Enter your note: ")
        with open("notes.txt", "a") as f:
            f.write(note + "\n")
        speak("Note saved!")

    else:
        speak("I didn't understand. Please repeat.")

if __name__ == "__main__":
    speak("Voice OS Activated. Say a command.")
    recognize_speech()
