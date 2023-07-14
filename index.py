#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dash import html, dcc
from dash.dependencies import Input, Output
from app import App
import dash_auth
from resources.conf import Conf

from data import Data
from graph import Graph
import html_cont


conf = Conf()
app_instence = App().get_instance()
app = app_instence.app

server = app_instence.server


graph = Graph()

#layout rendu par l'application
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),

    html.Div(className='page-content', id='page-content',
        children=[
            
            html.Div(className='content-stats',
                children=[
                    html.Div(
                        className='Elements_categorie_lvl',
                        children = [
                            html.H4("Repartition des éléments par niveau",id="titre-ele_Categ")
                        ]
                    ),
                    html.Div(
                        className='Repartition_niveau_item',
                        children=[
                            html.H4("Répartition des items pa quantité et niveau",id="titre-rep-niv"),
                            dcc.Graph(id='Rep_By_Level',
                                      figure=graph.get_graph_rep_by_item())

                        ]
                    ),
                    html.Div(
                        className='Repartition_poids_par_niveau',
                        children=[
                            dcc.Graph(id='Rep_By_poids',
                                      figure=graph.get_grap_level(),
                                      ),
                            html.Div(id='Choise_your_methode',
                                     
                                children = [
                                    html.P('Méthode de groupement', className='title_choise'),
                                    dcc.Dropdown(id='groupby-method',
                                    options=[
                                        {'label': 'Médiane', 'value': 'median'},
                                        {'label': 'Moyenne', 'value': 'mean'}
                                    ],
                                    placeholder="Méthode de groupement",
                        
                                    value='mean',  # Valeur par défaut
                       
                                    searchable=False,  # Désactiver la recherche
                                    clearable=False,
                                ),
                            ]),

                            html.H4("Répartition des poids des items par niveau",id="titre-rep-poids")
                            
                            

                        ]
                        
                    ),
                    html.Div(
                        className='Select_item',
                        children=[
                             html.Div(
                                className = 'stats-item',

                                children=[
                                    html.Div(
                                        className='part_graph_item',
                                        children=[html.H4("Coparaison du poids pour le niveau de l'item",id="titre-item-graphe-1"),
                                                  html.Div(className='part_graph_item_fig', children=[dcc.Graph(id='graph_pod_by_lvl',figure=graph.get_graph_gauge())])]
                                    ),
                                    html.Div(
                                        className='part_graph_item',
                                        children=[
                                            html.H4("Coparaison du poids pour tous niveau",id="titre-item-graphe-2"),
                                            html.Div(className='part_graph_item_fig', children=[dcc.Graph(id='graph_pod_global',figure=graph.get_graph_gauge())])]
                                    )
                                    
                                        ]
                            ),
                            html.Div(id='cont_item_view',
                                     children=[
                                        

                                     ]),
                            html.Div(id='Choise_your_item',
                                     
                                children = [
                                    html.P('Item', className='title_choise'),
                                    dcc.Dropdown(id='list_item',
                                    options=Data().get_instance().make_dict_dropdown_item(),
                                    placeholder="Arabottes",
                        
                                    value='Abrabottes',  # Valeur par défaut
                       
                                    searchable=True,  # Désactiver la recherche
                                    clearable=False,
                                ),
                            ]),
                            html.H4("Visualisation d'item",id="titre-ele_item")
                        ]
                    ),
                ],     
            ),
            html.Div(className='Menu',
                children=[
                    html.Img(className='logo',src="./assets/icons/logo_dofus.png"),
                    html.H1('Dashbord des équipements du jeu Dofus', className='Titre_dashbord'),
                    html.Div(id='Choise_your_categorie',
                                     
                                children = [
                                    html.P('Catégorie', className='title_choise'),
                                    dcc.Dropdown(id='list_categ',
                                    options=Data().get_instance().make_dict_dropdown_categ(),
                                    placeholder='Tout',
                        
                                    value='Tout',  # Valeur par défaut
                       
                                    searchable=False,  # Désactiver la recherche
                                    clearable=False,
                                ),
                            ]),
                ],
            ), 
        ]),
        
    ])
# Créez la fonction de rappel
@app.callback(
    Output('Rep_By_Level', 'figure'),
    Output('list_item', 'options'),
    Output('list_item', 'value'),
    Input('list_categ', 'value')
)
def update_graph_quantity(categ_name):
    option_equip = Data().make_dict_dropdown_item(categ_name=categ_name)
    item_value = Data().get_list_item(categ_name=categ_name)[0]
    print(option_equip)
    print(item_value)
    return graph.get_graph_rep_by_item(categ_name=categ_name),option_equip,item_value
    # Votre logique de mise à jour de la figure ici
    # Utilisez groupby_method pour déterminer  
    
    
# Créez la fonction de rappel
@app.callback(
    Output('Rep_By_poids', 'figure'),
    Input('groupby-method', 'value'),
    Input('list_categ', 'value')
)
def update_graph_level(groupby_method,categ_name):
    return graph.get_grap_level(methode=groupby_method,categ_name=categ_name)
    # Votre logique de mise à jour de la figure ici
    # Utilisez groupby_method pour déterminer

# Créez la fonction de rappel
@app.callback(
    Output('cont_item_view', 'children'),
    Output('graph_pod_by_lvl', 'figure'),
    Output('graph_pod_global', 'figure'),
    Output('titre-item-graphe-1', 'children'),
    Input('list_item', 'value'),
    Input('list_categ', 'value')
)
def update_item(item_name,categ_name):
    name, Niveau, Effects, Categorie, img_url, poids, mean_poid_general, max_poid_general, min_poid_general, mean_poid_by_lvl, max_poid_by_lvl ,min_poid_by_lvl = Data().get_instance().get_info_fo_card(item_name,categ_name)
    return  [html_cont.make_html_card_item(name=name, Niveau=Niveau, Effects=Effects, Categorie=Categorie, img_url=img_url)], graph.get_graph_gauge(value=poids,delta_ref=mean_poid_by_lvl,range_min=min_poid_by_lvl,range_max=max_poid_by_lvl), graph.get_graph_gauge(value=poids,delta_ref=mean_poid_general,range_min=min_poid_general,range_max=max_poid_general),f"Coparaison du poids pour le niveau {Niveau}"

    # Votre logique de mise à jour de la figure ici
    # Utilisez groupby_method pour déterminer

# def generate_variables(app):
#     new_request = Nouvelle_demande(app)
#     follow_request = Suivi_demande(app)
#     plu_city_state = Plu_city_state(app)
#     utilisation = Guide_utilisation(app)
#     return new_request,follow_request,plu_city_state,utilisation


# new_request,follow_request,plu_city_state,utilisation = generate_variables(app)


# endpoints = {
#         '/':  follow_request.build_page(),
#          '/gestion_des_demandes/nouvelle_demande':  new_request.build_page(),
#          '/gestion_des_demandes/suivi_des_demandes': follow_request.build_page(),
#         '/etat_des_PLU_villes': plu_city_state.build_page(),
#         '/guide_utilisation':utilisation.build_page()
#         }

#callback pour mettre à jour les pages
# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     try:
#         return endpoints[pathname]
#     except Exception as error:
#         return f"ERROR : {error}"

if __name__ == '__main__':
    App.app.run_server(debug=True,port=8051)
    #App().app.run_server(host='0.0.0.0', port=3002)