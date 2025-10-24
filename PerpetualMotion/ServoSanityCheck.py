from PerpetualMachine import PerpetualMachine
from time import sleep

def main(m: PerpetualMachine):
    m.turn_stairs_on()
    while True:
        print("high speed")
        m.set_stair_speed(100)
        sleep(5)
        print("low speed")
        m.set_stair_speed(0)
        sleep(5)


if __name__ == "__main__":
    machine = PerpetualMachine()
    try:
       main(machine)
    finally:
        machine.halt()
