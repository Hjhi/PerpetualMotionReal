from PerpetualMachine import PerpetualMachine

def main(m: PerpetualMachine):


if __name__ == "__main__":
    machine = PerpetualMachine()
    try:
        main(machine)
    finally:
        machine.halt()