import kivy
from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '608')

import math
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from circularlayout import CircularLayout
from CircularAnimationUtilities import *
from kivy.core.window import Window
from kivy.clock import Clock

def rotate(scatterObject, radius=0, direction = 1, duration=.03):
    scatterObject.size = (scatterObject.width+radius,scatterObject.height+radius)
    def update(ins):
        scatterObject.rotation += 8 * direction
    Clock.schedule_interval(update, duration)

def ScatterImage(imgSrc,imgSize,radius=0,**args):
    scatter = Scatter(size=imgSize,pos=(Window.center[0]-imgSize[0]/2.+radius,Window.center[1]-imgSize[1]/2.+radius-60),do_translation_x=False,do_translation_y=False,do_scale=False,do_rotation=False,auto_bring_to_front=False,size_hint=(None,None),**args)
    scatter.add_widget(Image(source=imgSrc, size=imgSize,size_hint=(None,None)))
    return scatter

class RadialMenu (App):
    def build (self):
        parent = FloatLayout()
        c = CircularLayout(pos=(Window.center[0],Window.center[1]-60),size_hint=(None,None))
        bg = Image(source="bg.jpg")
        parent.add_widget(bg)
        wheel = ScatterImage('wheel.png',(400,400))
        parent.add_widget(wheel)
        
        size = (470,470)
        followWheelWrap = Scatter(size=size,pos=(Window.center[0]-225,Window.center[1]-225-60),size_hint=(None,None))
        folloWheelInnerWrap = Scatter(size=(160,140),pos=(size[0]-160,0),size_hint=(None,None),rotation=-2.5)
        folloWheelInnerWrap.add_widget(Image(source='comparc.png',size_hint=(1,1)))
        followWheelWrap.add_widget(folloWheelInnerWrap)
        
        parent.add_widget(followWheelWrap)
        
        def whellCallBack(button):
            animation = Animation(pos=(button.pos[0]+50,button.pos[1]),duration=1.5,t="out_elastic")
            animation.start(button)
        
        button = [5]
        for i in range(1,6):
            button.append(Button (background_normal = 'img/'+str(i)+'.png', background_down='img/'+str(i)+'.png',size_hint = (None, None), size=(140, 140)))
            button[i].bind(on_press=whellCallBack)
            c.add_widget(button[i])
        
        scatterImg = []
        size = (200,200)
        dir = -1
        for i in range(0,8):
            src = str(i)+'.png'
            temp = ScatterImage(src,size)
            scatterImg.append(temp)
            parent.add_widget(scatterImg[i])
            dir = -dir
            rotate(scatterImg[i], direction = dir)
        
        parent.add_widget(c)
        
        def callback(*args):
            c.do_rotation(incrDenom = 30, circDuration = .1)
        def callback2(*args):
            a = Animation(rotation=360,duration=3,t='in_bounce')
            a.start(followWheelWrap)
        def callback3(*args):
            c.do_layout()
            
        b = Button(text="click",size_hint=(.1,.1),pos=(0,0))
        b.bind(on_press=callback)
        b2 = Button(text="rotate",size_hint=(.1,.1),pos=(100,0))
        b2.bind(on_press=callback2)
        b3 = Button(text="dolayout",size_hint=(.1,.1),pos=(200,0))
        b3.bind(on_press=callback3)
        parent.add_widget(b)
        parent.add_widget(b2)
        parent.add_widget(b3)
        
        lblTitle = Label(text='EcoCar2',font_size=66,bold=True,pos=(Window.center[0]-50,520),font_name="fonts/coopbl.tff",color=(1,1,1,0.3),size_hint=(None,None))
        parent.add_widget(lblTitle)
        timePane = Image(source="img/Extended.png",size_hint=(None,None),size=(500,400),allow_stretch=True,keep_ratio=False,pos=(Window.center[0]/2-35,500))
        parent.add_widget(timePane)
        
        return parent

if __name__ == '__main__':
    RadialMenu().run()
