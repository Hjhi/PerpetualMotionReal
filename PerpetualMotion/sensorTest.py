from dpeaDPi.DPiComputer import DPiComputer
from time import sleep

dpiComputer = DPiComputer()

def main():
    dpiComputer.initialize()

    proxSensorTop: int = dpiComputer.IN_CONNECTOR__IN_0
    proxSensorBottom: int = dpiComputer.IN_CONNECTOR__IN_1

    while True:
        _, sense_value_top = dpiComputer.readDigitalIn(proxSensorTop)
        _, sense_value_bottom = dpiComputer.readDigitalIn(proxSensorBottom)

        if sense_value_top:
            print("Top Input is high")
        else:
            print("Top input is low")

        if sense_value_bottom:
            print("Bottom Input is high")
        else:
            print("Bottom input is low")

        sleep(1)


if __name__ == '__main__':
    main()