import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import App#, build_graphfrom
from homepage import Homepage, build_main
from instruments import Instruments, build_season, build_subcat, build_prod
from product import Product
from store import Store

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    #print(pathname)
    if pathname == '/time-series':
        return App()
    elif pathname == '/instruments':
        return Instruments()
    elif pathname == '/product':
        return Product()
    elif pathname == '/store':
        return Store()
    else:
        return Homepage()


@app.callback(
    dash.dependencies.Output('sales', 'figure'),
    [dash.dependencies.Input('period', 'value'),
     dash.dependencies.Input('category', 'value'),
     dash.dependencies.Input('index', 'value')])
def update_main(selected_period, selected_category, selected_index):
    graph = build_main(selected_period, selected_category, selected_index)
    return graph

@app.callback(
    dash.dependencies.Output('subcategory', 'options'),
    dash.dependencies.Input('categ', 'value'))
def update_subcat(selected_category):
    print('selected_category!!!')
    t2 = build_subcat(selected_category)
    return [{"label": i, "value": i} for i in t2]

@app.callback(
    dash.dependencies.Output('product', 'options'),
    dash.dependencies.Input('subcategory', 'value'))
def update_prod(selected_subcategory):
    print('!!!')
    t3 = build_prod(selected_subcategory)
    return [{"label": i, "value": i} for i in t3]

@app.callback(
    [dash.dependencies.Output('season', 'figure'),
    dash.dependencies.Output('trend', 'figure')],
    dash.dependencies.Input('product', 'value'))
def update_season(selected_product):
    print('!!!')
    graph, graph2 = build_season(selected_product)
    return graph, graph2

# @app.callback(
#     dash.dependencies.Output('div', 'value'),
#     [dash.dependencies.Input('categ', 'value'),
#     dash.dependencies.Input('subcategory', 'value'),
#     dash.dependencies.Input('product', 'value')])
# def update_figure2(selected_category, selected_subcategory, selected_product):
#     print(selected_category)
#     print(selected_subcategory)
#     print(selected_product)
#     #graph = build_figure2(selected_category, selected_subcategory, selected_product)
#     return selected_product

if __name__ == '__main__':
    app.run_server(debug=True)