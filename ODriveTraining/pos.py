from dpea_odrive.odrive_helpers import *
from time import sleep

od = find_odrive(serial_number="207935A1524B")
assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."

ax = ODriveAxis(od.axis1)
ax.set_gains()
if not ax.is_calibrated():
    print("calibrating...")
    ax.calibrate()

ax.set_vel_limit(5)
ax.set_pos(5)
ax.wait_for_motor_to_stop()
print("Current Position in Turns = ", round(ax.get_pos(), 2))
ax.set_relative_pos(-5)
ax.wait_for_motor_to_stop()
print("Current Position in Turns = ", round(ax.get_pos(), 2))
sleep(3)