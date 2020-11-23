from dash.dependencies import Input, Output, State

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

METALLINVEST_LOGO = "https://www.metalloinvest.com/_v/_i/152.png"   #Логотип метталоинвеста
theme =  {
    'navcolor': '#ffffff',   # фоновый цвет навигационного меню
}
def Navbar():
    navbar = dbc.Navbar(
                [
                    dcc.Link(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=METALLINVEST_LOGO, height="52px"),width=3),
                                dbc.Col([
                                    html.H3("Металлоинвест", className="brandName"),
                                    html.P("Ресурсы создают возможности", className="brandSlogan"),
                                    ],width=9)
                            ],
                            align="center",
                        ),
                        href="/",
                    ),
                    dbc.NavbarToggler(id="navbar-toggler")
                    #dbc.Collapse(search_bar, id="navbar-collapse", navbar=True)
                ], 
                className="navbar_style",
                color=theme['navcolor'] #комментарий
            )
    return navbar
 
def Sidebar():
    sidebar = html.Div(
        [
            #html.H2("Sidebar", className="display-4"),
            #html.Hr(),
            #html.P(
            #     "A simple sidebar layout with navigation links", className="lead"
            #),
            dbc.Nav(
               [
                    dbc.NavLink("Мониторинг", href="/page-1", id="page-1-link"),
                    dbc.NavLink("Анализ", href="/page-2", id="page-2-link"),
                    dbc.NavLink("Планирование и прогнозирование", href="/page-3", id="page-3-link"),
                    dbc.NavLink("Мнемосхема", href="/page-4", id="page-4-link"),
               ],
               vertical=True,
               pills=True
            ),
        ],
        className="sidebar_style"
    )
    return sidebar
            