import logging
import threading
import time
import math
import requests
from smarthouse import persistence

from messaging import SensorMeasurement
import common


class Sensor:

    def __init__(self, did):
        self.did = did
        self.measurement = SensorMeasurement('0.0')

    def simulator(self):

        logging.info(f"Sensor {self.did} starting")

        while True:

            temp = round(math.sin(time.time() / 10) * common.TEMP_RANGE, 1)

            logging.info(f"Sensor {self.did}: {temp}")

            self.measurement.set_temperature(str(temp))

            time.sleep(common.TEMPERATURE_SENSOR_SIMULATOR_SLEEP_TIME)

            print(self.measurement.value)




    def client(self):

        logging.info(f"Sensor Client {self.did} starting")

        while True:

            logging.info(f"Sensor Client {self.did}: {self.measurement.value}")

            url = f'{common.BASE_URL}sensor/{self.did}/current/{self.measurement.value}'
            
            requests.post(url, json=self.measurement.to_json())
            
            time.sleep(common.TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME)


    def run(self):
        sim_sensor_thread = threading.Thread(target=self.simulator)
        sensor_thread = threading.Thread(target=self.client)
        return sim_sensor_thread, sensor_thread


