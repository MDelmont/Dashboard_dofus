from dash import html, dcc
from dash.dependencies import Input, Output
import os
import requests
import logging

def extract_value(value):
    try:
 
        values = value if isinstance(value,int) else value[1]

        return int(values)
    except Exception as error:
        logging.error(f'From extract_value : {error}')

def make_form_value(value):
    try:

        value = extract_value(value)

        return str(value).replace('-','- ')
    except Exception as error:
        logging.error(f'From make_form_value : {error}')
def make_form_key(key):
    try:

        return str(key).replace('(','').replace(')','')
    except Exception as error:
        logging.error(f'From make_form_key : {error}')

def make_html_card_item(name='Amulette de la shokkot',
                        Niveau='200',
                        Effects={'Vitalité': [251, 300], 'Intelligence': [31, 40], 'Chance': [41, 60], 'Sagesse': [31, 40], 'Soin(s)': [4, 5], 'Portée': 1, 'Prospection': [16, 20], 'Dommage(s)': [16, 20], 'Résistance(s) Feu': [11, 15], '% Résistance Air': [7, 10], 'Retrait PA': [6, 8], 'Fuite': [-11, -15]},
                        Categorie='Amulettes',
                        img_url = 'https://static.ankama.com/dofus/www/game/items/200/7728.png'):
    
    try:
        filename = img_url.split('/')[-1]
        destination_dir = "assets/icons/items"
        # Chemin complet vers le fichier de destination
        destination_path = os.path.join(destination_dir, filename)
        # Nom de fichier pour l'image téléchargée
        filename = f"{name}.png"
        # Vérifier si le fichier existe déjà dans le répertoire de destination
        if not os.path.exists(destination_path):
            # Télécharger l'image depuis l'URL
            response = requests.get(img_url)
            response.raise_for_status()

            # Vérifier si le répertoire de destination existe, sinon le créer
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            # Écrire les données de l'image dans le fichier de destination
            with open(destination_path, "wb") as file:
                file.write(response.content)

            print("L'image a été téléchargée et stockée avec succès dans", destination_path)
        else:
            print("Le fichier existe déjà dans", destination_path)

        return html.Div(

            className='Card-item',

            children=[

                html.P(
                    name,
                    className='name_of_card',
                
                ),
                html.P(f'Niveau {Niveau}',
                    className='niveau_of_card',
                
                ),
                html.Img(className='visuel',src=destination_path),

                html.P(
                    'Effets',
                    className='Effets-name',
                
                ),
                html.Div(
                    className='Cont-Effets',
                    children=[
                        html.P(
                            f'{make_form_value(value)} {make_form_key(key)}',
                            className='Effet-text green',
                        ) 
                        
                        if extract_value(key,value) > 0   else 
                        
                        html.P(
                            f'{make_form_value(value)} {make_form_key(key)}',
                            className='Effet-text red',
                        )
                        for key, value in Effects.items() if key!= 'special'
                    ]

                ),
                html.Div(
                    className ='cont_categ',
                    children=[
                        html.P(f'Catégorie',
                            className='title_categ_of_card',
                        
                        ),

                        html.P(f'{Categorie}',
                            className='categ_of_card',
                        
                        ),
                    ]

                ),
            
                

            ]
        )
    except Exception as error:
        logging.error(f'From make_html_card_item : {error}')

        return None

