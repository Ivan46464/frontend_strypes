
from kivymd.uix.navigationdrawer import MDNavigationDrawerLabel, MDNavigationDrawerItem
from kivy.uix.screenmanager import Screen
class DrawerLabelItem(MDNavigationDrawerLabel):
    pass
class DrawerClickableItem(MDNavigationDrawerItem):
    pass
class Home(Screen):
    def switch_screen(self, screen_name):
        self.manager.current = screen_name
        print(f"Switching to screen: {screen_name}")