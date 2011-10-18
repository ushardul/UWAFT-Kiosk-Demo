from CircularAnimationUtilities import CircularAnimationUtilities

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button


class TestApp(App):

    def animate(self, instance):
        animation = CircularAnimationUtilities.createArcAnimation (1, (100, 100), 50, 0, -3.14)

        # apply the animation on the button, passed in the "instance" argument
        animation.start(instance)

    def build(self):
        # create a button, and  attach animate() method as a on_press handler
        button = Button(size_hint=(None, None), text='plop')
        button.bind(on_press=self.animate)
        return button

if __name__ == '__main__':
   TestApp().run ()
