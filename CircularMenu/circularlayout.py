__all__ = ('CircularLayout', )
import math
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

class CircularLayout (FloatLayout):
    def __init__(self, **kvargs):
        self._max_widgets = 0
        self._first_widget = -1
        self._trigger_layout = Clock.create_trigger(self._do_layout, -1)
        super (FloatLayout, self).__init__(**kvargs)
        self.bind (children = self._trigger_layout,
                   pos = self._trigger_layout,
                   pos_hint = self._trigger_layout,
                   size_hint = self._trigger_layout,
                   size = self._trigger_layout)

    def _do_layout (self, *largs):
        if len(self.children) == 0:
            return
        self._max_widgets = num_widgets = len(self.children)
        temp_center_x, temp_center_y = self.center
        max_width = max_height = 0
        children = self.children[:]
        
        for c in children:
            csx, csy = c.size
            if csx > max_width:
                max_width = csx
            if csy > max_height:
                max_height = csy
                
        max_diagonal = math.sqrt (max_width*max_width + max_height*max_height)
        layout_radius = math.ceil (max_diagonal/2/math.sqrt(2*(1-math.cos(math.pi/len(children)))))
                
        theta = 0
        theta_increment = 2*math.pi/len(self.children)
        i = self._first_widget

        while True:
            new_center = temp_center_x + math.cos (theta)*layout_radius, temp_center_y + math.sin (theta)*layout_radius
            self.reposition_child (children[i], center=new_center)
            theta += theta_increment
            i = (i - 1)%num_widgets
            if i == self._first_widget:
                break

    def do_rotation (self, steps=1):
        num_widgets = len(self.children)
        if num_widgets == 0:
            return
        steps %= num_widgets
        self._first_widget = (self._first_widget - steps)%num_widgets
        self._do_layout ()

    def get_child (self, index=0):
        return self.children[(self._first_widget + index)%len(self.children)]

    def add_widget (self, widget, index=0):
        self._first_widget += 1
        widget.bind (
            size = self._trigger_layout,
            size_hint = self._trigger_layout,
            pos = self._trigger_layout,
            pos_hint = self._trigger_layout)
        return super (FloatLayout, self).add_widget (widget, index)

    def remove_widget (self, widget):
        self._first_widget -= 1
        widget.unbind(
            size = self._trigger_layout,
            size_hint = self._trigger_layout,
            pos = self._trigger_layout,
            pos_hint = self._trigger_layout)
        return super(Layout, self).remove_widget(widget)
