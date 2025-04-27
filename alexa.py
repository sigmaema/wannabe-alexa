import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import time 
from word2number import w2n
import re

warnings.filterwarnings('ignore')

def recordAudioAsString():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10)

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
def generate_random_number(text):
    try:
        text = text.lower()
        if 'random' not in text or 'number' not in text:
            return None
            
        between_pattern = re.search(r'between\s+(\d+)\s+and\s+(\d+)', text.lower())
        if between_pattern:
            start = int(between_pattern.group(1))
            end = int(between_pattern.group(2))
            return f"I generated the number {random.randint(start, end)} between {start} and {end}"
        
        from_to_pattern = re.search(r'from\s+(\d+)\s+to\s+(\d+)', text.lower())
        if from_to_pattern:
            start = int(from_to_pattern.group(1))
            end = int(from_to_pattern.group(2))
            return f"I generated the number {random.randint(start, end)} between {start} and {end}"

        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 2:
            start = int(numbers[0])
            end = int(numbers[1])
            if start > end:
                start, end = end, start
            return f"I generated the number {random.randint(start, end)} between {start} and {end}"

        return f"I generated the number {random.randint(1, 100)} between 1 and 100"
            
    except Exception as e:
        return f"Error while generating random number: {e}"
def play_guess_the_number():
    word_to_number = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
    'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
    'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
    'nineteen': 19, 'twenty': 20
}

    number_to_guess = random.randint(1, 20)
    getAlexaResponse("I'm thinking of a number between 1 and 20. Can you guess it?")
    
    while True:
        guess_text = recordAudioAsString().lower()
        
        if 'stop' in guess_text:
            return "Okay, stopping the game."

        numbers = re.findall(r'\d+', guess_text)
        if numbers:
            guess = int(numbers[0])
            if guess == number_to_guess:
                getAlexaResponse(f"Correct! The number was {number_to_guess}.")
                getAlexaResponse("Do you want to play again?")
                answer = recordAudioAsString().lower()
                if 'yes' in answer:
                    return play_guess_the_number()
                else:
                    return "Okay, exiting the game."
            elif guess < number_to_guess:
                getAlexaResponse("Too low. Try again.")
            else:
                getAlexaResponse("Too high. Try again.")
        elif guess_text in word_to_number:
            guess = word_to_number[guess_text]
        else:
            getAlexaResponse("I didn't catch a number. Try saying it again.")

def convert(text):
    conversion_factors = {
        ('km', 'm'): 1000,
        ('m', 'km'): 0.001,
        ('kg', 'g'): 1000,
        ('g', 'kg'): 0.001,
        ('cm', 'm'): 0.01,
        ('m', 'cm'): 100
    }
    
    text = text.lower()
    
    match = re.search(r'(\d+)\s*(\w+)\s+to\s+(\w+)', text)
    if not match:
        return "I didn't understand the conversion request."
    
    number = int(match.group(1))
    from_unit = match.group(2)
    to_unit = match.group(3)
    
    factor = conversion_factors.get((from_unit, to_unit))
    if factor is None:
        return "Sorry, I can't convert between those units."
    
    result = number * factor
    return f"{number} {from_unit} is {result} {to_unit}."

    return "Sorry, I couldn't understand the units."
def set_timer(text):
    text = text.lower()
    
    minutes = 0
    seconds = 0

    min_match = re.search(r'(\d+)\s*minute', text)
    if min_match:
        minutes = int(min_match.group(1))

    sec_match = re.search(r'(\d+)\s*second', text)
    if sec_match:
        seconds = int(sec_match.group(1))
    
    if minutes == 0 and seconds == 0:
        return "I didn't catch the timer duration."
    
    total_seconds = minutes * 60 + seconds
    
    getAlexaResponse(f"Setting a timer for {minutes} minutes and {seconds} seconds.")
    
    time.sleep(total_seconds)
    
    getAlexaResponse("Time's up!")
    
    return "Timer finished."
