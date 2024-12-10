from dash import Dash, dcc, html, Input, Output
import pandas as pd

import corr_graph_functions as cg
import map_functions as mf
import donut_graph_functions as dg
import corr_explain_functions as ce
import country_comparison_functions as ccf


app = Dash(__name__)

# Import mental health data
mh_data = pd.read_csv('mental_health.csv', delimiter=';')
countries = mh_data.Entity.unique()
available_years = mh_data['Year'].unique().tolist()

# Filter out nulls first, then remove duplicates
filtered_data = mh_data[mh_data["Code"].notna()]
unique_countries = filtered_data[["Entity", "Code"]].drop_duplicates()

smoth_border_style = {'border-radius':'5px', 'box-shadow': 'rgba(0, 0, 0, 0.13) 0px 1px 4px', 'overflow':'hidden'}
std_box_padding = {'padding': '20px'}

colors = {
    'green': '#38adad',
    'blue': '#3b4994',
    'lightblue': '#ace4e4',
    'midlbue': '#5ac8c8',
    'dense_pink': '#dfb0d6',
    'positive': '#34d399',  # Green for positive correlation
    'negative': '#f87171',  # Red for negative correlation
    'neutral': '#9ca3af'    # Gray for weak correlation
}

country_code_df = mh_data[['Entity', 'Code']].drop_duplicates()
country_dict = dict(zip(country_code_df['Code'], country_code_df['Entity']))

