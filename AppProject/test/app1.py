import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import pyodbc
import datetime
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Система ИАС УЭР"           # Название сайта

cnn = pyodbc.connect('DRIVER={SQL Server};PORT=port;SERVER=192.168.0.85;PORT=1433;DATABASE=Piramida2000;UID=sa;PWD=pswd')

app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div(["Введите даты: ",
              dcc.DatePickerRange(id='my-input', 
                                   min_date_allowed=datetime.date(2020, 1, 1),
                                   max_date_allowed=datetime.date(2020, 11, 1),
                                   start_date = datetime.date(2020,10, 28),
                                   end_date=datetime.date(2020, 10, 30))]),
    dcc.Graph(id='graph-with-slider'),
    #dcc.Graph(
    #    id='example-graph',
    #    figure={ 
    #        	'data': [{'x': df['DATA_DATE'],'y': df['VALUE0'],'type': 'line'}],
    #        	'layout': go.Layout(
    #                   	xaxis={"title":"Время"}, yaxis={"title":"Потребление"}) } )
    		]
    )


@app.callback(
    Output(component_id='graph-with-slider', component_property='figure'),
    [Input(component_id='my-input', component_property='start_date'),
     Input(component_id='my-input', component_property='end_date')]
)
def update_figure(start_date,end_date):
    qsql = "SELECT dev.NAME,dat.PARNUMBER,dat.ITEM,dat.VALUE0,dat.VALUE1,dat.DATA_DATE FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND dat.DATA_DATE > '"+start_date+"' AND dat.DATA_DATE < '"+end_date+"' AND (dat.OBJECT IN(4408,4409,4410,4411,4412,4413)) AND dat.ITEM = 1 ORDER BY dat.DATA_DATE ASC"
    dff = pd.read_sql_query(qsql,con=cnn)
    fig = px.line(dff, x="DATA_DATE", y="VALUE0", color="NAME", hover_name="NAME")

    #fig.update_layout(transition_duration=500)

    return fig
#def sql(start_date,end_date):
#    qsql = "SELECT dev.NAME,dat.PARNUMBER,dat.ITEM,dat.VALUE0,dat.VALUE1,dat.DATA_DATE FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND dat.DATA_DATE > '"+start_date+"' AND dat.DATA_DATE < '"+end_date+"' AND (dat.OBJECT IN(4412,4413)) AND dat.ITEM = 1 ORDER BY dat.DATA_DATE ASC"
#    dff = pd.read_sql_query(qsql,con=cnn)
#    return {
#        'data': [go.Scatter(
#                x=dff[(dff['DATA_DATE']>=start_date)&(dff['DATA_DATE']<=end_date)]['DATA_DATE'],
#                y=dff[(dff['DATA_DATE']>=start_date)&(dff['DATA_DATE']<=end_date)]['VALUE0'])
#        ],
#        'layout': go.Layout(
#                        	xaxis={"title":"Время"}, yaxis={"title":"Потребление"}) }




if __name__ == '__main__':
    app.run_server()