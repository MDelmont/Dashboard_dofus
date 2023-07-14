import json
import re
json_str_brut = '''{'Vitalité': [401, 450], 'Intelligence': [81, 120], 'Tacle': [16, 20], 'Dommage(s)': [16, 20], 'Retrait PM': [11, 15], '% Dommages distance': -15, 'PM': -2, 'special': "Si le porteur est au contact d'un ennemi au début de son tour, il gagne 20 Retrait PM pour 1 tour, sinon, il gagne 30 Tacle. Quand le porteur tue un adversaire (hors invocations) avec des dommages directs, il gagne 1 PM jusqu'à la fin du combat, cumulable 3 fois maximum.", 'Fuite': -20, '% Résistance Feu': [7, 10]}

'''
# Remplacer les simples guillemets par des guillemets doubles

pattern = r'(\'special\': \".+\",)'
match = re.search(pattern, json_str_brut)

special_value = None
if match:
    special_value = match.group(1)
if special_value:
    json_str_brut =  json_str_brut.replace(special_value,'')
json_str = json_str_brut.replace("'",'"')


# Charger le JSON
data = json.loads(json_str)



