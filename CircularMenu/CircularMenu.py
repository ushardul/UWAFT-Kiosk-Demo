import kivy
import math
from kivy.app import App
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import OptionProperty, StringProperty
from circularlayout import CircularLayout

class CircularMenu (CircularLayout):
    rotationCounter = 0

    def __init__(self, update, **kvargs):
        self.update = update
        super (CircularMenu, self).__init__(**kvargs)
    
    def on_touch_down (self, touch):
        # sets which object the touch initially hit
        if self.get_child().collide_point(touch.x, touch.y)== False:
            touch.ud['rotate']=True
            rotationCounter = 0
        else:
            touch.ud['expand']=True

    def on_touch_move (self, touch):
        if 'rotate' in touch.ud:
            # see statics -> moments
            self.rotationCounter += (touch.x - self.center_x)*touch.dy - (touch.y-self.center_y)*touch.dx
            # mess with the > 30000 value to make the wheel rotate faster/slower
            if math.fabs(self.rotationCounter) > 30000:
                self.do_rotation (int(-1*self.rotationCounter/math.fabs(self.rotationCounter)))
                self.rotationCounter = 0
                self.update.rotated()
        elif 'expand' in touch.ud and touch.x-touch.ox > 100:
            self.update.showChild(self.get_child().text)
            
class CustomInfoScreen (AnchorLayout):

    # get rid of the sliding info pane
    def rotated (self):
        self.clear_widgets ()

    # shows the sliding info pane with an animation
    def showChild (self, t):
        if len(self.children) == 0:
            info = Button (text=t, size_hint=(1.0, 0.5), x=self.pos[0], center_y = self.center[1])
            self.add_widget (info)
            animation = Animation(center=self.center,  t='out_quad')
            animation.start (info)

class MainMenu (App):
    def build (self):
        parent = BoxLayout ()

        center_layout = CustomInfoScreen (anchor_y = ('center'), size_hint=(None, None), size=(360, 600))
        c = CircularMenu (center_layout)
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
        
        parent.add_widget (c)
        parent.add_widget (center_layout)
        return parent

if __name__ == '__main__':
    MainMenu().run()
