import kivy
kivy.require('1.0.9')

import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.config import Config
from tablayout import TabLayout
from tablayout import Tab
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *

class ExpandableImage (FloatLayout):

    def __init__ (self, _img_source, expansion_cont, **kvargs):
        super (ExpandableImage, self).__init__(**kvargs)

        self._expansion_cont = expansion_cont
        
        self._img = Image (source = _img_source,
                           pos_hint={'x':0, 'y':0})
        
        self._btn = Button (text='Show',
                            pos_hint={'top':1, 'center_x':0.5},
                            size_hint=(0.4, 0.2),
                            background_color=(1,1,1,0.75))
        self._btn.bind (on_release=self._add_expanded_image)

    def set_up (self):
        self.add_widget (self._img)
        self.add_widget (self._btn)

    def _add_expanded_image (self, wid):
        for child in self._expansion_cont.children:
            if type (child) == FloatLayout:
                self._expansion_cont.remove_widget (child)
        self.pre_cont = FloatLayout (size_hint = (1, 1))
        self.pre_cont.canvas.add (Color (0,0,0,0.75))
        self.pre_cont.canvas.add (Rectangle (size=self._expansion_cont.size))
        _image = Image (source = self._img.source,
                        pos_hint={'center_x':0.5, 'center_y':0.5},
                        keep_ratio =False, allow_stretch=True, 
                        size_hint=(0.8, 0.8))
        _btn = Button (text='Hide', size_hint= (0.1, 0.8),
                       background_color=(1,1,1,0.75))
        
        def _center (wid, value):
            _btn.right = _image.right
            _btn.center_y = ((_image.top-_image.y)*0.5) + _image.y
            
        _image.bind (pos = _center)
        _btn.bind (on_release =self._rmv_expanded_image)
        self.pre_cont.add_widget (_image)
        self.pre_cont.add_widget (_btn)
        self._expansion_cont.add_widget (self.pre_cont)
    
    def _rmv_expanded_image (self, touch):
        self.pre_cont.parent.remove_widget (self.pre_cont)

class InformationView(BoxLayout):
    tab_cont = ObjectProperty(None)
    title = StringProperty ('Title')
    icon = StringProperty (None)
    pic_cont = ObjectProperty (None)
    vid_cont = ObjectProperty (None)
    t_lyt = None
    pictures = None

    def __init__ (self, title, icon, tabs, video = None, pictures = [], **kvargs):
        super (BoxLayout, self).__init__(**kvargs)        
        self.title = title

        self.icon = icon

        self.t_lyt = TabLayout ()
        for tab in tabs:
            self.t_lyt.add_tab (tab)
        
        if video is None:
            self.vid_cont.parent.remove_widget (self.vid_cont)
        else:
            self.vid_cont.source = video
            self.vid_cont.on_touch_down = self._click_vid
        self.pictures = pictures
        self.temp = Button (size_hint = (1, 1))

    def set_up (self):
        self.tab_cont.add_widget (self.t_lyt)
        for picture in self.pictures:
            ex = ExpandableImage (picture, self.parent)
            ex.set_up ()
            self.pic_cont.add_widget (ex)
        self.vid_cont.bind (size=self._draw_video_overlay)

    def _draw_video_overlay (self, wid, touch):
        draw = wid.canvas.after
        draw.clear ()
        draw.add (Color (0,0,0,0.75))
        draw.add (Rectangle (pos=self.vid_cont.pos, size=self.vid_cont.size))
        center = (wid.x +wid.width/2, wid.y + wid.height/2)
        side_len = 50
        altitude = math.sqrt (side_len*side_len - (side_len/2)*(side_len/2))
        point1 = (center[0]-altitude/2, center[1] + side_len/2)
        point2 = (point1[0], center[1]-side_len/2)
        point3 = (center[0] + altitude/2, center[1])
        draw.add (Color (1,1,1,1))
        draw.add (Triangle (points=(point1[0],point1[1],point2[0],point2[1],point3[0],point3[1])))

    def _click_vid (self, touch):
        if self.vid_cont.collide_point (touch.x, touch.y):
            if self.vid_cont.play == True:
                self._draw_video_overlay (self.vid_cont, None)
            else:
                self.vid_cont.canvas.after.clear ()
            self.vid_cont.play = not (self.vid_cont.play)

class InformationApp(App):
    def build (self):
        p = Parser ('info.uwaft')
        add = p.get_view ('img/icon2.png')
        top = FloatLayout (size_hint=(1, 1))
        top.add_widget (add)
        add.set_up ()
        return top

class Parser:
    def __init__ (self, parseSource):
        fsource = open(parseSource, 'r')
        self.views = {}
        line = fsource.readline ()
        while ('View' in line):
            v_title = self._get_property (line)
            line = fsource.readline ()
            v_icon = self._get_property (line)
            line = fsource.readline ()
            tabs = []
            while ('Tab' in line):
                cont_temp = BoxLayout (orientation='horizontal')
                vt = Tab (self._get_property (line), cont_temp)
                tabs.append (vt)
                line = fsource.readline ()
                if not 'Text' in line:
                    raise SyntaxError ('Tab text not fully specified')
                
                txt_wrapper = BoxLayout (orientation='horizontal', size_hint=(0.85, 1))
                txt_cnt = Label (text=self._get_property (line), valign='top')
                txt_wrapper.add_widget (txt_cnt)
                txt_cnt.bind (size=self._set_text_size)
                cont_temp.add_widget (txt_wrapper)
                line = fsource.readline ()
                url_cont = BoxLayout (orientation='vertical', size_hint=(0.15, 1), padding=10)
                cont_temp.add_widget (url_cont)
                while ('Url' in line):
                    txt_cnt = Label (text=self._get_property (line))
                    url_cont.add_widget(txt_cnt)
                    line = fsource.readline ()
            if len (tabs) == 0:
                raise SyntaxError ('No tabs specified for view')
            
            v_video = None
            if 'Video' in line:
                v_video = self._get_property (line)
                line = fsource.readline ()
            v_pictures = []
            while ('Picture' in line):
                v_pictures.append (self._get_property (line))
                line = fsource.readline ()
            
            self.views [v_icon] = InformationView (v_title, v_icon, tabs, v_video, v_pictures)
        if len (self.views) == 0:
            raise SyntaxError ('No views specified')

    def _get_property (self, raw):
        temp = raw.split (':')
        if len (temp) != 2:
            raise SyntaxError ('Required property value not defined')
        return temp[1].lstrip().rstrip()

    def _set_text_size (self, wid, size):
        wid.text_size = size

    def get_view (self, name):
        return self.views[name]

if __name__ == '__main__':
    Config.set ('graphics', 'fullscreen', 'auto')
    InformationApp().run()
