#import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
#from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.graph_objs as go
from navbar import Navbar

sales_returns = pd.read_csv('./processed_csv/Sales_returns.csv', parse_dates = True, index_col = 0)

t1 = sales_returns[sales_returns['Sold']=='Sold'].groupby('StoreName')['Sale'].sum()
t2 = sales_returns[sales_returns['Sold']=='Sold'].groupby('StoreLocation')['Sale'].sum()
t3 = sales_returns[sales_returns['Sold']=='Returned'].groupby('StoreName')['Sale'].sum()
t4 = sales_returns[sales_returns['Sold']=='Returned'].groupby('StoreLocation')['Sale'].sum()
fig1 = go.Figure(data=go.Pie(labels=t1.index, values=t1), layout=go.Layout(title='Sales per Stores'))
fig2 = go.Figure(data=go.Pie(labels=t2.index, values=t2), layout=go.Layout(title='Sales per Countries'))
fig3 = go.Figure(data=go.Pie(labels=t3.index, values=t3), layout=go.Layout(title='Returns per Stores'))
fig4 = go.Figure(data=go.Pie(labels=t4.index, values=t4), layout=go.Layout(title='Returns per Countries'))

nav = Navbar()


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
                )#,
                # dbc.Col(
                #     [
                #         dcc.Graph(id='p5', figure=fig5)
                #     ]
                # )
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
                )#,
                # dbc.Col(
                #     [
                #         dcc.Graph(id='p6', figure=fig6)
                #     ]
                # )
            ]
        )
    ]
)

def Store():
    layout = html.Div([
    nav,
    body
    ])
    return layout

def build_p1():
    # t1 = total_s.groupby('SubcategoryName')['Sale'].sum()
    # fig = go.Figure(data=go.Pie(value=t1), layout=go.Layout(title='trend'))
    return fig