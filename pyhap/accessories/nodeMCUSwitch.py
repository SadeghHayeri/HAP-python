# An Accessory for a LED attached to pin 11.
import logging
import requests

from pyhap.accessory import Accessory, Category
import pyhap.loader as loader


class NodeMCUSwitch(Accessory):

    category = Category.SWITCH

    def __init__(self, *args, URL, switchIndex, **kwargs):
        super(NodeMCU, self).__init__(*args, **kwargs)
        self.statusURL = URL + "/status/" + str(switchIndex)
        self.onURL = URL + "/set/" + str(switchIndex) + "/ON"
        self.offURL = URL + "/set/" + str(switchIndex) + "/OFF"

    def __setstate__(self, state):
        pass
        # self.__dict__.update(state)

    def set_bulb(self, value):
        if value:
            requests.get(self.onURL)
        else:
            requests.get(self.offURL)

    def _set_services(self):
        super(NodeMCU, self)._set_services()

        bulb_service = loader.get_serv_loader().get("Switch")
        self.add_service(bulb_service)

        self.switchState = bulb_service.get_characteristic("On")
        self.switchState.setter_callback = self.set_bulb


    def stop(self):
        super(NodeMCU, self).stop()

    def run(self):
        while not self.run_sentinel.wait(1):
            r = requests.get(self.statusURL)
            if '1' in r.text:
                self.switchState.set_value(1)
            elif '0' in r.text:
                self.switchState.set_value(0)
            else:
                print("error!", r.text)
