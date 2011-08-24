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

    def animate(self, instance):
        divisor = 3
        max_rad = math.pi/2
        increment = math.pi/divisor
        animation = Animation(pos=(300, 200),  t='linear')
        for i in range(1,math.floor (max_rad/increment) + 1):
            # create an animation object. 
            animation = animation + Animation(pos=(math.cos(increment*i)*100+200, math.sin(increment*i)*100+200), t='linear')

            # apply the animation on the button, passed in the "instance" argument
        animation.start(instance)

    def build(self):
        # create a button, and  attach animate() method as a on_press handler
        button = Button(size_hint=(None, None), text='plop', pos=(200, 200))
        button.bind(on_press=self.animate)
        return button

if __name__ in ('__main__', '__android__'):
    TestApp().run()

