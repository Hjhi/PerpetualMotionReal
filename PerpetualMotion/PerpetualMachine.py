from time import sleep
from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import DPiStepper

from enum import Enum


class PerpetualMachine:
    """
     backend/hardware methods for the perpetual motion machine
    """
    gate_servo_port: int = 0
    stair_servo_port: int = 1

    ramp_motor: int = 0

    ramp_speed: float = 0
    stair_speed: int = 90

    max_ramp_RPS: float = 5

    class GateState(Enum):
        OPENED = True
        CLOSED = False

    class OnOffState(Enum):
        ON = True
        OFF = False

    class RampState(Enum):
        EJECT = 0
        HOME = 1

    ramp_state: RampState = RampState.HOME
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

    def run_ramp_auto(self):
        status = self.dpiStepper.getStepperStatus(0)
        print(self.ramp_state)

        match self.ramp_state:
            case self.RampState.HOME:
                if not status[3]:
                    self.dpiStepper.moveToHomeInSteps(0, 1, self.ramp_speed, 99999)
                    self.close_gate()
                if status[3] and self.dpiComputer.readDigitalIn(self.prox_sensor_bottom):
                    self.open_gate()
                if status[3] and not self.dpiComputer.readDigitalIn(self.prox_sensor_bottom):
                    self.ramp_state = self.RampState.EJECT

            case self.RampState.EJECT:
                if not status[3] and not self.dpiComputer.readDigitalIn(self.prox_sensor_top):
                    self.ramp_state = self.RampState.HOME
                if status[3] and self.dpiComputer.readDigitalIn(self.prox_sensor_top):
                    self.dpiStepper.moveToRelativePositionInRevolutions(0, -self.ramp_top_pos, False)

    def halt(self):
        self.turn_stairs_off()
        self.turn_ramp_off()
        self.close_gate()

    def startup(self):
        self.dpiStepper.enableMotors(True)
        self.dpiStepper.moveToHomeInSteps(0, 1, 1600, 99999)
        sleep(0.5)
        while not self.dpiStepper.getAllMotorsStopped():
            sleep(0.02)
        self.dpiStepper.enableMotors(False)
        print("motor startup finished")

    def set_stair_speed(self, speed: float):
        s = speed * 40
        self.stair_speed = 90 if speed == 0 else int(90 - (20 + s))
        print(self.stair_speed)
        if self.stair_power == self.OnOffState.ON:
            self.turn_stairs_on()

    def set_ramp_speed(self, speed: float):
        self.ramp_speed = speed
        self.dpiStepper.setSpeedInStepsPerSecond(0, self.max_ramp_RPS * speed)
        self.dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(0, self.max_ramp_RPS * speed)

    def turn_ramp_on(self):
        if not self.dpiStepper.getStepperStatus(0)[2]:
            self.dpiStepper.enableMotors(True)


    def turn_ramp_off(self):
        if self.dpiStepper.getStepperStatus(0)[2]:
            self.dpiStepper.enableMotors(False)

    def turn_stairs_on(self):
        self.stair_power = self.OnOffState.ON
        self.dpiComputer.writeServo(self.stair_servo_port, self.stair_speed)

    def turn_stairs_off(self):
        self.stair_power = self.OnOffState.OFF
        self.dpiComputer.writeServo(self.stair_servo_port, 90)

    def open_gate(self):
        self.dpiComputer.writeServo(self.gate_servo_port, 90)

    def close_gate(self):
        self.dpiComputer.writeServo(self.gate_servo_port, 0)

    def is_stair_on(self):
        return self.stair_power == self.OnOffState.ON

    def is_ramp_on(self):
        return self.ramp_power == self.OnOffState.ON