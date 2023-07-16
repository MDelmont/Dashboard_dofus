#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import App
import plotly.graph_objects as go
import tkinter as tk
import json
import re
import numpy as np
import logging

class Data():
    __instance = None
    def __init__(self):
        app = App().get_instance()
        self.df = app.data
        pass
    @staticmethod
    def get_instance():
        if Data.__instance is None:
   
            Data.__instance = Data()
        return Data.__instance
    
    def get_list_item(self, categ_name='Tout'):
        try:
            df = self.df.copy()
            if categ_name != 'Tout':
                df = df[df['Type'] == categ_name]
            return sorted(df['nom'].unique())
        except Exception as error:
            logging.error(f'From get_list_item : {error}')

    def make_dict_dropdown_item(self,categ_name='Tout'):
        try:
            return [{ 'label':name ,'value':name } for name in self.get_list_item(categ_name=categ_name)]
        except Exception as error:
            logging.error(f'From make_dict_dropdown_item : {error}')
    
    def get_list_grp_lvl(self):
        try:
            grp_lvl = self.df['grp_lvl'].unique()
            grp_lvl = np.concatenate([np.array(['Tout']),grp_lvl])

            return grp_lvl
        except Exception as error:
            logging.error(f'From get_list_grp_lvl : {error}')
    
    def make_dict_dropdown_grp_lvl(self):
        try:
      
            return [{ 'label':name ,'value':name } for name in self.get_list_grp_lvl()]
        except Exception as error:
            logging.error(f'From make_dict_dropdown_grp_lvl : {error}')
    
    def get_list_categorie_element(self):

        try:
            categorie_element = self.df['categorie_element'].unique()
        

            return categorie_element
        except Exception as error:
            logging.error(f'From get_list_categorie_element : {error}')
    
    def make_dict_dropdown_categorie_element(self):
        try:
      
            return [{ 'label':name ,'value':name } for name in self.get_list_categorie_element()]
        except Exception as error:
            logging.error(f'From make_dict_dropdown_categorie_element : {error}')
    
    def get_list_categ(self):
        try:
            types = self.df['Type'].unique()
            types = np.concatenate([np.array(['Tout']),sorted(types)])
    
            return types
        except Exception as error:
            logging.error(f'From get_list_categ : {error}')
    
    def make_dict_dropdown_categ(self):
        try:
      
            return [{ 'label':name ,'value':name } for name in self.get_list_categ()]
        
        except Exception as error:
            logging.error(f'From make_dict_dropdown_categ : {error}')
    
    def get_info_fo_card(self,name,categ_name):
        try:
            df = self.df
            row = df[df['nom']==name].iloc[0]
            if categ_name != 'Tout':
                df = df[df['Type'] == categ_name]
            Niveau = int(row['niveau'])
            Effects_brut =  str(row['effets'])
    
            pattern = r'(\'special\': \".+\",)'
            match = re.search(pattern, Effects_brut)
            special_value = None
            if match:
                special_value = match.group(1)
            if special_value:
                Effects_brut =  Effects_brut.replace(special_value,'')
            Effects_brut = Effects_brut.replace("'",'"')
            Effects = json.loads(Effects_brut)
            Categorie = row['Type']
            img_url = row['illustration_url']

            poids = int(row['Poids'])
            
            mean_poid_general = int(df['Poids'].mean())
            max_poid_general = int(df['Poids'].max())
            min_poid_general= int(df['Poids'].min())

            df_filtre_niv = df[df['niveau']==Niveau]
            mean_poid_by_lvl = df_filtre_niv['Poids'].mean()
            max_poid_by_lvl = int(df_filtre_niv['Poids'].max())
            min_poid_by_lvl= int(df_filtre_niv['Poids'].min())



            return name, Niveau, Effects, Categorie, img_url, poids, mean_poid_general, max_poid_general, min_poid_general, mean_poid_by_lvl, max_poid_by_lvl ,min_poid_by_lvl
        except Exception as error:
            logging.error(f'From get_info_fo_card : {error}')
    
