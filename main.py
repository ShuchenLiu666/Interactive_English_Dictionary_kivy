from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random
from difflib import get_close_matches

Builder.load_file('design.kv')
data = json.load(open("data.json"))
mywordb = json.load(open("myword.json"))
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current="sign_up_screen"
    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = 'login_screen_success'
        else:
            self.ids.login_wrong.text = "Wrong username or password!"
    def forget_pass(self):
        self.ids.login_wrong.text = "Think about it yourself asshole!"

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword, 
            'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"  
        

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'

    
    def get_quote(self, feel):
        
        feel = feel.lower()
        if feel in data:
            s = ""
            n = 1
            for item in data[feel]:
                s += str(n)
                s += ". "
                s += item
                s += "\n"
                n += 1
                self.ids.quote.text = s
        elif feel.title() in data:
            s = ""
            n = 1
            for item in data[feel.title()]:
                s += str(n)
                s += ". "
                s += item
                s += "\n"
                n += 1
                self.ids.quote.text = s
        elif feel.upper() in data:
            s = ""
            n = 1
            for item in data[feel.upper()]:
                s += str(n)
                s += ". "
                s += item
                s += "\n"
                n += 1
                self.ids.quote.text = s
        elif len(get_close_matches(feel, data.keys())) > 0:
            s = ("Did you mean '%s' instead? If so, definations are listed below. If not, the word does not exist.\n" % get_close_matches(feel, data.keys())[0])
            n = 1
            for item in data[get_close_matches(feel, data.keys())[0]]:
                s += str(n)
                s += ". "
                s += item
                s += "\n"
                n += 1
                self.ids.quote.text = s
    def my_words(self):
        self.manager.transition.direction = 'left'
        self.manager.current="my_words"
    def add_word(self, newword):
        with open("myword.json") as file:
            wordbase = json.load(file)

        wordbase[newword] = data[newword]

        with open("myword.json", 'w') as file:
            json.dump(wordbase, file)
    
    

class Mywords(Screen):
    def load_word(self):
        s = ""
        n = 1
        for item in mywordb:
            s += str(n)
            s += ". "
            s += item
            s += "\n"
            i = 1
            for exp in mywordb[item]:
                s+="   "
                s+="def"
                s += str(i)
                s += ": "
                s += exp
                s += "\n"
                i+=1
            n += 1
            self.ids.myword.text = s
            if n==15:
                break
    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen_success'
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass 

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()
