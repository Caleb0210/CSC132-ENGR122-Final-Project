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

sm = ScreenManager()

# This function uses the BoxLayout to make the orientation either horizontal or vertical
def main_screen():
    # Create a screen for the main screen
    screen = Screen(name="MainScreen")
    screen.feedingTime = ""
    layout = BoxLayout(orientation='horizontal')

    button_weight = Button(
        text="Set Weight",
        background_color="red"  
    )

    button_weight.bind(on_press=on_button_weight_click) # type: ignore
    layout.add_widget(button_weight)

    button_time = Button(
        text="Set Time",
        background_color="red" 
    )
    
    button_time.bind(on_press=on_button_time_click) # type: ignore
    layout.add_widget(button_time)

    screen.add_widget(layout)

    Clock.schedule_interval(lambda dt: checkTime(screen.feedingTime), 1)

    return screen

# This function checks the current real world time
def checkTime(feedingTime):
    currentTime = datetime.now().strftime("%I:%M %p")
    print(f"{currentTime} current \n{feedingTime} feeding time")
    if (feedingTime == currentTime):
        print("hello world")

# This function switches to the "Set Weight" screen
def on_button_weight_click(instance):
    app = App.get_running_app()
    app.sm.current = "Set Weight"

# This function switches to the "Set Time" screen
def on_button_time_click(instance):
    app = App.get_running_app()
    app.sm.current = "Set Time"

# This function creates the "Set Time" screen
def set_time():
    # Create a screen for the Set Time screen
    screen = Screen(name="Set Time")
    layout = BoxLayout(orientation="vertical", spacing=5, padding=5)
    display = Label(text="", font_size='30sp', halign="right", valign="bottom", size_hint=(1, 0.5))
    layout.add_widget(display)

    # Add the buttons to the SetTime layout
    buttons = [
        "7", "8", "9", "back",
        "4", "5", "6", " ",
        "1", "2", "3", "AM",
        "0", ":", "enter", "PM"
        ]
    # Create a GridLayout to hold the buttons
    buttons_layout = GridLayout(cols=4, spacing=5)
    
    for button_text in buttons:
        button = Button(text=button_text, font_size=30, size_hint=(0.25, 0.2))
        button.bind(on_press=lambda button: on_button_press(button, screen))
        buttons_layout.add_widget(button)

    layout.add_widget(buttons_layout)

    screen.add_widget(layout)

    screen.feedTime = None

    return screen

# This function handles the button presses for the "Set Time" screen
def on_button_press(button, screen):
    if button.text == "clear":
        screen.display.text = ""
    elif button.text == "back":
        screen.display.text = screen.display.text[:-1]
    elif button.text == "enter":
        try:
            screen.feedTime = str(screen.display.text)
            app = App.get_running_app()
            app.sm.current = "MainScreen"
            app.root.get_screen("MainScreen").feedingTime = screen.feedTime
        except:
            print("Please enter a valid time")
    else:
        screen.display.text += button.text

# This function creates the "Set Weight" screen
def set_weight():
    # Create a screen for the Set Weight screen
    screen = Screen(name="Set Weight")
    layout = BoxLayout(orientation="vertical", spacing=5, padding=5)

    # Add a label and text input for the weight
    weight_label = Label(text="Enter weight (in grams)", font_size='30sp', halign="right", valign="bottom")
    weight_input = TextInput(multiline=False, font_size='30sp', size_hint=(1, 0.5), input_type='number')
    layout.add_widget(weight_label)
    layout.add_widget(weight_input)

    # Add a button to set the weight
    button_set_weight = Button(
        text="Set Weight",
        font_size='30sp',
        background_color="red",
        size_hint=(1, 0.5)
    )
    button_set_weight.bind(on_press=lambda instance: on_button_set_weight(instance, weight_input))
    layout.add_widget(button_set_weight)

    screen.add_widget(layout)

    return screen

# This function handles setting the weight
def on_button_set_weight(instance, weight_input):
    try:
        weight = float(weight_input.text)
        print(f"Weight set to {weight} grams")
        app = App.get_running_app()
        app.sm.current = "MainScreen"
    except:
        print("Please enter a valid weight")

# Add the screens to the ScreenManager
# sm.add_widget(main_screen())
# sm.add_widget(set_time())
# sm.add_widget(set_weight())

class FeederApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(main_screen())
        self.sm.add_widget(set_time())
        self.sm.add_widget(set_weight())
        print("ScreenManager instance created")
        return self.sm
        
if __name__ == "__main__":
    FeederApp().run()