from PerpetualMachine import PerpetualMachine
from time import sleep

def main(m: PerpetualMachine):
    m.turn_stairs_on()
    while True:
        for i in range(100):
            print(i)
            m.set_stair_speed(i/100.0)
            sleep(2)

if __name__ == "__main__":
    machine = PerpetualMachine()
    try:
       main(machine)
    finally:
        machine.halt()
