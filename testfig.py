import plotly.graph_objects as go

# Création des données de l'exemple
x = [1, 2, 3, 4, 5]
y = [1, 3, 2, 4, 3]

# Création du tracé
trace = go.Scatter(x=x, y=y, marker=dict(color='#c7e600'))

# Création de la figure
fig = go.Figure(data=[trace])

# Affichage du graphique
fig.show()

['#04ed8d','#55e64d','#c7e600','#99d70a','#48bd1b','#03a629']