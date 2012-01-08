import kivy
kivy.require('1.0.9')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.config import Config
from tablayout import TabLayout
from tablayout import Tab
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.image import Image

class InformationView(BoxLayout):
    tab_cont = ObjectProperty(None)
    title = StringProperty ('Title')
    pic_cont = ObjectProperty (None)
    vid_src = StringProperty ('')
    vid_cont = ObjectProperty (None)

    def __init__ (self, title, tabs, video = None, pictures = [], **kvargs):
        super (BoxLayout, self).__init__(**kvargs)
        self.title = title

        t_lyt = TabLayout ()
        for tab in tabs:
            t_lyt.add_tab (tab)
        self.tab_cont.add_widget (t_lyt)
        
        if video is None:
            self.vid_cont.parent.remove_widget (self.vid_cont)
        else:
            self.vid_src = video
        if len (pictures) == 0:
            self.pic_cont.parent.remove_widget (self.pic_cont)
        else:
            for picture in pictures:
                self.pic_cont.add_widget (picture)
                picture.bind (height=self.testchange)

    def testchange (self, wid, value):
        wid.width = wid.image_ratio * value

class InformationApp(App):
    def build (self):
        p = Parser ('C:\Users\Shardul\Desktop\UWAFT-Kiosk-Demo\info.uwaft')
        return p.get_view ('Some Other View')

class Parser:
    def __init__ (self, parseSource):
        fsource = open(parseSource, 'r')
        self.views = {}
        line = fsource.readline ()
        while ('View' in line):
            v_title = self._get_property (line)
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
                temp_image = Image (source=self._get_property (line), size_hint=(None, 1), allow_stretch = True, keep_ratio = False)
                v_pictures.append (temp_image)
                line = fsource.readline ()
            
            self.views [v_title] = InformationView (v_title, tabs, v_video, v_pictures)
        if len (self.views) == 0:
            raise SyntaxError ('No views specified')

    def _get_property (self, raw):
        return raw.split (':')[1].lstrip().rstrip()

    def _set_text_size (self, wid, size):
        wid.text_size = size

    def get_view (self, name):
        return self.views[name]
    

class View:

    def __init__ (self):
        self.title = 'Information'
        self.tabs = []
        self.pictures = []
        self.video = None

if __name__ == '__main__':
    # Config.set ('graphics', 'fullscreen', 'auto')
    InformationApp().run()
