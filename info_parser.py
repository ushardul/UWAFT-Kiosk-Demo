from time import sleep

class Parser:
    def __init__ (self, parseSource):
        fsource = open(parseSource, 'r')
        self.views = {}
        line = fsource.readline ()
        while ('View' in line):
            v = View ()
            v.title = self._get_property (line)
            self.views [v.title] = v
            line = fsource.readline ()
            while ('Tab' in line):
                vt = ViewTab ()
                v.tabs.append (vt)
                vt.title = self._get_property (line)
                line = fsource.readline ()
                if not 'Text' in line:
                    raise SyntaxError ('Tab text not fully specified') 
                vt.text = self._get_property (line)
                line = fsource.readline ()
                while ('Url' in line):
                    vt.urls.append (self._get_property (line))
                    line = fsource.readline ()
            if 'Video' in line:
                v.video = self._get_property (line)
                line = fsource.readline ()
            while ('Picture' in line):
                v.pictures.append (self._get_property (line))
                line = fsource.readline ()

    def _get_property (self, raw):
        return raw.split (':')[1].lstrip().rstrip()

class View:

    def __init__ (self):
        self.title = 'Information'
        self.tabs = []
        self.pictures = []
        self.video = None

class ViewTab:

    def __init__ (self):
        self.title = 'Tab'
        self.text = 'Hello'
        self.urls = []

if __name__ == '__main__':
    # Config.set ('graphics', 'fullscreen', 'auto')
    Parser ('info.uwaft')
