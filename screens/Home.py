from kivymd.uix.dialog import MDDialog
from kivymd.uix.navigationdrawer import MDNavigationDrawerLabel, MDNavigationDrawerItem
from kivy.uix.screenmanager import Screen
from common_func import logout
from common_func import token_store



class DrawerLabelItem(MDNavigationDrawerLabel):
    pass
class DrawerClickableItem(MDNavigationDrawerItem):
    pass
class Home(Screen):

    def on_enter(self):
        self.update_right_action_items()

    def switch_screen(self, screen_name):
        allowed_screens = ['login', 'register', 'home']
        if screen_name in allowed_screens:
            self.manager.current = screen_name
            print(f"Switching to screen: {screen_name}")
        elif token_store.get("vars")["token"] != "":
            self.manager.current = screen_name
            print(f"Switching to screen: {screen_name}")
        else:
            dialog = MDDialog(
                title="Access Denied",
                text="Please log in to access this feature.",
                size_hint=(0.8, 0.4),
            )
            dialog.elevation = 0
            dialog.open()

    def update_right_action_items(self):
        if token_store.get("vars")["token"] != "":
            self.ids.base_layout.ids.top_app_bar.right_action_items = [["logout", lambda x: self.logout(), "Logout"]]
        else:
            self.ids.base_layout.ids.top_app_bar.right_action_items = [["login", lambda x: self.switch_screen("login"), "Login"],
                                                       ["account-plus", lambda x: self.switch_screen("register"),
                                                        "Register"]]
    def logout(self):
        logout(self)