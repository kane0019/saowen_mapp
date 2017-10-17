from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

import scroll_view_dev 
import login

# set default fonts

resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'ARIALUNI.TTF')




class username_grid(GridLayout):
    def __init__(self, **kwargs):
        super(username_grid, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        self.size_hint = (.5, .05)
        self.pos_hint = {'x': 0.20, 'y': 0.4}

        label_username = Label(text='邮箱:',color=(0,0,0),size_hint=(.1,.05),pos_hint={'y':.7},font_size=25)
        self.add_widget(label_username)
        self.username = TextInput(multiline=False,size_hint=(.25,.05),pos_hint={'y':.7},font_size=15)
        self.add_widget(self.username)

        with self.canvas.before:
            Color(1,1,1,1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_rect)
    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
class password_grid(GridLayout):
    def __init__(self, **kwargs):
        super(password_grid, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        self.size_hint = (.5, .05)
        self.pos_hint = {'x': 0.20, 'y': 0.3}

        label_password = Label(text='密码:',size_hint=(.1,.05),pos_hint={'y':.5},color=(0,0,0),font_size=25)
        self.add_widget(label_password)
        self.password = TextInput(multiline=False,size_hint=(.25,.05),pos_hint={'y':.5},font_size=15,password=True)
        self.add_widget(self.password)
        with self.canvas.before:
            Color(1,1,1,1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_rect)
    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


class Login_Screen(FloatLayout):

    def __init__(self, **kwargs):
        super(Login_Screen, self).__init__(**kwargs)
        self.cols = 1
        self.login_username = username_grid()
        self.login_password = password_grid()
        self.label1 = Label(text='扫文小院',color=get_color_from_hex('#4499ee'),pos_hint={'y':.6},size_hint=(1,.4),font_size=70)
        self.add_widget(self.label1)
        self.add_widget(self.login_username)
        self.add_widget(self.login_password)
        login_button = Button(text='登陆',color=(0,0,0),pos_hint={'x':.425,'y':.2},size_hint=(.15,.05),font_size=20,background_normal='',background_color=get_color_from_hex('#4499ee'),on_release=self.auth)
        self.add_widget(login_button)

        with self.canvas.before:
            Color(1,1,1,1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_rect)
    def auth(self,release_event):
        username = self.login_username.username.text
        password = self.login_password.password.text
        if self.login_username.username.text != '' and self.login_password.password.text !='':
            login_code,session,headers= login.login_session(username,password)
            print(login_code)
            if login_code == 200:
        
                popup = Popup(title="成功",
                    content=Label(text="欢迎"),
                    size=(100, 100),
                    size_hint=(0.3, 0.3),
                    auto_dismiss=True)
                popup.open()
    
                App.get_running_app().sm.switch_to(App.get_running_app().screen2)
            else:
                popup = Popup(title="失败",
                    content=Label(text="用户名／密码不正确"),
                    size=(100, 100),
                    size_hint=(0.3, 0.3),
                    auto_dismiss=True)
                popup.open()
        elif username != '':
            popup = Popup(title="错误",
                content=Label(text='请填写密码'),
                size=(100, 100),
                size_hint=(0.3, 0.3),
                auto_dismiss=True)
            popup.open()
        else:
            popup = Popup(title="错误",
                content=Label(text='请填写登陆邮箱'),
                size=(100, 100),
                size_hint=(0.3, 0.3),
                auto_dismiss=True)
            popup.open()

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size




class front_login(App):
    sm = ScreenManager(transition=FadeTransition())
    screen1 = Screen(name='Main')
    screen1.add_widget(Login_Screen())
    screen2 = Screen(name='Test')
    screen2.add_widget(scroll_view_dev.main_display())
    sm.add_widget(screen1)
    sm.current = 'Main'
    def build(self):
        return self.sm

if __name__ == "__main__":
    front_login().run()