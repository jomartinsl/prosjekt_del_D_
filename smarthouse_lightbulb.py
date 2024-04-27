import logging
import threading
import time
import requests

from messaging import ActuatorState
import common


class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState('False')


    def simulator(self):

        logging.info(f"Actuator {self.did} starting")

        while True:

            logging.info(f"Actuator {self.did}: {self.state.state}")

            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)


    def client(self):

        logging.info(f"Actuator Client {self.did} starting")

        while True:
                
            logging.info(f"Actuator Client {self.did}: {self.state.state}")

            url = f'{common.BASE_URL}actuator/{self.did}/current'

            response = requests.get(url)
            data = response.json()
            
            self.state = ActuatorState(data)

            time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)




    def run(self):
        sim_actuator_thread = threading.Thread(target=self.simulator)
        actuator_thread = threading.Thread(target=self.client)
        return sim_actuator_thread, actuator_thread

