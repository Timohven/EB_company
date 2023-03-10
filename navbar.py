import dash_bootstrap_components as dbc
def Navbar():
     navbar = dbc.NavbarSimple(
           children=[
              dbc.NavItem(dbc.NavLink("Time-Series", href="/time-series")),
              dbc.DropdownMenu(
                 nav=True,
                 in_navbar=True,
                 label="Menu",
                 children=[
                    dbc.DropdownMenuItem("Customer analysis", href="/customer"),
                    dbc.DropdownMenuItem("Product analysis", href="/product"),
                    dbc.DropdownMenuItem("Store analysis", href="/store"),
                    dbc.DropdownMenuItem("Other metrics", href="/other"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Analytical instruments", href="/instruments"),
                    dbc.DropdownMenuItem("Predictive instruments", href="/predictions"),
                          ],
                      ),
                    ],
          brand="Home",
          brand_href="/home",
          sticky="top",
        )
     return navbar