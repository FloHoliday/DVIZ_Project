import plotly.graph_objects as go
def get_donut_graph(mh_data, country_code, country_name, year, colors):
    mental_health_columns = ['schizophrenia', 'depressive_disorder',
                        'anxiety_disorders', 'bipolar_disorders',
                        'eating_disorders']
    labels = [col.replace('_', ' ').title() for col in mental_health_columns]
    mh_data_filtered = mh_data[(mh_data['Code'] == country_code) & (mh_data['Year'] == year)]
    values = mh_data_filtered[mental_health_columns].values.flatten()
    donut_colors = [
        colors['aqua'],
        colors['rich-blue'],
        colors['lavender'],
        colors['magenta'],
        colors['deep-teal']
        ]
    
    
    # Create the donut chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        # textinfo='label+percent',
        # textposition='inside',
        # texttemplate='%{label}<br>%{percent:.1%}',
        marker=dict(colors=donut_colors)
    )])

    # Update layout
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


def get_default_donut(colors):
    values = [1]
    
    # Create the donut chart
    fig = go.Figure(data=[go.Pie(
        # labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=[colors['aqua']]),
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