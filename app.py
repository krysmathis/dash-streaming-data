# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State, Input, Output, Event
from stock_reader import get_yahoo_data #local file
from datetime import datetime, timedelta
import random
import plotly.graph_objs as go
from collections import deque
import sqlite3
import pandas as pd
import numpy as np
import base64

styles = {
    'background': 'white',
    'text': 'black'
}

X = deque(maxlen=20)
Y = deque(maxlen=20)
X.append(1)
Y.append(1)


sqlite_file = '/Users/krystopher/Desktop/my_db.sqlite'

conn = sqlite3.connect(sqlite_file)

static_df = pd.read_sql('SELECT * FROM DATA', conn)

conn.close()



def get_data_for_static():
    pass

def write_to_data_uri(s):
    """
    Writes to a uri.
    Use this function to embed javascript into the dash app.
    Adapted from the suggestion by user 'mccalluc' found here:
    https://community.plot.ly/t/problem-of-linking-local-javascript-file/6955/2
    """
    uri = (
        ('data:;base64,').encode('utf8') +
        base64.urlsafe_b64encode(s.encode('utf8'))
    ).decode("utf-8", "strict")
    return uri



app = dash.Dash()
app.layout = html.Div([
    
    dcc.Dropdown(id='dropdown',
        options=[{'label': 'Test', 'value': 1}],
        value=['test_value'],
        multi=False
    ),
    
    # dcc.Input(id='my-id', value='initial value', type="text"),
    
    html.Button('Click Me', id='my-button', n_clicks=0),
    html.Button('Click Me', id='btn', n_clicks=0),
    html.Div('',id='btnMessage'),
    html.Div(id='my-div', children='yellow'),
    
    dcc.Graph(id='live-graph', animate=True),
    
    dcc.Interval(
        id='graph-update',
        interval=500
    ),

    dcc.Graph(id='static-graph', figure = {
        'data': [
                {'x': static_df.X, 'y': static_df.Y, 'type': 'line', 'name': 'values'},
                # {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montréal'},
            ],
        'layout': {
            'title': 'Static Data'
        }
    })
])

@app.callback(Output('live-graph', 'figure'),
            events= [Event('graph-update', 'interval')])
def update_graph():
    
    global X
    global Y
    X.append(X[-1] + 1)
    Y.append(Y[-1]+(Y[-1]*random.uniform(-0.1,0.1)))

    data = go.Scatter(
        x = list(X),
        y = list(Y),
        name = 'Scatter', 
        mode = 'lines+markers'
    )
    return {'data': [data], 'layout': go.Layout(title="Streaming Data", xaxis = dict(range=[min(X), max(X)]),
                                                yaxis = dict(range=[min(Y), max(Y)])        
    )}



# @app.callback(
#     Output(component_id='my-div', component_property='children'),
#     [Input('my-button', 'n_clicks')],
#     state=[State(component_id='my-id', component_property='value')]
# )
@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input('my-button', 'n_clicks')]
)
def update_output_div(n_clicks):
    print('a thousand comanches...')
    return 'You\'ve entered "{}" and clicked {} times'.format(1,n_clicks)


app.scripts.append_script({
    'external_url': write_to_data_uri("""
    setTimeout(function(){
        document.getElementById("btn").addEventListener("click", function(){
            document.querySelector('#btnMessage').innerHTML = 'clicked'
        });

    }, 1000);
    """)})
# external_js = ['script.js']
# for js in external_js:
#     app.scripts.append_script({'absolute_path': js})


if __name__ == '__main__':
    app.run_server(debug=True)