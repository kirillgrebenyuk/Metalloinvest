import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt

import pandas as pd
import textwrap

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

print(dash.__version__)
print(table.__version__)

app = dash.Dash(__name__)
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

def create_tooltip(cell):
    try:
        num = float(cell)
        return textwrap.dedent(
            '''
            Tooltip for value **{value:+.2f}**.
            | Multiplier | Value |  Percent |
            |-------|-------|---------------|
            | 1     | {value_1:+.2f}     | {value_1:+.2f}% |
            | 2     | {value_2:+.2f}     | {value_2:+.2f}% |
            | 3     | {value_3:+.2f}     | {value_3:+.2f}% |
            '''.format(
                value=num,
                value_1=num,
                value_2=num * 2,
                value_3=num * 3
            )
        )
    except:
        return textwrap.dedent(
            '''
            Tooltip: **{value}**.
            '''.format(value=cell)
        )


app.layout = html.Div([
    table.DataTable(
        columns = [{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('rows'),
        tooltips={
            col: [
                {
                    'type': 'markdown',
                    'value': create_tooltip(df.loc[i, col])
                }
                for i in range(len(df))
            ]
            for col in df.columns
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)