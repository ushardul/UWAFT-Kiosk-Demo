__all__ = ('CircularLayout',)
import math
import types
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from CircularAnimationUtilities import CircularAnimationUtilities
from kivy.animation import Animation

class CircularLayout (FloatLayout):
    def __init__ (self, radius = 0, **kvargs):
        self._first_widget = -1
        self._layout_radius = radius
        super (CircularLayout, self).__init__ (**kvargs)

    def _do_layout (self,*largs):
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

    def do_rotation (self, callback=None, steps = 1, incrDenom = 100, circDuration=10, radius = 0):
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
            theta += THETA_INCREMENT

        i = self._first_widget
        
        #bind the callback function to the first widget if a callback is sent as parameter
        if type(callback) == types.FunctionType:
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
        return super (FloatLayout, self).add_widget (widget, index)

    # Binds the remove widget callback so that layout is rearranged when
    # a widget is removed and changes the first widget
    def remove_widget (self, widget):
        self._first_widget -= 1
        return super (FloatLayout, self).remove_widget (widget)
