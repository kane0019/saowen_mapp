from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition

class Connected(Screen):
    def search(self):
        self.manager.
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login_page'
        self.manager.get_screen('login_page').resetForm()
        
