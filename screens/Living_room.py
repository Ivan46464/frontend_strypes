import os

import requests
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from common_func import backend, token_store, logout
from screens.Home import Home


class LivingRoom(Screen):
    plot_image = ObjectProperty(None)
    image_path = "plot_image.png"

    def on_enter(self):
        self.ids.base_screen.ids.nav_drawer.set_state("close")
        self.ids.base_screen.ids.nav_drawer.opacity = 0
        Home.update_right_action_items(self)


    def show_plot(self, plot_type):

        if plot_type == "daily":
            url = f"{backend}/api/generate_plot_daily_sub_metering_3"
        elif plot_type == "weekly":
            url = f"{backend}/api/generate_plot_weekly_sub_metering_3"
        elif plot_type == "monthly":
            url = f"{backend}/api/generate_plot_monthly_sub_metering_3"
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
            print(f"Failed to retrieve {plot_type} plot")

    def on_leave(self):
        self.ids.plot_image.source = ""
        self.ids.plot_image.opacity = 0
        if os.path.exists(self.image_path):
            os.remove(self.image_path)

    def logout(self):
        logout(self)
        self.manager.current = "home"