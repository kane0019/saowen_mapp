from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class Login_Screen(Screen):
    pass

class Screen_M(ScreenManager):
    pass



class front_login(App):
    def build(self):
        root_widget = Builder.load_file('login_page.kv')
        return root_widget

if __name__ == "__main__":
    front_login().run()