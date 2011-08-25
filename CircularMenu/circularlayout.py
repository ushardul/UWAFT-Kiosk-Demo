__all__ = ('CircularLayout', )
import math
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

class CircularLayout (FloatLayout):
    def __init__(self, **kvargs):
        # The max widgets that the layout can hold, I think it does not have a purpose but I havent checked
        self._max_widgets = 0
        # Stores which widget is exactly to the right, even after rotation
        self._first_widget = -1
        # Kivy docs explain timers
        self._trigger_layout = Clock.create_trigger(self._do_layout, -1)
        super (FloatLayout, self).__init__(**kvargs)
        # Any changes to these attributes will trigger a method call to _do_layout at the earliest time possible
        self.bind (children = self._trigger_layout,
                   pos = self._trigger_layout,
                   pos_hint = self._trigger_layout,
                   size_hint = self._trigger_layout,
                   size = self._trigger_layout)

    def _do_layout (self, *largs):
        if len(self.children) == 0:
            return
        # see above
        self._max_widgets = num_widgets = len(self.children)
        # stores in local variables for efficient access
        temp_center_x, temp_center_y = self.center
        children = self.children[:]

        
        max_width = max_height = 0
        # looks for the max possible diagonal that can occur by finding max possible width and height
        for c in children:
            csx, csy = c.size
            if csx > max_width:
                max_width = csx
            if csy > max_height:
                max_height = csy
        max_diagonal = math.sqrt (max_width*max_width + max_height*max_height)

        # Some math to calculate minimum radius required to a widget given widget radius (max_diagonal/2)
        # and number of widgets. Math works I believe
        layout_radius = math.ceil (max_diagonal/2/math.sqrt(2*(1-math.cos(math.pi/len(children)))))

        # Iterates at each angle starting with the first widget set by the variable _first_widget
        # and does some work to find the widget's position
        theta = 0
        theta_increment = 2*math.pi/len(self.children)
        i = self._first_widget

        # No do/while loop in python so implemented as an infinite loop with a break
        # Basically, the first widget can be anywhere in the list and each widget in the list must be drawn in order
        # from that first widget including the ones behind it in terms of index
        # So, iterates with modulo operations
        while True:
            new_center = temp_center_x + math.cos (theta)*layout_radius, temp_center_y + math.sin (theta)*layout_radius
            self.reposition_child (children[i], center=new_center)
            theta += theta_increment
            i = (i - 1)%num_widgets
            if i == self._first_widget:
                break

    def do_rotation (self, steps=1):
        # Some modulo operations used to rotate the first child position
        num_widgets = len(self.children)
        if num_widgets == 0:
            return
        steps %= num_widgets
        self._first_widget = (self._first_widget - steps)%num_widgets
        self._do_layout ()

    def get_child (self, index=0):
        return self.children[(self._first_widget + index)%len(self.children)]

    def add_widget (self, widget, index=0):
        # Binds the new widget callback so that the layout is rearranged when a new widget is added
        self._first_widget += 1
        widget.bind (
            size = self._trigger_layout,
            size_hint = self._trigger_layout,
            pos = self._trigger_layout,
            pos_hint = self._trigger_layout)
        return super (FloatLayout, self).add_widget (widget, index)

    def remove_widget (self, widget):
        # Binds the new widget callback so that the layout is rearranged when a new widget is added
        self._first_widget -= 1
        widget.unbind(
            size = self._trigger_layout,
            size_hint = self._trigger_layout,
            pos = self._trigger_layout,
            pos_hint = self._trigger_layout)
        return super(Layout, self).remove_widget(widget)
