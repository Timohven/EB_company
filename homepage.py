import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
#from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

from navbar import Navbar
nav = Navbar()

total_sales = pd.read_csv('./processed_csv/Total_sales.csv', parse_dates=True, index_col=0)
period = ['D', 'W', 'M', '6M']
category = total_sales['CategoryName'].unique()
index = ['Sale', 'Profit']
total_sales.sort_index()

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("About the company"),
                        html.P(
                             """\
    Elevation Bikes (or EB for short) was established in 2008 and signed an
    exclusive distribution agreement with the British Tandem marketing
    company. Since then, 9 additional marketers have been added to EB's
    distribution network in the UK, Germany, France, Spain and Italy.
    EB started as a bicycle manufacturing company (all types, except
    electric bicycles). Later, in order to expand its product portfolio and
    meet the demand of its clients, EB also started producing clothing and
    accessories for riding."""
                               ),
                        dbc.Button("View details", color="secondary"),
                    ],
                    md=4
                ),
                dbc.Col(
                    [
                         html.H2("Main statistics"),
                         dcc.Graph(id='sales'),
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='period',
                        options=[
                            {'label': 'Day', 'value': period[0]},
                            {'label': 'Week', 'value': period[1]},
                            {'label': 'Month', 'value': period[2]},
                            {'label': 'Half year', 'value': period[3]}
                                ],
                        value=period[1]
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='category',
                        options=[
                            {'label': 'Bikes', 'value': category[0]},
                            {'label': 'Accessories', 'value': category[1]},
                            {'label': 'Clothing', 'value': category[2]}
                                ],
                        multi=True,
                        value=[category[0], category[1], category[2]]
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='index',
                        options=[
                            {'label': 'Sales', 'value': index[0]},
                            {'label': 'Profits', 'value': index[1]}
                                ],
                        value=index[0]
                    )
                )
            ]
        )
    ],
    className="mt-4",
)

def Homepage():
    layout = html.Div([
    nav,
    body
    ])
    return layout

def build_main(selected_period, selected_category, selected_index):
    #print(selected_index)
    trace = []
    for cat in selected_category:
        t = total_sales[total_sales['CategoryName'] == cat][selected_index].resample(selected_period).sum()
        trace.append(go.Scatter(x=t.index, y=t, name=cat))
    layout = go.Layout(title='Total ' + selected_index)
    fig = go.Figure(data=trace, layout=layout)
    return fig

# if __name__ == "__main__":
#     app.run_server(debug=True)