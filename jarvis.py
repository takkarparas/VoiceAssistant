import dialogflow 
import pyttsx3
import speech_recognition as sr
import datetime
import pyaudio
import wikipedia
import os
import webbrowser
from google.api_core.exceptions import InvalidArgument

DIALOGFLOW_PROJECT_ID = 'tablet-gtamwu'
DIALOGFLOW_LANGUAGE_CODE = 'en-IN'
GOOGLE_APPLICATION_CREDENTIALS ='tablet-gtamwu-081711b7571a.json'
SESSION_ID = 'paras'

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice',voices[1].id)

a=[]
i=0
j=0

def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()
    
def wishme():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("good morning")
    else:
        speak("good evening")
    speak("I am jarvis, new task or daily task")
    
def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")        
        r.energy_threshold = 400
        r.pause_threshold=1        
        r.adjust_for_ambient_noise(source,duration=.25)
        audio=r.listen(source)
    try:
        print("Recognising...")
        query=r.recognize_google(audio)
        print("You said: " + query)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        takeCommand()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        takeCommand()
    return query

def dailyTasks():
    while(True):
        speak("daily tasks are "+a[0])
        query=a[0]
        print(query)
        break
    return query

def tasks():
    query=takeCommand().lower()
    if "new task" in query:
        speak("say then")
        query=takeCommand().lower()        
    elif "daily task" in query:
        query=dailyTasks()
    else:
        speak("please repeat new task or daily task")
        tasks()
    
if __name__ == "__main__":
    wishme()
    tasks()    
    while True:
        print("query:", query)
        text_to_be_analyzed =query
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try: 
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            raise
        print("Query text:", response.query_result.query_text)
        print("Detected intent:", response.query_result.intent.display_name)
        print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        print("Fulfillment text:", response.query_result.fulfillment_text)
        if(response.query_result.fulfillment_text=="Sure sir, i have fixed your appointment"):
            i+=1
        speak(response.query_result.fulfillment_text)        
        if i>3:
            a.append("remind me to take medicines at 17:00 hours")
        query=takeCommand().lower()
                    
        if "exit"in query:
            break     