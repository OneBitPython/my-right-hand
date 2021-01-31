from nltk.corpus import stopwords
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit, QMessageBox, QWidget
from geopy.geocoders import Nominatim
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import psutil
from PyQt5.uic import loadUi
from win10toast import ToastNotifier
import requests
import subprocess
import playsound
import os
import time as t
import threading
import geocoder
import nltk
from nltk.tokenize import sent_tokenize
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pywhatkit
import datetime
import webbrowser
import wikipedia
import pyjokes
import wolframalpha
import pyttsx3
import time
import speech_recognition as sr
import random
import keyboard
import sys
from playsound import playsound
from quotes_facts import quotes, facts
import pyperclip
from wikiConsole import Console
from maps import *
import cv2


class start_up(QWidget):
    def __init__(self):
        super(start_up, self).__init__()
        loadUi('starting.ui', self)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        self.progressBar2.setValue(0)
        self.initUi()

    def initUi(self):
        thread = threading.Thread(target=self.progress)
        thread.start()

    def progress(self):
        try:
            self.completed = 0
            while self.completed < 100:
                self.completed += 3.5
                QThread.msleep(100)
                self.progressBar2.setValue(int(self.completed))
            starter.close()
        except:
            pass


next_app = QApplication(sys.argv)
starter = start_up()
starter.show()
next_app.exec_()


