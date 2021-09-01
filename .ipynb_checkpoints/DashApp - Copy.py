import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# load data
data = 'data_cleaned.csv'
# import data
data = pd.read_csv(data)
# column list to choose from
column_list = ['Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'WindGustDir',
               'WindGustSpeed', 'WindDir9am', 'WindDir3pm', 'WindSpeed9am',
               'WindSpeed3pm', 'Humidity9am', 'Humidity3pm', 'Pressure9am',
               'Pressure3pm', 'Temp9am', 'Temp3pm', 'RainToday', 'RainTomorrow']

data1 = data.select_dtypes(include=['object'])

data2 = data.select_dtypes(include=['float64'])

app = dash.Dash(__name__)

# ------------------------------------------------------------------------
app.layout = html.Div([
    html.Div([

html.H1("Pie Chart of Rain in Australia Data", style={'textAlign':'center'}
        ),

        dcc.Dropdown(
        id='my_dropdown',
        options=[{'label': s, 'value': s} for s in data1.columns],
        value='RainToday',
        multi=False,
        clearable=False,
        style={"width": "50%"}
    ),
        dcc.Graph(id='my_graph', figure={}),

        dcc.ConfirmDialog(
        id='confirm_dialog',
        displayed=False,
        message='Please choose checklist variables!',
    ),
        html.H1("Scatter Matrix of Rain in Australia Data", style={'textAlign':'center'}
        ),

        dcc.Checklist(
        id='my_checklist',
        options=[{'label': s, 'value': s} for s in data2.columns],
        value=['MinTemp', 'MaxTemp', 'Rainfall', 'WindGustSpeed'],
        labelStyle={'display': 'inline-block'}
    ),
        dcc.Graph(id="my_figure", figure={})


    ])
])



# ------------------------------------------------------------------------
@app.callback(
    Output('my_graph', 'figure'),

    Input('my_dropdown', 'value')
)
def update_graph(my_dropdown):

    dff = data1
    piechart=px.pie(
            dff,
            names=my_dropdown,
            hole=.3,
            )

    return piechart

@app.callback(
    Output('confirm_dialog', 'displayed'),
    Output('my_figure', 'figure'),

    Input('my_checklist', 'value'),
)
def update_graph(ckl_val):
    if len(ckl_val) > 0:
        fig = px.scatter_matrix(data2, dimensions=ckl_val, height=1300, color='MaxTemp',
                                hover_data={'MinTemp':True, 'MaxTemp':':,'})
        fig.update_traces(diagonal_visible=False, showupperhalf=True, showlowerhalf=True)
        fig.update_layout(yaxis1={'title':{'font':{'size':15}}}, yaxis2={'title':{'font':{'size':15}}},
                          yaxis3={'title':{'font':{'size':15}}}, yaxis4={'title':{'font':{'size':15}}},
                          yaxis5={'title':{'font':{'size':15}}}, yaxis6={'title':{'font':{'size':15}}},
                          yaxis7={'title':{'font':{'size':15}}}, yaxis8={'title':{'font':{'size':15}}}
                          )
        fig.update_layout(xaxis1={'title':{'font':{'size':15}}}, xaxis2={'title':{'font':{'size':15}}},
                          xaxis3={'title':{'font':{'size':15}}}, xaxis4={'title':{'font':{'size':15}}},
                          xaxis5={'title':{'font':{'size':15}}}, xaxis6={'title':{'font':{'size':15}}},
                          xaxis7={'title':{'font':{'size':15}}}, xaxis8={'title':{'font':{'size':15}}}
                          )
        return False, fig

    if len(ckl_val)==0:
        return True, dash.no_update


if __name__ == '__main__':
    app.run_server(debug=True)