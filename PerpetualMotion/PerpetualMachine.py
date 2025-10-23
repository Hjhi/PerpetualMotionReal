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
    stair_speed: float = 0
    max_ramp_RPS: float = 5
    max_stair_speed: float = 90

    class GateState(Enum):
        OPENED = True
        CLOSED = False

    class OnOffState(Enum):
        ON = True
        OFF = False

    ramp_state: OnOffState = OnOffState.OFF
    stair_state: OnOffState = OnOffState.OFF
    gate_state: GateState = GateState.CLOSED

    queue_auto_manual_change: bool = False

    def __init__(self, **kwargs):
        self.dpiComputer = DPiComputer()
        self.dpiStepper = DPiStepper()
        if not self.dpiStepper.initialize():
            print("Failed to initialize the DPiStepper board")

        self.dpiStepper.setMicrostepping(8)

        self.prox_sensor_top = self.dpiComputer.IN_CONNECTOR__IN_0
        self.prox_sensor_bottom = self.dpiComputer.IN_CONNECTOR__IN_1

    def open_gate(self):
        pass

    def close_gate(self):
        pass


    def run_auto(self):

        if (
            self.ramp_clear()
            and self.ramp_at_home
            and not self.queue_auto_manual_change
            and self.gate_state == self.GateState.CLOSED
        ):
            self.open_gate()

        elif self.gate_state == self.GateState.OPENED:
            self.close_gate()

        if not self.ramp_clear() and self.ramp_at_home:
            self.eject_marble()
        if self.ramp_clear() and not self.ramp_at_home:
            self.home_ramp()

        if self.ramp_clear() and self.ramp_at_home and self.gate_state == self.GateState.CLOSED:
            self.queue_auto_manual_change = False



        pass
    def ramp_clear(self):
        pass

    def set_stair_speed(self, speed: float):
        self.stair_speed = speed
        self.dpiComputer.writeServo(self.stair_servo_port, int(90 + self.max_stair_speed * speed))

    def set_ramp_speed(self, speed: float):
        self.ramp_speed = speed
        self.dpiStepper.setSpeedInStepsPerSecond(0, self.max_ramp_speed * speed)
        self.dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(0, self.max_ramp_RPS * speed)

    def toggle_ramp(self, state: bool):
        self.ramp_state = state
        self.dpiStepper.enableMotors(state)

    def toggle_stairs(self, state: bool):
        self.stair_state = state