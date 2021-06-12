import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.io as pio
import dash_bootstrap_components as dbc
import math

# Reading in the data frames from the World_Cup_Simulation
World_Cup_Player_Data = pd.read_csv('Player_Data_Set.csv')
World_Cup_Player_Data = World_Cup_Player_Data.round(2)
World_Cup_Nation_Data = pd.read_csv('Nation_Data_Set.csv')
World_Cup_Nation_Data = World_Cup_Nation_Data.round(2)
World_Cup_Award_Data = pd.read_csv('Award_Data_Set.csv')

# Ensuring pandas displays the whole data frame
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

World_Cup_Player_Data = World_Cup_Player_Data.sort_values(by=['Goals'], ascending=False)
World_Cup_Player_Data['Goals_Per_Game'] = World_Cup_Player_Data['Goals'] / World_Cup_Player_Data['P']
World_Cup_Player_Data['Assists_Per_Game'] = World_Cup_Player_Data['Assists'] / World_Cup_Player_Data['P']
World_Cup_Player_Data = World_Cup_Player_Data.sort_values(by=['Country'])

World_Cup_Nation_Data = World_Cup_Nation_Data.sort_values(by=['total_GF'], ascending=False)
World_Cup_Nation_Data['GF_Per_Game'] = World_Cup_Nation_Data['total_GF'] / World_Cup_Nation_Data['total_P']
World_Cup_Nation_Data['GA_Per_Game'] = World_Cup_Nation_Data['total_GA'] / World_Cup_Nation_Data['total_P']
World_Cup_Nation_Data = World_Cup_Nation_Data.sort_values(by=['Confederation', 'Country'])

# Extracting World Cup Finals Data
Finals_Player_Data = World_Cup_Player_Data[World_Cup_Player_Data.WC_P > 0]
Finals_Player_Data = Finals_Player_Data[["Name", "Country", "Position", "WC_P", "WC_Goals", "WC_Assists"]]

Goal_Data = Finals_Player_Data.sort_values(by=['WC_Goals', "WC_P"], ascending=False)
Assist_Data = Finals_Player_Data.sort_values(by=['WC_Assists', "WC_P"], ascending=False)

World_Cup_Player_Data = World_Cup_Player_Data.round(2)
World_Cup_Nation_Data = World_Cup_Nation_Data.round(2)

# Getting into the Plotly

pio.templates.default = "ggplot2"

tgfvtga = px.scatter(World_Cup_Nation_Data, x="total_GA", y="total_GF",
                       color="Confederation",
                       hover_name="Country", size_max=60)

nd_table = go.Figure(data=[go.Table(
    header=dict(values=["Country", "Confederation", "P", "Total GF", "Total GA", "GF/G", "GA/G"],
                align='left'),
    cells=dict(
        values=[World_Cup_Nation_Data.Country, World_Cup_Nation_Data.Confederation, World_Cup_Nation_Data.total_P,
                World_Cup_Nation_Data.total_GF, World_Cup_Nation_Data.total_GA, World_Cup_Nation_Data.GF_Per_Game,
                World_Cup_Nation_Data.GA_Per_Game],
        align='left'))
])

pd_table = go.Figure(data=[go.Table(
    header=dict(values=["Name", "Country", "Position", "Games Played", "Goals", "Assists", "Goals/G",
                        "Assists/G"],
                align='left'),
    cells=dict(
        values=[World_Cup_Player_Data.Name, World_Cup_Player_Data.Country, World_Cup_Player_Data.Position,
                World_Cup_Player_Data.P,
                World_Cup_Player_Data.Goals, World_Cup_Player_Data.Assists, World_Cup_Player_Data.Goals_Per_Game,
                World_Cup_Player_Data.Assists_Per_Game],
        align='left'))
])