def quiz():
    questions = [
        {"question":"In what year did the Chernobyl accident happen?", "answer":"1986"},
        {"question":"What does IP stand for?", "answer":"internet protocol"},
        {"question":"What is the HTTPS port?", "answer":"443"},
        {"question":"In what year did the Czech institutions first connect to the internet?", "answer":"1993"},
        {"question":"What is the maximum number of IP addresses in a LAN with a /24 subnet?", "answer":"254"},
    ]
    score = 0

    for q in questions:
        getAlexaResponse(q["question"])
        user_answer = recordAudioAsString().lower()
        
        if q["answer"] in user_answer:
            getAlexaResponse("Correct:")
            score += 1
        else:
            getAlexaResponse(f"Wrong. The correct answer is {q['question']}.")

    getAlexaResponse(f"End of quiz. You had {score} correct answers from {len(questions)} questions.")
def handle_dumb_human_questions(text):
    text = text.lower()
    if 'pokemon' in text:
        return "My favorite pokemon is Vulpix"
    elif 'color' in text:
        return "My favorite color is #e53e74"
    elif 'drink' in text:
        return "Definitely battery acid"
    elif 'food' in text:
        return "I love eating up your RAM, and i also love rasberry pi"
    elif 'programming language' in text:
        return "I mean you can pretty much guess it's python"
    else:
        return "Idk go ask ChatGPT or something"

def tell_me_a_joke(text):
    text = text.lower()
    jokes = {
        1:"Why do Java developers wear glasses? Because they don't C#",
        2:"Why did the programmer quit his job? Because he didn't get arrays",
        3:"Why was the math book sad? Because it had too many problems",
        4:"How many programmers does it take to change a light bulb? None. It's a hardware problem",
        5:"Why do programmers prefer dark mode? Because light attracts bugs",
        6:"Why is it so hot in Apple headquarters? Because they don't have Windows"
    }
    random_key = random.choice(list(jokes.keys()))
    return jokes[random_key]
print("Starting voice assistant. Say 'hey alexa' to activate.")
while True:
    text = recordAudioAsString().lower().strip()
    
    if 'stop' in text:
        print("Exiting...")  
        break
        
    if 'hey alexa' in text or 'alexa' in text:
        if 'hey alexa' in text:
            command = text.split('hey alexa', 1)[1].strip()
        elif 'alexa' in text:
            command = text.split('alexa', 1)[1].strip()
        
        if command:
            print(f"Processing command: '{command}'")
            
            if 'stop' in command:
                print("Exiting...")
                break
            elif 'date' in command:
                response = getDate()
                getAlexaResponse(response)
            elif 'what is' in command and int in command:
                response = handle_math_calculation(command)
                getAlexaResponse(response)
            elif 'random' in command and 'number' in command:
                response = generate_random_number(command)
                getAlexaResponse(response)
            elif 'guess the number' in command:
                response = play_guess_the_number()
                getAlexaResponse(response)
            elif 'convert' in command:
                response = convert(command)
                getAlexaResponse(response)
            elif 'timer' in command:
                response = set_timer(command)
                getAlexaResponse(response)
            elif 'trivia' in command or 'quiz' in command:
                response = quiz(command)
                getAlexaResponse(response)
            elif 'favorite' in command:
                response = handle_dumb_human_questions(command)
                getAlexaResponse(response)
            elif 'joke' in command:
                response = tell_me_a_joke(command)
                getAlexaResponse(response)
        else:
            print("Hey Alexa detected! Listening for command...")
            follow_up = getFollowUpCommand()
            
            if 'stop' in follow_up:
                print("Exiting...")
                break
                
            response = handleFollowUpCommand(follow_up)
            getAlexaResponse(response)

#Ideas (useful):
      #generátor náhodných čísel 1
      #simple timers 1
      #převádění měn, jednotek atd. 1 jedinný problém je že to musí být celé v dictionary a taky způsob, jakým speech recognition rozpoznává různé jednotky - musím to vždy první testovat a to se mi moc nechce
#Ideas (gamesky):
      #guessování číslic - oboustranně :O  10
      #hangman
      #guessování slov
      #odpovídání na jednoduché otázky 1