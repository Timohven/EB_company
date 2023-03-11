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

from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.forecasting.theta import ThetaForecaster
from sktime.performance_metrics.forecasting import mean_absolute_percentage_error
import plotly.express as px

from navbar import Navbar

nav = Navbar()
seasonable_products = pd.read_csv('./processed_csv/Seasonable_products.csv')
total_sales = pd.read_csv('./processed_csv/Total_sales.csv', parse_dates=True, index_col=0)
#period = ['W', 'M', '3M', '6M', 'Y']
period = ['M', '3M', 'Y']
for_period = [1, 3, 6, 12]
#models = total_sales['ModelName'].unique()
##models = total_sales.groupby('ModelName')['Sale'].sum().sort_values(ascending=False).reset_index()['ModelName']
t = seasonable_products['ProductName']
top_product = t.loc[0]

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
                        html.P("Select a name of product:")
                    ]
                ),
                dbc.Col(
                    [
                        html.P("Select a time cycle:")
                    ]
                ),
                dbc.Col(
                    [
                        html.P("Select a forecast period (in months):")
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='pro',
                        options=[
                            {'label': x, 'value': x} for x in t
                                ],
                        value=top_product
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='perd_period',
                        options=[
                            {'label': x, 'value': x} for x in period
                                ],
                        value=period[0]
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='for_period',
                        options=[
                            {'label': x, 'value': x} for x in for_period
                                ],
                        value=for_period[1]
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

def build_model(selected_product, selected_period):
    #print('selected_model->', selected_model)
    #t1 = total_sales[total_sales['ModelName'] == selected_model]['OrderQuantity'].resample(selected_period).sum()
    t1 = total_sales[total_sales['ProductName'] == selected_product]['OrderQuantity'].resample(selected_period).sum()
    #print(t1)
    #t2 = total_sales[total_sales['ModelName'] == selected_model]['Sale'].resample(selected_period).sum()
    decompose_result_mult = seasonal_decompose(t1, model="multiplicative")
    trend = decompose_result_mult.trend
    seasonal = decompose_result_mult.seasonal

    layout = go.Layout(title='Total sales: ' + selected_product)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=t1.index, y=t1, name='Quantity', line_shape='spline'),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=seasonal.index, y=seasonal, name='Seasonal coef', line_shape='spline'),
        secondary_y=True,
    )

    fig.update_layout(layout)
    fig.update_yaxes(title_text="Quantity", secondary_y=False)
    fig.update_yaxes(title_text="Seasonal coef", secondary_y=True)
    return fig

def build_pred(selected_product, selected_period, for_period):
    # print('selected_period->', selected_period)
    # print('for_period->', for_period)
    # print('selected_product->', selected_product)
    t2 = total_sales[total_sales['ProductName'] == selected_product]['OrderQuantity'].resample('M').sum()
    t2.index = t2.index.to_period('M')
    y = t2
    # y_train, y_test = temporal_train_test_split(y)
    y_train = y
    p = pd.period_range('Jul-2017', periods=for_period, freq='M')
    #p = pd.PeriodIndex(year=2017, month=[7, 8, 9, 10, 11, 12], freq='M')
    y_test = pd.Series([0]*for_period, index=p)
    fh = ForecastingHorizon(y_test.index, is_relative=False)
    forecaster = ThetaForecaster(sp=12)  # monthly seasonal periodicity
    forecaster.fit(y_train)
    y_pred = forecaster.predict(fh)
    #print(y_pred)
    #fig = make_subplots(specs=[[{"secondary_y": True}]])
    trace = []
    y_pred.index = pd.to_datetime(y_pred.index.to_timestamp())
    y_train.index = pd.to_datetime(y_train.index.to_timestamp())
    y_pred = pd.concat([y_train.iloc[-1:], y_pred], axis=0)
    #print(y_pred)
    # p1 = pd.concat([y_train, y_pred], axis=0)
    # fig.add_trace(
    #     go.Scatter(x=p1.index, y=p1, name='Quantity', line_shape='spline'),
    #     secondary_y=False,
    # )
    trace.append(go.Scatter(x=y_train.index, y=y_train, name='Quantity', line_shape='spline'))
    # fig.add_trace(
    #     go.Scatter(x=y_train.index, y=y_train, name='Quantity', line_shape='spline')
    # )
    trace.append(go.Scatter(x=y_pred.index, y=y_pred, name='Predicted quantity', line_shape='spline'))
    # fig.add_trace(
    #     go.Scatter(x=y_pred.index, y=y_pred, name='Predicted quantity', line_shape='spline')
    # )
    layout = go.Layout(title='Forecasting for ' + selected_product)
    fig = go.Figure(data=trace, layout=layout)
    return fig
