from dash import Dash, dcc, html, Input, Output, no_update
from dash import callback_context as ctx
import pandas as pd

import corr_graph_functions as cg
import map_functions as mf
import donut_graph_functions as dg
import corr_explain_functions as ce
import country_comparison_functions as ccf
import friendly_names as fn

app = Dash(__name__)

# Import mental health data
mh_data = pd.read_csv('Dashbord/data/mental_health_and_indicators.csv', delimiter=';')
available_years = mh_data['Year'].unique().tolist()

# Filter out nulls first, then remove duplicates
filtered_data = mh_data[mh_data["Code"].notna()]
unique_countries = filtered_data[["Entity", "Code"]].drop_duplicates()

country_code_df = mh_data[['Entity', 'Code']].drop_duplicates()
country_dict = dict(zip(country_code_df['Code'], country_code_df['Entity']))

# Data preparation for the map
disorders_factors = list(mh_data.columns)[3:]
mh_data_cp = mh_data.copy()
mh_data_map = mf.classify_disorders(mh_data_cp, disorders_factors)

colors = {
    'light-yellow' : '#f4f799',  
    'aqua': '#89d3d3',  
    'deep-teal': '#2ca3a3',  
    'blush-pink' : '#e8a3cc', 
    'lavender' : '#a983d5',
    'rich-blue' : '#416eb7',
    'magenta' : '#d96ba8',
    'amethyst' : '#9a52c2',
    'deep-navy' : '#2f3b99',
    'positive': '#34d399',
    'negative': '#f87171',
    'neutral': '#9ca3af',
}

map_colors = [
    colors['light-yellow'],
    colors['aqua'],
    colors['deep-teal'],
    colors['blush-pink'],
    colors['lavender'],
    colors['rich-blue'],
    colors['magenta'],
    colors['amethyst'],
    colors['deep-navy'],
]

