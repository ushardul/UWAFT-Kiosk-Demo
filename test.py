import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image

class BoxLay(Widget):
	pass

class BoxApp (App):
	def build (self):
		return BoxLay()



BoxApp().run()
