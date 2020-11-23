from dash.dependencies import Output,Input,State

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pyodbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

cnn = pyodbc.connect('DRIVER={SQL Server};PORT=port;SERVER=192.168.10.11;PORT=1433;DATABASE=EDC_ASKUE;UID=sa;PWD=ZAQ!2wsx')  #Подключение к БД

sqlsummaOEMK = "SELECT SUM([Val]) FROM [EDC_ASKUE].[dbo].[PointMains] WHERE ID_PP IN (9630,10036,10037,10038) AND (DT > '10-01-2020' AND DT < '11-01-2020')"
sqlobOEMK = "SELECT SUM([Val]) FROM [EDC_ASKUE].[dbo].[PointMains] WHERE ID_PP IN (5239,5240,5241,5242,5243,5244,5246,5249,5250,5251) AND (DT > '10-01-2020' AND DT < '11-01-2020')"
sqlPaOEMK = "SELECT SUM([Val]) FROM [EDC_ASKUE].[dbo].[PointMains] WHERE ID_PP IN (4806,4808,4810,4812,4814,4816,4819,4821,4823) AND (DT > '10-01-2020' AND DT < '11-01-2020')"
sqlTempOEMK = "SELECT AVG([Val]) FROM [EDC_ASKUE].[dbo].[PointMains] WHERE ID_PP IN (4807,4809,4811,4813,4815,4817,4818,4820,4822) AND (DT > '10-01-2020' AND DT < '11-01-2020')"
cursor = cnn.cursor().execute(sqlsummaOEMK)
for row in cursor:summaOEMK = row[0]
cursor = cnn.cursor().execute(sqlobOEMK)
for row in cursor:obOEMK = row[0]
cursor = cnn.cursor().execute(sqlPaOEMK)
for row in cursor:PaOEMK = row[0]
cursor = cnn.cursor().execute(sqlTempOEMK)
for row in cursor:TempOEMK = row[0]

app.layout = html.Div([
    html.P('Цех обжига извести'),
    html.Br(),
    html.Button(id='button1',
                children=['Энергоресурсы за октябрь'],
                className='buttonCss3',
                n_clicks=0
    ),
    html.Button(id='button2',
                children=['Электроэнергия за октябрь'],
                className='buttonCss3',
                n_clicks=0,
    ),
    dbc.Modal(
            [
                dbc.ModalHeader("Цех обжига извести"),
                dbc.ModalBody([
                    html.H5("Объем = {} м3".format(round(obOEMK,2))),                    
                    html.H5("Давление = {} Па".format(round(PaOEMK,2))),                    
                    html.H5("Средняя температура = {} C".format(round(TempOEMK,2)))
                    ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close1", className="ml-auto")
                ),
            ],
            id="modal1",
        ),
    dbc.Modal(
            [
                dbc.ModalHeader("Цех обжига извести"),
                dbc.ModalBody("Активная энергия прием (A+) = {} кВт*ч".format(round(summaOEMK,2))),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close2", className="ml-auto")
                ),
            ],
            id="modal2",
        )     
])

@app.callback(Output('button1', 'className'), [Input('button1', 'n_clicks')])
def change_button_style(n_clicks):

    if n_clicks%2 > 0:
        return 'buttonCss3New'

    else:
        return 'buttonCss3'

@app.callback(Output('button2', 'className'), [Input('button2', 'n_clicks')])
def change_button_style(n_clicks):

    if n_clicks%2 > 0:
        return 'buttonCss3New'

    else:
        return 'buttonCss3'

@app.callback(
    Output("modal1", "is_open"),
    [Input("button1", "n_clicks"), Input("close1", "n_clicks")],
    [State("modal1", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
@app.callback(
    Output("modal2", "is_open"),
    [Input("button2", "n_clicks"), Input("close2", "n_clicks")],
    [State("modal2", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server()