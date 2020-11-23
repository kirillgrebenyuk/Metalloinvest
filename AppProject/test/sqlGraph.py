import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import pyodbc
import datetime
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])       #Подключение темы для сайта

app.title = "Система ИАС УЭР Металлоинвест"           # Название сайта

cnn = pyodbc.connect('DRIVER={SQL Server};PORT=port;SERVER=192.168.10.11;PORT=1433;DATABASE=EDC_ASKUE;UID=sa;PWD=ZAQ!2wsx')  #Подключение к БД
sql = "SELECT * FROM [EDC_ASKUE].[dbo].[PointMains] WHERE ID_PP = 6029 AND (DT > '2020-10-01' AND DT < '2020-11-01')"
dff = pd.read_sql_query(sql,con=cnn)
fig = px.line(dff, x="DT", y="Val")
fig.update_traces(mode="markers+lines")

fig.update_layout(
   hoverlabel=dict(
       bgcolor="white",
       font_size=16,
       font_family="Rockwell"
   )
)

app.layout = html.Div([
    html.Div(["Введите даты: ",
              dcc.DatePickerRange(id='my-input', 
                                   min_date_allowed=datetime.date(2020, 1, 1),
                                   max_date_allowed=datetime.date(2020, 12, 1),
                                   start_date = datetime.date(2020,10, 28),
                                   end_date=datetime.date(2020, 10, 30),
                                   month_format='DD-MM-YYYY',
                                   display_format='DD-MM-YYYY')]),
    dcc.Graph(id='example-graph',figure={
            	'data': [ {'x': dff['DT'],'y': dff['Val'],'type': 'line'} ],
            	'layout': go.Layout(
                        	xaxis={"title":"DT"}, yaxis={"title":"Val"})
                }),
    html.Div([
    	html.A(html.Button('Download Graph Data'), href='/dash/data_download')
    ],style={"textAlign":"left","font-size":"20"})
])

@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input(component_id='my-input', component_property='start_date'),
     Input(component_id='my-input', component_property='end_date')]
)
def update_figure(start_date,end_date):    
    #fig.update_layout(transition_duration=500)
    return {
    'data': [go.Scatter(
                x=dff[(dff['DT']>=start_date)&(dff['DT'] <=end_date)]['DT'],
                y=dff[(dff['DT']>=start_date)&(dff['DT']<=end_date)]['Val'])]
            ,
    "layout": go.Layout(
               xaxis={"title":"Time"}, yaxis={"title":"Sales"}
             )
        }

if __name__ == '__main__':
    app.run_server()
