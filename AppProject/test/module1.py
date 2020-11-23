import time

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


loading_component = html.H1(
    style={},
    children='Loading...'
)

app = dash.Dash(__name__)
app.layout = html.Div([

    # Create arbitrary element to fire the callback below
    dcc.Input(id='trigger-live-chart'),
    html.Div(id='live-graph-container', children=[
        loading_component
    ]),
])

@app.callback(Output('live-graph-container', 'children'),
    [Input('trigger-live-chart','value')])
def generate_live_chart(_):
    time.sleep(3) # simmulate 3 seconds of data processing
    return dcc.Graph(
        id='live-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )


if __name__ == '__main__':
    app.run_server()
