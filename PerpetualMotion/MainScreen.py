from kivy.properties import ColorProperty
from kivy.uix.screenmanager import Screen

from PerpetualMachine import PerpetualMachine


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
        self.machine: PerpetualMachine = machine

    def stateMachine(self):
        pass

    def toggler(self):
        pass

    def step(self):
        self.stateMachine()

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

