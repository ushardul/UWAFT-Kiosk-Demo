__all__ = ('CircularLayout', )
import math
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

class CircularLayout (FloatLayout):
    def __init__(self, **kvargs):
        self._max_widgets = 0
        self._trigger_layout = Clock.create_trigger(self._do_layout, -1)
        super (FloatLayout, self).__init__(**kvargs)
        self.bind (children = self._trigger_layout,
                   pos = self._trigger_layout,
                   pos_hint = self._trigger_layout,
                   size_hint = self._trigger_layout,
                   size = self._trigger_layout)

    def _do_layout (self, *largs):
        print 'HERE'
        max_size = 0
        if len(self.children) > self._max_widgets:
            for c in self.children:
                size = math.sqrt(math.pow (c.size[0], 2) + math.pow(c.size[1], 2))
                if size > max_size:
                    max_size = size
            layout_radius = math.ceil (max_size/math.sqrt(2*(1-math.cos(math.pi/len(self.children)))))
            print len (self.children)
            temp_width = temp_height = (layout_radius+max_size)*2
            temp_center_x = (self.pos[0] + temp_width)/2
            temp_center_y = (self.pos[1] + temp_height)/2
            theta = 0
            theta_increment = 2*math.pi/len(self.children)
            
            for c in self.children:
                c.center_x = temp_center_x + math.cos (theta)*layout_radius
                c.center_y = temp_center_y + math.sin (theta)*layout_radius
                theta += theta_increment

            self._max_widgets = len(self.children)

        
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
