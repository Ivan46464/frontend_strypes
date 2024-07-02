import requests
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex
from kivymd.uix.dialog import MDDialog
import re
from common_func import backend, token_store


class Register(Screen):
    def on_enter(self):
        self.ids.base_screen.ids.nav_drawer.set_state("close")
        self.ids.base_screen.ids.nav_drawer.opacity = 0
    def show_error(self, widget):
        widget.error = True
        widget.background_color = get_color_from_hex("#FF0000")

    def clear_error(self, widget):
        # Clear the error indication
        widget.error = False
        widget.background_color = get_color_from_hex("#FFFFFF")

    def validate_inputs(self):
        email = self.ids.ml
        username = self.ids.urnm
        password = self.ids.pswrd
        password_confirm = self.ids.cnfrm
        is_valid = True
        if not email.text or not self.check_email():
            self.show_error(email)
            is_valid = False
        else:
            self.clear_error(email)

        if not password.text:
            self.show_error(password)
            is_valid =  False
        else:
            self.clear_error(password)

        if not password_confirm.text:
            self.show_error(password_confirm)
            is_valid = False
        else:
            self.clear_error(password_confirm)

        if password.text != password_confirm.text:
            self.show_error(password)
            self.show_error(password_confirm)
            is_valid = False
        else:
            self.clear_error(password)
            self.clear_error(password_confirm)

        if not username.text:
            self.show_error(username)
            is_valid =  False
        else:
            self.clear_error(username)

        return is_valid
    def check_email(self):
        email = self.ids.ml.text
        email_check = re.match(r"^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}$", email)
        return bool(email_check)
    def register(self):
        if not self.validate_inputs():
            return
        self.validate_inputs()
        email = self.ids.ml.text
        username = self.ids.urnm.text
        password = self.ids.pswrd.text
        data = {
            "email": email,
            "username": username,
            "password": password
        }
        url = f"{backend}/api/register"
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                token_response = response.json()
                self.switch_screen("home")
                print(token_response)
                token_store.put("vars", token="Token " + token_response.get("token"))
            else:
                dialog = MDDialog(
                    title="Username or email already used",
                    text="Please try another.",
                    size_hint=(0.8, 0.4),
                )
                dialog.elevation = 0
                dialog.open()
                print("Failed to fetch sessions. Status code:", response.status_code)
        except Exception as e:
            print("An error occurred while fetching sessions:", str(e))

    def switch_screen(self, screen_name):
        self.manager.current = screen_name
        print(f"Switching to screen: {screen_name}")
