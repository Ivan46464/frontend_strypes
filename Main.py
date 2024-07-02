import requests
from kivy import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from common_func import backend, token_store
from screens.Global_active_power import Global_active_power
from screens.Home import Home
from screens.Kitchen import Kitchen
from screens.Laundry_room import LaundryRoom
from screens.Living_room import LivingRoom
from screens.Login import Login
from screens.Object_detect import Object_detect
from screens.Register import Register
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
        Builder.load_file("Global_active_power.kv")
        Builder.load_file("Kitchen.kv")
        Builder.load_file("Laundry_room.kv")
        Builder.load_file("Living_room.kv")
        Builder.load_file("Object_detect.kv")
        sm = ScreenManager()
        sm.add_widget(Home(name="home"))
        sm.add_widget(Login(name="login"))
        sm.add_widget(Register(name="register"))
        sm.add_widget(Global_active_power(name="global_active_power"))
        sm.add_widget(Kitchen(name="kitchen"))
        sm.add_widget(LaundryRoom(name="laundry_room"))
        sm.add_widget(LivingRoom(name="living_room"))
        sm.add_widget(Object_detect(name="object_detect"))
        print("Screens added to ScreenManager:", sm.screen_names)
        Clock.schedule_interval(self.take_information_for_report_and_report_it, 3600)

        return sm

    def take_information_for_report_and_report_it(self, dt):
        try:
            url = f'{backend}/api/get_info'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json().get('dataForHomeConsumption')

                payload = {
                    'global_active_power': data['Global_active_power'],
                    'global_reactive_power': data['Global_reactive_power'],
                    'voltage': data['Voltage'],
                    'global_intensity': data['Global_intensity'],
                    'sub_metering_1': data['Sub_metering_1'],
                    'sub_metering_2': data['Sub_metering_2'],
                    'sub_metering_3': data['Sub_metering_3'],
                }
                token = token_store.get("vars")["token"]
                headers = {
                    'Authorization': f'{token}',
                    'Content-Type': 'application/json'
                }

                create_report_url = f'{backend}/api/create_report'
                response = requests.post(create_report_url, json=payload, headers=headers)

                if response.status_code == 201:
                    print('Report created successfully')
                else:
                    print(f'Failed to create report. Status code: {response.status_code}')
            else:
                print(f'Failed to fetch data from API. Status code: {response.status_code}')
        except Exception as e:
            print(f'Error: {str(e)}')

Example().run()
