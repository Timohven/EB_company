#import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
#from prophet import Prophet
# import cmdstanpy
# cmdstanpy.install_cmdstan()
#cmdstanpy.install_cmdstan(compiler=True) # only valid on Windows

from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from navbar import Navbar

nav = Navbar()

total_sales = pd.read_csv('./processed_csv/Total_sales.csv', parse_dates=True, index_col=0)
period = ['W', 'M', '3M', '6M', 'Y']
for_period = [30.5, 91.5, 183, 274.5, 365]
#models = total_sales['ModelName'].unique()
models = total_sales.groupby('ModelName')['Sale'].sum().sort_values(ascending=False).reset_index()['ModelName']
top_model = models.loc[0]

# df = total_sales.groupby(['ModelName', 'OrderDate'])['OrderQuantity'].sum().reset_index()
# df1 = df[df['ModelName'] == top_model][['OrderDate', 'OrderQuantity']]
# df1.rename(columns={'OrderDate': 'ds', 'OrderQuantity': 'y'}, inplace=True)
# m = Prophet()
# print(df1)
# m.fit(df1)
# future = m.make_future_dataframe(periods=for_period[2])
# forecast = m.predict(future)



body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P("Select a name of model:")
                    ]
                ),
                dbc.Col(
                    [
                        html.P("Select a time cycle:")
                    ]
                ),
                dbc.Col(
                    [
                        html.P("Select a forecast period:")
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='model',
                        options=[
                            {'label': x, 'value': x} for x in models
                                ],
                        value=top_model
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='perd_period',
                        options=[
                            {'label': x, 'value': x} for x in period
                                ],
                        value=period[1]
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='for_period',
                        options=[
                            {'label': x, 'value': x} for x in for_period
                                ],
                        value=for_period[2]
                    )
                )
            ]
        ),
        dbc.Row(
            [
                html.H2('Historical:'),
                #dcc.Textarea(id='text'),
                dcc.Graph(id='hist'),
                #dcc.Graph(id='trend')
            ]
        ),
        dbc.Row(
            [
                html.H2('Predicted:'),
                #dcc.Textarea(id='text'),
                dcc.Graph(id='pred'),
                #dcc.Graph(id='trend')
            ]
        )
    ]
)

def Predictions():
    layout = html.Div([
    nav,
    body
    ])
    return layout

def build_model(selected_model, selected_period):
    print('selected_model->', selected_model)
    t1 = total_sales[total_sales['ModelName'] == selected_model]['OrderQuantity'].resample(selected_period).sum()
    #print(t1)
    t2 = total_sales[total_sales['ModelName'] == selected_model]['Sale'].resample(selected_period).sum()
    #print(t2)
    trace1 = go.Scatter(x=t1.index, y=t1, name=selected_model)
    trace2 = go.Scatter(x=t2.index, y=t2, name='Sales')
    layout = go.Layout(title='Total ' + selected_model)
    #fig = go.Figure(data=trace, layout=layout)
    #fig = go.Figure(layout=layout)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=t1.index, y=t1, name=selected_model),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=t2.index, y=t2, name='Sales'),
        secondary_y=True,
    )
    # fig.add_trace(trace1, secondary_y=False)
    # fig.add_trace(trace2, secondary_y=True)
    fig.update_layout(layout)
    # fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
    # fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)
    return fig



