from dpeaDPi.DPiStepper import DPiStepper
from time import sleep


def main(dpi: DPiStepper):
    dpi.setMicrostepping(8)
    dpi.setSpeedInStepsPerSecond(0, 1600 * 3)
    dpi.setAccelerationInStepsPerSecondPerSecond(0, 1600 * 3)
    dpi.enableMotors(True)
    dpi.moveToHomeInSteps(0, 1, 1600 * 3, 1600 * 28)

    while not dpi.getStepperStatus(0)[3]:
        sleep(0.02)

    dpi.setSpeedInStepsPerSecond(0, 1600 * 3)
    dpi.setAccelerationInStepsPerSecondPerSecond(0, 1600 * 3)
    #  Exit:   [0]: True returned on success, else False
    #          [1]: True returned if motor is stopped
    #          [2]: True returned if motors are enabled
    #          [3]: True returned if the "Homing" switch indicates "At home"
    #
    for _ in range(3):
        dpi.moveToAbsolutePositionInRevolutions(0, -28, False)

        while not dpi.getStepperStatus(0)[1]:
            print(dpi.getCurrentPositionInRevolutions(0))
            sleep(0.02)


        # dpi.moveToHomeInRevolutions(0, 1, 3, 1600 * 28)
        dpi.moveToAbsolutePositionInRevolutions(0, 0, False)

        while not dpi.getStepperStatus(0)[1]:
            print(dpi.getCurrentPositionInRevolutions(0))
            sleep(0.02)

        # dpi.setSpeedInRevolutionsPerSecond(0, 3)
        # dpi.setAccelerationInRevolutionsPerSecondPerSecond(0, 3)





if __name__ == "__main__":
    dpiStepper = DPiStepper()
    try:
        main(dpiStepper)
    finally:
        dpiStepper.enableMotors(False)