# Data preparation for the map
disorders_factors = list(mh_data.columns)[3:]
mh_data_cp = mh_data.copy()
mh_data_map = mf.classify_disorders(mh_data_cp, disorders_factors)

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
                        html.H3("Select disorder & indicator", style={'margin': '0 0 20px 0'}),
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
                        ),
                        html.H4("Selected country", style={'margin': '50px 0 20px 0'}),
                        html.Img(id='selected-flag',
                            style={'width':'100%'},
                            src='https://flagcdn.com/w160/xx.png'  # Default blank flag
                        )
                    ]
                ),
                html.P('© 2024 Karim, Florian & Finn', id='copyright-text', style={'font-size': '12px'})
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
                    style={
                        'width': '100%', 
                        'margin-bottom': '20px', 
                        **smoth_border_style, 
                        **std_box_padding, 
                        'box-sizing': 'border-box', 
                        'background-color': 'white',
                        'position': 'sticky',
                        'top': '20px',
                        'z-index': '900',
                        'backdrop-filter': 'blur(8px)',
                    },
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
                    style={'width':'100%', 'display':'flex', 'justify-content':'space-between', 'margin': '0 0 20px 0'},
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
                ),
                # Correlation Analysis Section
                html.Div(id='correlation-box',
                    style={'width': '100%', 'background-color': 'white', **smoth_border_style, 'padding': '20px', 'box-sizing': 'border-box'},
                    children=[
                        html.H3('Correlation Analysis', style={'margin-bottom': '15px'}),
                        html.Div(id='correlation-content',
                            style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between'},
                            children=[
                                # Left section - Correlation coefficient
                                html.Div(style={'width': '30%', 'text-align': 'center'},
                                    children=[
                                        html.H2(id='correlation-value',
                                            style={'font-size': '48px', 'margin': '0', 'font-weight': 'bold'}
                                        ),
                                        html.P(id='correlation-label',
                                            style={'margin': '5px 0', 'color': '#666'}
                                        )
                                    ]
                                ),
                                # Center section - Strength bar
                                html.Div(style={'width': '40%'},
                                    children=[
                                        html.Div(style={'margin-bottom': '5px'},
                                            children=[
                                                html.Span("Correlation Strength", style={'color': '#666'}),
                                                html.Span(id='strength-label',
                                                    style={'float': 'right', 'font-weight': 'bold'}
                                                )
                                            ]
                                        ),
                                        html.Div(style={
                                            'width': '100%',
                                            'height': '10px',
                                            'background-color': '#f3f4f6',
                                            'border-radius': '5px',
                                            'overflow': 'hidden'
                                        },
                                            children=[
                                                html.Div(id='strength-bar',
                                                    style={
                                                        'height': '100%',
                                                        'width': '0%',
                                                        'transition': 'width 0.5s ease-in-out'
                                                    }
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                # Right section - Interpretation
                                html.Div(id='correlation-interpretation', style={'width': '25%', 'padding': '10px', 'border-left': '2px solid #f3f4f6'})
                            ]
                        ),
                        html.Em("Note: Correlation does not imply causation—these relationships are complex and multifaceted.", style={'color': '#666', 'font-size': '14px'})
                    ]
                ),
                
                # comparison
                html.Div(id='country-comparison-box',
                    style={'width': '100%', 'background-color': 'white', **smoth_border_style, 'margin-top': '20px', 'padding': '20px', 'box-sizing': 'border-box'},
                    children=[
                        # Title and description section
                        html.Div(
                            style={'margin-bottom': '20px'},
                            children=[
                                html.H3('Country Comparison', style={'margin-bottom': '8px'}),
                                html.P(
                                    'Compare mental health indicators and societal factors between two countries to identify patterns and correlations.',
                                    style={'color': '#666', 'margin': '0'}
                                )
                            ]
                        ),
                        # Country selection row
                        html.Div(
                            style={'display': 'flex', 'align-items': 'center', 'gap': '20px', 'margin-bottom': '20px'},
                            children=[
                                # First country display
                                html.Div(
                                    style={'flex': '1'},
                                    children=[
                                        html.Label("Base Country", style={'margin-bottom': '5px', 'display': 'block', 'font-weight': 'bold'}),
                                        html.Div(id='selected_country_display', 
                                            style={
                                                'padding': '8px 12px',
                                                'border': '1px solid #e5e7eb',
                                                'border-radius': '4px',
                                                'background-color': '#f9fafb'
                                            })
                                    ]
                                ),
                                # Second country dropdown
                                html.Div(
                                    style={'flex': '1'},
                                    children=[
                                        html.Label("Comparison Country", style={'margin-bottom': '5px', 'display': 'block', 'font-weight': 'bold'}),
                                        dcc.Dropdown(
                                            id='country_2_dropdown',
                                            options=ccf.format_dropdown_options(unique_countries),
                                            placeholder='Search and select a country',
                                            style={'width': '100%'},
                                            searchable=True,
                                            clearable=True
                                        )
                                    ]
                                )
                            ]
                        ),
                        dcc.Graph(id='country_comparison_graph')
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


@app.callback(
    Output('selected-flag', 'src'),
    Input('disorder_map', 'clickData')
)

def update_flag(click_data):
    if not click_data:
        # Return a default flag or empty image when no country is selected
        return 'https://flagcdn.com/w160/xx.png'  # xx is a blank flag
    
    country_code = click_data['points'][0]['location']
    # Convert 3-letter code to 2-letter code using your existing function
    two_letter_code = ccf.three_to_two_letter_code(country_code)
    return f'https://flagcdn.com/w160/{two_letter_code}.png'


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
    country_name = country_dict[country_code]
    corr_fig = cg.get_corr_graph(mh_data, disorder, indicator, country_code, country_name, colors)
    donut_fig = dg.get_donut_graph(mh_data, country_code, country_name, year, colors)

    return corr_fig, donut_fig    



# Correlation explaination callback
@app.callback(
    [Output('correlation-value', 'children'),
     Output('correlation-value', 'style'),
     Output('correlation-label', 'children'),
     Output('strength-bar', 'style'),
     Output('strength-label', 'children'),
     Output('correlation-interpretation', 'children')],
    [Input(component_id='disorder_map', component_property='clickData'),
     Input('slct_disorder', 'value'),
     Input('slct_indicator', 'value')]
)
def update_correlation(click_data, disorder, indicator):
    if not all([click_data, disorder, indicator]):
        return ce.get_default_corr_expl(colors)

    country_code = click_data['points'][0]['location']
    country_name = country_dict[country_code]
    corr_explain = ce.get_corr_expl(mh_data, country_code, country_name, disorder, indicator, colors)
    
    return corr_explain[0], corr_explain[1], corr_explain[2], corr_explain[3], corr_explain[4], corr_explain[5]


@app.callback(
    [Output('country_comparison_graph', 'figure'),
     Output('selected_country_display', 'children')],
    [Input('disorder_map', 'clickData'),
     Input('country_2_dropdown', 'value'),
     Input('slct_disorder', 'value'),
     Input('slct_indicator', 'value')]
)
def update_comparison_graph(click_data, country2, disorder, indicator):
    if not click_data:
        return ccf.get_default_comparison_graph(colors), "No country selected"
    
    country1 = click_data['points'][0]['location']
    
    if not all([country2, disorder, indicator]):
        return ccf.get_default_comparison_graph(colors), f"Selected country: {country_dict[country1]}"
    
    return (
        ccf.create_country_comparison(
            mh_data, country1, country2, disorder, indicator, country_dict, colors
        ),
        f"Selected country: {country_dict[country1]}"
    )

if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
    
    
