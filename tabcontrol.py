import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.config import Config
from tablayout import TabLayout
from tablayout import Tab
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

class InformationScreen(BoxLayout):
    tabInterface = ObjectProperty(None)

    def __init__ (self, data, **kvargs):
        super (BoxLayout, self).__init__(**kvargs)
        tabs = TabLayout ()
        tabs.add_tab (Tab (ToggleButton (text='test 1'), Button (text='tab 1')))
        tabs.add_tab (Tab (ToggleButton (text='test 2'), Button (text='tab 2')))
        self.tabInterface.add_widget (tabs)

class InformationApp(App):
    def build (self):
        return InformationScreen ('bs')

if __name__ == '__main__':
    # Config.set ('graphics', 'fullscreen', 'auto')
    InformationApp().run()
