import json
import logging

import obd
import pandas as pd
from sense_hat import SenseHat

rows = []

sense = SenseHat()

port = obd.Async()

log = logging.getLogger(__name__)

green = [(45, 200, 45) for i in range(64)]
red = [(225, 30, 30) for i in range(64)]

def add_value(response):
    if len(rows[-1]) < 6:
        rows[-1][response.command] = response.value
    elif len(rows[-1]) == 6:
        rows[-1][response.command] = response.value
        rows[-1]["Accelerometer"] = sense.get_accelerometer_raw()
        rows[-1]["Orientation"] = sense.get_orientation()
        log.info("Log run complete")
    else:
        rows.append({response.command: response.value})

try:
    port = obd.Async(delay_cmds=0.2)

    log.info("Port opened")

    port.watch(obd.commands["RPM"], callback=add_value)
    port.watch(obd.commands["SPEED"], callback=add_value)
    port.watch(obd.commands["ENGINE_LOAD"], callback=add_value)
    port.watch(obd.commands["THROTTLE_POS"], callback=add_value)
    port.watch(obd.commands["FUEL_RATE"], callback=add_value)
    port.watch(obd.commands["RELATIVE_ACCEL_POS"], callback=add_value)

    port.start()

    log.info("Port started")

    sense.set_pixels(green)

    while True:
        if len(sense.stick.get_events()) < 1:
            port.stop()
            df = pd.DataFrame(rows)
            df.to_csv("log.csv")
            log.info("Data saved")
            print("Data saved")
            raise KeyboardInterrupt
except KeyboardInterrupt:
    print("Joystick pressed, shutting down...")
    log.warning("Joystick pressed, shutting down...")
except Exception as e:
    print(f"Error while logging: {e}")
    log.exception("Error while logging")
    sense.set_pixels(red)
finally:
    if port.running:
        port.stop()
    port.close()

    with open("logs.backup", "w") as f:
        json.dump(rows, f, indent=4)
    print("Data dumped")
    log.info("Data dumped")