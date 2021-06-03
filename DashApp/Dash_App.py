import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import math

app = dash.Dash()

World_Cup_Player_Data = pd.read_csv('../Python_Files/Player_Data_Set.csv')
World_Cup_Nation_Data = pd.read_csv('Nation_Data_Set.csv')

# Ensuring pandas displays the whole data frame
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

World_Cup_Player_Data = World_Cup_Player_Data.sort_values(by=['Goals'], ascending=False)
World_Cup_Player_Data['Goals_Per_Game'] = World_Cup_Player_Data['Goals'] / World_Cup_Player_Data['P']
World_Cup_Player_Data['Assists_Per_Game'] = World_Cup_Player_Data['Assists'] / World_Cup_Player_Data['P']
World_Cup_Player_Data = World_Cup_Player_Data.sort_values(by=['Assists_Per_Game'], ascending=False)

World_Cup_Nation_Data = World_Cup_Nation_Data.sort_values(by=['total_GF'], ascending=False)
World_Cup_Nation_Data['GF_Per_Game'] = World_Cup_Nation_Data['total_GF'] / World_Cup_Nation_Data['total_P']
World_Cup_Nation_Data['GA_Per_Game'] = World_Cup_Nation_Data['total_GA'] / World_Cup_Nation_Data['total_P']
World_Cup_Nation_Data = World_Cup_Nation_Data.sort_values(by=['GF_Per_Game'], ascending=False)

# print(World_Cup_Player_Data.to_string(columns=['Name', 'Country', 'P', 'Goals', 'Goals_Per_Game', 'Assists', 'Assists_Per_Game']))

# print(World_Cup_Nation_Data.to_string(columns=['Country', 'total_P', 'total_GF', 'total_GA', 'GF_Per_Game', 'GA_Per_Game']))

gpg_v_apg = px.scatter(World_Cup_Player_Data, x="Assists_Per_Game", y="Goals_Per_Game",
                       color="Confederation",
                       hover_name="Name", size_max=60)

nd_table = go.Figure(data=[go.Table(
    header=dict(values=list(World_Cup_Nation_Data.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(
        values=[World_Cup_Nation_Data.Country, World_Cup_Nation_Data.Confederation, World_Cup_Nation_Data.total_P,
                World_Cup_Nation_Data.total_GF, World_Cup_Nation_Data.total_GA, World_Cup_Nation_Data.GF_Per_Game,
                World_Cup_Nation_Data.GA_Per_Game],
        fill_color='lavender',
        align='left'))
])

pd_table = go.Figure(data=[go.Table(
    header=dict(values=list(World_Cup_Player_Data.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(
        values=[World_Cup_Player_Data.Name, World_Cup_Player_Data.Country,World_Cup_Player_Data.Position, World_Cup_Player_Data.ShirtNumber, World_Cup_Player_Data.Attack,
                World_Cup_Player_Data.Passing, World_Cup_Player_Data.P,
                World_Cup_Player_Data.Goals, World_Cup_Player_Data.Assists, World_Cup_Player_Data.Goals_Per_Game,
                World_Cup_Player_Data.Assists_Per_Game, World_Cup_Player_Data.Confederation],
        fill_color='lavender',
        align='left'))
])

app = dash.Dash()

app.layout = html.Div(
    children=[
        html.H1(children="World Cup Analytics", ),
        html.P(
            children="A Dashboard for you to explore the data produced in your World Cup Simulation",
        ),

        dcc.Graph(id="gva"),
        html.P("Games Played:"),
        dcc.RangeSlider(
            id='range-slider',
            min=0, max=30, step=1,
            marks={0: '0', 10: '10', 20: '20'},
            value=[0, 30]
        ),
        dcc.Graph(figure=nd_table),
        dcc.Graph(figure=pd_table)
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

app.run_server(debug=True, use_reloader=False)