class GUI(QMainWindow):
    stop_signal = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super(GUI, self).__init__()
        loadUi('GUI.ui', self)

        self.backend = backend()
        self.InitUi()

    def InitUi(self):
        self.log.setStyleSheet('background-color:#222831;')

        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')

        for line in open('all_tasks.txt', 'r').readlines():
            line = line.strip()
            self.listWidget.insertItem(0, line)

        with open('comms.txt', 'w') as f:
            f.truncate(0)

        for line in open('log.txt', 'r').readlines():
            self.textEdit_2.setPlainText(line)

        self.progressBar.setValue(0)
        memory = psutil.virtual_memory().percent
        self.RAM_text.setText(f'RAM : {memory}')

        self.go_to_todo.clicked.connect(self.todo)

        self.back_in_todo.clicked.connect(self.back_to_home)

        for line in open('config.txt').readlines():
            line = line.strip()
            info = line.split('  ')

        try:
            self.my_location.setText(f"Location : {info[2]}")
        except:
            pass

        if str(info[0]) == "Male(Jarvis)":
            self.name.setText('JARVIS')
            self.name_in_set.setText('JARVIS CONFIG')

        if str(info[0]) == "Female(Friday)":
            self.name.setText('Friday')
            self.name_in_set.setText('Friday CONFIG')

        self.name_text.setReadOnly(True)
        self.location.clicked.connect(self.locator)

        self.settings_btn.clicked.connect(self.setting)
        self.back.clicked.connect(self.go_back)

        self.log.clicked.connect(self.logger)

        self.checkDate()

        self.setWindowTitle("Virtual Assistant")
        self.calendar.setGridVisible(True)

        self.insert.clicked.connect(self.inserter)
        self.delete_2.clicked.connect(self.deletor)
        self.edit.clicked.connect(self.editor)
        self.clear.clicked.connect(self.clearer)

        self.lineEdit_2.setText("Todo items...")

        self.always()

        my_thread = threading.Thread(target=self.show_time)
        my_thread.start()

        # Thread
        self.thread = QThread()
        self.backend = backend()
        self.stop_signal.connect(self.backend.stop)
        self.backend.moveToThread(self.thread)

        self.backend.finished.connect(self.thread.quit)
        self.backend.finished.connect(self.backend.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.started.connect(self.backend.start)
        self.thread.finished.connect(self.backend.stop)

        self.start.clicked.connect(self.thread.start)

        self.ender.clicked.connect(self.close_program)

        self.up.clicked.connect(self.push_up)
        self.down.clicked.connect(self.push_down)

        last_thread = threading.Thread(target=self.play_sick_beat)
        last_thread.start()

        final = threading.Thread(target=self.say)
        final.start()

        self.name_text.setPlainText(
            f"QUOTE :\n{random.choice(quotes)}\n\n\nFUN FACT :\n{random.choice(facts)}\n\n\nJOKE :\n{pyjokes.get_joke()}")

    def speak(self, text):
        self.engine.setProperty("rate", 178)

        self.engine.setProperty("volume", 1)

        self.engine.say(text)
        self.engine.runAndWait()

    def say(self):
        if self.name.text() == 'Friday':
            self.id = 1
            self.WAKE = 'Friday'
        else:
            self.WAKE = 'Jarvis'
            self.id = 0

        self.engine.setProperty('voice', self.voices[self.id].id)

        self.start.setEnabled(False)
        self.speak(f"{self.WAKE} 2.0 ready and at your service!")
        time.sleep(5)
        self.start.setEnabled(True)

    def play_sick_beat(self):
        playsound('updated_marvel.wav')

    def push_down(self):
        row = self.listWidget.currentRow()

        self.listWidget.insertItem(row + 2, self.listWidget.currentItem().text())
        try:
            take = self.listWidget.currentRow()
            self.listWidget.takeItem(take)
        except:
            pass

    def push_up(self):
        num = self.listWidget.currentRow()

        self.listWidget.insertItem(num - 1, self.listWidget.currentItem().text())
        try:
            number = self.listWidget.currentRow()
            self.listWidget.takeItem(number)
        except:
            pass

    def close_program(self):

        items = []
        for i in range(self.listWidget.count()):
            items.append(self.listWidget.item(i).text())

        with open('all_tasks.txt', 'a+') as f:
            f.truncate(0)
            for i in items:
                f.write(i)
                f.write("\n")

        window.close()

        self.backend.stop()
        self.stop_signal.emit()


    def stop_thread(self):
        self.backend = backend()
        self.backend.stop()
        self.stop_signal.emit()

    def locator(self):
        my_cord = geocoder.ip('me')

        latitude = str(my_cord.lat)
        longitude = str(my_cord.lng)

        geolocator = Nominatim(user_agent="app")
        self.location = geolocator.reverse((latitude, longitude))
        self.location = self.location.raw["address"]
        self.location = self.location['state_district']

        self.location_label.setText(f"Your location : {self.location}")

    def logger(self):

        text = self.textEdit_2.toPlainText()
        with open('log.txt', 'w+') as f:
            f.truncate(0)
            f.write(text)

    def back_to_home(self):
        self.stackedWidget.setCurrentWidget(self.main)

    def todo(self):
        self.stackedWidget.setCurrentWidget(self.todo_page)

    def show_time(self):
        while True:

            date = datetime.datetime.now()
            time = date.strftime('%H:%M')
            self.lcdNumber.display(time)

            cpu = psutil.cpu_percent(interval=2)
            self.progressBar.setValue(int(cpu))

            value = self.progressBar.value()
            value = int(value)

            if value in range(60, 101):
                self.progressBar.setStyleSheet('color:red')
                self.progressBar.setStyleSheet('background-color:red')
            elif value in range(30, 60):
                self.progressBar.setStyleSheet('color:orange')
                self.progressBar.setStyleSheet('background-color:orange')
            else:
                self.progressBar.setStyleSheet("color:green")
                self.progressBar.setStyleSheet('background-color:green')

            t.sleep(2)

    def setting(self):
        self.stackedWidget.setCurrentWidget(self.settings)

    def go_back(self):
        self.location = 'Bengaluru Urban'
        if str(self.lineEdit.text().strip()) == '':
            text = 'person'
        else:
            text = str(self.lineEdit.text().strip())
        with open('config.txt', 'w+') as f:
            f.truncate(0)
            f.write(str(self.comboBox.currentText()))
            f.write('  ')
            f.write(text)
            f.write('  ')
            f.write(self.location)

        self.stackedWidget.setCurrentWidget(self.main)

        for line in open('config.txt').readlines():
            line = line.strip()
            info = line.split('  ')

        try:
            self.my_location.setText(f"Location : {info[2]}")
        except:
            pass

        if str(info[0]) == "Male(Jarvis)":
            self.name.setText('JARVIS')
            self.name_in_set.setText('JARVIS CONFIG')

        if str(info[0]) == "Female(Friday)":
            self.name.setText('Friday')
            self.name_in_set.setText('Friday CONFIG')

    def checkDate(self):

        items = []
        for x in range(self.listWidget.count()):
            items.append(self.listWidget.item(x).text())

        for i in items:
            i = i.split("                          ")
            # i[1] is essentially the date
            i[1] = i[1].split("-")
            date1 = i[1]

            date = datetime.datetime.now()
            date = int(date.day)

            if int(date1[2]) - date == 0 or int(date1[2]) - date == 1 or int(date1[2]) - date == 2 or int(
                    date1[2]) - date == -29 or int(date1[2]) - date == -28 or int(date1[2]) - date == -27:
                thread = threading.Thread(target=self.noti)
                thread.start()

    def inserter(self):
        item = self.lineEdit_2.text()
        item = item.strip()

        date = self.calendar.selectedDate()
        date = date.toString("yyyy-MM-dd")

        date1 = datetime.datetime.now()

        if int(date1.month) >= int(date.split("-")[1]) and int(date1.day) > int(date.split("-")[2]) and int(
                date1.year) >= int(date.split("-")[0]):
            self.label.setText("Invalid Date selected.")
        elif item == "":
            self.label.setText("No text put!")
        else:

            self.label.setText("")

            no_of_items = self.listWidget.count()
            self.listWidget.insertItem(int(no_of_items) + 1, item + "                          " + date)
            self.lineEdit_2.clear()

            items = []
            for x in range(self.listWidget.count() - 1):
                items.append(self.listWidget.item(x).text())

            for i in items:
                if item in i:
                    self.label.setText("already in todo")
                    self.listWidget.takeItem(int(no_of_items))

    def deletor(self):
        try:
            number = self.listWidget.currentRow()
            self.listWidget.takeItem(number)
        except:
            pass

    def always(self):
        items = []
        for i in range(self.listWidget.count()):
            items.append(self.listWidget.item(i).text())

        with open('all_tasks.txt', 'a+') as f:
            f.truncate(0)
            for i in items:
                f.write(i)
                f.write("\n")

    def editor(self):
        try:
            items = self.listWidget.currentItem()
            text, ok = QInputDialog.getText(self, 'Edit value', 'Edit this value to:', QLineEdit.Normal,
                                            str(items.text().split("                          ")[0]))
            if ok:
                self.label.setText("Now set the date")

                date = self.calendar.selectedDate()
                date = date.toString("yyyy-MM-dd")

                date1 = datetime.datetime.now()

                if int(date1.month) >= int(date.split("-")[1]) and int(date1.day) > int(date.split("-")[2]) and int(
                        date1.year) >= int(date.split("-")[0]):
                    self.label.setText("Invalid date")
                else:
                    items.setText(str(text.strip()) + "                          " + date)
                    self.label.setText("")
            else:
                pass
        except Exception as e:
            pass

    def clearer(self):
        msg = QMessageBox()
        msg.setText("Are you sure you want to clear all your tasks?")
        msg.setIcon(QMessageBox.Question)
        msg.setDetailedText("This will not allow you to view these tasks again as it will delete all records")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Close)
        msg.setDefaultButton(QMessageBox.No)
        msg.buttonClicked.connect(self.msganswer)
        x = msg.exec_()

    def msganswer(self, i):
        if i.text() == "&Yes":
            self.listWidget.clear()

    def noti(self):
        try:
            items = []
            for x in range(self.listWidget.count()):
                items.append(self.listWidget.item(x).text())

            for i in items:
                i = i.split("                          ")
                # i[1] is essentially the date
                i[1] = i[1].split("-")
                date1 = i[1]

                date = datetime.datetime.now()
                date = int(date.day)

                if int(date1[2]) - date == 0 or int(date1[2]) - date == 1 or int(date1[2]) - date == 2 or int(
                        date1[2]) - date == -29 or int(date1[2]) - date == -28 or int(date1[2]) - date == -27:
                    h = ToastNotifier()
                    h.show_toast("Virtual Assistant",
                                 f"Hurry up, you have less than 3 days to finish the task you had set {i[0]}!!", )
        except:
            pass


