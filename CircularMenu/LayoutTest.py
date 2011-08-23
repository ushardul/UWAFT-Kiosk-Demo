import kivy
from circularlayout import CircularLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.app import App

class RotateRightButton (Button):
    def __init__(self, callback, **kwargs):
        self.addCallback = callback
        super (Button, self).__init__(**kwargs)

class MyApp (App):
    
    def build (self):
        parent = BoxLayout ()
        self.btnIndex = 1
        self.c = CircularLayout ()
        editlayout = BoxLayout (orientation='vertical')
        addwidgetbutton = Button (text='Add buttons')
        addwidgetbutton.bind (on_press=self.add_widget_action)
        rotateleftbutton = Button (text='Rotate Left')
        rotateleftbutton.bind (on_press=self.rotate_left_action)
        rotaterightbutton = Button (text='Rotate right')
        rotaterightbutton.bind (on_press=self.rotate_right_action)
        editlayout.add_widget (addwidgetbutton)
        editlayout.add_widget (rotateleftbutton)
        editlayout.add_widget (rotaterightbutton)
        parent.add_widget (self.c)
        parent.add_widget (editlayout)
        return parent

    def add_widget_action (self, instance):
        btnText = 'Button text ' + str(self.btnIndex)
        self.c.add_widget(Button (text=btnText))
        self.btnIndex += 1

    def rotate_right_action (self, instance):
        self.c.do_rotation()

    def rotate_left_action (self, instance):
        self.c.do_rotation(-1)

if __name__ == '__main__':
    MyApp().run ()
