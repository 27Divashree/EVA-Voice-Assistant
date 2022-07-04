import datetime
import os
import pprint
import random
import smtplib
import time
import webbrowser
from email.message import EmailMessage
from time import strftime
from tkinter import *
from tkinter.ttk import *
import re
import JarvisAI
import goslate as goslate
import now
import phonenumbers
import pyautogui
import requests
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import pywhatkit

import wolframalpha
from bs4 import BeautifulSoup
from pyttsx3 import engine
from translate import Translator
from wikipedia import wikipedia

obj = JarvisAI.JarvisAssistant()

def t2s(text) -> object:
    obj.text2speech(text)


def scrape_weather(city):
    url = 'https://www.google.com/search?q=accuweather+' + city
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')
    links = [a['href'] for a in soup.findAll('a')]
    link = str(links[16])
    link = link.split('=')
    link = str(link[1]).split('&')
    link = link[0]

    page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content, 'lxml')

    time = soup.find('p', attrs={'class': 'cur-con-weather-card__subtitle'})
    time = re.sub('\n', '', time.text)
    time = re.sub('\t', '', time)
    time = 'Time: ' + time
    temperature = soup.find('div', attrs={'class': 'temp'})
    temperature = 'Temperature: ' + temperature.text

    realfeel = soup.find('div', attrs={'class': 'real-feel'})
    realfeel = re.sub('\n', '', realfeel.text)
    realfeel = re.sub('\t', '', realfeel)
    realfeel = 'RealFeel: ' + realfeel[-3:] + 'C'
    climate = soup.find('span', attrs={'class': 'phrase'})
    climate = "Climate: " + climate.text

    info = 'For more information visit: ' + link

    print('The weather for today is: ')
    print(time)
    print(temperature)
    print(realfeel)
    print(climate)
    print(info)
    t2s('The weather for today is: ')
    t2s(time)
    t2s(temperature)
    t2s(realfeel)
    t2s(climate)
    t2s('For more information visit accuweather.com')


def tellDay():
    # This function is for telling the
    # day of the week
    day = datetime.today().weekday() + 1

    # this line tells us about the number
    # that will help us in telling the day
    Day_dict = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}

    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        t2s("The day is " + day_of_the_week)


def sendWhatMsg(pyautogui=None):
    user_name = {
        'demo': '+91 76673 93105'
    }
    try:
        print("To whom you want to send the message?")
        t2s("To whom you want to send the message?")
        name = obj.mic_input()
        print("What is the message")
        t2s("What is the message")
        webbrowser.open("https://web.whatsapp.com/send?phone=" +
                        user_name[name] + '&text=' + obj.mic_input())
        time.sleep(6)
        #pyautogui.press('enter')
        print("Message sent")
        t2s("Message sent")
    except Exception as e:
        print(e)
        print("Unable to send the Message")

print("Hello I am Eva. What can I do for you?")
t2s("hello i am Eva. What can i do for you")


