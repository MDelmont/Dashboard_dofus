#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import App
import plotly.graph_objects as go
import tkinter as tk
from tkinter import TclError
class Graph():
    def __init__(self):
        app = App().get_instance()
        self.df = app.data
         # Calculer la hauteur en pourcentage
        desired_percentage = 20  # Mettez ici le pourcentage désiré
        screen_height = tk.Tk().winfo_screenheight()
        self.desired_height = (screen_height * desired_percentage) / 100
        pass

    def get_graph_rep_by_item(self,categ_name='Tout'):
        
        df = self.df.copy()
        if categ_name != 'Tout':
            df = df[df['Type'] == categ_name]

        # Compter les occurrences de chaque niveau
        level_counts = df['niveau'].value_counts()
        
        echelle_max = level_counts.mean()*6

        fig = go.Figure(data=[go.Bar(x=level_counts.index, y=level_counts.values,
                                    marker=dict(color='#d6f204'))])
        if level_counts[200] >echelle_max:
            # Créer l'histogramme
            fig.update_traces(marker=dict(color=['#d6f204' if x != 200 else 'red' for x in level_counts.index]))
            fig.update_layout(
                 annotations=[
                    dict(
                        x=1.05, y=0.5,
                        xref="paper", yref="paper",
                        text="Dépasse la limite",
                        showarrow=False,
                        font=dict(color='red', family='Roboto, sans-serif'),
                        textangle=90
                    )
                ]
            )
        # Personnaliser la mise en page de l'histogramme
        
        fig.update_layout(
            xaxis_title="Niveau",
            yaxis_title="Quantité",
            plot_bgcolor='rgba(0,0,0,0)', # Fond transparent
            paper_bgcolor='#22231d',
            font=dict(color='#d6f204', family='Roboto, sans-serif'),
            margin=dict(t=50),           
         
            xaxis=dict(showgrid=False, tickfont=dict(family="Roboto", size=12, color="#d9d9d7")), 
            yaxis=dict(showgrid=False, range=[0, echelle_max],tickfont=dict(family="Roboto", size=12, color="#d9d9d7"),zeroline= False),  # Masquer la grille sur l'axe y
            height=self.desired_height,  # Définir la hauteur du graphique
           
        )


        # Afficher l'histogramme
        return fig
        
    
    def get_grap_level(self,methode='mean',categ_name='Tout'):
        df =self.df.copy()
        # Créer la boîte à moustaches pour chaque niveau
        fig = go.Figure()

        if categ_name != 'Tout':
            df = df[df['Type'] == categ_name]
            

        # Regrouper les données par niveau et calculer la médiane des poids

        grouped_data = df.groupby('niveau')['Poids'].mean().reset_index() if methode == 'mean' else df.groupby('niveau')['Poids'].median().reset_index() 

        # Créer le graphique en barres
        fig = go.Figure(data=go.Bar(x=grouped_data['niveau'], y=grouped_data['Poids'],
                           marker=dict(color='#d6f204')))

        # Personnaliser la mise en page du graphique
        fig.update_layout(
            xaxis_title="Niveau",
            yaxis_title="Poids",
            plot_bgcolor='rgba(0,0,0,0)',  # Fond transparent
            xaxis=dict(showgrid=False, tickfont=dict(family="Roboto", size=12, color="#d9d9d7")), 
            yaxis=dict(showgrid=False, tickfont=dict(family="Roboto", size=12, color="#d9d9d7"),zeroline= False),
            paper_bgcolor='#22231d',
            font=dict(color='#d6f204', family='Roboto, sans-serif'),
            title_font=dict(family="Roboto", size=18),
            height=self.desired_height*0.8,  # Définir la hauteur du graphique
            margin=dict(t=50)
        )

        return fig
    
    def get_graph_gauge(self,value=90,delta_ref=80,range_min=0,range_max = 100):


        fig = go.Figure(go.Indicator(
            mode = "gauge+delta+number",
            value = value,
            number={'font': {'size': 25}},
            delta = {'reference': delta_ref,
                    'font': {'family': "Roboto, sans-serif"},
                    'increasing': {'color': "#4ca53c"},
                    'decreasing': {'color': "#bf635a"}},

            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {'bar': {'color': '#d6f204',
                            'thickness': 1},
                    'shape': 'angular',
                    'bordercolor':'#d6f204',
                    'borderwidth': 0.5,  # Espacement fin entre le bord et la barre
                    'axis': {
                            'range': [range_min, range_max],
                            'tickcolor': '#d6f204',  
                        },
                        
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': delta_ref
                        }
                    
                    },

        )
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Fond transparent
            paper_bgcolor='#22231d',
            
            font=dict(color='#d6f204', family='Roboto, sans-serif'),
            margin=dict(l=60, r=60, t=0, b=0),  # Définir les marges souhaitées en pixels
            height=160,
        )
 
      
        
        fig.add_annotation(x=0.5, y=0.55, text="Poid", font= {'family': "Roboto, sans-serif" ,'color': "#d6f204",'size': 20}, showarrow=False)

        # fig.add_annotation(
        #     x=0.5, y=0.85,
        #     text="Moyenne des poids total",
        #     showarrow=False,
        #     font={ 'color': 'red', 'size':8}
        # )
        # fig.update_layout(
            
        #     shapes=[
        #         dict(
        #             type="line",
        #             x0=0.9, y0=0.838,
        #             x1=0.92, y1=0.838,
        #             line=dict(color="red", width=2)
        #         )
        #     ]
        # )
        return fig







