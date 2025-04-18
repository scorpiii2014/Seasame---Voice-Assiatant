#lrva
# GBM

import pyttsx3
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import requests
import imdb
import wolframalpha
#import pyautogui
from datetime import datetime
from decouple import config
from random import choice
from conv import  random_text
from  online import find_my_ip,search_on_google,search_on_wikipedia,youtube,send_email,get_news,weather_forecast


engine = pyttsx3.init('sapi5')
engine.setProperty('volume',1.5)
engine.setProperty('rate',180)
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

USER = config('USER')
HOSTNAME = config('BOT')


def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_me():
    hour = datetime.now().hour
    if(hour>=6) and (hour<12):
        speak(f"Good Morning {USER} Sir")
    elif (hour>= 12) and (hour <=16):
        speak(f"Good Afternoon {USER} Sir")
    elif (hour>=16) and (hour <22):
        speak(f"Good Evening {USER} Sir")
    speak(f"I am {HOSTNAME}. How may i assist You?")

def respond_to_thank_you():
    speak("Welcome sir, any other thing you need? Please ask.")

def tell_date():
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today's date is {current_date}")
    print(f"Today's date is {current_date}")

def tell_time():
    current_time = datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")
    print(f"The current time is {current_time}")

def tell_date_and_time():
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    current_time = datetime.now().strftime("%I:%M %p") 
    speak(f"Today's date is {current_date}, and the time is {current_time}.")
    print(f"Today's date is {current_date}, and the time is {current_time}.")

listening = False

def start_listening():
    global listening
    listening = True
    print("started Listening")

def pause_listening():
    global listening
    listening = False
    print("stopped Listening")

keyboard.add_hotkey('ctrl+alt+k',start_listening)
keyboard.add_hotkey('ctrl+alt+p',pause_listening)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        queri = r.recognize_google(audio,language='english')
        print(queri)

        if not 'stop' in query or 'exit' in  query:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir, take care")
            else:
                speak("Have a good day sir!")
            exit()

    except Exception:
        speak("Sorry I couldn't understand. Can you please repeat that?")
        queri = 'None'
    return queri

def create_file_with_voice():
    r = sr.Recognizer()
    
    # Step 1: Get the file name
    with sr.Microphone() as source:
        speak("Please say the name of the file.")
        print("Listening for file name...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing the file name...")
        file_name = r.recognize_google(audio, language='english')
        print(f"File name recognized: {file_name}")
        speak(f"The file name is {file_name}. Now, please say the file extension, like txt or py.")
        
        # Step 2: Get the file extension
        with sr.Microphone() as source:
            print("Listening for file extension...")
            audio = r.listen(source)

        extension = r.recognize_google(audio, language='english').strip().lower()
        print(f"File extension recognized: {extension}")
        speak(f"Creating a {file_name}.{extension} file.")
        
        # Combine file name and extension
        full_file_name = f"{file_name}.{extension}"
        
        # Creating the file
        with open(full_file_name, 'w') as f:
            speak(f"File {full_file_name} has been created successfully.")

    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand. Please try again.")
    except sr.RequestError as e:
        speak(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        speak(f"An error occurred while creating the file: {e}")
        print(f"An error occurred while creating the file: {e}")
def shutdown_pc():
    speak("Shutting down the PC, sir.")
    print("Shutting down the PC...")
    os.system("shutdown /s /t 1")

if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak(f"I am absoultely Fine Sir. What about you {USER} Sir.")

            elif "date" in query:
                tell_date()

            elif "time" in query:
                tell_time()

            elif "date" in query and "time" in query:
                tell_date_and_time()

            elif "open command prompt" in query:
                speak("Opening Command Prompt")
                os.system('start cmd')

            elif "open camera" in query:
                speak("Opening Camera Sir")
                sp.run('start microsoft.windows.camera:',shell = True)

            elif "open notepad" in query:
                speak("opening Notepad sir")
                notepad_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\Notepad"
                os.startfile(notepad_path)

            elif "open word" in query:
                speak("opening word")
                word_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.lnk"
                os.startfile(word_path)

            elif "open excel" in query:
                speak("opening excel")
                excel_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Excel.lnk"
                os.startfile(excel_path)
                

            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(
                    f"your ip address is{ip_address}"
                )
                print(f"Your ip address is{ip_address}")

            elif "create a file" in query:
                create_file_with_voice()


            elif " open youtube" in query:
                speak(f"What do you want to play on youtube {USER} Sir")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"what do you want to search on google {USER} sir")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak(f"what you want to search on wikipedia {USER} Sir")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia {results}")
                speak("I am printing on terminal")
                print(results)


            elif "send an email" in query:
                speak(f"On what email address do you want to send {USER} sir. Please Enter in the Terminal")
                receiver_add = input("Email address:")
                speak("what should be the subject sir?")
                subject = take_command().lower()
                speak("What is the message?")
                message = take_command().capitalize()
                if send_email(receiver_add, subject,message):
                    speak("I've Sent the Email sir")
                    print("I've Sent the Email Sir")
                else:
                    speak("Something Went Wrong Please check the error log")

            elif "give news" in query:
                speak(f"I'm reading out the latest headline of Today,sir")
                speak(get_news())
                speak("I am printing it on screen sir")
                print(*get_news(),sep='\n')


            elif "weather" in query:
                ip_address = find_my_ip()
                speak("Tell me the name of your City")
                city = input("Enter the name of your city")
                speak(f"Getting Weather report of your city {city}")
                weather,temp,feels_like = weather_forecast(city)
                speak(f"The Current Temperature is {temp},But it feels like {feels_like}")
                speak(f"Also the weather report talk about{weather}")
                speak("I am printing the weather Info on the screen")
                print(f"Description:{weather}\nTemperature:{temp}\nFeels Like:{feels_like}")


            elif "movie" in query :
                movies_db = imdb.IMDb()
                speak("Please tell me the Movie name")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("Searching for" + text)
                speak("I found these")
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title}-{year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info["rating"]
                    cast = movie_info["cast"]
                    actor = cast[0:5]
                    plot = movie_info.get('plot outline','plot summary not available')
                    speak(f"{title} was released in {year} has imdb rating of {rating}. It has a cast of {actor}.The"
                          f"plot summary of movie is {plot}")
                    print(f"{title} was released in {year} has imdb rating of {rating}. It has a cast of {actor}.The"
                          f"plot summary of movie is {plot}")


            elif "calculate" in query:
                app_id = "V9UKYH-K8H8PXA97X"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(result.results).text
                    speak("The answer is " + ans)
                    print("The Answer is " + ans)
                except StopIteration:
                    speak("I couldn't find that. Please try again")

            elif "what is" in query or "who is" in query or "which is"in query :
                app_id = "V9UKYH-K8H8PXA97X"
                client = wolframalpha.Client(app_id)
                try:
                    ind = query.lower().index("what is") if "what is" in query.lower() else \
                        query.lower().index("who is") if "who is" in query.lower() else \
                        query.lower().index("which is") if "which is" in query.lower() else None

                    if ind is not None:
                        text = query.split()[ind + 2:]
                        result = client.query(" ".join(text))
                        ans = next(result.results).text
                        speak("The answer is" + ans)
                        print("The answer is" + ans)

                    else:
                        speak("I could not find that")

                except StopIteration:
                    speak("I couldn,t find that. Please try again")

            elif "shutdown the pc" in query or "shut down the pc" in query:
                shutdown_pc()

            elif "thank you" in query:
                respond_to_thank_you()











