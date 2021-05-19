import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout 
from kivy.core.window import Window
from kivy.config import Config
from kivy.graphics import *
Config.set('postproc', 'window_state', 'maximized')
#Window.borderless = True
#Window.fullscreen = '1'

class TestApp(App):
	def build(self):
		root = BoxLayout()
		with root.canvas:
			Color(1, 1, 1)
			Rectangle(pos=root.pos, size=(1500,1500))
		return root

TestApp().run()