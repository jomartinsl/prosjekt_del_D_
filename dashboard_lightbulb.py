import tkinter as tk
from tkinter import ttk
import logging
import requests
from smarthouse import domain

from messaging import ActuatorState
import common


def lightbulb_cmd(state, did):
    new_state = state.get()
    logging.info(f"Dashboard: {new_state}")
    Geturl = f"http://127.0.0.1:8000/smarthouse/actuator/{did}/current"
    Puturl = f"http://127.0.0.1:8000/smarthouse/actuator/{did}"
    response = requests.get(Geturl)

    domain.SmartHouse.get_device_by_id(did).state = new_state

    if new_state == 'On':
        new_data = {"state": "running"}
        domain.SmartHouse.get_device_by_id(did).state = True
        Cmd_To_Actuator = requests.put(Puturl)

    if new_state == "Off":
        new_data = {"state": "off"} # oppdaterer ny tilstand til OFF
        domain.SmartHouse.get_device_by_id(did).state = False
        Cmd_To_Actuator = requests.put(Puturl)
    
    logging.info(f"Dashboard: {new_state}")

def init_lightbulb(container, did):

    lb_lf = ttk.LabelFrame(container, text=f'LightBulb [{did}]')
    lb_lf.grid(column=0, row=0, padx=20, pady=20, sticky=tk.W)

    # variable used to keep track of lightbulb state
    lightbulb_state_var = tk.StringVar(None, 'Off')

    on_radio = ttk.Radiobutton(lb_lf, text='On', value='On',
                               variable=lightbulb_state_var,
                               command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    on_radio.grid(column=0, row=0, ipadx=10, ipady=10)

    off_radio = ttk.Radiobutton(lb_lf, text='Off', value='Off',
                                variable=lightbulb_state_var,
                                command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    off_radio.grid(column=1, row=0, ipadx=10, ipady=10)
