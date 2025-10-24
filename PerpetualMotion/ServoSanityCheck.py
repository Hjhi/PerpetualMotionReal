from PerpetualMachine import PerpetualMachine
from time import sleep

def main(m: PerpetualMachine):
    m.turn_stairs_on()
    while True:
        m.set_stair_speed(87)
        sleep(5)
        m.set_stair_speed(50)
        sleep(5)


if __name__ == "__main__":
    machine = PerpetualMachine()
    try:
       main(machine)
    finally:
        machine.halt()
