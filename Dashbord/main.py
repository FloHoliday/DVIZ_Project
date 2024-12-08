from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import numpy as np

import corr_graph_functions as cg
import map_functions as mf
import donut_graph_functions as dg


app = Dash(__name__)

# Import mental health data
mh_data = pd.read_csv('/Users/finneyer/Documents/HSLU/Semester 3/DVIZ/Projektarbeit/DVIZ_Project/mental_health.csv', delimiter=';')
countries = mh_data.Entity.unique()
available_years = mh_data['Year'].unique().tolist()

smoth_border_style = {'border-radius':'5px', 'box-shadow': 'rgba(0, 0, 0, 0.13) 0px 1px 4px', 'overflow':'hidden'}
std_box_padding = {'padding': '20px'}
colors = {'green': '#38adad', 'blue': '#3b4994', 'lightblue':'#ace4e4', 'midlbue': '#5ac8c8', 'dense_pink':'#dfb0d6'}

# Data preparation for the map
disorders_factors = list(mh_data.columns)[3:]
mh_data_map = mf.classify_disorders(mh_data, disorders_factors)

# Main wrapper element
app.layout = html.Div(
    id='main-wrapper',
    style={'width' : '100%', 'display': 'flex', 'justify-content':'space-between'},
    children=[
        
        # Selecter sidebar
        html.Div(
            id='selecter-sidebar',
            style={
                'width' : '20%', 
                'height' : '100vh', 
                'position' : 'sticky', 
                'display':'flex', 
                'flex-direction':'column', 
                'align-items': 'center',
                'justify-content':'space-between',
                'top':'0', 
                **smoth_border_style, 
                'background-color':'white', 
                'padding':'20px', 
                'box-sizing': 'border-box'
            },
            children=[
                html.Div(id='logo-container',
                    style={'width': '30%', 'overflow': 'hidden', 'margin-top': '30px'},
                    children=[
                        html.Img(id='logo-img',
                            style={'width':'100%'},
                            src='assets/img/logo_frei.jpg'
                        )
                    ]
                ),
                html.Div(
                    id='dropdown-wrapper',
                    style={'width':'100%', 'margin-bottom': '150px'},
                    children=[
                        html.H3("Select", style={'margin': '0 0 20px 0'}),
                        dcc.Dropdown(id='slct_disorder',
                            options=[
                                {'label': 'Schizophrenia', 'value': 'schizophrenia'},
                                {'label': 'Depressive disorder', 'value': 'depressive_disorder'},
                                {'label': 'Anxiety disorders', 'value': 'anxiety_disorders'},
                                {'label': 'Bipolar disorders', 'value': 'bipolar_disorders'},
                                {'label': 'Eating disorders', 'value': 'eating_disorders'}
                            ],
                            multi=False,
                            placeholder='Select a disorder',  
                            style={'width': '100%', 'margin': '0 0 5px 0'}
                        ),
                        dcc.Dropdown(id='slct_indicator',
                            options=[
                                {'label': 'GDP', 'value': 'gdp'},
                                {'label': 'CO2 emissions', 'value': 'co2_emissions'},
                                {'label': 'Unemployment rate', 'value': 'unemployment_rate'}
                            ],
                            multi=False,
                            placeholder='Select an indicator',
                            style={'width': '100%'}
                        )
                    ]
                ),
                html.P('© 2024 Team cool guys', id='copyright-text', style={'font-size': '12px'})
            ]
        ),
        
        # Content wrapper
        html.Div(id='content-wrapper',
            style={'width': '80%', 'display': 'flex', 'flex-direction':'column', 'align-items':'center', 'padding':'20px'},
            children=[  
                html.Div(id='title-wrapper',
                    style={'background-color': 'white', **smoth_border_style, 'margin': '0 0 20px 0', **std_box_padding},
                    children=[
                        html.H1('Mental Health & Societal Factors Dashboard'),
                        html.Div(
                            style={'color': '#737373'},
                            children=[
                                html.P("Mental health conditions affect hundreds of millions of people worldwide, yet their relationship with societal and economic factors remains under-explored. This dashboard visualizes the prevalence of various mental health disorders across different countries and examines their potential correlations with key societal indicators such as GDP, CO₂ emissions, and unemployment rates."),
                                html.P("Each mental health condition tracked here—from depression and anxiety to schizophrenia and eating disorders—affects individuals differently and may be influenced by various environmental and societal factors. By exploring these relationships, we can better understand how economic and environmental conditions might interact with mental health at a population level."),
                                html.P("Use the sidebar controls to select specific mental health conditions and indicators. The visualization tools allow you to explore prevalence rates across different countries, analyze trends over time, and examine potential correlations between mental health and societal factors. ")
                            ]
                        )
                    ]
                ),
                
                # Year Slider box
                html.Div(id='year-slider-box',
                    style={'width': '100%', 'margin-bottom':'20px', **smoth_border_style, **std_box_padding, 'box-sizing':'border-box', 'background-color':'white'},
                    children=[
                        dcc.Slider(id='year_slider',
                            min=min(available_years),
                            max=max(available_years),
                            value=2010,
                            marks={year: {'label': str(year), 'style': {'font-size': '14px'}} if year % 5 == 0 or year == 2019 else '' for year in available_years},
                            step=None
                        )
                    ]
                ),
                
                # Box for the map
                html.Div(id='map-box',
                    style={'width':'100%', 'margin-bottom': '20px', **smoth_border_style},
                    children=[
                        dcc.Graph(id='disorder_map')
                    ]
                ),
                
                # Wrapper for first row after map
                html.Div(id='disorder-graph-wrapper',
                    style={'width':'100%', 'display':'flex', 'justify-content':'space-between'},
                    children=[
                        html.Div(id='graph1-container',
                            style={'width':'69%'},
                            children=[
                                html.Div(id='disorder-graph-text-box',
                                    style={'width':'100%','background-color': 'white', 'margin-bottom':'10px', **smoth_border_style,'padding':'0 20px 0 20px'},
                                    children=[
                                        html.H3('Graph title comes here', style={'margin-bottom':'0'}),
                                        html.P('And here a short description of the Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua')
                                    ]
                                ),
                                html.Div(id='disorder-graph-box',
                                    style={**smoth_border_style},
                                    children=[
                                        dcc.Graph(id='disorders_graph',
                                            style={}  
                                        )
                                    ]
                                )
                            ]
                        ),
                        html.Div(id='donut-box',
                            style={'width':'29%','background-color':'white', **smoth_border_style},
                            children=[
                                dcc.Graph(id='disorders_donut',style={'width':'100%'})
                            ]
                        )
                    ]
                )
            ]
        )
    ] 
)

