import kivy
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.app import App


class MyEvents(Widget):
	def on_touch_down(self,touch):
		print 'Touched Start: ', touch.x, ',', touch.y
	
	def on_touch_up(self,touch):
		print 'Touch End: ' , touch.x , ',' , touch.y
	
	#def on_touch_move(self,touch):
		

class MyRectangles(Widget):
	def __init__(self,**kwargs):
		super(MyRectangles, self).__init__(**kwargs)
		self.register_event_type('on_paint')
	
	def on_paint(self):
		with self.canvas:
			Color(1, 1, 0)
			R1 = Rectangle(pos=(200,300),size=(100,80), size_hint=(None,None))
			R2 = Rectangle(pos=(320,300),size=(100,80), size_hint=(None,None))
			R3 = Rectangle(pos=(200,400),size=(100,80), size_hint=(None,None))
			R4 = Rectangle(pos=(320,400),size=(100,80), size_hint=(None,None))
	
class MyApp(App):
    def build(self):
		parent = BoxLayout()
		eventhandle = MyEvents()
		painthandle = MyRectangles()
		painthandle.dispatch('on_paint')
		parent.add_widget(eventhandle)
		parent.add_widget(painthandle)
		#root = ScrollView(size_hint=(None, None), size=(400, 400))
		#root.add_widget(parent)
		return parent
		
if __name__ == '__main__':
    MyApp().run()