from kivy import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from screens.Home import Home
from screens.Login import Login
from screens.Register import Register
from common_func import token_store
Config.set('graphics', 'fullscreen', 'auto')
Window.size = (400, 600)


from kivy.uix.floatlayout import FloatLayout

class Base(FloatLayout):
    pass


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "900"
        Builder.load_file("Base.kv")
        Builder.load_file("Home.kv")
        Builder.load_file("Login.kv")
        Builder.load_file("Register.kv")
        sm = ScreenManager()
        sm.add_widget(Home(name="home"))
        sm.add_widget(Login(name="login"))
        sm.add_widget(Register(name="register"))
        print("Screens added to ScreenManager:", sm.screen_names)
        return sm

    def callback(self):
        print("Menu button clicked!")

Example().run()
