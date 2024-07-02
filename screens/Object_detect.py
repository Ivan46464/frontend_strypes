import os
import string

import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import ObjectProperty

from common_func import backend, token_store, logout
from screens.Home import Home


class Object_detect(Screen):
    plot_image = ObjectProperty(None)
    image_path = None

    def on_enter(self):
        self.ids.base_screen.ids.nav_drawer.set_state("close")
        self.ids.base_screen.ids.nav_drawer.opacity = 0
        Home.update_right_action_items(self)
    def choose_file(self):
        # Create a popup with buttons for each available drive
        drives = self.get_available_drives()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        for drive in drives:
            btn = Button(text=drive, size_hint_y=None, height=40)
            btn.bind(on_release=self.create_filechooser_popup)
            layout.add_widget(btn)

        spacer = BoxLayout(size_hint_y=None, height=480)
        layout.add_widget(spacer)

        popup = Popup(title='Select Drive', content=layout, size_hint=(0.9, 0.9))
        self.drive_popup = popup
        popup.open()

    def create_filechooser_popup(self, instance):
        drive = instance.text
        self.drive_popup.dismiss()  # Dismiss the drive selection popup

        box = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(path=drive, on_submit=self.load_selected_image)
        back_btn = Button(text="Back", size_hint_y=None, height=40)
        back_btn.bind(on_release=lambda x: self.back_to_drive_selection())

        box.add_widget(filechooser)
        box.add_widget(back_btn)

        popup = Popup(title='Select an Image', content=box, size_hint=(0.9, 0.9))
        self.filechooser_popup = popup  # Store the popup reference to dismiss later
        self.filechooser = filechooser  # Store the filechooser reference to update later
        popup.open()

    def back_to_drive_selection(self):
        self.filechooser_popup.dismiss()
        self.choose_file()

    def load_selected_image(self, filechooser, selection, touch):
        if selection:
            self.image_path = selection[0]
            self.ids.plot_image.source = self.image_path
            self.ids.plot_image.opacity = 1
            self.filechooser_popup.dismiss()

    @staticmethod
    def get_available_drives():
        if os.name == 'nt':
            drives = [f'{d}:\\' for d in string.ascii_uppercase if os.path.exists(f'{d}:\\')]
            return drives
        else:
            return ['/']

    def fetch_prediction(self):
        if not self.image_path:
            print("No image selected")
            return

        url = f"{backend}/api/object_detect"
        headers = {
            'Authorization': f'{token_store.get("vars")["token"]}',
        }
        files = {'file': open(self.image_path, 'rb')}

        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            prediction = response.json().get('results', [])
            self.change_text(", ".join(prediction))
        else:
            print(f"Failed to get prediction: {response.status_code}, {response.text}")

    def change_text(self, prediction):
        self.ids.prediction.text = prediction

    def on_submit(self):
        self.fetch_prediction()

    def logout(self):
        logout(self)
        self.manager.current = "home"


