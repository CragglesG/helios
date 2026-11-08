from time import sleep

import obd
import json
import pandas as pd
from sense_hat import SenseHat

rows = []

sense = SenseHat()

port = obd.Async()

def add_value(response):
    if len(rows[-1]) < 6:
        rows[-1][response.command] = response.value
    elif len(rows[-1]) == 6:
        rows[-1][response.command] = response.value
        rows[-1]["Accelerometer"] = sense.get_accelerometer_raw()
        rows[-1]["Orientation"] = sense.get_orientation()
    else:
        rows.append({response.command: response.value})

try:
    port = obd.Async(delay_cmds=0.2)

    port.watch(obd.commands["RPM"], callback=add_value)
    port.watch(obd.commands["SPEED"], callback=add_value)
    port.watch(obd.commands["ENGINE_LOAD"], callback=add_value)
    port.watch(obd.commands["THROTTLE_POS"], callback=add_value)
    port.watch(obd.commands["FUEL_RATE"], callback=add_value)
    port.watch(obd.commands["RELATIVE_ACCEL_POS"], callback=add_value)

    port.start()

    while True:
        if len(sense.stick.get_events()) < 1:
            port.stop()
            df = pd.DataFrame(rows)
            df.to_csv("log.csv")
            print("Data saved")
except KeyboardInterrupt:
    print("Joystick pressed, shutting down...")
except Exception as e:
    print(f"Error while logging: {e}")
finally:
    if port.running:
        port.stop()
    port.close()

    with open("logs.backup", "w") as f:
        json.dump(rows, f, indent=4)
    print("Data dumped")
