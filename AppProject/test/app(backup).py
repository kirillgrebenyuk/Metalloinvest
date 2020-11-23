from navbar import Navbar
from dash.dependencies import Input, Output, State

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
import dash.dependencies
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import pyodbc
import base64
import datetime

nav = Navbar()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.title = "Система ИАС УЭР"           # Название сайта

cnn = pyodbc.connect('DRIVER={SQL Server};PORT=port;SERVER=192.168.0.85;PORT=1433;DATABASE=Piramida2000;UID=sa;PWD=pswd')
#date = '2020-10-29'
#query = "SELECT dev.NAME,dat.PARNUMBER,dat.ITEM,dat.VALUE0,dat.VALUE1,dat.DATA_DATE FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND dat.DATA_DATE > '"+date+"' AND (dat.OBJECT IN(4413)) AND dat.ITEM = 1 ORDER BY dat.DATA_DATE ASC"
#df=pd.read_sql(query, con=cnn, parse_dates=['DATA_DATE'])

#cursor = cnn.cursor()
#cursor.execute(query)

#data_uri = base64.b64encode(open('assets/unnamed.png', 'rb').read()).decode('utf-8')

#for row in cursor:
#	ch = row[0]
#fig = px.line(df, x="DATA_DATE", y="VALUE0",color="NAME")

body = html.Div([	
    #-------------------------------------------
    #html.Div(["Введите даты: ",
    #          dcc.DatePickerRange(id='my-input', 
    #                               min_date_allowed=datetime.date(2020, 1, 1),
    #                               max_date_allowed=datetime.date(2020, 12, 1),
    #                               start_date = datetime.date(2020,11, 1),
    #                               end_date=datetime.date(2020, 11, 2))]),
    #dcc.Graph(id='graph-with-slider'),
    #-------------------------------------------
    #dcc.Graph(
    #    id='example-graph1',
    #    figure=fig    
    #),
	#html.H4(children=ch),
	#dt.DataTable(
	#	data=df.to_dict('record'),
	#	columns=[{'id': c, 'name': c} for c in df.columns],
    #    page_size=10
	#),
    html.H2('Потребление по всему заводу',id="button-clicks", className="TitleSite"),
    html.Div(className="divZavod",children=[
        #html.A(html.Img(src='data:image/png;base64,{}'.format(data_uri)), href='#zavod1'),
        html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0),
        html.Img(src='assets/unnamed.png', id='image-btn-mgok', className="btnZavod", n_clicks = 0),
        html.Img(src='assets/unnamed.png', id='image-btn-oemk', className="btnZavod", n_clicks = 0),
        html.Img(src='assets/unnamed.png', id='image-btn-ystal', className="btnZavod", n_clicks = 0)
    ]),
    html.Div(id="some-component")
])

def Homepage():
    layout = html.Div([
    nav,
    body
    ])
    return layout

app.layout = Homepage()

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

#---------------------------------------------
@app.callback(
    Output(component_id='graph-with-slider', component_property='figure'),
    [Input(component_id='my-input', component_property='start_date'),
     Input(component_id='my-input', component_property='end_date')]
)
def update_figure(start_date,end_date):
    
    qsql = "SELECT dev.NAME,dat.PARNUMBER,dat.ITEM,dat.VALUE0,dat.VALUE1,dat.DATA_DATE FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND dat.DATA_DATE > '"+start_date+"' AND dat.DATA_DATE < '"+end_date+"' AND (dat.OBJECT IN(4412,4413)) AND dat.ITEM = 1 ORDER BY dat.DATA_DATE ASC"
    cnn = pyodbc.connect('DRIVER={SQL Server};PORT=port;SERVER=192.168.0.85;PORT=1433;DATABASE=Piramida2000;UID=sa;PWD=pswd')
    dff = pd.read_sql_query(qsql,cnn)
    fig = px.line(dff, x="DATA_DATE", y="VALUE0", color="NAME", hover_name="NAME")

    return fig

@app.callback(
    Output("some-component", "property"), 
    [Input("image-btn-lgok", "n_clicks"),
     Input("image-btn-mgok", "n_clicks"),
     Input("image-btn-oemk", "n_clicks"),
     Input("image-btn-ystal", "n_clicks")])
def on_off(n_lgok,n_mgok,n_oemk,n_ystal):
    if not n_lgok or n_lgok % 2 == 0:
        print('Нажата картинка Лгок')
    else:
        print('Отжата картинка Лгок')
    if not n_mgok or n_mgok % 2 == 0:
        print('Нажата картинка МГОК')
    else:
        print('Отжата картинка МГОК')
    if not n_oemk or n_oemk % 2 == 0:
        print('Нажата картинка ОЭМК')
    else:
        print('Отжата картинка ОЭМК')
    if not n_ystal or n_ystal % 2 == 0:
        print('Нажата картинка Уральская сталь')
    else:
        print('Отжата картинка Уральская сталь')
#---------------------------------------------

cnn.close()

if __name__ == '__main__':
    # Run the app server on localhost:8050
    app.run_server()


#df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
#fig = px.scatter(df, x="gdp per capita", y="life expectancy",
#                 size="population", color="continent", hover_name="country",
#                log_x=True, size_max=60)