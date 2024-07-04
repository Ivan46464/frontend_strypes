import os
import requests
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from screens.Home import Home
from common_func import backend, token_store, logout

class BaseRoom(Screen):
    plot_image = ObjectProperty(None)
    image_path = "plot_image.png"
    current_plot_type = None
    plot_endpoint = ""
    predict_endpoint = ""

    def on_enter(self):
        self.ids.base_screen.ids.nav_drawer.set_state("close")
        self.ids.base_screen.ids.nav_drawer.opacity = 0
        Home.update_right_action_items(self)

    def show_plot(self, plot_type):
        self.current_plot_type = plot_type
        if plot_type == "daily":
            url = f"{backend}/api/generate_plot_daily_{self.plot_endpoint}"
        elif plot_type == "weekly":
            url = f"{backend}/api/generate_plot_weekly_{self.plot_endpoint}"
        elif plot_type == "monthly":
            url = f"{backend}/api/generate_plot_monthly_{self.plot_endpoint}"
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
            self.ids.daily_prediction_button.opacity = 1
            self.ids.daily_label.opacity = 0
            self.ids.plot_image.source = self.image_path
            self.ids.plot_image.reload()
            self.ids.plot_image.opacity = 1
        else:
            try:
                error_details = response.json()
                error_message = error_details.get('error', 'Unknown error occurred')
                self.show_dialog("Error", f"Failed to get plot: {error_message}, Wait a little bit till we get information")
            except Exception as e:
                self.show_dialog("Error", "Failed to retrieve plot")

    def show_prediction(self):
        try:
            if self.current_plot_type:
                url = f"{backend}/api/predict_{self.predict_endpoint}_{self.current_plot_type}"
                headers = {
                    'Authorization': f'{token_store.get("vars")["token"]}',
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    prediction = response.json().get(f'predicted_{self.predict_endpoint}')
                    if self.current_plot_type == "daily":
                        self.ids.daily_label.text = f"Prediction for the next day: {round(prediction, 2)}"
                    elif self.current_plot_type == "weekly":
                        self.ids.daily_label.text = f"Prediction for the next week: {round(prediction, 2)}"
                    elif self.current_plot_type == "monthly":
                        self.ids.daily_label.text = f"Prediction for the next month: {round(prediction, 2)}"
                    self.ids.daily_label.opacity = 1
                else:
                    print(f"Failed to fetch prediction for {self.current_plot_type}. Status code: {response.status_code}")
            else:
                print("No plot type selected.")
        except Exception as e:
            print(f'Error: {str(e)}')


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
        self.ids.daily_prediction_button.opacity = 0
        self.ids.daily_label.text = ""
        self.ids.daily_label.opacity = 0
        self.ids.plot_image.source = ""
        self.ids.plot_image.opacity = 0
        if os.path.exists(self.image_path):
            os.remove(self.image_path)

    def logout(self):
        logout(self)
        self.manager.current = "home"
