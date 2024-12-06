from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy import stats
import default_components as dc

app = Dash(__name__)

# Import mental health data
mh_data = pd.read_csv('mental_health.csv', delimiter=';')
available_years = mh_data['Year'].unique().tolist()

# Filter out rows where Code is missing/null and create the lists
mask = mh_data['Code'].notna()  # Get only rows where Code exists
countries = list(dict.fromkeys(mh_data[mask]['Entity']))
country_codes = list(dict.fromkeys(mh_data[mask]['Code']))

# smoth_border_style = {'border-radius':'5px', 'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px', 'overflow':'hidden'}
smoth_border_style = {'border-radius':'5px', 'box-shadow': 'rgba(0, 0, 0, 0.13) 0px 1px 4px', 'overflow':'hidden'}
std_box_padding = {'padding': '20px'}
colors = {
    'green': '#38adad',
    'blue': '#3b4994',
    'color2': '#ace4e4',
    'color3': '#5ac8c8',
    'color1': '#dfb0d6',
    'positive': '#34d399',  # Green for positive correlation
    'negative': '#f87171',  # Red for negative correlation
    'neutral': '#9ca3af'    # Gray for weak correlation
}

# Main wrapper element
app.layout = html.Div(
    id='main-wrapper',
    style={'width': '100%', 'display': 'flex', 'justify-content':'space-between'},
    children=[
        # Selecter sidebar
        html.Div(
            id='selecter-sidebar',
            style={
                'width': '20%', 
                'height': '100vh', 
                'position': 'sticky', 
                'display': 'flex', 
                'flex-direction': 'column', 
                'align-items': 'center',
                'justify-content': 'space-between',
                'top': '0', 
                **smoth_border_style, 
                'background-color': 'white', 
                'padding': '20px', 
                'box-sizing': 'border-box',
                'z-index': '1000'
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
                                {'label': 'CO2 emissions', 'value': 'co2'},
                                {'label': 'Unemployment rate', 'value': 'ur'}
                            ],
                            multi=False,
                            placeholder='Select an indicator',
                            style={'width': '100%'}
                        ),
                        dcc.Dropdown(id='slct_country',
                            options=[{'label': country, 'value': country_codes[i]} for i, country in enumerate(countries)],
                            multi=False,
                            placeholder='Select an Country',
                            style={'width': '100%'}
                        )
                    ]
                ),
                html.P('© 2024 Team cool guys', id='copyright-text', style={'font-size': '12px'})
            ]
        ),
        
        # Content wrapper
        html.Div(id='content-wrapper',
            style={'width': '80%', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'padding': '20px'},
            children=[  
                html.Div(id='title-wrapper',
    style={'width': '100%', 'background-color': 'white', **smoth_border_style, 'margin': '0 0 20px 0', **std_box_padding},
    children=[
        html.H1('Mental Health & Societal Factors Dashboard'),
        html.Div(style={'color': '#737373', 'line-height': '1.6'},
            children=[
                html.P([
                    "Mental health conditions affect hundreds of millions of people worldwide, yet their relationship with societal and economic factors remains under-explored. This dashboard visualizes the prevalence of various mental health disorders across different countries and examines their potential correlations with key societal indicators such as GDP, CO₂ emissions, and unemployment rates."
                ]),
                html.P([
                    "Each mental health condition tracked here—from depression and anxiety to schizophrenia and eating disorders—affects individuals differently and may be influenced by various environmental and societal factors. By exploring these relationships, we can better understand how economic and environmental conditions might interact with mental health at a population level."
                ]),
                html.P([
                    "Use the sidebar controls to select specific mental health conditions and indicators. The visualization tools allow you to explore prevalence rates across different countries, analyze trends over time, and examine potential correlations between mental health and societal factors. ",
                ])
            ]
        )
    ]
),
                # Year Slider box - sticky
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
                
                # Map box
                html.Div(id='map-box',
                    style={'width': '100%', 'margin-bottom': '20px', **smoth_border_style},
                    children=[
                        dcc.Graph(id='disorder_map')
                    ]
                ),
                
                # Wrapper for first row after map
                html.Div(id='disorder-graph-wrapper',
                    style={'width':'100%', 'display':'flex', 'justify-content':'space-between', 'margin-bottom': '20px'},
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
                            style={'width':'29%', 'background-color':'white', **smoth_border_style},
                            children=[
                                dcc.Graph(id='disorders_donut', style={'width':'100%'})
                            ]
                        )
                    ]
                ),
                
                # New Correlation Analysis Section
                html.Div(id='correlation-box',
                    style={
                        'width': '100%',
                        'background-color': 'white',
                        **smoth_border_style,
                        'padding': '20px',
                        'box-sizing': 'border-box'
                    },
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
                                html.Div(id='correlation-interpretation',
                                    style={'width': '25%', 'padding': '10px', 'border-left': '2px solid #f3f4f6'}
                                )
                            ]
                    ),
                        html.Em("Note: Correlation does not imply causation—these relationships are complex and multifaceted.",
                    style={'color': '#666', 'font-size': '14px'}
                )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    Output(component_id='disorders_graph', component_property='figure'),
    [Input(component_id='slct_country', component_property='value'),
     Input(component_id='slct_disorder', component_property='value'),
     Input(component_id='slct_indicator', component_property='value')]
)

