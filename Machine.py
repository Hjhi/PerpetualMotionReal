from time import sleep
from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import DPiStepper



class Machine:
    """
     backend/hardware methods for the perpetual motion machine
    """
    def __init__(self, **kwargs):
        self.dpiComputer = DPiComputer()
        self.dpiStepper = DPiStepper()

        if not self.dpiStepper.initialize():
            print("Failed to initialize the DPiStepper board")

        self.dpiStepper.setMicrostepping(8)



    def halt(self):
        """
            create halting program here for when program ends
        """
        pass

    def startup(self):
        """
            create a startup sequence here
        """
        pass