from navbar import Navbar,Sidebar

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import datetime
from dash.dependencies import Input, Output, State

import pyodbc

nav = Navbar()            # Подключаем код навигационной панели
sidebar = Sidebar()       # Подключаем код левого меню

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])       #Подключение темы для сайта

app.title = "Система ИАС УЭР Металлоинвест"           # Название сайта

preload_page = dbc.Fade(id='pr_load',children=[
                html.Div(id='p_prldr',children=[
                        html.Div(className='contpre',children=[
                            html.Span(className='svg_anm'),
                            html.Br(),
                            html.P('Подождите идет загрузка')
                            ])
                        ]),
                    ],
                    is_in=True,
                    appear=False,
                )

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    preload_page,
    nav,    
    dbc.Row([
            dbc.Col(sidebar, id="left", className="leftMenu", md=2),
            dbc.Col([
                html.Div(id='page-content'),
                ])
        ],className="mainRow")
    ])
#------------------------------------
# Главная страница
#------------------------------------

#--------Графики для главной страницы
cnn = pyodbc.connect('DRIVER={SQL Server};PORT=port;SERVER=192.168.10.11;PORT=1433;DATABASE=EDC_ASKUE;UID=sa;PWD=ZAQ!2wsx')  #Подключение к БД
sql = "SELECT * FROM [EDC_ASKUE].[dbo].[PointMains] WHERE ID_PP = 6029 AND (DT > '2020-01-01' AND DT < '2020-11-14')"
dff = pd.read_sql_query(sql,con=cnn)

fig = {'data': [ {'x': dff['DT'],'y': dff['Val'],'type': 'line'} ],
        'layout': go.Layout(xaxis={"title":"Дата"}, yaxis={"title":"Значение"}),
        'color': "#FF00FF"}
fig1 = {'data': [ {'x': dff['DT'],'y': dff['Val'],'type': 'bar'} ],
        'layout': go.Layout(xaxis={"title":"Дата"}, yaxis={"title":"Значение"}),
        'type': 'bar'}

index_page = html.Div(id='index_page',children=[ 
                dbc.Row([
                     dbc.Col([
                       dcc.Link(html.Img(src='assets/unnamed.png',width='100%', id='image-btn-oemk', n_clicks = 0), href='/page-1')
                       ], md=3),
                   dbc.Col([
                       html.H3('Лебединский горно-обогатительный комбинат'),
                       html.Hr(),
                       dbc.Row([dbc.Col(dbc.Card("Ресурс 1",color="danger", body=True,outline=True), width=3), 
                                dbc.Col(dbc.Card("Ресурс 2",color="info", body=True), width=3), 
                                dbc.Col(dbc.Card("Ресурс 3",color="secondary", body=True,outline=True), width=3), 
                                dbc.Col(dbc.Card("Ресурс 4",color="success", body=True,outline=True), width=3)], className="rowCard"),
                       html.Br(),
                       dbc.Row([
                          html.Div(["Введите даты: ",
                            dcc.DatePickerRange(id='my-input', 
                                                min_date_allowed=datetime.date(2020, 1, 1),
                                                max_date_allowed=datetime.date(2020, 12, 1),
                                                start_date = datetime.date(2020,10, 28),
                                                end_date=datetime.date(2020, 10, 30),
                                                month_format='DD-MM-YYYY',
                                                display_format='DD-MM-YYYY')]),
                       ]),                  
                       dbc.Row([
                           dbc.Col(dcc.Graph(id='example-graph1',figure=fig), md=4),                           
                           dbc.Col(dcc.Graph(id='example-graph2',figure=fig1), md=8)]),
                       dbc.Row([
                           dbc.Col(dcc.Graph(id='example-graph3',figure=fig), md=8),
                           dbc.Col(dcc.Graph(id='example-graph4',figure=fig1), md=4)])
                       ], md=9),
                   ])
    ])

#------------------------------------
# Второй уровень по сайту
#------------------------------------

page_1_layout = html.H4('Страница предназначенная для мониторинга')
page_2_layout = html.H4('Страница предназначенная для анализа')
page_3_layout = html.H4('Страница предназначенная для планирования и прогнозирования')
page_4_layout = html.H4('Страница предназначенная для мнемосхем')

#------------------------------------
# Указываем активные в левом меню
#------------------------------------

@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]
  

#--------------------------------------------------
# Обработка ссылок и открытие необходимого контента
#--------------------------------------------------

@app.callback(Output('page-content', 'children'),
              Output('left', 'style'), 
              [Input('url', 'pathname')])
def display_page(pathname):
    
    if pathname == '/':
        return index_page,{'display': 'none'}
    elif pathname == '/page-1':
        return page_1_layout,{'display': 'block'}
    elif pathname == '/page-2':
        return page_2_layout,{'display': 'block'}
    elif pathname == '/page-3':
        return page_3_layout,{'display': 'block'}
    elif pathname == '/page-4':
        return page_4_layout,{'display': 'block'}
    elif pathname == '/setting':
        return page_setting,{'display': 'block'}
    elif pathname == '/about':
        return page_help,{'display': 'block'}
    elif pathname == '/help':
        return page_about,{'display': 'block'}
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Страница не найдена", className="text-danger"),
                html.Hr(),
                html.P(f"Страница {pathname} не найдена..."),
            ]
        )
    # Последним указывается код для несуществующей страницы

#--------------------------------------------------
# убираем preload страницы
#--------------------------------------------------
@app.callback(Output('pr_load', 'is_in'),
              [Input('example-graph4', 'is_loading')])
def display_load(is_loading):
    if is_loading == True:
        return False  


#--------------------------------------------------
# выбор даты для отображения на графике
#--------------------------------------------------
@app.callback(
    Output(component_id='example-graph1', component_property='figure'),
    Output(component_id='example-graph2', component_property='figure'),
    Output(component_id='example-graph3', component_property='figure'),
    Output(component_id='example-graph4', component_property='figure'),
    [Input(component_id='my-input', component_property='start_date'),
     Input(component_id='my-input', component_property='end_date')]
)
def update_figure(start_date,end_date):    
    #fig.update_layout(transition_duration=500)
    figLine = {
    'data': [go.Scatter(
                x=dff[(dff['DT']>=start_date)&(dff['DT'] <=end_date)]['DT'],
                y=dff[(dff['DT']>=start_date)&(dff['DT']<=end_date)]['Val'])]
            ,
    "layout": go.Layout(
               xaxis={"title":"Дата"}, yaxis={"title":"Значение"}
             )
        }

    figBar = {
    'data': [go.Bar(
                x=dff[(dff['DT']>=start_date)&(dff['DT'] <=end_date)]['DT'],
                y=dff[(dff['DT']>=start_date)&(dff['DT']<=end_date)]['Val'])]
            ,
    "layout": go.Layout(
               xaxis={"title":"Дата"}, yaxis={"title":"Значение"}
             )
        }

    figBox = {
    'data': [go.Box(
                x=dff[(dff['DT']>=start_date)&(dff['DT'] <=end_date)]['DT'],
                y=dff[(dff['DT']>=start_date)&(dff['DT']<=end_date)]['Val'])]
            ,
    "layout": go.Layout(
               xaxis={"title":"Дата"}, yaxis={"title":"Значение"}
             )
        }
    return figLine,figBar,figLine,figBox

# Добавление отслеживание нажатия мобильного меню
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