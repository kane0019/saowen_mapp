from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp

layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
layout_top = GridLayout(cols=1,rows=1)
btn_top = Button(text=str("Top"), size_hint=(.1,.1), height=40)
layout_top.add_widget(btn_top)
# Make sure the height is such that there is something to scroll.
layout.bind(minimum_height=layout.setter('height'))
for i in range(100):
    btn = Button(text=str(i), size_hint_y=None, height=40)
    layout.add_widget(btn)
ScrollView = ScrollView(size_hint=(1, None), size=(Window.width, Window.height-50))

ScrollView.add_widget(layout)

root = GridLayout(cols=1,rows=2)
root.add_widget(layout_top)
root.add_widget(ScrollView)
runTouchApp(root)