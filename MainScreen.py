from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from time import sleep

from Machine import Machine
import Machine
from Machine import dpiStepper
# from dpeaDPi.DPiComputer import DPiComputer
# from dpeaDPi.DPiStepper import *
#
# dpiComputer = DPiComputer()
# dpiStepper = DPiStepper()
# dpiStepper.setBoardNumber(0)


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    in other words, the frontend (grr)
    """

    def __init__(self, machine: Machine, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.machine: Machine = machine
        self.machine.startup()
        print("startup done")

    def on_enter(self, *args):
        print("entered main screen")
        Clock.schedule_interval(self.update, 0.05)

    def on_leave(self, *args):
        print("left main screen")
        Clock.unschedule(self.update)

    def update(self, dt=None):
        pass

    def check_start(self):
        self.stop_all()
        self.motion()

    def motion(self):
        gate_number = 1
        staircase_number = 0
        ramp_speed = int(self.ids.ramp_speed.value)
        staircase_speed = int(90 - 90*self.ids.staircase_speed.value)
        Machine.dpiStepper.setSpeedInRevolutionsPerSecond(0, ramp_speed)

        #open/close gate
        Machine.dpiComputer.writeServo(gate_number, 90)
        while Machine.dpiComputer.readDigitalIn(Machine.dpiComputer.IN_CONNECTOR__IN_0):
            sleep(0.05)
        Machine.dpiComputer.writeServo(gate_number, 0)

        # start ramp
        Machine.dpiStepper.moveToAbsolutePositionInRevolutions(0, -29, True)
        Machine.dpiStepper.setSpeedInRevolutionsPerSecond(0, 6)
        Machine.dpiStepper.moveToAbsolutePositionInRevolutions(0, 0, False)

        #staircase
        Machine.dpiComputer.writeServo(staircase_number, staircase_speed)
        sleep(10)
        Machine.dpiComputer.writeServo(staircase_number, 90)

    def staircase(self):
        staircase_speed = int(90 - 90*self.ids.staircase_speed.value)
        staircase_number = 0
        if self.ids.staircase_button.text == "Staircase up":
            Machine.dpiComputer.writeServo(staircase_number, staircase_speed)
            self.ids.staircase_button.text = "Stop staircase"
        else:
            Machine.dpiComputer.writeServo(staircase_number, 90)
            self.ids.staircase_button.text = "Staircase up"

    def gate(self):
        gate_number = 1
        if self.ids.gate_button.text == "Open gate":
            Machine.dpiComputer.writeServo(gate_number, 90)
            self.ids.gate_button.text = "Close gate"
        else:
            Machine.dpiComputer.writeServo(gate_number, 0)
            self.ids.gate_button.text = "Open gate"

    def ramp(self):
        Machine.dpiStepper.setSpeedInRevolutionsPerSecond(0, int(self.ids.ramp_speed.value))
        if self.ids.ramp_button.text == "Ramp up":
            Machine.dpiStepper.moveToAbsolutePositionInRevolutions(0, -29, True)
            self.ids.ramp_button.text = "Ramp down"
        else:
            Machine.dpiStepper.moveToAbsolutePositionInRevolutions(0, 0, True)
            self.ids.ramp_button.text = "Ramp up"

    def stop_all(self):
        Machine.dpiComputer.writeServo(1, 0)
        Machine.dpiComputer.writeServo(0, 90)
        Machine.dpiStepper.setSpeedInRevolutionsPerSecond(0, 6)
        Machine.dpiStepper.moveToAbsolutePositionInRevolutions(0, 0, True)



    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        self.manager.current = 'passCode'

