from kivy.lang import Builder
from kivy.properties import ListProperty,StringProperty,ObjectProperty
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





Builder.load_string('''
#:import get_color_from_hex kivy.utils.get_color_from_hex
<Label>
    height: 30

[Search_Bar@GridLayout]:
    cols:2
    rows:1
    size_hint:ctx.size_hint
    canvas.before:
        Color: 
            rgba: get_color_from_hex('#4499ee')
        Rectangle:
            size: self.size
            pos: self.pos
    GridLayout:
        id: search_field
        cols: 1
        rows: 1
        canvas.before:
            Color: 
                rgba: get_color_from_hex('#4499ee')
            Rectangle:
                size: self.size
                pos: self.pos                
        TextInput:
            id: search_text
            multiline: False
    GridLayout:
        id: search_buttons
        cols: 2
        rows: 1
        canvas.before:
            Color: 
                rgba: get_color_from_hex('#4499ee')
            Rectangle:
                size: self.size
                pos: self.pos    
        Button:
            text: '正文/作者搜索'
            on_release: app.sm.get_screen('Test').children[0].test(search_text.text)
        Button:
            text: '标签搜索'
            on_release: app.sm.get_screen('Test').children[0].test2(search_text.text)


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
        on_release: app.sm.get_screen('Test').children[0].review_pop(app.sm.get_screen('Test').children[0].session,app.sm.get_screen('Test').children[0].headers,ctx.novel_id)
        

[Novel_Review@GridLayout]:
    size_hint_y: ctx.size_hint_y
    height: reviewer_vote.size[1]+review_content.texture_size[1]
    rows: ctx.rows
    cols: ctx.cols
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

class main_display(GridLayout):

    def search(self,search_item):
        session = requests.session()
        session.cookies = http.cookiejar.LWPCookieJar(filename = 'cookies')
        try:
                session.cookies.load(ignore_discard=True)
        except FileNotFoundError:
                session.cookies.save(filename='cookies')
        except:
                raise
        agent = 'Mozilla/5.0 (Windows Nt 5.1;rv:33.0) Gecko/20100101 Firefox/33.0'
        headers = {
            'User-Agent': agent
        }

        if search_item != '':
            novel_info_list = saowen_main(search_item,0,session,headers)
        else:
            novel_info_list =[]
        return (session,headers,novel_info_list)
    def tag_search(self,search_item):
        session = requests.session()
        session.cookies = http.cookiejar.LWPCookieJar(filename = 'cookies')
        try:
                session.cookies.load(ignore_discard=True)
        except FileNotFoundError:
                session.cookies.save(filename='cookies')
        except:
                raise
        agent = 'Mozilla/5.0 (Windows Nt 5.1;rv:33.0) Gecko/20100101 Firefox/33.0'
        headers = {
            'User-Agent': agent
        }

        if search_item != '':
            novel_info_list = saowen_main(search_item,1,session,headers)
        else:
            novel_info_list =[]
        return (session,headers,novel_info_list)

    def review_pop(self,session,headers,novel_id):
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
    def test(self,text):
        self.session,self.headers,search_result = self.search(text)
        screen = App.get_running_app().sm 
        while screen.get_screen('Test').children[0].children:
            screen.get_screen('Test').children[0].remove_widget(screen.get_screen('Test').children[0].children[0])
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        search_bar = Builder.template('Search_Bar',size_hint=(1,0.06))
        screen.get_screen('Test').children[0].add_widget(search_bar)
        if search_result != []:
            for novel in search_result:
                novel_info_view = Builder.template('Novel_Info',**novel,cols=1,size_hint_y=None)
                layout.add_widget(novel_info_view)
                tag_box=GridLayout(cols=4,size_hint=(1,None))
                for tag in novel['tags']:
                    tag_button=Button(text=tag)
                    tag_box.add_widget(tag_button)
                layout.add_widget(tag_box)
            scrollView_page = ScrollView(size=(Window.width, Window.height*0.94))
            scrollView_page.add_widget(layout)
        else:
            scrollView_page = ScrollView(size=(Window.width, Window.height*0.94))
            scrollView_page.add_widget(info_display)
        self.add_widget(scrollView_page)
    def test2(self,text):
        self.session,self.headers,search_result = self.tag_search(text)
        screen = App.get_running_app().sm 
        while screen.get_screen('Test').children[0].children:
            screen.get_screen('Test').children[0].remove_widget(screen.get_screen('Test').children[0].children[0])
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        search_bar = Builder.template('Search_Bar',size_hint=(1,0.06))
        screen.get_screen('Test').children[0].add_widget(search_bar)
        if search_result != []:
            for novel in search_result:
                novel_info_view = Builder.template('Novel_Info',**novel,cols=1,size_hint_y=None)
                layout.add_widget(novel_info_view)
                tag_box=GridLayout(cols=4,size_hint=(1,None))
                for tag in novel['tags']:
                    tag_button=Button(text=tag)
                    tag_box.add_widget(tag_button)
                layout.add_widget(tag_box)
            scrollView_page = ScrollView(size=(Window.width, Window.height*0.94))
            scrollView_page.add_widget(layout)
        else:
            scrollView_page = ScrollView(size=(Window.width, Window.height*0.94))
            scrollView_page.add_widget(info_display)
        self.add_widget(scrollView_page)
    def __init__(self, **kwargs):
        super(main_display, self).__init__(**kwargs)
        resource_add_path('./fonts')
        LabelBase.register(DEFAULT_FONT, 'ARIALUNI.TTF')
        Window.clearcolor = (1, 1, 1, 1)
        session = ObjectProperty()
        headers = ObjectProperty()
        self.cols=1
        search_bar = Builder.template('Search_Bar',size_hint=(1,0.06))
        self.add_widget(search_bar)
        info_display = GridLayout(cols=1, spacing=10, size_hint_y=None)
        info_display.bind(minimum_height=info_display.setter('height'))
        self.session,self.headers,search_result = self.search('')    
        if search_result != []:
            for novel in search_result:
                novel_info_view = Builder.template('Novel_Info', **novel,cols=1,size_hint_y=None)
                info_display.add_widget(novel_info_view)
                tag_box=GridLayout(cols=4,size_hint=(1,None))
                for tag in novel['tags']:
                    tag_button=Button(text=tag)
                    tag_box.add_widget(tag_button)
                info_display.add_widget(tag_box)
            scrollView_page = ScrollView(size=(Window.width, Window.height*0.94))
            scrollView_page.add_widget(info_display)
        else:
            scrollView_page = ScrollView(size=(Window.width, Window.height*0.94))
            scrollView_page.add_widget(info_display)
        self.add_widget(scrollView_page)