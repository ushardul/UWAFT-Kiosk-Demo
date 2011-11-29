import kivy
import math
from kivy.app import App
from kivy.core.image import Image
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Ellipse
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
        img = Image(source='pie.png',size=(100,100))
        scatter = Scatter(pos=(240,200),size=img.size,size_hint=(None,None))
        scatter.add_widget(img)
        parent.add_widget(scatter)
        b = Button(text="click",size_hint=(.1,.1))
        def callback(inst):
            rotate(scatter,duration=1)
        b.bind(on_press=callback)
        parent.add_widget(b)
        return parent
        

if __name__ == '__main__':
    RadialMenu().run()
