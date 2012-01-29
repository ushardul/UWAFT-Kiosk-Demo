import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty


class BoxLay(FloatLayout):
	title_box = ObjectProperty(None)
	def printStuff(self):
		print self.title_box.pos

class BoxApp (App):
	def build (self):
		parent = BoxLay()
		parent.printStuff()
		return parent

BoxApp().run()
