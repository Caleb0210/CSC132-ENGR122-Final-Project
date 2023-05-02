from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.clock import Clock

from datetime import datetime
import requests
response = requests.get("https://www.protohacks.net/LATech/AutomaticFeeder/read.php")
# from motor import *
data = {"gearControl", 0}

folder = "images-gif/"

# This class uses the BoxLayout to make the orientation 
# either horizontal or vertical
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='horizontal')

        self.button_weight = Button(
            text="Set Weight",
            background_color="blue"  
        )

        self.button_weight.bind(on_press=self.on_button_weight_click) # type: ignore
        self.layout.add_widget(self.button_weight)

        self.button_time = Button(
            text="Set Time",
            background_color="blue" 
        )
        
        self.button_time.bind(on_press=self.on_button_time_click) # type: ignore
        self.layout.add_widget(self.button_time)

        self.add_widget(self.layout)

        Clock.schedule_interval(lambda dt: self.checkWeight(SetWeight.refillWeightLimit), 1)
        Clock.schedule_interval(lambda dt: self.checkTime(SetTime.feedTime), 1)

    #checks the current real world time
    def checkTime(self, feedTime):
        currentTime = datetime.now().strftime("%I:%M %p")
        # print(f"'{currentTime}' current \n'{feedTime}' feeding time")
        if (not SetTime.hasFed and feedTime == currentTime):
            SetTime.hasFed = True
            '''
            if(SetWeight.refillWeightLimit >= "weight"):
                SetWeight.filling = True
                data = {"gearControl": 1}
                response = requests.get("https://www.protohacks.net/LATech/AutomaticFeeder/write.php", params = data)
                print("feeding now!")
            '''
            print("feeding now!")
        if (SetTime.hasFed and feedTime != currentTime):
            SetTime.hasFed == False
            

    def checkWeight(self, weightLimit):
        if (SetWeight.filling and weightLimit == "weight"):
            SetWeight.filling = False
            data = {"gearControl": 2}
            response = requests.get("https://www.protohacks.net/LATech/AutomaticFeeder/write.php", params = data)
            print("closing")

    # These on click functions basically calls for the Weight_Time function to switch screens
    def on_button_weight_click(self, instance):
        app = App.get_running_app()
        app.sm.current = "Set Weight"

    def on_button_time_click(self, instance):
        app = App.get_running_app()
        app.sm.current = "Set Time"

    

class SetTime(Screen):
    feedTime = ""
    hasFed = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create the GUI layout using a BoxLayout
        layout = BoxLayout(orientation="vertical", spacing=5, padding=5)
        self.display = Label(text="", font_size='30sp', halign="right", valign="bottom", size_hint=(1, 0.5))
        layout.add_widget(self.display)
        self.answer = False

        # Add the buttons to the SetTime layout
        buttons = [
            "7", "8", "9", "back",
            "4", "5", "6", " ",
            "1", "2", "3", " AM",
            "0", ":", "enter", " PM"
            ]
        # Create a GridLayout to hold the buttons
        buttons_layout = GridLayout(cols=4, spacing=5)
        
        for button_text in buttons:
            button = Button(text=button_text, font_size=30, size_hint=(0.25, 0.2))
            button.bind(on_press=self.on_button_press)
            buttons_layout.add_widget(button)

        layout.add_widget(buttons_layout)

        self.add_widget(layout)

    def on_button_press(self, button):
        if button.text == "clear":
            self.display.text = ""
        elif button.text == "back":
            self.display.text = self.display.text[:-1]
        elif button.text == "enter":
            try:
                SetTime.feedTime = str(self.display.text).strip()
                self.answer = True
                print(SetTime.feedTime + " feed time")
                if len(SetTime.feedTime) > 14:
                    self.display.text = SetTime.feedTime[:11] + "..."
                else:
                    self.display.text = SetTime.feedTime
                # switch back to MainScreen if the result is valid
                SetTime.hasFed = False
                app = App.get_running_app()
                app.sm.current = "MainScreen"
            except:
                self.display.text = "ERROR131"
        else:
            if self.display.text == "ERROR131" or self.answer:
                self.display.text = ""
                self.answer = False
            self.display.text += button.text

    def update_feedTime(self):
        SetTime.feedTime = self.display.text


class SetWeight(Screen):
    refillWeightLimit = ""
    filling = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create the GUI layout
        layout = BoxLayout(orientation="vertical", spacing=5, padding=5)
        self.display = Label(text="", font_size='30sp', halign="right", valign="bottom", size_hint=(1, 0.5))
        layout.add_widget(self.display)

        # add the buttons to the layout
        buttons = [
            '7', '8', '9', 'back',
            '4', '5', '6', 'clear',
            '1', '2', '3', 'g',
            '0', '.', 'enter', '']
        
        # Create a GridLayout to hold the buttons
        buttons_layout = GridLayout(cols=4, spacing=5)

        for button_text in buttons:
            button = Button(text=button_text, font_size=30, size_hint=(0.25, 0.2))
            button.bind(on_press=self.button_pressed)
            buttons_layout.add_widget(button)

        layout.add_widget(buttons_layout)

        self.add_widget(layout)

    def button_pressed(self, button):
        if button.text == "clear":
            self.display.text = ""
        elif button.text == "back":
            self.display.text = self.display.text[:-1]
        elif button.text == "enter":
            try:
                SetWeight.refillWeightLimit = str(self.display.text)
                if len(SetWeight.refillWeightLimit) > 14:
                    self.display.text = SetWeight.refillWeightLimit[:11] + "..."
                else:
                    self.display.text = SetWeight.refillWeightLimit
                # switch back to MainScreen if the result is valid
                SetWeight.filling = False
                app = App.get_running_app()
                app.sm.current = "MainScreen"
            except:
                self.display.text = "ERROR131"
        else:
            if self.display.text == "ERROR131":
                self.display.text = ""
            self.display.text += button.text



# This class basically takes the inputs of the buttons
# And switchs between the screens
class Weight_Time(App):
    def build(self):
        self.sm = ScreenManager()
        self.main_screen = MainScreen(name="MainScreen")
        self.set_weight = SetWeight(name="Set Weight")
        self.set_time = SetTime(name="Set Time")
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.set_weight)
        self.sm.add_widget(self.set_time)
        return self.sm


if __name__ == "__main__":
    Weight_Time().run()
