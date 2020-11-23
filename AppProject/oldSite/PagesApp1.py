from navbar import Navbar, Sidebar
from math import ceil
from dash.dependencies import Output,Input,State

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import pyodbc
import datetime
import dash_table as dt
import textwrap

nav = Navbar()
sidebar = Sidebar()

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.title = "Система ИАС УЭР"           # Название сайта

cnn = pyodbc.connect('DRIVER={SQL Server};PORT=port;SERVER=192.168.0.85;PORT=1433;DATABASE=Piramida2000;UID=sa;PWD=pswd')  #Подключение к БД

LGOK = '4407,4408,4409,4410,4411,4412,4413,4414'
#MGOK = '4418,4407,4408,4409,4410,4411,4412,4413,4415'
#OEMK = '4417,4414,4415,4417'
#YSTAL = '4418,4369,4413,4414,4415'

sqlsummaLGOK = "SELECT SUM(VALUE0)as Summa FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND (dat.DATA_DATE > '01-01-2020' AND dat.DATA_DATE < '11-01-2020')AND OBJECT IN ("+LGOK+") AND dat.ITEM = 1"
#sqlsummaMGOK = "SELECT SUM(VALUE0)as Summa FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND (dat.DATA_DATE > '01-01-2020' AND dat.DATA_DATE < '11-01-2020')AND OBJECT IN ("+MGOK+") AND dat.ITEM = 1"
#sqlsummaOEMK = "SELECT SUM(VALUE0)as Summa FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND (dat.DATA_DATE > '01-01-2020' AND dat.DATA_DATE < '11-01-2020')AND OBJECT IN ("+OEMK+") AND dat.ITEM = 1"
#sqlsummaYSTAL = "SELECT SUM(VALUE0)as Summa FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND (dat.DATA_DATE > '01-01-2020' AND dat.DATA_DATE < '11-01-2020')AND OBJECT IN ("+YSTAL+") AND dat.ITEM = 1"
cursor = cnn.cursor().execute(sqlsummaLGOK)
for row in cursor:summaLGOK = row[0]
#cursor = cnn.cursor().execute(sqlsummaMGOK)
#for row in cursor:summaMGOK = row[0]
#cursor = cnn.cursor().execute(sqlsummaOEMK)
#for row in cursor:summaOEMK = row[0]
#cursor = cnn.cursor().execute(sqlsummaYSTAL)
#for row in cursor:summaYSTAL = row[0]

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
     dbc.Row(
            [
                dbc.Col(sidebar, md=2),
                dbc.Col(html.Div(id='page-content'))
            ]
        ),
])

index_page = html.Div([
    #html.H2('Потребление по всему заводу',id="button-clicks", className="TitleSite"),
    html.Div(className="divZavod",children=[        
    html.P(str(ceil(summaLGOK))+' кВт*ч',className="Potreblenie"),
    dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0), href='/page-1'),
    
    #html.P(str(ceil(summaMGOK))+' кВт*ч',className="Potreblenie"),
    #dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0), href='/page-2'),
    
    #html.P(str(ceil(summaOEMK))+' кВт*ч',className="Potreblenie"),
    #dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0), href='/page-3'),
    
    #html.P(str(ceil(summaYSTAL))+' кВт*ч',className="Potreblenie"),
    #dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0), href='/page-4')
    ]),
    #html.Br(),
    #dcc.Link('Go to Page 2', href='/page-2'),
])

page_1_layout = html.Div([
    html.H1('ЛГОК'),
    html.Br(),
    html.H6("Вывод SQL запроса"),
    html.Div(["Введите даты: ",
              dcc.DatePickerRange(id='my-input', 
                                   min_date_allowed=datetime.date(2020, 1, 1),
                                   max_date_allowed=datetime.date(2020, 11, 1),
                                   start_date = datetime.date(2020,1, 1),
                                   end_date=datetime.date(2020, 11, 1))]),
    html.Div(id='graph-with-slider', children=[
            dcc.Loading(
                id="loading-1",
                type="deaful",
                children=html.Div(id="graph-with-slider"),
                className="loadingStyle"
            )
        ],className="grafPage1"),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])
@app.callback(
    Output(component_id='graph-with-slider', component_property='children'),
    [Input(component_id='my-input', component_property='start_date'),
     Input(component_id='my-input', component_property='end_date')]
)
def update_figure(start_date,end_date):
    qsql = "SELECT dev.NAME,dat.PARNUMBER,dat.ITEM,dat.VALUE0,dat.VALUE1,dat.DATA_DATE FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND dat.DATA_DATE > '"+start_date+"' AND dat.DATA_DATE < '"+end_date+"' AND (dat.OBJECT IN(4407,4408,4409,4410,4411,4412,4413,4414)) AND dat.ITEM = 1 ORDER BY dat.DATA_DATE ASC"
    dff = pd.read_sql_query(qsql,con=cnn)
    fig = px.line(dff, x="DATA_DATE", y="VALUE0", color="NAME", hover_name="NAME")
    fig.update_traces(mode="markers+lines")

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )

    return dcc.Graph(figure = fig, animate=True)

@app.callback(Output('page-1-content', 'children'),
              [Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


page_2_layout = html.Div([
    html.H1('МГОК'),
    dcc.RadioItems(
        id='page-2-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    ),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)

page_3_layout = html.Div([
    html.H1('ОЭМК'),
    html.Div(id='page-3-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

page_4_layout = html.Div([
    html.H1('Уральская сталь'),
    html.Div(id='page-4-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

page_setting = html.Div([
    html.H1('Настройки'),
    html.Div(id='setting-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

page_help = html.Div([
    html.H1('О системе'),
    html.Div(id='about-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

page_about = html.Div([
    html.H1('Справка'),
    html.Div(id='help-content'),
    html.Br(),
    dcc.Link('Ссылка на отсутствующую ссылку', href='/page-noname'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]

# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    
    if pathname == '/':
        return index_page
    elif pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    elif pathname == '/setting':
        return page_setting
    elif pathname == '/about':
        return page_help
    elif pathname == '/help':
        return page_about
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Страница не найдена", className="text-danger"),
                html.Hr(),
                html.P(f"Страница {pathname} не найдена..."),
            ]
        )
    # You could also return a 404 "URL not found" page here

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

if __name__ == '__main__':
    app.run_server()