from dpeaDPi.DPiStepper import DPiStepper
from time import sleep

from PerpetualMachine import PerpetualMachine

def main():
    dpiStepper = DPiStepper()
    dpiStepper.setMicrostepping(8)
    dpiStepper.setSpeedInRevolutionsPerSecond(0, 3)
    dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(0, 3)
    dpiStepper.enableMotors(True)
    dpiStepper.moveToHomeInSteps(0, 1, 1600 * 3, 999999999)

    while not dpiStepper.getStepperStatus(0)[3]:
        sleep(0.02)

    dpiStepper.setSpeedInRevolutionsPerSecond(0, 3)
    dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(0, 3)
    #  Exit:   [0]: True returned on success, else False
    #          [1]: True returned if motor is stopped
    #          [2]: True returned if motors are enabled
    #          [3]: True returned if the "Homing" switch indicates "At home"
    #
    for _ in range(3):
        dpiStepper.moveToAbsolutePositionInRevolutions(0, -28, False)

        while not dpiStepper.getStepperStatus(0)[1]:
            sleep(0.02)

        dpiStepper.moveToHomeInRevolutions(0, 1, 3, 999999)

        while not dpiStepper.getStepperStatus(0)[3]:
            sleep(0.02)





if __name__ == "__main__":
    try:
        main()
    finally:
        DPiStepper().enableMotors(False)