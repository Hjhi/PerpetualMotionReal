from enum import Enum
from unittest import case

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
    auto_start: bool = True

    def __init__(self, machine: PerpetualMachine, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        sleep(1)
        self.machine: PerpetualMachine = machine
        self.machine.startup()
        print("startup done")

    def on_enter(self, *args):
        Clock.schedule_interval(self.update, 0.05)
        self.machine.turn_stairs_on()
        self.machine.turn_ramp_on()


    def manual_state_machine(self):
        pass

    def update(self, dt=None):
        if self.auto_start:
            self.machine.run_ramp_auto()
            self.machine.set_stair_speed(self.ids.stair_speed_slider.value / 100)
            self.machine.set_ramp_speed(self.ids.ramp_speed_slider.value/100)
        else:
            self.machine.set_stair_speed(0)
            self.machine.set_ramp_speed(0)



    def toggle_auto_manual(self):
        print("pressed")
        self.auto_toggle = not self.auto_toggle
        if self.auto_toggle:
            # Do auto stuff, statemachine stuff
            self.ids.auto_start_stop.x = self.width * (0.5 - 0.05)
            self.ids.auto_manual_toggle.text = "Set Manual Mode"
            self.machine.turn_stairs_on()
            self.machine.turn_ramp_on()
            self.machine.set_stair_speed(0)
            self.machine.set_ramp_speed(0)
        else:
            # Do manual stuff, button stuff
            self.start_stop_auto() if self.auto_start else 0
            self.ids.auto_start_stop.x = self.width * 10
            self.machine.turn_stairs_off()
            self.machine.turn_ramp_off()

    def start_stop_auto(self):
        self.auto_start = not self.auto_start
        if self.auto_start:
            self.ids.auto_start_stop.text = "Stop"
            self.ids.auto_start_stop.fill_color = self.red
        else:
            self.ids.auto_start_stop.text = "Start"
            self.ids.auto_start_stop.fill_color = self.green

    def toggle_stairs(self):
        if self.machine.is_stair_on():
            self.machine.turn_stairs_off()
        else:
            self.machine.turn_stairs_on()

    def toggle_ramp(self):
        if self.machine.is_ramp_on():
            self.machine.turn_ramp_off()
        else:
            self.machine.turn_ramp_on()

    def toggle_machine(self):
        if self.start_stop_machine:
            self.machine.open_gate()
        else:
            self.machine.close_gate()
        pass

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        self.manager.current = 'passCode'

