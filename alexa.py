import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import time 
from word2number import w2n

warnings.filterwarnings('ignore')

def recordAudioAsString():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=5)

    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: ' + data)
    except sr.UnknownValueError:
        print('We cannot understand the audio, unknown error')
    except sr.RequestError as e:
        print('Service Error ' + e)

    return data
def getAlexaResponse(inputCommandText):
    if inputCommandText != '': 
        print(inputCommandText)
        obj = gTTS(text=inputCommandText, lang='en', slow=False)
        obj.save('alexa_response.mp3')
        os.system('afplay alexa_response.mp3')
    else:
        print("No response to speak.")

def greet(text):
    inputGreetWords  = ['hi', 'hello']
    outputGreetWords = ['Hello, how can I help you?', 'Hey, wassup']
    for w in text.lower().split():
        if w in inputGreetWords:
            return random.choice(outputGreetWords)
    return ''  

def getDate():
    now = datetime.datetime.now()
    current_date = datetime.datetime.today()
    current_day = calendar.day_name[current_date.weekday()]
    month = now.month
    day = now.day
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
    ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])
    ordinal_list = [ordinal(n) for n in range(1, 32)]
    return 'Today is ' + current_day + ' ' + month_list[month-1] + ' ' + ordinal_list[day-1]


def handleFollowUpCommand(follow_up):
    response = ''
    
    if 'stop' in follow_up:
        return "Stopping"
    elif 'date' in follow_up:
        response = getDate()
    elif 'what is' in follow_up or 'calculate' in follow_up:
        response = handle_math_calculation(follow_up)
    
    if not response or not response.strip():
        response = "Sorry, I didn't understand that command."
        
    return response

def getFollowUpCommand():
    print("What can I help you with?")
    time.sleep(0.5) 
    return recordAudioAsString()
def handle_math_calculation(text):
    """Extract numbers and operation from text like 'what is 1 + 1'"""
    try:
        text = text.lower()
        if 'what is' not in text and 'calculate' not in text:
            return None

        if 'what is' in text:
            expression = text.split('what is')[1].strip()
        else:
            expression = text.split('calculate')[1].strip()
            
        expression = expression.replace('plus', '+')
        expression = expression.replace('add', '+')
        expression = expression.replace('minus', '-')
        expression = expression.replace('subtract', '-')
        expression = expression.replace('times', '*')
        expression = expression.replace('multiply by', '*')
        expression = expression.replace('multiplied by', '*')
        expression = expression.replace('divided by', '/')
        expression = expression.replace('divide by', '/')
        
        result = eval(expression)
        
        return f"The answer is {result}"
        
    except Exception as e:
        return f"I couldn't calculate that: {e}"
print("Starting voice assistant. Say 'hey alexa' to activate.")
while True:
    text = recordAudioAsString().lower().strip()
    
    if 'stop' in text:
        print("Exiting...")  
        break
        
    if 'hey alexa' in text:
        command = text.split('hey alexa', 1)[1].strip()
        
        if command:
            print(f"Processing command: '{command}'")
            
            if 'stop' in command:
                print("Exiting...")
                break
            elif 'date' in command:
                response = getDate()
                getAlexaResponse(response)
            elif 'what is' in command or '+' in command or '-' in command:
                response = handle_math_calculation(command)
                getAlexaResponse(response)
            
        else:
            print("Hey Alexa detected! Listening for command...")
            follow_up = getFollowUpCommand()
            
            if 'stop' in follow_up:
                print("Exiting...")
                break
                
            response = handleFollowUpCommand(follow_up)
            getAlexaResponse(response)