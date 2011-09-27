'''
Widget animation
================

This is showing an example of a animation creation, and how you can apply yo a
widget.
'''
import kivy
import math
kivy.require('1.0.7')

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):

    @staticmethod
    def calculateIncrement (radius, startAngle, endAngle):
        # Should do some calculations to ensure a smooth rotation given
        # the parameters rather than arbritary hard coded value
        _INCREMENT = math.pi/200
        return _INCREMENT

    @staticmethod
    def createArcAnimation (circDuration, center, radius, startAngle, endAngle):
        arcPos = (center[0] + math.cos (startAngle)*radius, center[1] + math.sin (startAngle)*radius)
        arcAnim = Animation (pos = arcPos, duration = 0.15, t='linear')
        animIncrement = TestApp.calculateIncrement (radius, startAngle, endAngle)
        steps = (int)(math.ceil ((endAngle - startAngle)/animIncrement))
        singleDuration = circDuration/(steps + 0.0)
        if startAngle > endAngle:
            animIncrement *= -1
        startAngle += animIncrement
        arcPos = (center[0] + math.cos (startAngle)*radius, center[1] + math.sin (startAngle)*radius)
        arcAnim = arcAnim + Animation (pos=arcPos, duration = singleDuration, t='in_quad')
        for i in range (2, steps):
            startAngle += animIncrement
            if animIncrement < 0 and startAngle < endAngle:
                startAngle = endAngle
            elif animIncrement > 0 and startAngle > endAngle:
                startAngle = endAngle;
            arcPos = (center[0] + math.cos (startAngle)*radius, center[1] + math.sin (startAngle)*radius)
            arcAnim = arcAnim + Animation (pos=arcPos, duration = singleDuration, t='linear')
        startAngle += animIncrement
        arcPos = (center[0] + math.cos (startAngle)*radius, center[1] + math.sin (startAngle)*radius)
        arcAnim = arcAnim + Animation (pos=arcPos, duration = singleDuration, t='out_quad')
        return arcAnim

    def animate(self, instance):
        animation = TestApp.createArcAnimation (1, (300, 200), 300, 0, math.pi)
        animation.start (instance)

    def build(self):
        # create a button, and  attach animate() method as a on_press handler
        button = Button(size_hint=(None, None), text='plop', pos=(200, 200))
        button.bind(on_press=self.animate)
        return button

if __name__ in ('__main__', '__android__'):
    TestApp ().run ()

