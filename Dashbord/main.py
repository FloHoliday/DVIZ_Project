from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import helper
import default_components as dc


app = Dash(__name__)

# Import mental health data
mh_data = pd.read_csv('/Users/finneyer/Documents/HSLU/Semester 3/DVIZ/Projektarbeit/DVIZ_Project/mental_health.csv', delimiter=';')
countries = mh_data.Entity.unique()
available_years = mh_data['Year'].unique().tolist()

# smoth_border_style = {'border-radius':'5px', 'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px', 'overflow':'hidden'}
smoth_border_style = {'border-radius':'5px', 'box-shadow': 'rgba(0, 0, 0, 0.13) 0px 1px 4px', 'overflow':'hidden'}
std_box_padding = {'padding': '20px'}
colors = {'green': '#38adad', 'blue': '#3b4994', 'color2':'#ace4e4', 'color3': '#5ac8c8', 'color1':'#dfb0d6'}

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
                        ),
                        # Drop down for the country (delete as soon as the map works)
                        dcc.Dropdown(id='slct_country',
                            options=[
                                {'label': 'Switzerland', 'value': 'CHE'},
                                {'label': 'Afghanistan', 'value': 'AFG'},
                            ],
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
            style={'width': '80%', 'display': 'flex', 'flex-direction':'column', 'align-items':'center', 'padding':'20px'},
            children=[  
                html.Div(id='title-wrapper',
                    style={'background-color': 'white', **smoth_border_style, 'margin': '0 0 20px 0', **std_box_padding},
                    children=[
                        html.H1('Mental Illness Correlation'),
                        html.P('Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',
                            style={'color':'#737373'}),
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
                        dcc.Graph(id='disorder_map'
                           
                        )
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

@app.callback(
     Output(component_id='disorders_graph', component_property='figure'),
    [Input(component_id='slct_disorder', component_property='value'),
     Input(component_id='slct_indicator', component_property='value'),
     Input(component_id='slct_country', component_property='value')]
)

def update_corr_graph(disorder, indicator, country_code):
    if not disorder or not indicator or not country_code:
        return dc.get_default_disorder_graph(colors)
    
    mh_data_country = mh_data[mh_data['Code'] == country_code]
    mh_data_disorder = mh_data_country[['Year', disorder]]
    mh_data_indicator = mh_data_country[['Year', indicator]]
    mh_display_name = disorder.replace('_', ' ').capitalize()
    indicator_title = ''

    match indicator:
        case 'gdp':
            indicator_title = 'GDP (in billions)'
        case 'co2_emissions':
            indicator_title = 'CO2 emissions'
        case 'unemployment_rate':
            indicator_title = 'Unemployment rate'
        case _:
            print(f"An unknown indicator {indicator} is given")
            return dc.get_default_disorder_graph(colors)
        
    fig = go.Figure()
    # Add mental health line (primary y-axis)
    fig.add_trace(go.Scatter(
        x=mh_data_disorder['Year'],
        y=mh_data_disorder[disorder],
        mode='lines',
        name=f'{mh_display_name}',
        line=dict(color=colors['green'], width=2),
        line_shape='spline',
        yaxis='y1'
    ))
    # Add line (secondary y-axis)
    fig.add_trace(go.Scatter(
        x=mh_data_indicator['Year'],
        y=mh_data_indicator[indicator],
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
            'text': f'{mh_display_name} and {indicator_title} in Switzerland over the Years',
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
    
    
    
    
    
    
