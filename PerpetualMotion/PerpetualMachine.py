import math
from unittest import case

from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import DPiStepper

from enum import Enum

from PerpetualMotion.sensorTest import dpiComputer


class PerpetualMachine:
    """
     backend/hardware methods for the perpetual motion machine
    """
    gate_servo_port: int = 0
    stair_servo_port: int = 1

    ramp_motor: int = 0

    ramp_speed: float = 0
    stair_speed: float = 0
    max_ramp_RPS: float = 5
    max_stair_speed: float = 90

    class GateState(Enum):
        OPENED = True
        CLOSED = False

    class OnOffState(Enum):
        ON = True
        OFF = False

    class RampState(Enum):
        EJECT = 0
        HOME = 1
        OFF = 2

    ramp_state: RampState = RampState.OFF
    ramp_power: OnOffState = OnOffState.OFF
    stair_power: OnOffState = OnOffState.OFF
    gate_state: GateState = GateState.CLOSED

    queue_auto_manual_change: bool = False
    ramp_top_pos: float = 10 # revolutions

    def __init__(self, **kwargs):
        self.dpiComputer = DPiComputer()
        self.dpiStepper = DPiStepper()
        if not self.dpiStepper.initialize():
            print("Failed to initialize the DPiStepper board")

        self.dpiStepper.setMicrostepping(8)

        self.prox_sensor_top = self.dpiComputer.IN_CONNECTOR__IN_0
        self.prox_sensor_bottom = self.dpiComputer.IN_CONNECTOR__IN_1

    def run_ramp(self):
        status = self.dpiStepper.getStepperStatus(0)

        match self.ramp_power:
            case self.OnOffState.ON:
                if not status[2]:
                    self.dpiStepper.enableMotors(True)
            case self.OnOffState.OFF:
                if status[2]:
                    self.dpiStepper.enableMotors(False)

        match self.ramp_state:
            case self.RampState.HOME:

                if not status[3]:
                    self.dpiStepper.moveToHomeInSteps(0, -1, self.ramp_speed, 99999)
                    self.close_gate()
                if status[3] and self.dpiComputer.readDigitalIn(self.prox_sensor_bottom):
                    self.open_gate()
                if status[3] and not self.dpiComputer.readDigitalIn(self.prox_sensor_bottom):
                    self.ramp_state = self.RampState.EJECT

            case self.RampState.EJECT:
                if not status[3] and not self.dpiComputer.readDigitalIn(self.prox_sensor_top):
                    self.ramp_state = self.RampState.HOME
                if status[3] and self.dpiComputer.readDigitalIn(self.prox_sensor_top):
                    self.dpiStepper.moveToRelativePositionInRevolutions(0, self.ramp_top_pos, False)

    def set_stair_speed(self, speed: float):
        self.stair_speed = speed
        self.dpiComputer.writeServo(self.stair_servo_port, int(90 + self.max_stair_speed * speed))

    def set_ramp_speed(self, speed: float):
        self.ramp_speed = speed
        self.dpiStepper.setSpeedInStepsPerSecond(0, self.max_ramp_RPS * speed)
        self.dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(0, self.max_ramp_RPS * speed)

    def turn_ramp_on(self):
        self.ramp_power = self.OnOffState.ON

    def turn_ramp_off(self):
        self.ramp_power = self.OnOffState.OFF

    def turn_stairs_on(self):
        self.stair_power = self.OnOffState.ON

    def turn_stairs_off(self):
        self.stair_power = self.OnOffState.OFF

    def open_gate(self):
        self.dpiComputer.writeServo(self.gate_servo_port, 90)

    def close_gate(self):
        self.dpiComputer.writeServo(self.gate_servo_port, 0)
