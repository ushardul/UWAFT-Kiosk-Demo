__all__ = ('CircularLayout',)
import math
import types
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from CircularAnimationUtilities import CircularAnimationUtilities
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from info_display import Parser

class CircularLayout (FloatLayout):
    def __init__ (self, fin=None, radius = 0, pushAnimate=False,**kvargs):
        self._first_widget = -1
        self._layout_radius = radius
        self.pushAnimate = pushAnimate
        self.p = fin
        super (CircularLayout, self).__init__ (**kvargs)
    
    def infoView(self,a,img):
        self.do_layout()
        self.parent.parent.parent.parent.remove_widget(self.screen)
        view = self.p.get_view(img.button.background_normal)
        self.parent.parent.parent.parent.add_widget(view)
        view.set_up()
    
    def windowFade(self,anim,button):
        self.screen = Image(size=Window.size,color=(0,0,0,0))
        self.screen.button = button
        self.parent.parent.parent.parent.add_widget(self.screen,0)
        animation = Animation(color=(0,0,0,1),duration=0.5,t="linear")
        animation.bind(on_complete=self.infoView)
        animation.start(self.screen)
        
    def icon_vector_anim(self,button):
        center = self.center
        bCenter = button.center
        children = self.children
        theta = math.atan2(bCenter[1] - center[1],bCenter[0]-center[0])
        r = 20
        x = bCenter[0] + r*math.cos(theta)
        y = bCenter[1] + r*math.sin(theta)
        animation = Animation(center=(x,y),duration=0.5,t="out_back")
        animation.bind(on_complete=self.windowFade)
        animation.start(button)
    
    def do_layout (self,*largs):
        if len (self.children) == 0:
            return
        # local variable initialization for efficiency
        CENTER = self.center
        children = self.children [:]
        NUM_WIDGETS = len(children)
        max_width = max_height = 0

        # find the max widths and heights
        for c in children:
            csx, csy = c.size
            if csx > max_width:
                max_width = csx
            if csy > max_height:
                max_height = csy
        # It is now known that an object with the greatest diagonal in the layout
        # will at MOST have a width and height equal to the max width and height
        max_diagonal = math.sqrt (max_width*max_width + max_height*max_height)
        self.maxRadius = max_diagonal
        # The required radius is calculated using arc sectors and cosine law
        if self._layout_radius == 0:
            self._layout_radius = math.ceil (max_diagonal/2/math.sqrt (2*(1 - math.cos (math.pi/NUM_WIDGETS))))
        LAYOUT_RADIUS = self._layout_radius

        # Now simply position the center of the children's evenly over the circle
        theta = 0
        THETA_INCREMENT = 2*math.pi/NUM_WIDGETS
        i = self._first_widget
        # Using modulous operations, starts laying out children from the "first"
        # child specified - the child directly to the right in the layout
        while True:
            center2=(CENTER[0] + math.cos (theta)*LAYOUT_RADIUS, CENTER[1] + math.sin (theta)*LAYOUT_RADIUS)
            self.reposition_child(children[i],
                                  center=(CENTER[0] + math.cos (theta)*LAYOUT_RADIUS, CENTER[1] + math.sin (theta)*LAYOUT_RADIUS))
            theta += THETA_INCREMENT
            i = (i - 1)%NUM_WIDGETS
            if i == self._first_widget:
                break

    def do_rotation (self, callback=None, oncall=None, steps = 1, incrDenom = 100, circDuration=10, radius = 0):
        if radius == 0:
            radius = self._layout_radius
        NUM_WIDGETS = len(self.children)
        if NUM_WIDGETS == 0:
            return
        animations = []
        
        theta = 0
        negative = 1

        if (steps > 0):
            negative = -1

        THETA_INCREMENT = 2*math.pi/NUM_WIDGETS*negative
        
        for i in range (0, NUM_WIDGETS):
            animations.append (CircularAnimationUtilities.createArcAnimation(circDuration, self.center, radius, theta, theta + THETA_INCREMENT,incrDenom))
            animations[i].bind(on_progress=oncall)
            theta += THETA_INCREMENT

        i = self._first_widget
        
        #bind the callback function to the first widget if a callback is sent as parameter
        if callback != None:
            animations[i].bind(on_complete=callback)
        
        animIndex = 0
        children = self.children [:]
        while True:
            animations[animIndex].start (children[i])
            animIndex += 1
            i = (i - negative)%NUM_WIDGETS
            if i == self._first_widget:
                break

        self._first_widget = (self._first_widget - steps)%NUM_WIDGETS
                        

    # Gets children as the first children being the one immediately to the right
    def get_child (self, index=0):
        return self.children[(self._first_widget + index)%len(self.children)]


    # Binds the new widget callback so that the layout is rearranged when
    # a new widget is added and changes the first widget
    def add_widget (self, widget, index=0):
        self._first_widget += 1
        widget.bind(on_press=self.icon_vector_anim)
        return super (FloatLayout, self).add_widget (widget, index)

    # Binds the remove widget callback so that layout is rearranged when
    # a widget is removed and changes the first widget
    def remove_widget (self, widget):
        self._first_widget -= 1
        return super (FloatLayout, self).remove_widget (widget)
