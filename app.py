#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash
import logging
from datetime import datetime
import pytz
import pandas as pd

class App:
    __instance = None

    def __init__(self):
  
        self.start_time = datetime.now()
        self.launch_time = pytz.timezone('Europe/Paris').localize(datetime.now()).strftime('%Y-%m-%d_%H_%M')
   

        logging.basicConfig(filename=f"./logs/outlogs_{self.launch_time}.log",level=logging.INFO)

        logging.info(f"[ INITIALISATION : APP for Dashbord Dofus {self.launch_time} ]")
        
        #bootstrap_theme=[dbc.themes.BOOTSTRAP,'https://bootswatch.com/5/flatly/bootstrap.min.css']
        # meta_tags are required for the app layout to be mobile responsive

    @staticmethod
    def get_instance():
        if App.__instance is None:
            print("Création du service")
            App.__instance = App()
        return App.__instance


    app = dash.Dash(__name__, 
                            suppress_callback_exceptions=True,
                        meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}],
                        external_stylesheets= ['./assets/styles/styles.css']
                        )
    server = app.server
    data = pd.read_csv("./assets/datas/final_product.csv")