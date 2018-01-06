import os
from kivy.config import Config

Config.set('graphics', 'resizable', 0)

from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from subprocess import Popen, PIPE
from kivy.core.window import Window
from kivy.app import App

SCRIPT_NAME = "temp.py"
Window.size = (350, 500)
Builder.load_string("""
<MainScreen>:
    orientation: 'vertical'
    spacing: 5
    padding: 5
    Label:
        text: 'Code'
        size: root.width, 20
        halign: 'center'
        size_hint: None, None
    TextInput:
        id: input
        font_size: '15sp'
        size_hint: None, None
        focus: True
        size: root.width - 10, 200
    Label:
        text: 'Log'
        size: root.width, 20
        halign: 'center'
        size_hint: None, None
    ScrollView:
        id: sv2
        bar_margin: 2
        bar_width: 4
        scroll_distance: 10
        scroll_y: 1
        TextInput:
            id: output
            readonly: True
            size_hint: None, None
            width: root.width - 10 
            cursor_blink: True
            height: self.minimum_height
    BoxLayout:
        spacing: 5
        padding: 5
        Button:
            id: run
            text: 'run'
            size: 50, 30
            size_hint: None, None
            on_press: root.run_press()
        Button:
            id: clear
            text: 'clear'
            size_hint: None, None
            size: 50, 30
            on_press: root.clear_press()""")


class MainScreen(BoxLayout):
    def clear_press(self):
        self.ids.input.text = ""
        self.ids.output.text = ""

    def menu_press(self):
        pass

    def run_press(self):
        code = str(self.ids.input.text)
        with open(SCRIPT_NAME, "w") as f:
            f.write(code)
        result = Popen(["python", SCRIPT_NAME], stdout=PIPE, stderr=PIPE).communicate()
        if result[0] == b'':
            self.ids.output.text = result[1].decode(encoding='utf-8')
        else:
            self.ids.output.text = result[0].decode(encoding='utf-8')


class MyApp(App):
    def build(self):
        self.title = "Reactive PyIDE"
        return MainScreen()

def run():
    MyApp().run()

if __name__ == "__main__":
    run()
    if os.path.isfile(SCRIPT_NAME):
        os.remove(SCRIPT_NAME)