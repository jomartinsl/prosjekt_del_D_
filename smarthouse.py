import logging
import subprocess
import threading
from smarthouse_temperature_sensor import Sensor
from smarthouse_lightbulb import Actuator

import common

log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

# https://realpython.com/intro-to-python-threading/

def start_api():
    # Denne funksjonen vil starte api.py skriptet
    subprocess.run(["python", "smarthouse/api.py"])

def start_dashboard():
    # Denne funksjonen vil vente til API-serveren er oppe før den starter dashboard.py
    subprocess.run(["python", "dashboard.py"])


api_thread = threading.Thread(target=start_api)
api_thread.start()

# Opprett en tråd for å kjøre dashboardet
dashboard_thread = threading.Thread(target=start_dashboard)
dashboard_thread.start()


# Starter sensor tråden
sensor = Sensor(common.TEMPERATURE_SENSOR_DID)
sim_sensor_thread, client_sensor_thread = sensor.run()


# Starter actuator tråden
actuator = Actuator(common.LIGHTBULB_DID)
sim_actuator_thread, actuator_thread = actuator.run()


sim_actuator_thread.start()
actuator_thread.start()
sim_sensor_thread.start()
client_sensor_thread.start()




