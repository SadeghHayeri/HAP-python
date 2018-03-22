# An Accessory for a LED attached to pin 11.
import logging
import requests

from pyhap.accessory import Accessory, Category
import pyhap.loader as loader


class NodeMCUGarage(Accessory):

    category = Category.GARAGE_DOOR_OPENER

    def __init__(self, *args, URL, **kwargs):
        super(NodeMCUGarage, self).__init__(*args, **kwargs)
        self.statusURL = URL + "/status"
        self.openURL = URL + "/open"
        self.closeURL = URL + "/close"

    def __setstate__(self, state):
        pass

    def set_door_state(self, value):
        if value == 0:
            requests.get(self.openURL)
        if value == 1:
            requests.get(self.closeURL)

    def _set_services(self):
        super(NodeMCUGarage, self)._set_services()

        garage_service = loader.get_serv_loader().get("GarageDoorOpener")
        self.add_service(garage_service)

        self.currDoorState = garage_service.get_characteristic("CurrentDoorState")
        self.targetDoorState = garage_service.get_characteristic("TargetDoorState")
        self.ObstructionDetected = garage_service.get_characteristic("ObstructionDetected")

        self.targetDoorState.setter_callback = self.set_door_state

    def stop(self):
        super(NodeMCUGarage, self).stop()

    def run(self):
        self.ObstructionDetected.set_value(False)
        while not self.run_sentinel.wait(1):
            r = requests.get(self.statusURL)
            if r.text == 'Open':
                self.currDoorState.set_value(0)
            elif r.text == 'Opening':
                self.currDoorState.set_value(2)
            if r.text == 'Closed':
                self.currDoorState.set_value(1)
            elif r.text == 'Closing':
                self.currDoorState.set_value(3)
            elif r.text == 'Stopped':
                self.currDoorState.set_value(4)
            else:
                print("error!", r.text)
