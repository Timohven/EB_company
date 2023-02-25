#import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.graph_objs as go
from navbar import Navbar

nav = Navbar()

total_sales = pd.read_csv('./processed_csv/Total_sales.csv', parse_dates = True, index_col = 0)
period = ['D', 'W', 'M', '6M']
category = total_sales['CategoryName'].unique()
t1 = total_sales.groupby('CategoryName')['Sale'].sum().sort_values(ascending=False).reset_index()['CategoryName']
top_category = t1.loc[0]
t2 = total_sales[total_sales['CategoryName']==top_category].groupby('SubcategoryName')['Sale'].sum().sort_values(ascending=False).reset_index()['SubcategoryName']
top_subcategory = t2.loc[0]
t3 = total_sales[total_sales['SubcategoryName']==top_subcategory].groupby('ProductName')['Sale'].sum().sort_values(ascending=False).reset_index()['ProductName']
top_product = t3.loc[0]


index = ['Sale', 'Profit']
total_sales.sort_index()

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P("Select a category:")
                    ]
                ),
                dbc.Col(
                    [
                        html.P("Select one of the top subcategory:")
                    ]
                ),
                dbc.Col(
                    [
                        html.P("Select one of the top products:")
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='categ',
                        options=[
                            {'label': x, 'value': x} for x in t1
                                ],
                        value=top_category
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='subcategory',
                        options=[
                            {'label': x, 'value': x} for x in t2
                                ],
                        value=top_subcategory
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='product',
                        options=[
                            {'label': x, 'value': x} for x in t3
                                ],
                        value=top_product
                    )
                )
            ]
        ),
        dbc.Row(
            [
                html.H2('Seasonality for the product:'),
                #dcc.Textarea(id='text'),
                dcc.Graph(id='season'),
                dcc.Graph(id='trend')
            ]
        )
    ]
)

def Instruments():
    layout = html.Div([
    nav,
    body
    ])
    return layout

def build_subcat(selected_category):
    print('selected_category->')
    t2 = total_sales[total_sales['CategoryName'] == selected_category].groupby('SubcategoryName')['Sale'].sum().sort_values(ascending=False).reset_index()['SubcategoryName']
    top_subcategory = t2.loc[0]
    print(top_subcategory)
    return t2

def build_prod(selected_subcategory):
    print('selected_subcategory->')
    t3 = total_sales[total_sales['SubcategoryName'] == selected_subcategory].groupby('ProductName')['Sale'].sum().sort_values(ascending=False).reset_index()['ProductName']
    top_product = t3.loc[0]
    print(top_product)
    return t3

def build_season(selected_product):
    t = total_sales[total_sales['ProductName'] == selected_product]['OrderQuantity'].resample('M').sum()
    decompose_result_mult = seasonal_decompose(t, model="multiplicative")
    trend = decompose_result_mult.trend
    seasonal = decompose_result_mult.seasonal
    season = go.Figure(data=go.Scatter(x=seasonal.index, y=seasonal), layout=go.Layout(title='season'))
    tr = go.Figure(data=go.Scatter(x=trend.index, y=trend), layout=go.Layout(title='trend'))
    return season, tr


