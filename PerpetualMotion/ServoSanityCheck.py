from PerpetualMachine import PerpetualMachine
from time import sleep

def main(m: PerpetualMachine):
    while True:
        m.turn_stairs_on()
        m.set_stair_speed(87)


if __name__ == "__main__":
    machine = PerpetualMachine()
    try:
       main(machine)
    finally:
        machine.halt()
