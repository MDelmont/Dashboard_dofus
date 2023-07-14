import plotly.graph_objects as go

fig = go.Figure(go.Indicator(
    mode = "gauge+delta+number",
    value = 50,
    delta = {'reference': 80,
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
                    'range': [0, 100],
                    'tickcolor': '#d6f204',  
                },
                
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            
            },


))
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',  # Fond transparent
    paper_bgcolor='#22231d',
    font=dict(color='#d6f204', family='Roboto, sans-serif'))
fig.add_annotation(x=0.5, y=0.6, text="Poid", font= {'family': "Roboto, sans-serif", 'size': 50, 'color': "#d6f204"}, showarrow=False)

fig.add_annotation(
    x=1, y=0.85,
    text="Moyenne des poids total",
    showarrow=False,
    font={'size': 12, 'color': 'red'}
)
fig.update_layout(
    shapes=[
        dict(
            type="line",
            x0=0.9, y0=0.838,
            x1=0.92, y1=0.838,
            line=dict(color="red", width=2)
        )
    ]
)

fig.show()