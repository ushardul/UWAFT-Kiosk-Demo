import kivy
import math
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import OptionProperty, StringProperty
from circularlayout import CircularLayout
from CircularAnimationUtilities import *
from kivy.core.window import Window

def rotate(scatterObject, angleDeg=720,radius=0,duration=3):
    scatterObject.size = (scatterObject.width+radius,scatterObject.height+radius)
    animation = Animation(rotation=angleDeg,duration=duration,t='linear')
    animation.start(scatterObject)

class RadialMenu (App):
    def build (self):
        parent = FloatLayout()
        c = CircularLayout(anchor_y=('center'))
        batteryBtn = Button (text='Batteries', color=[0, 61, 245, 255], background_normal = 'img/battery.png', background_down = 'img/battery_selected.png', size_hint = (None, None), size=(128, 128))
        environBtn = Button (text='Emissions', color=[0, 61, 245, 255], background_normal = 'img/environ.png', background_down = 'img/environ_selected.png', size_hint = (None, None), size=(128,128))
        transmissionBtn = Button (text='Transmission', color=[0, 61, 245, 255], background_normal = 'img/transmission.png', background_down = 'img/transmission_selected.png',  size_hint = (None, None), size=(128,128))
        wheelsBtn = Button (text='Wheels', color=[0, 61, 245, 255], background_normal = 'img/wheels.png', background_down = 'img/wheels_selected.png', size_hint = (None, None), size=(128,128))
        engineBtn = Button (text='Engine', color=[0, 61, 245, 255], background_normal = 'img/engine.png', background_down = 'img/engine_selected.png', size_hint = (None, None), size=(128,128))
        c.add_widget (batteryBtn)
        c.add_widget (environBtn)
        c.add_widget (transmissionBtn)
        c.add_widget (wheelsBtn)
        c.add_widget (engineBtn)
        b = Button (text=('Click me nigger'),size_hint=(0.2,0.2))
        def callback(instance):
            c.do_rotation(-1,incrDenom=10,circDuration=1)
        b.bind(on_press=callback)
        
        img = Image(source='pie.png',size=(100,100),size_hint=(None,None))
        scatter = Scatter(pos=Window.center,size=img.size,size_hint=(None,None))
        print Window.center
        scatter.add_widget(img)
        parent.add_widget(scatter)
        b1 = Button(text="click",size_hint=(.1,.1),pos=(300,0))
        def callback2(inst):
            rotate(scatter,duration=1)
        b1.bind(on_press=callback2)
        
        parent.add_widget(c)
        parent.add_widget (b)
        parent.add_widget (b1)
        return parent
        

if __name__ == '__main__':
    RadialMenu().run()
