from kivy.lang import Builder
from kivy.properties import ListProperty,StringProperty
from kivy.app import App
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp

import requests
import http.cookiejar
from saowen import saowen_main


resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'ARIALUNI.TTF')


Builder.load_string('''
[DataViewItem@BoxLayout]:
    size_hint_y: ctx.size_hint_y
    height: ctx.height
    Button:
        text: ctx.author
    Button:
        text: ctx.title
    Label:
        text: ctx.novel_info
    Button:
        text: ctx.star
    Button:
        text: ctx.ave
    Button:
        text: ctx.sum
''')

'''
class DataView(BoxLayout):

    templates = StringProperty()

    items = ListProperty([])


    def on_items(self, *args):
       self.clear_widgets()
      
       for item in self.items:
            print (item)
            w = Builder.template('DataViewItem', **item)
            print (w)
            self.add_widget(w)
'''  


class TestApp(App):
    def build(self):

        session = requests.session()
        session.cookies = http.cookiejar.LWPCookieJar(filename = 'cookies')
        try:
                session.cookies.load(ignore_discard=True)
        except:
                raise

        agent = 'Mozilla/5.0 (Windows Nt 5.1;rv:33.0) Gecko/20100101 Firefox/33.0'
        headers = {
            'User-Agent': agent
        }
        items = saowen_main(session,headers)

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout_top = GridLayout(cols=1,rows=1)
        btn_top = Button(text=str("Top"), size_hint=(.1,.1), height=40)
        layout_top.add_widget(btn_top)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for item in items:
            print (item)
            w = Builder.template('DataViewItem', **item,size_hint_y=None,height=40)
            layout.add_widget(w)

        ScrollView_page = ScrollView(size_hint=(1, None), size=(Window.width, Window.height-60))
        ScrollView_page.add_widget(layout)

        root = GridLayout(cols=1,rows=2)
        root.add_widget(layout_top)
        root.add_widget(ScrollView_page)
        return runTouchApp(root)



    '''
        root = BoxLayout()
        root.clear_widgets()
        for item in items:
            print (item)
            w = Builder.template('DataViewItem', **item)
            root.add_widget(w)
        return root
    '''
if __name__ == "__main__":
    TestApp().run()