from PerpetualMachine import PerpetualMachine

def main(m: PerpetualMachine):
    m.startup()
    m.set_ramp_speed(0.5)
    while True:
        m.run_ramp_auto()



if __name__ == "__main__":
    machine = PerpetualMachine()
    try:
        main(machine)
    finally:
        machine.halt()