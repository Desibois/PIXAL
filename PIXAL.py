import speech_recognition as sr
import pyttsx3
import threading
import google.generativeai as genai
import webbrowser

genai.configure(api_key="")
config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 500
}
model = genai.GenerativeModel("gemini-1.0-pro-latest", generation_config=config)
convo = model.start_chat()
system_message = '''YOU ARE A CONVERSATIONAL VOICE ASSISTANT NAMED PICK SOL. REPLY TO THIS MESSAGE WITH - 
Hi, I'm PICK SOL, how may I help you :) - FURTHERMORE, KEEP YOUR ANSWERS RELATIVELY SHORT. 
IF THE USER SAYS SOMETHING SIMILAR TO GOODBYE, I WANT YOU TO SAY EXACTLY THIS -FAREWELL- IN CAPS AND EVERYTHING.
IF THE USER ASKS FOR A WEBSITE, I WANT YOU TO SAY THE URL OF THE WEBSITE, STARTING FROM -www-
IF THE USER ASKS FOR A PROGRAM, I WANT YOU TO SAY THE CODE IN AS IT WOULD APPEAR IN A PYTHON FILE, STARTING WITH -import os- AND NOT -python'''
system_message = system_message.replace(f'\n', '')
convo.send_message(system_message)

def listen():
    rec = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as mic:
                rec.adjust_for_ambient_noise(mic, duration=0.2)
                audio = rec.listen(mic)
                text = rec.recognize_google(audio)
                text = text.lower()
                return text
        
        except sr.UnknownValueError() or TypeError:
            rec = sr.Recognizer()
            continue

def think(text):
    convo.send_message(text)
    return convo.last.text

def speak(text):
    engine = pyttsx3.init()
    if text == "FAREWELL":
        engine.say(text)
        engine.runAndWait()
        quit()
    elif text[0:3] == "www":
        engine.say("HERE YOU GO.")
        engine.runAndWait()
        webbrowser.open(text)
        return None
    elif text[0:6] == "import":
        with open("program.py", "w") as f:
            f.write(text)
        engine.say("HERE'S YOUR PROGRAM.")
        engine.runAndWait()
        return None
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        input = listen()
        output = think(input)
        speak(output)

thread = threading.Thread(target=main)
thread.start()
