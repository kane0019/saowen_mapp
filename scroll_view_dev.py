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
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import requests
import http.cookiejar
from saowen import saowen_main


resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'ARIALUNI.TTF')


Builder.load_string('''
[DataViewItem@GridLayout]:
    size_hint_y: ctx.size_hint_y
    cols: ctx.cols
    Label:
        text: '作者:  '+ctx.author
        
    Label:
        text: '书名:  '+ctx.title
        
    Label:
        text: ctx.novel_info_p1
        text_size: self.width, None
        height: self.texture_size[1]
        halign: 'center'

    Label:
        text: ctx.novel_info_p2
        text_size: self.width, None
        height: self.texture_size[1]
        halign: 'center'
        
    Label:
        text: '星级:  '+ctx.star+'      平均分:  '+ctx.ave+'    总评:  '+ctx.sum

    Button:
        text: ctx.novel_id
        size:(1,.2)
        on_release: app.review_pop(ctx.novel_id)
        
      
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
        novel_info_list = saowen_main(session,headers)

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout_top = GridLayout(cols=1,rows=1)
        btn_top = Button(text=str("Top"), size_hint=(1,None), height=40)
        layout_top.add_widget(btn_top)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for novel in novel_info_list:
            print (novel)
            novel_view = Builder.template('DataViewItem', **novel,cols=1,size_hint_y=None)
            layout.add_widget(novel_view)

        ScrollView_page = ScrollView(size_hint=(1, None), size=(Window.width, Window.height-50))
        ScrollView_page.add_widget(layout)

        root = GridLayout(cols=1,rows=2)
        root.add_widget(layout_top)
        root.add_widget(ScrollView_page)
        return runTouchApp(root)
    def review_pop(release_event,novel_id):
        popup = Popup(title="成功",
                    content=Label(text=novel_id),
                    size=(100, 100),
                    size_hint=(0.3, 0.3),
                    auto_dismiss=True)
        popup.open()
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