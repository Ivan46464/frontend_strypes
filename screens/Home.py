import os

import requests
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.navigationdrawer import MDNavigationDrawerLabel, MDNavigationDrawerItem
from kivy.uix.screenmanager import Screen
from common_func import logout, backend
from common_func import token_store
from kivy.clock import Clock


class DrawerLabelItem(MDNavigationDrawerLabel):
    pass
class DrawerClickableItem(MDNavigationDrawerItem):
    pass
class Home(Screen):
    plot_image = ObjectProperty(None)
    image_path = "plot_image.png"
    plot_endpoint = ""
    def on_enter(self):
        self.update_right_action_items()
        self.ids.base_screen.ids.nav_drawer.set_state("close")
        self.ids.base_screen.ids.nav_drawer.opacity = 0

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
            self.ids.base_screen.ids.top_app_bar.right_action_items = [["logout", lambda x: self.logout(), "Logout"]]
        else:
            self.ids.base_screen.ids.top_app_bar.right_action_items = [["login", lambda x: self.switch_screen("login"), "Login"],
                                                       ["account-plus", lambda x: self.switch_screen("register"),
                                                        "Register"]]

    def show_plot(self, plot_type):

        if plot_type == "daily":
            url = f"{backend}/api/plot_consumption/daily"
        elif plot_type == "weekly":
            url = f"{backend}/api/plot_consumption/weekly"
        elif plot_type == "monthly":
            url = f"{backend}/api/plot_consumption/monthly"
        else:
            print(f"Invalid plot type: {plot_type}")
            return

        headers = {
            'Authorization': f'{token_store.get("vars")["token"]}',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(self.image_path, "wb") as f:
                f.write(response.content)
            self.ids.plot_image.source = self.image_path
            self.ids.plot_image.reload()
            self.ids.plot_image.opacity = 1
        else:
            if token_store.get("vars")["token"] == "":
                self.show_dialog("Not logged in", "You have to log in to access these features")
                return
            try:
                error_details = response.json()
                error_message = error_details.get('error', 'Unknown error occurred')
                self.show_dialog("Error",
                                 f"Failed to get plot: {error_message}, Wait a little bit till we get information")
            except Exception as e:
                print(response.status_code)
                self.show_dialog("Error", "Failed to retrieve plot")



    def show_dialog(self, title, message):
        dialog = MDDialog(
            title=title,
            text=message,
            size_hint=(0.8, 0.4),
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.elevation = 0
        dialog.open()
    def on_leave(self):
        self.ids.plot_image.source = ""
        self.ids.plot_image.opacity = 0
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
    def logout(self):
        logout(self)
