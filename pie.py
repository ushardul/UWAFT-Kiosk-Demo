import kivy
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '540')

import math
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from circularlayout import CircularLayout
from CircularAnimationUtilities import *
from kivy.core.window import Window
from kivy.clock import Clock


animation = {};
def rotate(scatterObject, angleDeg=720,radius=0,duration=3,inf=False):
    global animation
    objID = id(scatterObject)
    scatterObject.size = (scatterObject.width+radius,scatterObject.height+radius)
    animation[objID] = Animation(rotation=angleDeg,duration=duration,t='linear')
    animation[objID].start(scatterObject)
    if inf:
        def callback(ins):
            global animation
            animation[objID] += Animation(rotation=angleDeg,duration=duration,t='linear')
        Clock.schedule_interval(callback, duration*0.25)

def ScatterImage(imgSrc,imgSize,radius=0,**args):
    scatter = Scatter(size=imgSize,pos=(Window.center[0]-imgSize[0]/2.+radius,Window.center[1]-imgSize[1]/2.+radius),do_translation_x=False,do_translation_y=False,do_scale=False,do_rotation=False,auto_bring_to_front=False,size_hint=(None,None),**args)
    scatter.add_widget(Image(source=imgSrc, size=imgSize,size_hint=(None,None)))
    return scatter

class RadialMenu (App):
    def build (self):
        parent = FloatLayout()
        c = CircularLayout()
        bg = Image(source="bg.jpg")
        parent.add_widget(bg)
        wheel = ScatterImage('wheel.png',(400,400))
        parent.add_widget(wheel)
        
        size = (470,470)
        followWheelWrap = Scatter(size=size,pos=(Window.center[0]-225,Window.center[1]-225),size_hint=(None,None))
        folloWheelInnerWrap = Scatter(size=(160,140),pos=(size[0]-160,0),size_hint=(None,None),rotation=-2.5)
        folloWheelInnerWrap.add_widget(Image(source='comparc.png',size_hint=(1,1)))
        followWheelWrap.add_widget(folloWheelInnerWrap)
        
        parent.add_widget(followWheelWrap)
        
        button = [5]
        for i in range(1,6):
            button.append(Button (background_normal = 'img/'+str(i)+'.png', background_down='img/'+str(i)+'.png',size_hint = (None, None), size=(140, 140)))
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
            rotate(scatterImg[i], angleDeg=780*dir,inf=True)
        
        parent.add_widget(c)
        
        def callback(*args):
            c.do_rotation(incrDenom = 30, circDuration = .1)
        def callback2(*args):
            a = Animation(rotation=360,duration=3,t='in_bounce')
            a.start(followWheelWrap)
            
        b = Button(text="click",size_hint=(.1,.1),pos=(0,0))
        b.bind(on_press=callback)
        b2 = Button(text="rotate",size_hint=(.1,.1),pos=(100,0))
        b2.bind(on_press=callback2)
        parent.add_widget(b)
        parent.add_widget(b2)
        
        
        #timePane = Image(source="img/Extended.png",size_hint=(None,None),size=(900,600),allow_stretch=True,keep_ratio=False)
        #parent.add_widget(timePane)
        
        return parent

if __name__ == '__main__':
    RadialMenu().run()