def update_graphs(country, disorder, indicator):
    if not country or not disorder or not indicator:
        return dc.get_default_disorder_graph(colors)
    
    # Get mental health data for selected country and disorder
    mh_data_filtered = mh_data[mh_data['Code'] == country]
    mh_display_name = disorder.replace('_', ' ').capitalize()

    country_name = mh_data[mh_data['Code'] == country]['Entity'].iloc[0]
    
    # Match indicator to get corresponding column and title
    match indicator:
        case 'gdp':
            indicator_column = 'gdp'
            indicator_title = 'GDP (in billions)'
        case 'co2':
            indicator_column = 'co2_emissions'
            indicator_title = 'CO2 emissions'
        case 'ur':
            indicator_column = 'unemployment_rate'
            indicator_title = 'Unemployment rate'

    fig = go.Figure()
    # Add mental health line (primary y-axis)
    fig.add_trace(go.Scatter(
        x=mh_data_filtered['Year'],
        y=mh_data_filtered[disorder],
        mode='lines',
        name=f'{mh_display_name}',
        line=dict(color=colors['green'], width=2),
        line_shape='spline',
        yaxis='y1'
    ))
    # Add indicator line (secondary y-axis)
    fig.add_trace(go.Scatter(
        x=mh_data_filtered['Year'],
        y=mh_data_filtered[indicator_column],
        mode='lines',
        name=indicator_title,
        line=dict(color=colors['blue'], width=2),
        line_shape='spline',
        yaxis='y2'
    ))

    # Update layout for secondary y-axis
    fig.update_layout(
        # Title
        title={
            'text': f'{mh_display_name} and {indicator_title} in {country_name} over the Years',
            'x': 0.5,  # Center the title
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 18,
                'color': '#333',  # Dark gray for a modern look
                'family': 'Roboto, Arial, sans-serif'  # Clean sans-serif font
            }
        },
        
        # Background
        plot_bgcolor='#f9f9f9',  
        paper_bgcolor='#ffffff',  
        
        # Axes
        xaxis=dict(
            title='Year',
            showgrid=False,  # No grid lines for a clean look
            showline=True,  # Show axis lines
            linecolor='black',  # Axis line color
            ticks='outside',  # Ticks pointing outward
            tickcolor='black',
            tickfont=dict(
                size=12,
                color='#333'
            ),
            titlefont=dict(
                size=14,
                color='#333'
            )
        ),
        yaxis=dict(
            title=f'{mh_display_name}',
            showgrid=False,  
            gridcolor='#eaeaea', 
            zeroline=False,  
            showline=True,
            linecolor=colors['green'],
            ticks='outside',
            tickcolor=colors['green'],
            tickfont=dict(
                size=12,
                color=colors['green']
            ),
            titlefont=dict(
                size=14,
                color=colors['green']
            )
        ),
        yaxis2=dict(
            title=indicator_title,
            overlaying='y',
            side='right',
            showgrid=False,
            showline=True,
            linecolor=colors['blue'],
            tickcolor=colors['blue'],
            tickfont=dict(
                size=12,
                color=colors['blue']
            ),
            titlefont=dict(
                size=14,
                color=colors['blue']
            )
        ),
        
        # Legend
        legend=dict(
            orientation='h',  # Horizontal layout for the legend
            x=0.5,
            xanchor='center',
            y=-0.2,
            font=dict(
                size=12,
                color='#333'
            )
        ),
        
        # Margins
        margin=dict(
            l=50,  # Left margin
            r=50,  # Right margin
            t=50,  # Top margin
            b=40   # Bottom margin
        ),
        
        # Template
        template='simple_white',  # Clean white template
    )

    return fig


