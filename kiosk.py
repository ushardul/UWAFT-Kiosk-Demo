import kivy

from kivy.app import App
from kivy.config import Config
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
from info_display import Parser

class KioskLayout(FloatLayout):
	wheel1 = ObjectProperty(None)

	def rotate(self,scatterObject, radius=0, direction = 1, duration=.03):
		scatterObject.size = (scatterObject.width+radius,scatterObject.height+radius)
		def update(ins):
			scatterObject.rotation += 8 * direction
		Clock.schedule_interval(update, duration)
		
	def scatter_image(self,imgSrc,imgSize,radius=0,**args):
		scatter = Scatter(size=imgSize,size_hint=(None,None),center=(Window.center[0]-imgSize[0]/4,Window.center[1]-imgSize[1]/2+10),do_translation_x=False,do_translation_y=False,do_scale=False,do_rotation=False,auto_bring_to_front=False,**args)
		scatter.add_widget(Image(source=imgSrc, size=imgSize,size_hint=(None,None)))
		return scatter
	
	def layout_setup(self):
		self.p = Parser('info.uwaft')
	
		wheelRim = CircularLayout(pos=(Window.center[0],Window.center[1]-40),size_hint=(None,None),radius=self.wheel1.parent.height*1,rotate=True)
		for i in range(1,5):
			wheelRim.add_widget(Button (background_normal = 'img/n'+str(i)+'.png', background_down='img/n'+str(i)+'.png',size_hint=(None,None),size=(self.wheel1.parent.size[0]*1.1,self.wheel1.parent.size[1]*1.1)))
		self.wheel1.add_widget(wheelRim)
		
		wheelMenu = CircularLayout(fin=self.p,pos=(Window.center[0],Window.center[1]-55),size_hint=(None,None),radius=self.wheel1.parent.height*1.7,pushAnimate=True)
		self.menu = wheelMenu
		for view in self.p.v_icons:
			wheelMenu.add_widget(Button (background_normal = view, background_down=view,size_hint=(None,None),size=(self.wheel1.parent.size[0]*1.1,self.wheel1.parent.size[1]*1.1)))
		self.wheel1.add_widget(wheelMenu)
		
		scatterImg = []
		size = (200,200)
		dir = -1
		for i in range(0,8):
			src = 'img/' + str(i)+'w.png'
			temp = self.scatter_image(src,size)
			scatterImg.append(temp)
			self.wheel1.add_widget(scatterImg[i])
			dir = -dir
			self.rotate(scatterImg[i], direction = dir)
	
class KioskApp(App):
	def build (self):
                parent = KioskLayout()
		parent.layout_setup()
		return parent

if __name__ in ('__main__', '__android__'):
        Config.set ('graphics', 'fullscreen', 'auto')
	KioskApp().run()