while True:
    res = obj.mic_input()

    r = sr.Recognizer()

    if re.search('weather', res):
        print('..')
        words = res.split(' ')
        print(words[-1])
        scrape_weather(words[-1])

    if re.search('music',res):
        t2s("Which song do you want to listen")
        def talk(res):
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.say('Playing ' + res)
            engine.runAndWait()


        def takeCommand():
            listener = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    voice = listener.listen(source)
                    command = listener.recognize_google(voice)
                    song = command.replace('play', '')
                    talk(song)
                    pywhatkit.playonyt(song)

            except:
                pass


        takeCommand()

    if re.search('news', res):
        news_res = obj.news()
        pprint.pprint(news_res)
        t2s(f"I have found {len(news_res)} news. You can read it. Let me tell you first 2 of them")
        t2s(news_res[0])
        t2s(news_res[1])

    if re.search('date', res):
        date = obj.tell_me_date()
        print(date)
        print(t2s(date))

    if re.search('open', res):
        domain = res.split(' ')[-1]
        open_result = obj.website_opener(domain)
        print(open_result)
        t2s("opening"+domain)

    if re.search('hello', res):
        print('Hi')
        t2s('Hi')

    if re.search('how are you', res):
        li = ['good', 'fine', 'great']
        response = random.choice(li)
        print(f"I am {response}")
        t2s(f"I am {response}")

    if re.search('your name|what is your name?', res):
        print("My name is Eva, I am your personal assistant")
        t2s("My name is Eva, I am your personal assistant")

    if re.search('what can you do', res):
        li_commands = {
            "open websites": "Example: 'open youtube.com",
            "time": "Example: 'what time it is?'",
            "date": "Example: 'what date it is?'",
            "launch applications": "Example: 'launch chrome'",
            "tell me": "Example: 'tell me about India'",
            "weather": "Example: 'what weather/temperature in Mumbai?'",
            "news": "Example: 'news for today' "
        }
        ans = """I can do lots of things, for example you can ask me time, date, weather in your city, 
        I can open websites for you and more. See the list of commands-"""
        print(ans)
        pprint.pprint(li_commands)
        t2s(ans)

    if re.search("day", res):
        tellDay()

    if re.search("calculate", res):
        app_id = "GRQ8G7-LHT23UVLQJ"
        client = wolframalpha.Client(app_id)
        indx = res.lower().split().index('calculate')
        query = res.split()[indx + 1:]
        rest = client.query(' '.join(query))
        answer = next(rest.results).text
        print("The answer is " + answer)
        t2s("The answer is " + answer)

    if re.search("covid", res):
        r = requests.get(
            'https://coronavirus-19-api.herokuapp.com/all').json()
        print(
            f'Confirmed Cases: {r["cases"]} \nDeaths: {r["deaths"]} \nRecovered {r["recovered"]}')
        t2s(f'Confirmed Cases: {r["cases"]} \nDeaths: {r["deaths"]} \nRecovered {r["recovered"]}')

    if re.search("message", res):
        print("Sending...")
        sendWhatMsg()

    if re.search("translate", res):
        res = res.replace("translate", "")
        convert = res
        translator = Translator(from_lang="english", to_lang="hindi")
        translation = translator.translate(convert)
        print(translation)
        t2s(translation)

    if re.search('tell me a joke', res):
        li = [
            'Mother: Did you enjoy your first day at school? Girl: First day? Do you mean I have to go back tomorrow? ',
            'If big elephants have big trunks, do small elephants have suitcases?',
            'In a restaurant: Customer: Waiter, waiter! There is a frog in my soup!!! Waiter: Sorry, sir. The fly is on vacation.',
            'Student: I was born in California. Teacher: Which part? Student: All of me.',
            'Teacher: Do you have trouble making decisions? Student: Well...yes and no.',
            'Son: Dad, what is an idiot? Dad: An idiot is a person who tries to explain his ideas in such a strange and long way that another person who is listening to him cannot understand him. Do you understand me? Son: No.',
            'Teacher: How can we get some clean water? Student: Bring the water from the river and wash it.',
            'Father: Can a kangaroo jump higher than the Empire State Building? Son: Yes, because the Empire State Building cannot jump!'
        ]
        response = random.choice(li)
        print(f"{response}")
        t2s(f"{response}")

    if re.search('mc', res):
        t2s("Here you go with music")
        music_dir = "C:\\Users\\divas\\Music"
        songs = os.listdir(music_dir)
        print(songs)
        os.startfile(os.path.join(music_dir, songs[1]))


    if re.search('write note', res):
        now=datetime.now()
        t2s("What should i write")
        note = obj.mic_input()
        file = open('jarvis.txt', 'w')
        strTime = now.strftime("%m/%d/%Y, %H:%M:%S")
        file.write(strTime)
        file.write(" :- ")
        file.write(note)
        t2s("noted")

    if re.search("show note", res):
            t2s("Here's what I've noted")
            file = open("jarvis.txt", "r")
            print(file.read())
            #t2s(file.read(6))

    if re.search('wikipedia',res):
        t2s('Searching Wikipedia...')
        query = res.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=3)
        t2s("According to Wikipedia")
        print(results)
        t2s(results)

    if re.search('question',res):
        t2s('I can answer to computational and geographical questions  and what question do you want to ask now')
        question = obj.mic_input()
        app_id = "GRQ8G7-LHT23UVLQJ"
        client = wolframalpha.Client('R2K75H-7ELALHR35X')
        rest = client.query(question)
        answer = next(rest.results).text
        t2s(answer)
        print(answer)


    if re.search('email',res):
        t2s("Do you want to see a mail or check inbox")

        with sr.Microphone() as source:
            t2s("Tell the password")
            passw = r.listen(source)
            t2s("Checking the password")
            ps = r.recognize_google(passw)
            print(ps)

            if (("Red Hat" in ps)):
                t2s("Access Granted")
                exec(open("EvaMail23.py").read())
                break
            else:
                t2s("Acces Denied")
                exit()


        break

    if re.search('inbox',res):
        exec(open('evaemail.py').read())

    if re.search('thank you', res):
        print("You are welcome")
        t2s("You are welcome")
        break