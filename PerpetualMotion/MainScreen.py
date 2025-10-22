from kivy.clock import Clock
from kivy.properties import ColorProperty
from kivy.uix.screenmanager import Screen

from PerpetualMachine import PerpetualMachine

from pidev.kivy.DPEAButton import DPEAButton
from time import sleep


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    in other words, the frontend (grr)
    """

    green: ColorProperty = ColorProperty("#00D200")
    red: ColorProperty = ColorProperty("#D20000")

    nice_grey: ColorProperty = ColorProperty("#D7DAE5")
    bluish_grey: ColorProperty = ColorProperty("#B9CDDA")
    teal_blue: ColorProperty = ColorProperty("#A6D8D4")
    forrest_green: ColorProperty = ColorProperty("#8EAF9D")
    slate_green: ColorProperty = ColorProperty("#6B7D7D")

    auto_toggle: bool = True

    def __init__(self, machine: PerpetualMachine, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.machine: PerpetualMachine = machine

    # def on_enter(self, *args):
    #     sleep(1)
    #     print("woah!")
    #     # Clock.schedule_interval(self.update, 0.05)

    def stateMachine(self):
        pass

    def toggler(self):
        pass

    def update(self, dt=None):
        self.stateMachine()
        self.ids.stair_speed_label.text = f"Stair Speed {self.ids.stair_speed_slider.value}"
        self.ids.ramp_speed_label.text = f"Ramp Speed {self.ids.ramp_speed_slider.value}"

    def toggle_auto_manual(self):
        self.auto_toggle = not self.auto_toggle
        if self.auto_toggle:
            # Do auto stuff, statemachine stuff
            pass
        else:
            # Do manual stuff, button stuff
            pass

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        self.manager.current = 'passCode'

