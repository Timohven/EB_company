#import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
#from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.graph_objs as go
from navbar import Navbar

total_sales = pd.read_csv('./processed_csv/Total_sales.csv', parse_dates = True, index_col = 0)
returns = pd.read_csv('./processed_csv/Returns_per_products.csv', parse_dates = True, index_col = 0)

t1 = total_sales.groupby('SubcategoryName')['Sale'].sum()
t2 = total_sales.groupby('CategoryName')['Sale'].sum()
t3 = returns.groupby('SubcategoryName')['Total'].sum()
t4 = returns.groupby('CategoryName')['Total'].sum()
t5 = total_sales.groupby('SubcategoryName')['Profit'].sum()
t6 = total_sales.groupby('CategoryName')['Profit'].sum()
fig1 = go.Figure(data=go.Pie(labels=t1.index, values=t1), layout=go.Layout(title='Sales per Subcategories'))
fig2 = go.Figure(data=go.Pie(labels=t2.index, values=t2), layout=go.Layout(title='Sales per Categories'))
fig3 = go.Figure(data=go.Pie(labels=t3.index, values=t3), layout=go.Layout(title='Returns per Subcategories'))
fig4 = go.Figure(data=go.Pie(labels=t4.index, values=t4), layout=go.Layout(title='Returns per Categories'))
fig5 = go.Figure(data=go.Pie(labels=t5.index, values=t5), layout=go.Layout(title='Profit per Subcategories'))
fig6 = go.Figure(data=go.Pie(labels=t6.index, values=t6), layout=go.Layout(title='Profit per Categories'))

nav = Navbar()

total_sales = pd.read_csv('./processed_csv/Total_sales.csv', parse_dates = True, index_col = 0)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='p1', figure=fig1)
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='p3', figure=fig3)
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='p5', figure=fig5)
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='p2', figure=fig2)
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='p4', figure=fig4)
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='p6', figure=fig6)
                    ]
                )
            ]
        )
    ]
)

def Product():
    layout = html.Div([
    nav,
    body
    ])
    return layout

def build_p1():
    # t1 = total_s.groupby('SubcategoryName')['Sale'].sum()
    # fig = go.Figure(data=go.Pie(value=t1), layout=go.Layout(title='trend'))
    return fig