# Add this new callback
@app.callback(
    [Output('correlation-value', 'children'),
     Output('correlation-value', 'style'),
     Output('correlation-label', 'children'),
     Output('strength-bar', 'style'),
     Output('strength-label', 'children'),
     Output('correlation-interpretation', 'children')],
    [Input('slct_country', 'value'),
     Input('slct_disorder', 'value'),
     Input('slct_indicator', 'value')]
)
def update_correlation(country, disorder, indicator):
    if not all([country, disorder, indicator]):
        return "—", {'font-size': '48px', 'margin': '0', 'font-weight': 'bold', 'color': colors['neutral']}, \
               "Select data to analyze", \
               {'height': '100%', 'width': '0%', 'background-color': colors['neutral']}, \
               "No data", \
               "Please select a country, disorder, and indicator to see the correlation analysis."

    # Filter data for selected country
    country_data = mh_data[mh_data['Code'] == country].copy()
    country_name = mh_data[mh_data['Code'] == country]['Entity'].iloc[0]
    
    # Get the indicator column name
    indicator_col = {
        'gdp': 'gdp',
        'co2': 'co2_emissions',
        'ur': 'unemployment_rate'
    }.get(indicator)
    
    # Calculate correlation
    x = country_data[disorder].values
    y = country_data[indicator_col].values
    
    # Remove any rows where either value is NaN
    mask = ~(np.isnan(x) | np.isnan(y))
    x = x[mask]
    y = y[mask]
    
    # Calculate Pearson correlation coefficient
    if len(x) > 1:  # Need at least 2 points for correlation
        correlation, _ = stats.pearsonr(x, y)
    else:
        correlation = 0

    # Determine correlation characteristics
    abs_corr = abs(correlation)
    if abs_corr >= 0.7:
        strength = "Strong"
    elif abs_corr >= 0.3:
        strength = "Moderate"
    else:
        strength = "Weak"

    # Set color based on correlation direction
    if correlation > 0.1:
        color = colors['positive']
        direction = "positive"
    elif correlation < -0.1:
        color = colors['negative']
        direction = "negative"
    else:
        color = colors['neutral']
        direction = "negligible"

    # Create interpretation text
    disorder_name = disorder.replace('_', ' ').title()
    indicator_name = {
        'gdp': 'GDP',
        'co2': 'CO2 emissions',
        'ur': 'unemployment rate'
    }.get(indicator, indicator)
    
    interpretation = f"There is a {strength.lower()} {direction} correlation between {disorder_name} and {indicator_name} in {country_name}"

    return (
        f"{correlation:.2f}",  # Correlation value
        {'font-size': '48px', 'margin': '0', 'font-weight': 'bold', 'color': color},  # Value style
        f"{strength} {direction.title()} Correlation",  # Label
        {'height': '100%', 'width': f'{abs_corr * 100}%', 'background-color': color, 'transition': 'all 0.5s ease-in-out'},  # Strength bar
        strength,  # Strength label
        interpretation  # Interpretation text
    )


@app.callback(
    Output(component_id='disorders_donut', component_property='figure'),
    [Input(component_id='slct_country', component_property='value'),
     Input(component_id='year_slider', component_property='value')]
)

def update_donut(country, year):
    
    if not country or not year:
        return dc.get_default_donut(colors)
    
    mental_health_columns = ['schizophrenia', 'depressive_disorder',
                        'anxiety_disorders', 'bipolar_disorders',
                        'eating_disorders']
    labels = [col.replace('_', ' ').title() for col in mental_health_columns]
    mh_data_filtered = mh_data[(mh_data['Code'] == country) & (mh_data['Year'] == year)]
    values = mh_data_filtered[mental_health_columns].values.flatten()
    
    
    # Create the donut chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        # textinfo='label+percent',
        # textposition='inside',
        # texttemplate='%{label}<br>%{percent:.1%}',
        marker=dict(colors=[color for key, color in colors.items()])
    )])

    # Update layout
    country_name = mh_data_filtered[mh_data_filtered['Code'] == country]['Entity'].iloc[0]
    fig.update_layout(
        title={
            'text': f"Mental Health Distribution -<br>{country_name} ({year})",
            # 'y': 0.95,
            'x': 0.5,
            'xanchor': 'center'
            # 'yanchor': 'top'
        },
        autosize=True,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.6,
            x= 0.5,
            xanchor="center",
        ),
        margin=dict(t=90, b=120, l=30, r=30)
    )
    return fig
    


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
    
    
