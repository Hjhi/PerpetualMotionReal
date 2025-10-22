from dpeaDPi.DPiDigitalIn import DPiDigitalIn
from time import sleep

digitalIn = DPiDigitalIn()

def main():
    digitalIn.setBoardNumber(0)
    if digitalIn.initialize() != True:
        print("Communication with the DPiDigitalIn board failed.")
        return

    proxSensorTop: int = 0
    proxSensorBottom: int = 1

    while True:
        _, sense_value_top = digitalIn.readDigitalInput(proxSensorTop)
        _, sense_value_bottom = digitalIn.readDigitalInput(proxSensorBottom)

        if sense_value_top:
            print("Top Input is high")
        else:
            print("Top input is low")

        if sense_value_bottom:
            print("Bottom Input is high")
        else:
            print("Bottom input is low")

        sleep(1);