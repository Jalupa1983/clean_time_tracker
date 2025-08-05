from kivy.app import App
from kivy.uix.image import Image

class TestApp(App):
    def build(self):
        return Image(source="images/test.png")  # Change to your image name

TestApp().run()
