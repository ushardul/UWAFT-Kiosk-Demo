import kivy
from circularlayout import CircularLayout
from kivy.uix.button import Button
from kivy.app import App

class MyApp (App):
    def build (self):
        c = CircularLayout ()
        c.add_widget(Button (text='Test'))
        c.add_widget(Button (text='Test 2'))
        c.add_widget(Button (text='Test 3'))
        c.add_widget(Button (text='Test 4'))
        c.add_widget(Button (text='Test 5'))
        return c

if __name__ == '__main__':
    MyApp().run ()
