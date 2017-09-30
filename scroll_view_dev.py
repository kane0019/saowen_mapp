from kivy.lang import Builder
from kivy.properties import ListProperty,StringProperty
from kivy.uix.floatlayout import FloatLayout
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
from novel_reviews import novel_reviews_get_content


resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'ARIALUNI.TTF')


Builder.load_string('''
#:import get_color_from_hex kivy.utils.get_color_from_hex
<Label>:
    height: 30
[Search_Bar@GridLayout]:
    cols:2
    rows:1
    canvas.before:
        Color: 
            rgba: get_color_from_hex('#4499ee')
        Rectangle:
            size: self.size
            pos: self.pos
    GridLayout:
        cols: 1
        rows: 1
        size_hint: (1,1)
        canvas.before:
            Color: 
                rgba: get_color_from_hex('#4499ee')
            Rectangle:
                size: self.size
                pos: self.pos                
        TextInput:
            id: search_text
            multiline: False
            size_hint: (.75,1)
            font_size: self.height



[Novel_Info@GridLayout]:
    size_hint_y: ctx.size_hint_y
    cols: ctx.cols
    height: sum(x.height for x in self.children)
    canvas.before:
        Color: 
            rgb: 1,1,1
        Rectangle:
            size: self.size
            pos: self.pos

    Label:
        text: '作者:  '+ctx.author
        color: (0,0,0)
        
    Label:
        text: '书名:  '+ctx.title
        color: (0,0,0)
        
    Label:
        text: ctx.novel_info_p1
        text_size: self.width, None
        height: self.texture_size[1]
        halign: 'center'
        color: (0,0,0)

    Label:
        text: ctx.novel_info_p2
        text_size: self.width, None
        height: self.texture_size[1]
        halign: 'center'
        color: (0,0,0)
        
    Label:
        text: '星级:  '+ctx.star+'      平均分:  '+ctx.ave+'    总评:  '+ctx.sum
        color: (0,0,0)

    Button:
        text: '显示评论'
        size:(1,.2)
        on_release: app.review_pop(ctx.novel_id)
        

[Novel_Review@GridLayout]:
    size_hint_y: ctx.size_hint_y
    rows: ctx.rows
    cols: ctx.cols
    height: reviewer_vote.size[1]+review_content.texture_size[1]
    canvas.before:
        Color: 
            rgb: 1,1,1
        Rectangle:
            size: self.size
            pos: self.pos
    BoxLayout:
        id: reviewer_vote
        orientation: 'horizontal'
        height: reviewer.texture_size[1]
        GridLayout:
            cols: 1
            Label:
                id:reviewer
                text: ctx.reviewer
                color: (0,0,0)
                
        GridLayout:
            id: vote
            cols: 4
            Button:
                text: '有用'
                
            Label: 
                text: ctx.up_vote
                color: (0,0,0)
               
            Button:
                text: '没用'

            Label:
                text: ctx.down_vote
                color: (0,0,0)

    Label:
        id: review_content
        text: ctx.review_content
        text_size: self.width, None
        size_hint: (1, None)
        size: self.parent.width, self.texture_size[1]
        halign: 'left'
        padding_bottom: 20
        color: (0,0,0)

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
        search_bar = Builder.template('Search_Bar',size=(Window.width,5))
        layout.bind(minimum_height=layout.setter('height'))

        for novel in novel_info_list:
            novel_info_view = Builder.template('Novel_Info', **novel,cols=1,size_hint_y=None)
            layout.add_widget(novel_info_view)

        scrollView_page = ScrollView(size_hint=(1, None), size=(Window.width, Window.height-50))
        scrollView_page.add_widget(layout)

        root = GridLayout(cols=1,rows=2)
        root.add_widget(search_bar)
        root.add_widget(scrollView_page)
        return runTouchApp(root)
    def review_pop(release_event,novel_id):

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
        pop_layout = GridLayout(cols=1)
        info_layout = GridLayout(cols=1,spacing=5,size_hint=(1,None))
        pop_scrollView_page = ScrollView(size_hint=(1,1))

        pop_scrollView_page.add_widget(info_layout)
        info_layout.bind(minimum_height=info_layout.setter('height'))
        review_list = novel_reviews_get_content(novel_id,session,headers)
        for review in review_list:
            novel_review_view = Builder.template('Novel_Review', **review,rows=2,cols=1,size_hint_y=None)
            info_layout.add_widget(novel_review_view)

        pop_layout.add_widget(pop_scrollView_page)

        popup = Popup(title='Top5 评论',
                    content=pop_layout,
                    size_hint=(.8,.6),
                    auto_dismiss=True)


        # bind the on_press event of the button to the dismiss function
        # content.bind(on_press=popup.dismiss)

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