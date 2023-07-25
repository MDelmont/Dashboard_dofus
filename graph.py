#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import App
import plotly.graph_objects as go
import logging

class Graph():
    def __init__(self):
        app = App().get_instance()
        self.df = app.data
        self.desired_height=250

        pass

    def get_graph_rep_by_item(self,categ_name='Tout'):
        
        try:
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
                # height=self.desired_height,  # Définir la hauteur du graphique
            
            )


            # Afficher l'histogramme
            return fig
        except Exception as error:
            logging.error(f'From get_graph_rep_by_item : {error}')
        
    
    def get_grap_level(self,methode='mean',categ_name='Tout'):
        try:
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
                # height=self.desired_height*0.8,  # Définir la hauteur du graphique
                margin=dict(t=50)
            )

            return fig
        except Exception as error:
            logging.error(f'From get_grap_level : {error}')

    def get_graph_gauge(self,value=90,delta_ref=80,range_min=0,range_max = 100):

        try:
            fig = go.Figure(go.Indicator(
                mode = "gauge+delta+number",
                value = value,
                number={'font': {'size': 20}},
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
                paper_bgcolor='rgba(0,0,0,0)',
                
                font=dict(color='#d6f204', family='Roboto, sans-serif'),
                margin=dict(l=60, r=60, t=15, b=15),  # Définir les marges souhaitées en pixels
                height=150,
                width=300,
            
            )
    
        
            
            fig.add_annotation(x=0.5, y=0.55, text="Poid", font= {'family': "Roboto, sans-serif" ,'color': "#d6f204",'size': 15}, showarrow=False)

            return fig
        except Exception as error:
            logging.error(f'From get_graph_gauge : {error}')
        

    def get_graph_pie(self,categ_name='Tout',categ_ele='mono-élément',grp_lvl='Tout'):
        try:
            df =self.df.copy()
            # Créer un sous-ensemble de données pour chaque catégori
            df = df[df['categorie_element'] == categ_ele]
            if grp_lvl != 'Tout':
                df = df[df['grp_lvl'] == grp_lvl]
            
            if categ_name != 'Tout':
                df = df[df['Type'] == categ_name]

            # Calculer les pourcentages des éléments dans chaque catégorie
            element_counts = df['Elements'].value_counts(normalize=True) * 100
            nb_color = len(df['Elements'].unique())
            color_list = ['#04ed8d','#55e64d','#c7e600','#99d70a','#48bd1b','#03a629'][0:nb_color]
            # Créer le pie chart
            fig = go.Figure(data=[go.Pie(labels=element_counts.index, values=element_counts.values, marker=dict(colors=color_list))])
            if grp_lvl != 'Tout':
                fig.update_layout(title=dict(text=f"Graphique pour la catégorie <br>{categ_ele}  <br>concernant les du niveau {grp_lvl}",x=0.5,xanchor='center'))
            else:
                fig.update_layout(title=dict(text=f"Graphique pour la catégorie <br>{categ_ele}",x=0.5,xanchor='center'))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',  # Fond transparent
                paper_bgcolor='#22231d',
                
                font=dict(color='#d6f204', family='Roboto, sans-serif'),
        
            
            )
        
            # Mise à jour du layout pour personnaliser la légende
            fig.update_layout(
                legend=dict(

                    orientation='h',  # Orientation horizontale
                    x=0.3,
                    y=-0.2,
                )
            )
            # Afficher les filtres interactifs pour les catégories et grp_lvls
            return fig

        except Exception as error:
            logging.error(f'From get_graph_pie : {error}')

        