smoth_border_style = {'border-radius':'5px', 'box-shadow': 'rgba(0, 0, 0, 0.13) 0px 1px 4px', 'overflow':'hidden'}
std_box_padding = {'padding': '20px'}

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
                # Logo container
                html.Div(id='logo-container',
                    style={'width': '30%', 'overflow': 'hidden', 'margin-top': '30px'},
                    children=[
                        html.Img(id='logo-img',
                            style={'width':'100%'},
                            src='assets/img/logo_frei.jpg'
                        )
                    ]
                ),
                # Disorder & Indicator dropdown wrapper
                html.Div(
                    id='dropdown-wrapper',
                    style={'width':'100%', 'margin-bottom': '0px'},
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
                                {'label': 'Unemployment rate', 'value': 'unemployment_rate'},
                                {'label': 'Life expectancy', 'value': 'life_expectancy'},
                                {'label': 'Health expenditure', 'value': 'health_expenditure'}
                            ],
                            multi=False,
                            placeholder='Select an indicator',
                            style={'width': '100%'}
                        )
                    ]
                ),
                # Display the currently selected country
                html.Div(
                    id='flag-container',
                    style={
                        'width': '100%',
                        'height': '100px',  
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'overflow': 'hidden'
                    },
                    children=[
                        html.Div(id='flag-component')
                    ]
                ),
                html.P('© 2025 Finn, Florian & Karim', id='copyright-text', style={'font-size': '12px'})
            ]
        ),
        # Main content wrapper
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
                                html.P("Mental health conditions affect hundreds of millions of people worldwide, yet their relationship with societal and economic factors remains under-explored. This dashboard visualizes the prevalence of various mental health disorders across different countries and examines their potential correlations with key societal indicators such as GDP, CO₂ emissions, and more."),
                                html.P("Each mental health condition tracked here — from depression and anxiety to schizophrenia and eating disorders — affects individuals differently and may be influenced by various environmental and societal factors. By exploring these relationships, we can better understand how economic and environmental conditions might interact with mental health at a population level."),
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
                html.Div(id='map-box',
                    style={'width':'100%', 'margin-bottom': '20px', 'display':'flex', 'justify-content':'space-between'},
                    children=[
                        # Map box
                        html.Div(
                            style={'width' : '72%'},
                            children=[
                                html.Div(
                                    style={**smoth_border_style, 'margin-bottom' : '10px', 'background-color' : 'white', 'padding': '0 20px 0 20px'},
                                    children=[
                                        html.H3("", style={'margin-bottom' : '0'}, id='map-title'),
                                        html.P("text here", id='map-description')
                                    ]
                                ),
                                html.Div(id='map-conainter',
                                    style={**smoth_border_style},
                                    children=[
                                        dcc.Graph(id='disorder_map')
                                    ]
                                )
                            ]
                        ),
                        # Pie chart box
                        html.Div(id='donut-box',
                            style={'width':'26%','background-color':'white', **smoth_border_style},
                            children=[
                                dcc.Graph(id='disorders_donut',style={'width':'100%'}),
                                html.P('', id='donut_note', style={'color': '#666', 'font-size': '14px', 'padding': '0 20px 0 20px'})
                            ]
                        )
                    ]
                ),
                # Wrapper for first row after map
                html.Div(id='disorder-graph-wrapper',
                    style={'width':'100%', 'display':'flex', 'justify-content':'space-between', 'margin': '0 0 20px 0'},
                    children=[
                        html.Div(id='graph1-container',
                            style={'width':'72%'},
                            children=[
                                html.Div(id='disorder-graph-text-box',
                                    style={'width':'100%','background-color': 'white', 'margin-bottom':'10px', **smoth_border_style,'padding':'0 20px 0 20px'},
                                    children=[
                                        html.H3('Please select a country, disorder and indicator', id='graph-title', style={'margin-bottom':'0'}),
                                        html.P(id='graph-description')
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
                        # Correlation analysis section
                        html.Div(id='correlation-box',
                            style={'width': '26%', 'background-color': 'white', **smoth_border_style, 'padding': '20px', 'box-sizing': 'border-box', 'position':'relative'},
                            children=[
                                html.H3('Correlation Analysis', style={'margin-bottom': '15px'}),
                                html.Div(id='correlation-content',
                                    style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'flex-direction':'column'},
                                    children=[
                                        # Left section - Correlation coefficient
                                        html.Div(style={'width': '100%', 'text-align': 'center', 'margin-bottom': '30px'},
                                            children=[
                                                html.H2(id='correlation-value',
                                                    style={'font-size': '48px', 'margin': '0', 'font-weight': 'bold'}
                                                ),
                                                html.P(id='correlation-label',
                                                    style={'margin': '5px 0', 'color': '#666'}
                                                )
                                            ]
                                        ),
                                        html.Div(style={'width': '100%', 'margin-bottom': '30px'},
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
                                        html.Div(id='correlation-interpretation', style={'width': '100%', 'padding': '10px', 'margin-bottom': '30px'}),
                                        html.Em("Note: Correlation does not imply causation — these relationships are complex and multifaceted.", style={'color': '#666', 'font-size': '14px', 'position':'absolute', 'bottom':'20px', 'left':'20px'})
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
                # country comparison
                html.Div(id='country-comparison-box',
                    style={'width': '100%', 'background-color': 'white', **smoth_border_style, 'padding': '20px', 'box-sizing': 'border-box', 'position':'relative'},
                    children=[
                        html.Div(
                            style={'margin-bottom': '20px'},
                            children=[
                                html.H3('Country Comparison', style={'margin-bottom': '8px'}),
                                html.Div(id='comparison-desc-box',
                                    style={'display':'flex', 'justify-content':'space-between'},
                                    children=[
                                        html.P(
                                            'Compare mental health indicators and societal factors between two countries to identify patterns and correlations. All data are normalized in order to make visual correlations in the curves optimally recognizable.',
                                            style={'color': '#666', 'margin': '0', 'width': '96%'}
                                        ),
                                        html.Div(id='questionmark-box',
                                            style={'width': '3%','display':'flex', 'justify-content':'center', 'align-items':'center', 'cursor':'pointer'},
                                            children=[
                                                html.Div(id='questionmark-hover-box',
                                                    style={'position':'absolute', 'top':'120px', 'right':'15px', 'width': '50%', 'background-color':'white', 'z-index':'50', **smoth_border_style, 'padding': '20px'},
                                                    children=[
                                                        html.H3('Information about Normalized Data', style={'margin-top':'0'}),
                                                        html.P('The data displayed in the graph is normalized, meaning that all values have been scaled to enable better visual comparison between the countries. This approach helps to highlight patterns and potential correlations between the curves. However, it is important to note that the normalized data does not represent actual values of the indicators or the mental disorders. Instead, it illustrates relative trends and behaviors, allowing for the identification of similarities in dynamics between the selected countries.', style={'margin-bottom':'0'})
                                                    ],
                                                    className='hidden'
                                                ),
                                                html.Div(
                                                    style={'height':'20px', 'width': '20px'},
                                                    children=[
                                                        html.P('?', style={'margin':'0', 'height': '20px', 'width':'20px', 'text-align':'center', 'line-height': '20px', 'color': 'white', 'background-color':'black', 'border-radius': '30px', 'font-size':'.8em'})
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
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
    [Output(component_id='disorder_map', component_property='figure'),
     Output(component_id='map-title', component_property='children'),
     Output(component_id='map-description', component_property='children')],
    [Input(component_id='slct_disorder', component_property='value'),
     Input(component_id='slct_indicator', component_property='value'),
     Input(component_id='year_slider', component_property='value'),
     Input(component_id='disorder_map', component_property='clickData'),
    Input(component_id='disorder_map', component_property='relayoutData')
     ]
)

def update_map(disorder, indicator, year, click_data, relayout_data):
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    # When zooming occurs, check and enforce zoom limits
    if trigger == 'disorder_map' and 'relayoutData' in ctx.triggered[0]['prop_id']:
        if relayout_data and 'geo.projection.scale' in relayout_data:
            current_zoom = relayout_data['geo.projection.scale']

            # Define our zoom limits
            MIN_ZOOM = 1
            MAX_ZOOM = 10

            # If zoom is within bounds, maintain current view
            if MIN_ZOOM <= current_zoom <= MAX_ZOOM:
                return no_update

    if not all([disorder, indicator]):
        return mf.plot_default_map(mh_data_map), 'Please select all parameters', "Select a country and a disorder to view the bivariate map"

    clicked_country = None
    if click_data and 'points' in click_data and len(click_data['points']) > 0:
        clicked_country = click_data['points'][0].get('location')

    map_fig = mf.plot_bivariate_map(mh_data_map, disorder, indicator, year, map_colors, highlight_country=clicked_country)
    disorder_title = fn.get_friendly_disorder(disorder)
    indicator_title = fn.get_friendly_indicator_text(indicator)
    map_title = f'Bivariate map of {disorder_title} and {indicator_title} in {year}'
    explaination_text = f'This bivariate map visualizes the relationship between {disorder_title} prevalence and {indicator_title} across countries. Combined color gradients highlight patterns or correlations, revealing how these variables interact globally.'

    return map_fig, map_title, explaination_text

# Sidebar flag callback
@app.callback(
    Output(component_id='flag-component', component_property='children'),
    [Input(component_id='disorder_map', component_property='clickData')]
)
def update_flag(click_data):
    if not click_data:
        return None
    
    country_code = click_data['points'][0]['location']
    two_letter_code = ccf.three_to_two_letter_code(country_code)
    
    if two_letter_code:
        return html.Img(
            src=f"https://flagcdn.com/w160/{two_letter_code}.png",
            style={
                'max-width': '160px',
                'max-height': '90px',
                'width': 'auto',
                'height': 'auto',
                'border-radius': '4px',
                'border': '1px solid #e5e7eb',
                'box-shadow': '0 1px 3px rgba(0,0,0,0.24)'
            }
        )
    else:
        return None

# Correlation graph & pie chart callback
@app.callback(
     [Output(component_id='disorders_graph', component_property='figure'),
      Output(component_id='graph-title', component_property='children'),
      Output(component_id='graph-description', component_property='children')],
      Output(component_id='disorders_donut', component_property='figure'),
      Output(component_id='donut_note', component_property='children'),
    [Input(component_id='slct_disorder', component_property='value'),
     Input(component_id='slct_indicator', component_property='value'),
     Input(component_id='disorder_map', component_property='clickData'),
     Input(component_id='year_slider', component_property='value')]
)

def update_corr_and_donut(disorder, indicator, click_data, year):

    if not all([disorder, indicator, click_data]):
        return (cg.get_default_corr_graph(colors), 
                "Please select all parameters",
                "Select a country, disorder and indicator to view the analysis",
                dg.get_default_donut(colors), 
                ''
        )

    country_code = click_data['points'][0]['location']
    country_name = country_dict[country_code]
    corr_fig = cg.get_corr_graph(mh_data, disorder, indicator, country_code, colors)
    
    # Format disorder name for display
    friendly_disorder = fn.get_friendly_disorder(disorder)
    friendly_indicator = fn.get_friendly_indicator_title(indicator)
    
    # Create title and description
    title = f"{friendly_disorder} and {friendly_indicator} analysis for {country_name}"
    description = (
        f"This graph shows the relationship between {friendly_disorder} prevalence "
        f"and {friendly_indicator} in {country_name} over time. The lines represent "
        f"the trends for both metrics, allowing you to observe any potential correlations "
        f"or patterns between them."
    )
    
    donut_fig, donut_note = dg.get_donut_graph(mh_data, country_code, country_name, year, colors)

    return corr_fig, title, description, donut_fig, donut_note

# Correlation explaination callback
@app.callback(
    [Output(component_id='correlation-value', component_property='children'),
     Output(component_id='correlation-value', component_property='style'),
     Output(component_id='correlation-label', component_property='children'),
     Output(component_id='strength-bar', component_property='style'),
     Output(component_id='strength-label', component_property='children'),
     Output(component_id='correlation-interpretation', component_property='children')],
    [Input(component_id='disorder_map', component_property='clickData'),
     Input(component_id='slct_disorder', component_property='value'),
     Input(component_id='slct_indicator', component_property='value')]
)
def update_correlation(click_data, disorder, indicator):
    if not all([click_data, disorder, indicator]):
        return ce.get_default_corr_expl(colors)

    country_code = click_data['points'][0]['location']
    country_name = country_dict[country_code]
    corr_explain = ce.get_corr_expl(mh_data, country_code, country_name, disorder, indicator, colors)

    return corr_explain[0], corr_explain[1], corr_explain[2], corr_explain[3], corr_explain[4], corr_explain[5]

# Country comparison callback
@app.callback(
    [Output(component_id='country_comparison_graph', component_property='figure'),
     Output(component_id='selected_country_display', component_property='children')],
    [Input(component_id='disorder_map', component_property='clickData'),
     Input(component_id='country_2_dropdown', component_property='value'),
     Input(component_id='slct_disorder', component_property='value'),
     Input(component_id='slct_indicator', component_property='value')]
)
def update_comparison_graph(click_data, country2, disorder, indicator):
    if not click_data:
        return ccf.get_default_comparison_graph(colors), "No country selected"

    country1 = click_data['points'][0]['location']

    if not all([country2, disorder, indicator]):
        return ccf.get_default_comparison_graph(colors), f"Selected country: {country_dict[country1]}"

    return (
        ccf.create_country_comparison(mh_data, country1, country2, disorder, indicator, country_dict, colors),
        f"Selected country: {country_dict[country1]}"
    )


if __name__ == '__main__':
    app.run_server(debug=False)
