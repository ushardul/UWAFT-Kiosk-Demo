import kivy
kivy.require ('1.0.9')

from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty, ObjectProperty, StringProperty

class TabLayout (BoxLayout):
    contents=DictProperty ({})
    header_obj=ObjectProperty(None)
    content_obj=ObjectProperty(None)
    selected_content=StringProperty (None)

    def add_tab (self, tab):
        tab.lyt_button.group='tlayout%d'%self.uid
        tab.lyt_button.bind (on_release=self._on_tab_click)
        self.header_obj.add_widget(tab.lyt_button)
        self.contents[tab.lyt_button.text]=tab.lyt_content
        if self.selected_content is None:
            self.bind (selected_content=self._change_tab)
            self.selected_content=tab.lyt_button.text
            tab.lyt_button.state='down'

    def _on_tab_click (self, button):
        if button.text == self.selected_content:
            button.state='down'
        else:
            self.selected_content=button.text

    def _change_tab (self, instance, value):
        self.content_obj.clear_widgets()
        self.content_obj.add_widget (self.contents.get (value, None))

class Tab:

    lyt_button = ObjectProperty (None)
    lyt_content = ObjectProperty (None)
    
    def __init__ (self, button, content):
        self.lyt_button = button
        self.lyt_content = content
        
