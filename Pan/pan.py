import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics.transformation import Matrix

"""
UI is designed with the kivy language file
"""
class PanUI(BoxLayout):
    pass
    
class KioskApp(App):
    def build(self):
        layout = PanUI()
        scatter = Scatter(do_translation_x=False,do_rotation=False,scale_max=1.5, scale_min=1)
        scatter.add_widget(layout)
        return scatter

if __name__ in ('__main__', '__android__'):
    KioskApp().run()

