import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

PLOTLY_LOGO = "https://www.metalloinvest.com/_v/_i/152.png"

theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Поиск")),
        dbc.Col(
            dbc.Button("Поиск", color="primary", className="ml-2"),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

def Navbar():
    navbar = dbc.Navbar(
                [
                    dcc.Link(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px")),
                                dbc.Col(dbc.NavbarBrand("АО «РЭС Групп»", className="ml-2")),
                            ],
                            align="center",
                            no_gutters=True,
                        ),
                        href="/",
                    ),
                    dbc.NavbarToggler(id="navbar-toggler"),
                    #dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
                    dbc.Collapse([
                        dbc.Row([
                                dbc.Col( 
                                    dbc.DropdownMenu(
                                    label="Menu",
                                    children=[
                                        dcc.Link(dbc.DropdownMenuItem("Настройки"),href="/setting"),
                                        dcc.Link(dbc.DropdownMenuItem("О системе"),href="/about"),
                                        dcc.Link(dbc.DropdownMenuItem("Справка"),href="/help"),
                                        ],
                                    right=True,
                                    className="MenuButton"
                                    )),
                                   ],
                                no_gutters=True,
                                className="ml-auto flex-nowrap mt-3 mt-md-0"
                                )],
                            id="navbar-collapse", 
                            navbar=True)
                ],
                color=theme['secondary'],
                dark=True
            )
    return navbar
 
def Sidebar():
    sidebar = html.Div(
        [
            html.H2("Sidebar", className="display-4"),
            html.Hr(),
            html.P(
                 "A simple sidebar layout with navigation links", className="lead"
            ),
            dbc.Nav(
               [
                    dbc.NavLink("ЛГОК", href="/page-1", id="page-1-link"),
                    dbc.NavLink("МГОК", href="/page-2", id="page-2-link"),
                    dbc.NavLink("ОЭМК", href="/page-3", id="page-3-link"),
                    dbc.NavLink("Уральская сталь", href="/page-4", id="page-4-link"),
               ],
               vertical=True,
               pills=True,
            ),
        ],
        className="sidebar_style"
    )
    return sidebar
            