import os
import string

import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

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
        self.drive_popup.dismiss()

        box = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(path=drive, on_submit=self.load_selected_image)
        back_btn = Button(text="Back", size_hint_y=None, height=40)
        back_btn.bind(on_release=lambda x: self.back_to_drive_selection())

        box.add_widget(filechooser)
        box.add_widget(back_btn)

        popup = Popup(title='Select an Image', content=box, size_hint=(0.9, 0.9))
        self.filechooser_popup = popup
        self.filechooser = filechooser
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
            self.show_location_dialog(prediction)
        else:
            print(f"Failed to get prediction: {response.status_code}, {response.text}")

    def change_text(self, prediction):
        self.ids.prediction.text = prediction

    def show_location_dialog(self, prediction):
        places = {
            "living room": ['Dining table', "TV", 'Laptop'],
            "kitchen": ['Microwave', 'Oven', 'Refrigerator', 'Sink', 'Toaster'],
            "laundry room": ["Sink", "Toilet"],
        }

        object_locations = {}
        for obj in prediction:
            for place, items in places.items():
                if obj in items:
                    if place not in object_locations:
                        object_locations[place] = []
                    object_locations[place].append(obj)

        if not object_locations:
            self.show_dialog("Info", "No known objects found in the predefined locations.")
            return

        message_parts = []
        for place, objects in object_locations.items():
            objects_str = ", ".join(objects)
            message_parts.append(f"{objects_str} belong(s) in the {place}")

        message = " and ".join(message_parts)
        self.show_dialog("Success", message)
    def on_submit(self):
        self.fetch_prediction()

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
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
    def logout(self):
        logout(self)
        self.manager.current = "home"
    def on_leave(self):
        self.ids.plot_image.source = ""
        self.ids.plot_image.opacity = 0
        self.change_text("")



