import obd

port = obd.OBD()

print(f"Connected: {port.is_connected()}")

print("\n--------\n")

print(f"RPM: {"available" if port.supports(obd.commands["RPM"]) else "unavailable"}")
print(f"Speed: {"available" if port.supports(obd.commands["SPEED"]) else "unavailable"}")
print(f"Engine Load: {"available" if port.supports(obd.commands["ENGINE_LOAD"]) else "unavailable"}")
print(f"Throttle Position: {"available" if port.supports(obd.commands["THROTTLE_POS"]) else "unavailable"}")
print(f"Fuel Rate: {"available" if port.supports(obd.commands["FUEL_RATE"]) else "unavailable"}")

print("\n--------\n")

if port.supports(obd.commands["ACCELERATOR_POS_D"]):
    print(f"Accel D: {port.query("ACCELERATOR_POS_D").value}")
else:
    print("Accel D: unavailable")

if port.supports(obd.commands["ACCELERATOR_POS_E"]):
    print(f"Accel E: {port.query("ACCELERATOR_POS_E").value}")
else:
    print("Accel E: unavailable")

if port.supports(obd.commands["ACCELERATOR_POS_F"]):
    print(f"Accel F: {port.query("ACCELERATOR_POS_F").value}")
else:
    print("Accel F: unavailable")

if port.supports(obd.commands["RELATIVE_ACCEL_POS"]):
    print(f"Relative: {port.query("RELATIVE_ACCEL_POS").value}")
else:
    print("Relative: unavailable")

port.close()
