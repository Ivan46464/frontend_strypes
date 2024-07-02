import re

import requests
from kivy.properties import get_color_from_hex
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog

from common_func import token_store,backend


class Login(Screen):
    def on_enter(self):
        self.ids.base_screen.ids.nav_drawer.set_state("close")
        self.ids.base_screen.ids.nav_drawer.opacity = 0
    def show_error(self, widget):
        widget.error = True
        widget.background_color = get_color_from_hex("#FF0000")

    def clear_error(self, widget):
        widget.error = False
        widget.background_color = get_color_from_hex("#FFFFFF")

    def validate_inputs(self):
        password = self.ids.psswrd
        username = self.ids.usrnm
        is_valid = True

        if not password.text:
            self.show_error(password)
            is_valid = False
        else:
            self.clear_error(password)

        if not username.text:
            self.show_error(username)
            is_valid = False
        else:
            self.clear_error(username)

        return is_valid
    def get_token(self):

        if not self.validate_inputs():
            return
        username = self.ids.usrnm.text
        password = self.ids.psswrd.text
        url = f"{backend}/api/login"
        payload = {
            "username": username,
            "password": password
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                token_response = response.json()
                print(token_response)
                token_store.put("vars", token="Token " + token_response.get("token"))
                self.manager.current = "home"
            else:
                dialog = MDDialog(
                    title="Wrong username or password",
                    text="Please input correct information",
                    size_hint=(0.8, 0.4),
                    background_color=(1, 1, 1, 0)
                )
                dialog.elevation = 0
                dialog.open()
                print("Status code:", response.status_code)
        except Exception as e:
            print("An error occurred: ", str(e))
