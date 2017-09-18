from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex

class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        # use a (r, g, b, a) tuple
        blue = (0, 0, 1.5, 2.5)
        red = (2.5, 0, 0, 1.5)
        btn =  Button(text='Touch me!', background_color=blue, font_size=120)        
        btn.bind(on_press=self.callback)
        self.label = Label(text="------------", font_size='50sp')
        self.username = TextInput(text='',multiline=False,size_hint=(.25,.05),pos_hint={'y':.7},font_size=15)
        layout.add_widget(self.username)
        layout.add_widget(btn)
        layout.add_widget(self.label)
        return layout
    def callback(self, event):
        print("button touched")  # test
        self.label.text = "button touched"
        print(self.username.text)
TestApp().run()