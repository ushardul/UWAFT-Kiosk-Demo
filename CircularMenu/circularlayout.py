__all__ = ('CircularLayout', )
import math
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

class CircularLayout (FloatLayout):
    def __init__(self, **kvargs):
        self._max_widgets = 0
        self._start_angle = 0
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
        max_size = 0
        max_child = None
        for c in self.children:
            size = math.sqrt(math.pow (c.size[0], 2) + math.pow(c.size[1], 2))/2
            if size > max_size:
                max_size = size
                max_child = c
        
        layout_radius = math.ceil (max_size/math.sqrt(2*(1-math.cos(math.pi/len(self.children)))))
        width_given, height_given = self.size

        width_required = (layout_radius + max_child.size[0])*2
        height_required = (layout_radius + max_child.size[1])*2

        if width_required > width_given:
            pass
        if height_required > height_given:
            pass
        
        temp_center_x = self.pos[0] + layout_radius + max_child.size[0]/2
        temp_center_y = self.pos[1] + layout_radius + max_child.size[1]/2
        
        theta = self._start_angle
        theta_increment = 2*math.pi/len(self.children)
        
        for c in self.children:
            c.center_x = temp_center_x + math.cos (theta)*layout_radius
            c.center_y = temp_center_y + math.sin (theta)*layout_radius
            theta += theta_increment

        self._max_widgets = len(self.children)

    def do_left_rotation (self, steps=1):
        if len(self.children) == 0:
            return
        self._start_angle += 2*math.pi/len(self.children)
        self._do_layout ()

    def do_right_rotation (self, steps=1):
        if len(self.children) == 0:
            return
        self._start_angle -= 2*math.pi/len(self.children)
        self._do_layout ()

    def add_widget (self, widget, index=0):
        widget.bind (
            size = self._trigger_layout,
            size_hint = self._trigger_layout,
            pos = self._trigger_layout,
            pos_hint = self._trigger_layout)
        return super (FloatLayout, self).add_widget (widget, index)

    def remove_widget (self, widget):
        widget.unbind(
            size = self._trigger_layout,
            size_hint = self._trigger_layout,
            pos = self._trigger_layout,
            pos_hint = self._trigger_layout)
        return super(Layout, self).remove_widget(widget)
