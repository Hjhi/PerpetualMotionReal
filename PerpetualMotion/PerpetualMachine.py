from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import DPiStepper


class PerpetualMachine:
    """
     backend/hardware methods for the perpetual motion machine
    """

    gate_servo_port: int = 0
    stair_servo_port: int = 1

    ramp_motor: int = 0

    def __init__(self, **kwargs):
        self.dpiComputer = DPiComputer()
        self.dpiStepper = DPiStepper()
        if not self.dpiStepper.initialize():
            print("Failed to initialize the DPiStepper board")

        self.prox_sensor_top = self.dpiComputer.IN_CONNECTOR__IN_0
        self.prox_sensor_bottom = self.dpiComputer.IN_CONNECTOR__IN_1

