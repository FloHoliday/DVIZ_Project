import plotly.graph_objects as go

def get_corr_graph(mh_data, disorder, indicator, country_code, colors):
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
            return get_default_disorder_graph(colors)
        
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
    
    
def get_default_disorder_graph(colors):
    """Create a default figure with styling but no data."""
    fig = go.Figure()
    fig.update_layout(
        # Title
        title={
            'text': 'Select a Disorder and Indicator',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 18,
                'color': '#333',
                'family': 'Roboto, Arial, sans-serif'
            }
        },
        
        # Background
        plot_bgcolor='#f9f9f9',
        paper_bgcolor='#ffffff',
        
        # Axes
        xaxis=dict(
            title='Year',
            showgrid=False,
            showline=True,
            linecolor='black',
            ticks='outside',
            tickcolor='black',
            tickfont=dict(size=12, color='#333'),
            titlefont=dict(size=14, color='#333')
        ),
        yaxis=dict(
            title='Mental Health Metric',
            showgrid=False,
            showline=True,
            linecolor=colors['green'],
            ticks='outside',
            tickcolor=colors['green'],
            tickfont=dict(size=12, color=colors['green']),
            titlefont=dict(size=14, color=colors['green'])
        ),
        yaxis2=dict(
            title='Indicator Metric',
            overlaying='y',
            side='right',
            showgrid=False,
            showline=True,
            linecolor=colors['blue'],
            tickcolor=colors['blue'],
            tickfont=dict(size=12, color=colors['blue']),
            titlefont=dict(size=14, color=colors['blue'])
        ),
        
        # Legend
        legend=dict(
            orientation='h',
            x=0.5,
            xanchor='center',
            y=-0.2,
            font=dict(size=12, color='#333')
        ),
        
        # Margins
        margin=dict(l=50, r=50, t=50, b=40),
        
        # Template
        template='simple_white'
    )
    return fig