wcpd_table = go.Figure(data=[go.Table(
    header=dict(values=["Name", "Country", "Position", "Games Played", "Goals", "Assists"],
                # fill_color='paleturquoise',
                align='left'),
    cells=dict(
        values=[Finals_Player_Data.Name, Finals_Player_Data.Country, Finals_Player_Data.Position,
                Finals_Player_Data.WC_P,
                Finals_Player_Data.WC_Goals, Finals_Player_Data.WC_Assists],
        # fill_color='lavender',
        align='left'))
])

wcgs_table = go.Figure(data=[go.Table(
    header=dict(values=["Name", "Country", "Position", "Games Played", "Goals"],
                # fill_color='paleturquoise',
                align='left'),
    cells=dict(
        values=[Goal_Data.Name, Goal_Data.Country, Goal_Data.Position,
                Goal_Data.WC_P,
                Goal_Data.WC_Goals],
        # fill_color='lavender',
        align='left'))
])

wcas_table = go.Figure(data=[go.Table(
    header=dict(values=["Name", "Country", "Position", "Games Played", "Assists"],
                # fill_color='paleturquoise',
                align='left'),
    cells=dict(
        values=[Assist_Data.Name, Assist_Data.Country, Assist_Data.Position,
                Assist_Data.WC_P,
                Assist_Data.WC_Assists],
        # fill_color='lavender',
        align='left'))
])

award_table = go.Figure(data=[go.Table(
    header=dict(values=["Award", "Winner"],
                align='left'),
    cells=dict(
        values=[World_Cup_Award_Data.Award, World_Cup_Award_Data.Winner],
        align='left'))
])

#######

external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

PAGE_SIZE = 10

app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1("Python World Cup Analytics"),
                    width={'size': 6, 'offset': 4},
                    ),
            ),
    dbc.Row(dbc.Col(html.P(
        "A Dashboard for you to explore the data produced in your World Cup Simulation, produced with Plotly Dash"),
                    width={'size': 8, 'offset': 3},
                    ),
            ),

    dbc.Row(dbc.Col(dcc.Graph(id="gva"),
                    width={'size': 12, 'offset': 0},
                    ),
            ),

    dbc.Row([
        dbc.Col(html.P("Games Played:"),
                width=1,
                ),
        dbc.Col(dcc.RangeSlider(id='range-slider',
                                min=0, max=30, step=1,
                                marks={0: '0', 10: '10', 20: '20'},
                                value=[0, 30]),
                ),
    ],
    ),

    dbc.Row(dbc.Col(
        html.H3("Goal and Assist Charts for the World Cup Finals"),
        width={'size': 10, 'offset': 4},
    ),
    ),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=wcgs_table, style={'display': 'inline-block'}),
                width={'size': 6, 'offset': 0},
                ),
        dbc.Col(dcc.Graph(figure=wcas_table, style={'display': 'inline-block'}),
                width=6,
                ),
        dbc.Col(dcc.Graph(figure=award_table, style={'display': 'inline-block'}),
                width={'size': 6, 'offset': 0},
                ),
        #need to add a fourth table for looks
    ]),

    dbc.Row(dbc.Col(dcc.Graph(figure=tgfvtga),
                    width={'size': 12, 'offset': 0},
                    ),
            ),

    dbc.Row(dbc.Col(html.P("The complete data frames for all players and nations, these tables are huge!"),
                    width={'size': 6, 'offset': 4},
                    ),
            ),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=nd_table, style={'display': 'inline-block'}),
                width={'size': 6, 'offset': 0},
                ),
        dbc.Col(dcc.Graph(figure=pd_table, style={'display': 'inline-block'}),
                width=6,
                ),
    ]),

    #dcc.Graph(figure=wcpd_table),

])


@app.callback(
    Output("gva", "figure"),
    [Input("range-slider", "value")])
def update_bubble(slider_range):
    low, high = slider_range
    mask = (World_Cup_Player_Data['P'] > low) & (World_Cup_Player_Data['P'] < high)
    gva = px.scatter(World_Cup_Player_Data[mask], x="Assists_Per_Game", y="Goals_Per_Game",
                     color="Confederation",
                     hover_name="Name", size_max=60)
    return gva

app.run_server(debug=True)
