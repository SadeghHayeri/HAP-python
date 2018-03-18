"""An example of how to setup and start an Accessory.

This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client queries, etc.
"""
import logging
import signal

# from pyhap.accessories.DisplaySwitch import DisplaySwitch
# from pyhap.accessories.LightBulb import LightBulb
# from pyhap.accessories.ShutdownSwitch import ShutdownSwitch
from pyhap.accessories.TemperatureSensor import TemperatureSensor
from pyhap.accessories.nodeMCUSwitch import NodeMCUSwitch
from pyhap.accessory import Bridge
from pyhap.accessory_driver import AccessoryDriver

logging.basicConfig(level=logging.INFO)


def get_bridge():
    """Call this method to get a Bridge instead of a standalone accessory."""
    bridge = Bridge(display_name="Bridge")

    bridge.add_accessory( NodeMCUSwitch("Relay 1", URL="http://192.168.1.11", switchIndex=1) )
    bridge.add_accessory( NodeMCUSwitch("Relay 2", URL="http://192.168.1.11", switchIndex=2) )
    bridge.add_accessory( NodeMCUSwitch("Relay 3", URL="http://192.168.1.11", switchIndex=3) )
    bridge.add_accessory( NodeMCUSwitch("Relay 4", URL="http://192.168.1.11", switchIndex=4) )

    return bridge

acc = get_bridge()  # Change to get_bridge() if you want to run a Bridge.

# Start the accessory on port 51826
driver = AccessoryDriver(acc, port=60000)
# We want KeyboardInterrupts and SIGTERM (kill) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGINT, driver.signal_handler)
signal.signal(signal.SIGTERM, driver.signal_handler)
# Start it!
driver.start()
