from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class MainScreen(Screen):
    pass
class AnotherScreen(Screen):
    pass
class ScreenManagement(ScreenManager):
    pass


presentation = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return presentation
 
if __name__ == "__main__":
    MainApp().run()