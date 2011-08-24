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

        max_width = max_height = 0
        max_width_child = max_height_child = None
        wg, hg = self.size
        children = self.children[:]
        
        for c in children:
            csx, csy = c.size
            if c.size[0] > max_width:
                max_width = c.size[0]
                max_width_child = c
            if c.size[1] > max_height:
                max_height = c.size[1]
                max_height_child = c
                
        max_diagonal = math.sqrt (max_width*max_width + max_height*max_height)
        
        layout_radius = math.ceil (max_diagonal/2/math.sqrt(2*(1-math.cos(math.pi/len(children)))))
        
        wr = layout_radius*2 + max_width
        hr = layout_radius*2 + max_height
        cf_x = cf_y = 1
        
        if wr > wg:
            cf_x = (wg - 2*layout_radius)/max_width
            if cf_x < 0.3:
                cf_x = 0.3
        if hr > hg:
            cf_y = (hg - 2*layout_radius)/max_height
            if cf_y < 0.3:
                cf_y = 0.3
            
        max_width, max_height = cf_x * max_width, cf_y*max_height
        max_diagonal = math.sqrt(math.pow (cf_x*max_width, 2) + math.pow (cf_y*max_height, 2))
            
        layout_radius = math.ceil (max_diagonal/2/math.sqrt(2*(1-math.cos(math.pi/len(children)))))
        temp_center_x = self.pos[0] + layout_radius + max_width/2
        temp_center_y = self.pos[1] + layout_radius + max_height/2
        theta = 0
        theta_increment = 2*math.pi/len(self.children)
        i = self._first_widget

        while True:
            new_center = temp_center_x + math.cos (theta)*layout_radius, temp_center_y + math.sin (theta)*layout_radius
            csx, csy = children[i].size
            if (layout_radius*2 + csx) > max_width:
                csx = cf_x*csx
            if (layout_radius*2 + csy) > max_height:
                csy = cf_y*csy
            self.reposition_child (children[i], center=new_center, size=(csx, csy))
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
