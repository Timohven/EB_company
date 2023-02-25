from dash.dependencies import Output, Input
import dash_html_components as html
from navbar import Navbar

nav = Navbar()

header = html.H3(
    'Testing...'
)
output = html.Div(id = 'output',
                  children = [],
                  )

def App():
    layout = html.Div([
        nav,
        header,
        output
    ])
    return layout