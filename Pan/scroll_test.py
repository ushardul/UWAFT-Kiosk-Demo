import kivy
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.app import App


class MyEvents(Widget):
	def on_touch_down(self,touch):
		print 'Touched Start: ', touch.x, ',', touch.y
	
	def on_touch_up(self,touch):
		print 'Touch End: ' , touch.x , ',' , touch.y
	
	#def on_touch_move(self,touch):
		
	
class MyApp(App):
    def build(self):
		parent = GridLayout(cols=1, spacing=10, size_hint=(None,None))
		for i in range(30):
			btn = Button(text=str(i), size_hint=(None,None), height=40)
			parent.add_widget(btn)
		root = ScrollView(size_hint=(None,None), size=(400, 400))
		eventhandle = MyEvents()
		parent.add_widget(eventhandle)
		root.add_widget(parent)
		return root
				
if __name__ == '__main__':
    MyApp().run()