# Map Callback
@app.callback(
      Output(component_id='disorder_map', component_property='figure'),
    [Input(component_id='slct_disorder', component_property='value'),
     Input(component_id='slct_indicator', component_property='value'),
     Input(component_id='year_slider', component_property='value')]
)

def update_map(disorder, indicator, year):
    if not disorder or not indicator:
        return cg.get_default_corr_graph(colors)
    
    map_fig = mf.plot_bivariate_map(mh_data_map, disorder, indicator, year,'pink-blue')

    return map_fig


# Correlation graph & donut callback
@app.callback(
     [Output(component_id='disorders_graph', component_property='figure'),
      Output(component_id='disorders_donut', component_property='figure')],
    [Input(component_id='slct_disorder', component_property='value'),
     Input(component_id='slct_indicator', component_property='value'),
     Input(component_id='disorder_map', component_property='clickData'),
     Input(component_id='year_slider', component_property='value')]
)

def update_corr_and_donut(disorder, indicator, click_data, year):
    
    if not disorder or not indicator or not click_data:
        return cg.get_default_corr_graph(colors), dg.get_default_donut(colors)
    
    country_code = click_data['points'][0]['location']
    corr_fig = cg.get_corr_graph(mh_data, disorder, indicator, country_code, colors)
    donut_fig = dg.get_donut_graph(mh_data, country_code, year, colors)

    return corr_fig, donut_fig    


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
    
    
