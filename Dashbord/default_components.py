import plotly.graph_objects as go

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


def test():
    """Generate a default donut chart with grey segments and a placeholder legend."""
    labels = ['Schizophrenia', 'Depressive Disorder', 'Anxiety Disorders', 'Bipolar Disorders', 'Eating Disorders']
    values = [1, 1, 1, 1, 1]  # Equal placeholder values for all segments

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        textinfo='label',  # Show only labels on the chart
        marker=dict(colors=['#d3d3d3'] * len(labels))  # All grey segments
    )])

    # Update layout
    fig.update_layout(
        title={
            'text': "Mental Health Distribution",
            'x': 0.5,
            'xanchor': 'center'
        },
        autosize=True,
        showlegend=True,  # Show legend with placeholder labels
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.6,
            x=0.5,
            xanchor="center",
        ),
        margin=dict(t=90, b=120, l=30, r=30)
    )

    return fig


def get_default_donut(colors):
    values = [1]
    
    # Create the donut chart
    fig = go.Figure(data=[go.Pie(
        # labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=[colors['green']]),
        hoverinfo ='none',
        textinfo='none'
        
    )])

    fig.update_layout(
        title={
            'text': f"Mental Health Distribution -<br>select a country",
            'x': 0.5,
            'xanchor': 'center'
        },
        autosize=True,
        showlegend=False,
        margin=dict(t=90, b=120, l=30, r=30)
    )
    return fig