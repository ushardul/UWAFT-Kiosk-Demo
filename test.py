import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from circularlayout import CircularLayout
from kivy.uix.scatter import Scatter
from kivy.clock import Clock

class KioskLayout(FloatLayout):
	wheel1 = ObjectProperty(None)

	def wheelCallBack(self,button):
		animation = Animation(pos=(button.pos[0]+50,button.pos[1]),duration=1.5,t="out_elastic")
		animation.start(button)
	
	def rotate(self,scatterObject, radius=0, direction = 1, duration=.03):
		scatterObject.size = (scatterObject.width+radius,scatterObject.height+radius)
		def update(ins):
			scatterObject.rotation += 8 * direction
		Clock.schedule_interval(update, duration)
		
	def ScatterImage(self,imgSrc,imgSize,radius=0,**args):
		scatter = Scatter(size=imgSize,pos=(Window.center[0]/2+imgSize[0]/2,Window.center[1]/2+7),do_translation_x=False,do_translation_y=False,do_scale=False,do_rotation=False,auto_bring_to_front=False,size_hint=(None,None),**args)
		scatter.add_widget(Image(source=imgSrc, size=imgSize,size_hint=(None,None)))
		return scatter
	
	def dostuff(self):
		c = CircularLayout(pos=(Window.center[0],Window.center[1]-30),size_hint=(None,None),radius=self.wheel1.parent.height*1.7)
		button = [5]
		for i in range(1,6):
			button.append(Button (background_normal = 'img/'+str(i)+'.png', background_down='img/'+str(i)+'.png',size_hint=(None,None),size=(self.wheel1.parent.size[0]*1.1,self.wheel1.parent.size[1]*1.1)))
			c.add_widget(button[i])
	
		self.wheel1.add_widget(c)
		
		scatterImg = []
		size = (200,200)
		dir = -1
		for i in range(0,8):
			src = str(i)+'.png'
			temp = self.ScatterImage(src,size)
			scatterImg.append(temp)
			self.wheel1.add_widget(scatterImg[i])
			dir = -dir
			self.rotate(scatterImg[i], direction = dir)
	
class KioskApp(App):
	def build (self):
		parent = KioskLayout()
		parent.dostuff()
		return parent


KioskApp().run()
