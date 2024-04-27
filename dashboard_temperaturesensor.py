import tkinter as tk
from tkinter import ttk

import logging
import requests

from messaging import SensorMeasurement
import common


def refresh_btn_cmd(temp_widget, did):
    logging.info("Temperature refresh")
    url = common.BASE_URL + f"sensor/{did}/current"
    response = requests.get(url)
    if response.status_code == 200:
        temperature = response.json()['temperature']['value']
        sensor_measurement = SensorMeasurement(temperature)
        temp_widget['state'] = 'normal'
        temp_widget.delete(1.0, 'end')
        temp_widget.insert(1.0, sensor_measurement.value)
        temp_widget['state'] = 'disabled'
    else:
        logging.error(f"Failed to fetch temperature: {response.text}")



def init_temperature_sensor(container, did):

    ts_lf = ttk.LabelFrame(container, text=f'Temperature sensor [{did}]')

    ts_lf.grid(column=0, row=1, padx=20, pady=20, sticky=tk.W)

    temp = tk.Text(ts_lf, height=1, width=10)
    temp.insert(1.0, 'None')
    temp['state'] = 'disabled'

    temp.grid(column=0, row=0, padx=20, pady=20)

    refresh_button = ttk.Button(ts_lf, text='Refresh',
                                command=lambda: refresh_btn_cmd(temp, did))

    refresh_button.grid(column=1, row=0, padx=20, pady=20)