class ask_input(QMainWindow):
    def __init__(self):
        super(ask_input, self).__init__()

    def take_input(self, information):
        self.val, ok = QInputDialog.getText(self, 'Info', information)

        if ok:
            pass
        else:
            pass

    def text(self):
        return self.val


class backend(QObject):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self.continue_run = True

        with open('dialogs.txt') as f:
            output = f.read()

        self.tokens = sent_tokenize(output)

        self.lemmers = nltk.stem.WordNetLemmatizer()

        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')

        self.ask_input = ask_input()

    def search_on_quora(self, where_to_search):
        vector = TfidfVectorizer()

        text = self.my_val
        text = text.lower()
        text = text.split()

        tokens = [word for word in text if word not in stopwords.words()]

        val = vector.fit_transform(tokens)
        var = vector.get_feature_names()

        my_list = []
        for word in var:
            if word not in ['search', where_to_search]:
                my_list.append(word)

        self.hey = ''
        for word in my_list:
            self.hey += word
            self.hey += '-'

        self.hey = self.hey.split('-')
        self.hey.reverse()
        self.hey.pop(0)

        self.string = ''
        for i in self.hey:
            self.string += i
            self.string += '-'

    def search(self, where_to_search, opt=None):
        vector = TfidfVectorizer()

        text = self.my_val
        text = text.strip()
        text = text.lower()
        text = text.split()

        tokens = [word for word in text if word not in stopwords.words()]

        val = vector.fit_transform(tokens)
        var = vector.get_feature_names()

        my_list = []
        for word in var:
            if word not in ['search', where_to_search, opt]:
                my_list.append(word)

        self.hey = ''

        for i in my_list:
            self.hey += i
            self.hey += ' '

        self.hey = self.hey.split(' ')
        self.hey.reverse()
        self.hey.pop(0)

        self.val = ''
        for i in self.hey:
            self.val += i
            self.val += ' '

    def speak(self, text):
        for line in open('config.txt', 'r').readlines():
            info = line.split('  ')
            self.name = info[1]
            city = info[2]
            info = info[0]

        if info == 'Male(Jarvis)':
            self.WAKE = "jarvis"
            self.id = 0
        else:
            self.WAKE = "friday"
            self.id = 1

        self.engine.setProperty('voice', self.voices[self.id].id)
        self.engine.setProperty('rate', 200)

        try:
            say = text.split('https')

            if len(say[0]) > 450:
                print(text)
                self.speak(
                    "\nThe message was extremely long so I didnt read it out aloud, I will wait for 15 seconds so you can go through the article")
                time.sleep(15)
                self.speak("Hope you are done reading it.")
            else:
                self.engine.say(say[0])
                self.engine.runAndWait()




        except:
            self.engine.say(text)
            self.engine.runAndWait()

        with open('comms.txt', 'a+') as f:
            f.write(f'{self.WAKE.upper()} : ' + text)
            f.write('\n')

        text = ""

    def get_audio(self):
        r = sr.Recognizer()
        playsound('Siri_Sound_Effect_HD.mp3')
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                with open('comms.txt', 'a+') as f:
                    f.write(f'{self.name.upper()} : {said}\n')

            except Exception as e:
                self.ask_input.take_input()
                said = self.ask_input.text()

        return said.lower()

    def note(self, query):
        date = datetime.datetime.now()
        file_name = str(date).replace(":", "-") + "-note.txt"
        with open(file_name, "w") as f:
            f.write(query)

        subprocess.Popen(["notepad.exe", file_name])

    def save_results(self):
        self.speak("Do you want me to save these results, yes or no?")
        query = self.get_audio()
        query = query.lower()
        if 'save' in query or 'yes' in query:
            self.speak("Tell me the name of the file you want me to store it in.")
            self.ask_input.take_input("File name : ")
            query = self.ask_input.text()

            if query.strip() != '':
                n = 1
                while n <= 3:
                    if os.path.isfile(query + ".py") == True:
                        self.speak("This file already exists. Please choose another name")
                        query = input("File name:")
                        n += 1
                    else:
                        with open(query + ".py", 'a+') as f:
                            f.write(answer)
                            self.speak("Your files have been saved")
                            self.speak(
                                "Next time you want to view these files just say view or if you want to delete that file just say delete.")
                            break
        while 'no' in query:
            break

    def expected_result(self):
        self.speak("Were these the results that you were looking for?")
        query = self.get_audio()
        query = query.lower()

        while 'yes' in query or 'yeah' in query or 'yup' in query:
            self.speak("Glad I could provide you with what you wanted")
            break
        if 'no' in query:
            self.speak("I am extremely sorry. I will be more careful next time.")
            webbrowser.open("https://google.com/search?q=%s" % query)

    def retrieve_file(self):
        self.speak("Tell me the name of the file that you had stored your results in:")
        self.ask_input.take_input("Filename : ")
        query = self.ask_input.text()

        if query.strip() != '':
            m = 1
            while m < 3:
                try:
                    with open(query + ".py") as f:
                        self.speak("We have retrieved your files")
                        f_contents = f.read()
                        print(f_contents)
                        break
                except:
                    self.speak("Your file was not found")
                    query = input("Filename:")
                    m += 1

    def delete(self):
        self.speak("Tell me the name of the file you want to delete")
        self.ask_input.take_input("Filename : ")
        query = self.ask_input.text()

        if query.strip() != '':
            a = 1
            while a < 3:
                try:
                    os.remove(query + ".py")
                    self.speak("Your file has been deleted")
                    break
                except:
                    self.speak("The file you wanted to delete was not found")
                    self.ask_input.take_input("Filename : ")
                    query = self.ask_input.text()
                    a += 1

    def pic(self):
        cam = cv2.VideoCapture(0)
        retval, frame = cam.read()
        if retval != True:
            raise ValueError("Can't read frame")

        cv2.imwrite('picture.png', frame)
        cv2.imshow("img1", frame)
        cv2.destroyAllWindows()

    def weather_forecast(self, query):
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=58053e4c2e9aada6bf198864ba91ce47'.format(
            query)

        res = requests.get(url)

        data = res.json()

        temp = data['main']['temp']
        temp = round(temp - 273.15)
        wind_speed = data['wind']['speed']

        latitude = data['coord']['lat']
        longitude = data['coord']['lon']

        description = data['weather'][0]['description']

        if temp >= 30:
            self.speak("its a hot " + str(temp) + "degree Celsius")

        elif temp >= 22 and temp < 30:
            self.speak("its a pleasant " + str(temp) + "degrees")

        else:
            self.speak("Its a cool " + str(temp) + " degree Celsius")

        if wind_speed >= 4:
            self.speak("with fast winds of " + str(wind_speed) + " meter per second")

        elif wind_speed > 0 and wind_speed <= 3:
            self.speak("with average winds of " + str(wind_speed) + " meter per second")

        else:
            self.speak("with no winds")

        if description == 'haze':
            self.speak("and a hazy day")

        elif description == 'mist':
            self.speak("and a misty day")

        elif description == 'light rain':
            self.speak("and some light rains")

        elif description == 'scattered clouds':
            self.speak("with scattered clouds")

        else:
            self.speak("and a " + description + " day")
        query = ""

    for line in open('config.txt', 'r').readlines():
        info = line.split('  ')
        city = info[2]

    def stop(self):
        self.continue_run = False

    print(
        "Basic Instructions\n-------------------------------------------------------------------\n1. For better results, try without writing 'in python'..\n2. You can say change voice to male and change to voice to female to change voice of the model.\n3. For resources just say the word 'resources'.\n4 'Table of contents' is another keyword you can use to recieve all the topics taught in order.\n5. Say 'features' to get a list of available features\n6. You can also ask me to sleep.\n\n")

    def lemmatizer(self, every_token):
        return [self.lemmers.lemmatize(token) for token in every_token]

    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def tokenize(self, query):
        return self.lemmatizer(nltk.word_tokenize(query.lower()))

    def start(self):
        self.continue_run = True
        self.bot_run()

    def bot_run(self):
        self.speak("Systems online")
        self.speak("Integration complete")
        self.speak(f"Hello {self.name}")
        while self.continue_run:
            query = self.get_audio()

            # *******************************************************************************************************************************
            NOTE_STRS = ["make a note", "write this down",
                         "remember this", "write a note"]
            for phrase in NOTE_STRS:
                if phrase in query:
                    self.speak("What would you like me to write down?")
                    note_query = self.get_audio()
                    self.note(note_query)
                    self.speak("I've made a note of that.")
                    query = ""

            # *********************************************************************************************************************************
            weather = ["weather", "tell me the weather", "what is the weather"]
            for word in weather:
                if word in query:
                    # self.speak('Enter your city : ')
                    self.weather_forecast('Bengaluru')
                    query = ""

            # *******************************************************************************************
            sign_off = ["switch off", "sign off", "exit", "bye", "shutdown", 'goodbye', 'see ya']
            for word in sign_off:
                if word in query:
                    self.speak("Powering off")
                    sys.exit(0)
                    query = ""

            joke_keys = ["tell me a joke", "tell me something funny", "make me laugh", 'im bored']
            for word in joke_keys:
                if word in query:
                    self.speak("Here is a good joke")
                    joke = pyjokes.get_joke()
                    print(joke)
                    self.speak(joke)
                    query = ""

            questions_april = ["who are you",
                               "what are you", "created you", "made you"]
            for questions in questions_april:
                if questions in query:
                    self.speak("I am a virtual assistant created and developed by PHP_sucks")
                    query = ""

            time = ['what is the time', 'tell me the time']
            for word in time:
                if word in query:
                    time = datetime.datetime.now()
                    current_time = time.strftime("%H-%M")
                    print("Current Time =", current_time)
                    self.speak("The time now is " + current_time.replace("-", " "))
                    query = ""

            command = ['change voice to male', 'voice change male']
            for word in command:
                if word in query:
                    self.engine.setProperty('voice', self.voices[0].id)
                    self.speak("Changed voice to male")
                    query = ''

            command2 = ['change voice to female', 'voice change female']
            for word in command2:
                if word in query:
                    self.engine.setProperty('voice', self.voices[1].id)
                    self.speak("Changed voice to female")
                    query = ''

            sleep = ['go to sleep', 'sleep']
            for word in sleep:
                if word in query:
                    self.speak("Going to Sleep")
                    print("PRESS (SHIFT+S) TO self.WAKE ME UP")
                    keyboard.wait("shift+s")
                    akn = ["I'm Online Boss",
                           "I'm with you", "i'm ready"]
                    self.speak(random.choice(akn))
                    query = ""

            take_pic = ['click a picture', 'Take a picture']
            for word in take_pic:
                if word.lower() in query:
                    self.speak("Taking Picture")
                    self.pic()
                    self.speak("Picture saved in the file, picture")
                    query = ""

            maps = ["show me"]
            for word in maps:
                if word in query:

                    n = query
                    n = n.replace("show ", '')
                    n = n.replace('me ', '')

                    place = n
                    print(place)

                    regularMap(place)
                    roadMap(place)
                    self.speak("Would you like to see the satellite map of " + place + "?")
                    ans = self.get_audio()
                    if ans == 'yes' or ans == 'yes please':
                        satelliteMap(place)
                    else:
                        pass

            comm = ['retrieve a file', 'view a file', 'show a file', 'retrieve file', 'show my file', 'view']
            for word in comm:
                if word in query:
                    self.retrieve_file()
                    query = ''

            comm = ['delete a file', 'delete file', 'delete my file', 'delete something']
            for word in comm:
                if word in query:
                    self.delete()
                    query = ''

            names = ['my name', 'who am i', 'do you know me']
            for word in names:
                if word in query:
                    self.speak(f"Your name is {self.name}, you can also change it in settings.")
                    query = ''

            open_web = ["open"]
            for word in open_web:
                if word in query:
                    print(query)
                    word = query.replace("open ", "")
                    self.speak("Opening " + word)
                    webbrowser.open("https://google.com//#q=" + word)
                    query = ""

            if query != '':
                self.tokens.append(query)

                TfidfVec = TfidfVectorizer(tokenizer=self.tokenize, stop_words='english')
                tfidf = TfidfVec.fit_transform(self.tokens)

                vals = cosine_similarity(tfidf[-1], tfidf)

                values = vals.argsort()[0][-2]

                flat = vals.flatten()
                flat.sort()

                req_tfidf = flat[-2]

                if req_tfidf == 0:
                    print("Please wait a moment")
                    try:
                        try:
                            app_id = 'K4EU2R-Q3GKP66LVP'
                            client = wolframalpha.Client(app_id)
                            res = client.query(query)
                            answer = next(res.results).query
                            print(answer)
                            self.speak(answer)
                            self.expected_result()
                            self.save_results()
                            query = ""


                        except:
                            try:
                                result = Console(query)
                            except:
                                pass
                            self.speak(result)
                            self.save_results()
                            query = ""

                    except:
                        self.speak("would you like me to search the web for " + query + "?")
                        ans = self.get_audio()
                        if "yes" in ans:
                            webbrowser.open("https://google.com//#q=" + query)
                            query = ""
                        else:
                            self.speak("Alright!")
                            query = ""
                else:
                    ans = self.tokens[values]
                    self.speak(ans)

                    ans = ans.lower()
                    self.tokens.remove(query)
                    query = query.lower()
                    if 'sleep' in ans:
                        print("PRESS (SHIFT+S) TO WAKE ME UP")
                        keyboard.wait("shift+s")
                        akn = ["I'm Online Boss",
                               "I'm with you", "i'm ready"]
                        self.speak(random.choice(akn))
                        query = ""
                    elif 'features' in ans:
                        pass
                    elif 'change voice to male' in query:
                        self.engine.setProperty('voice', self.voices[0].id)
                        self.speak("Changed voice to male")
                    elif 'change voice to female' in query:
                        self.engine.setProperty('voice', self.voices[1].id)
                        self.speak("Changed voice to female")
                    elif 'whatsapp' in query:
                        try:
                            date = datetime.datetime.now()

                            hour = date.strftime("%H")
                            tmin = date.strftime("%M")

                            tmin = int(tmin) + 2

                            self.speak("What do you want the content of the message to be?")
                            message = self.get_audio()

                            self.speak("Please enter your area code")

                            try:
                                self.ask_input.take_input("What is your area code, + not required")
                                area_code = self.ask_input.text()
                            except:
                                pass

                            if area_code.strip() != '':
                                self.speak("Who should I send the whatsapp message to (number)")
                                self.ask_input.take_input("Number : ")
                                number = self.ask_input.text()

                                if number.strip() != '':
                                    pywhatkit.sendwhatmsg("+" + str(area_code) + str(number), str(message), int(hour),
                                                          tmin)

                        except:
                            pass

                    elif 'opening youtube' in ans:
                        webbrowser.open('www.youtube.com')

                    elif 'gmail' in query:
                        webbrowser.open('https://mail.google.com/')

                    elif 'outlook' in query:
                        webbrowser.open('https://outlook.live.com/')

                    elif 'playing video on youtube' in ans:
                        say = self.speak('What do you want me to play')
                        what_to_play = self.get_audio()
                        pywhatkit.playonyt(what_to_play)

                    elif 'text on google' in ans:
                        self.my_val = query
                        self.search('google')

                        if self.val == '':
                            tell4 = self.speak("What do you want to search for?")
                            subject = self.get_audio()
                            pywhatkit.search(subject)
                        else:
                            pywhatkit.search(self.val)
                            try:
                                Console(self.val)
                            except:
                                pass

                    elif 'wikipedia' in query or 'wiki' in query:
                        self.my_val = query
                        self.search('wikipedia', 'wiki')

                        if self.val == '':
                            goto = self.speak("What do you want to search for on wikipedia : ")
                            subject = self.get_audio()
                            try:
                                answer = wikipedia.summary(subject, sentences=2)

                                self.speak(f'\n{answer}')
                                webbrowser.open(f'https://en.wikipedia.org/wiki/{subject}')

                            except:
                                webbrowser.open(f'https://en.wikipedia.org/wiki/{subject}')
                                print("\nThere was an error. So we directly took you to the wikipedia site.\n")

                        else:
                            try:
                                Console(self.val)
                            except:
                                pass

                    elif 'music' in ans:
                        webbrowser.open(
                            'https://www.amazon.in/music/prime?ref_=dmm_acq_marin_d_bra_zzz_jkBWTRVw-dc_c_335004885047')

                    elif 'joke' in ans:
                        self.speak(pyjokes.get_joke())

                    elif 'quora' in ans:
                        self.my_val = query
                        self.search_on_quora('quora')
                        try:
                            if self.string == '':
                                say = self.speak("What do you want to search for on quora")
                                what = self.get_audio()
                                what = what.lower()

                                ans = what.split(' ')

                                final = ''
                                for i in ans:
                                    final += i
                                    final += '-'

                                webbrowser.open(f'https://www.quora.com/{final[0:-1]}')
                            else:
                                self.my_val = query
                                self.search('quora')
                                webbrowser.open(f'https://www.quora.com/{self.string[0:-1]}')

                        except:
                            pass
                    else:
                        pass

        self.finished.emit()


app = QApplication(sys.argv)
window = GUI()
window.show()
app.exec_()

window.always()
window.close_program()


class end(QMainWindow):
    def __init__(self):
        super(end, self).__init__()
        loadUi('ending.ui', self)

        self.initUi()

    def initUi(self):
        with open('comms.txt') as f:
            contents = f.read()

        self.textEdit.setReadOnly(True)
        self.textEdit.setPlainText(contents)

        self.copy_text.clicked.connect(self.copied)
        self.save.clicked.connect(self.save_info)

    def save_info(self):
        text, ok = QInputDialog.getText(self, 'FileName', 'Name of the file you want to save info in : ')

        if ok:
            with open(f'{text}.txt', 'a+') as f:
                f.write(self.textEdit.toPlainText())

            self.INFO.setText('SAVED!')

        else:
            pass

    def copied(self):
        pyperclip.copy(self.textEdit.toPlainText())
        self.INFO.setText('COPIED!!')


last_app = QApplication(sys.argv)
ending = end()
ending.show()
last_app.exec_()
