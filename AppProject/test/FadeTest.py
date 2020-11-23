import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.layout = html.Div(
    [
        dbc.Button("Toggle fade", id="fade-button", className="mb-3"),
        dbc.Fade(
            dbc.Card(
                dbc.CardBody(
                    html.P(
                        "This content fades in and out", className="card-text"
                    )
                )
            ),
            id="fade",
            is_in=True,
            appear=False,
        ),
    ]
)

print(pathname)


@app.callback(
    Output("fade", "is_in"),
    [Input("fade-button", "n_clicks")],
    [State("fade", "is_in")],
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked        
        return True
    return not is_in

if __name__ == '__main__':
    app.run_server()