## Map functions
import pandas as pd
import plotly.express as px

def classify_disorders(df, disorders_factors):
    """
    Classify the values of multiple disorders into categories 'A', 'B', or 'C' based on their percentage.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    disorders (list): A list of disorder column names to process.

    Returns:
    None: The function directly modifies the given DataFrame.
    """
    # Create a copy of the DataFrame to avoid SettingWithCopyWarning
    df_copy = df.copy()

    for disorder in disorders_factors:
        classification_column = f"{disorder}_classification"
        max_value = df_copy[disorder].max()

        # Use .loc to safely assign values to a new column
        df.loc[:, classification_column] = df_copy[disorder].apply(
            lambda x: classify_percentage((x / max_value) * 100 if pd.notna(x) else None)
        )
    
    return df

def classify_percentage(percentage):
    """
    Classify a given percentage into one of three categories: 'A', 'B', or 'C'.

    Parameters:
    percentage (float): The input percentage to be classified.

    Returns:
    str: A single character representing the classification ('A', 'B', or 'C').
    """
    if percentage is None:  # Handle NaN values
        return None
    elif percentage < 100 / 3:
        return 'A'
    elif percentage < 100 * 2 / 3:
        return 'B'
    else:
        return 'C'


def get_map_color_sets():
    color_sets = {
        'pink-blue':   ['#e8e8e8', '#ace4e4', '#5ac8c8', '#dfb0d6', '#a5add3', '#5698b9', '#be64ac', '#8c62aa', '#3b4994'],
        'teal-red':    ['#e8e8e8', '#e4acac', '#c85a5a', '#b0d5df', '#ad9ea5', '#985356', '#64acbe', '#627f8c', '#574249'],
        'blue-organe': ['#fef1e4', '#fab186', '#f3742d',  '#97d0e7', '#b0988c', '#ab5f37', '#18aee5', '#407b8f', '#5c473d']
    }
    return color_sets


def create_bivariate_color_mapping(colors):
    return {
        ('A', 'A'): colors[0],  # Bottom-left
        ('B', 'A'): colors[1],  # Middle-left
        ('C', 'A'): colors[2],  # Top-left
        ('A', 'B'): colors[3],  # Bottom-center
        ('B', 'B'): colors[4],  # Center
        ('C', 'B'): colors[5],  # Top-center
        ('A', 'C'): colors[6],  # Bottom-right
        ('B', 'C'): colors[7],  # Middle-right
        ('C', 'C'): colors[8],  # Top-right
    }
    
    
def assign_bivariate_colors(df, disorder, factor, color_mapping):
    df['color'] = df.apply(
        lambda row: color_mapping.get(
            (row[f"{disorder}_classification"], row[f"{factor}_classification"]),
            'gray'  # Default color if classification is missing
        ),
        axis=1
    )
    return df


def add_bivariate_legend(fig, x_legend, y_legend, colors, conf=None):
    """
    Add a bivariate choropleth coddlor legend to a Plotly figure.

    Parameters:
    - fig (plotly.graph_objects.Figure): The Plotly figure to which the legend will be added.
    - colors (list): A list of 9 colors representing the bivariate legend. The colors should be ordered from low-low to high-high.
    - conf (dict, optional): Configuration dictionary for legend customization. Defaults are used if not provided.

    Returns:
    - fig (plotly.graph_objects.Figure): The updated Plotly figure with the legend added.
    """
    # Use default configuration if none is provided
    if conf is None:
        conf = {
            'top': 0.3,  # Vertical position of the top right corner (0: bottom, 1: top)
            'right': 0.2,  # Horizontal position of the top right corner (0: left, 1: right)
            'box_w': 0.04,  # Width of each rectangle
            'box_h': 0.08,  # Height of each rectangle
            'line_color': 'rgba(0,0,0,0)',  # Transparent borders
            'line_width': 0,  # Width of the rectangle borders
            'legend_x_label': f'{x_legend}'+  '→',  # Label for the x-axis
            'legend_y_label': f'{y_legend}' '→',  # Label for the y-axis
            'legend_font_size': 14,  # Font size for the legend text
            'legend_font_color': '#000',  # Font color for the legend text
        }

    # Reverse the order of colors for correct display
    legend_colors = colors[:]
    legend_colors.reverse()

    # Calculate coordinates for all nine rectangles
    coord = []
    width = conf['box_w']
    height = conf['box_h']

    for row in range(1, 4):  # 3 rows
        for col in range(1, 4):  # 3 columns
            coord.append({
                'x0': round(conf['right'] - (col - 1) * width, 4),
                'y0': round(conf['top'] - (row - 1) * height, 4),
                'x1': round(conf['right'] - col * width, 4),
                'y1': round(conf['top'] - row * height, 4)
            })

    # Create rectangles and add to the figure
    for i, value in enumerate(coord):
        fig.add_shape(
            type='rect',
            x0=value['x0'], y0=value['y0'], x1=value['x1'], y1=value['y1'],
            xref='paper', yref='paper',
            fillcolor=legend_colors[i],
            line=dict(
                color=conf['line_color'],
                width=conf['line_width']
            )
        )

    # Add x-axis legend label
    fig.add_annotation(
        x=coord[8]['x1'], y=coord[8]['y1'],  #position
        xref='paper', yref='paper',
        showarrow=False,
        text=f"{conf['legend_x_label']} 🠒",
        font=dict(
            size=conf['legend_font_size'],
            color=conf['legend_font_color']
        ),
        xanchor='left', yanchor='top',
        borderpad=0
    )

    # Add y-axis legend label
    fig.add_annotation(
        x=coord[8]['x1'], y=coord[8]['y1'],  #position
        xref='paper', yref='paper',
        showarrow=False,
        text=f"{conf['legend_y_label']}",
        font=dict(
            size=conf['legend_font_size'],
            color=conf['legend_font_color']
        ),
        textangle=270,
        xanchor='right', yanchor='bottom',
        borderpad=0
    )

    return fig

def plot_bivariate_map(df, disorder, factor, year, color_set_name):
    df_year = df[df['Year'] == year]
    
    # Select the color set and create color mapping (previous code remains the same)
    color_sets = get_map_color_sets()
    colors = color_sets[color_set_name]
    color_mapping = create_bivariate_color_mapping(colors)
    df_year = assign_bivariate_colors(df_year, disorder, factor, color_mapping)

    # Create the choropleth map
    fig = px.choropleth(
        df_year,
        locations="Code",
        color="color",
        custom_data=["Entity"],
        title=f"Bivariate Map of {disorder.replace('_', ' ').title()} and {factor.replace('_', ' ').title()}",
        color_discrete_map="identity"
    )

    # Update hover template (previous code remains the same)
    fig.update_traces(
        hovertemplate='<b>%{customdata[0]}</b><extra></extra>',
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_color="black",
            font_family="Open Sans",
            bordercolor='#d3d3d3',
            namelength=0
        )
    )

    # Update the geo layout to fill the container
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="lightgray",
        showcountries=True,
        countrycolor="Black",
        fitbounds="locations",  # This ensures the map fits the container
        visible=True,
        projection=dict(
            type='equirectangular',
        ),
    )

    # Update layout settings
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        height=500,  # Set a fixed height
        geo=dict(
            scope='world',
            showframe=False,
            projection_type='equirectangular',
            # Set the bounds to show the entire world without extra space
            lonaxis=dict(
                range=[-180, 180],
                showgrid=False
            ),
            lataxis=dict(
                range=[-60, 85],  # Adjusted to avoid stretching at poles
                showgrid=False
            )
        ),
        # Configure the modebar
        modebar=dict(
            orientation='v',
            remove=[
                'pan',
                'lasso2d',
                'select2d',
                'autoScale2d',
            ]
        )
    )

    add_bivariate_legend(fig, factor.replace('_', ' ').title(), disorder.replace('_', ' ').title(), colors)

    # Add configuration to control zoom behavior
    fig.update_layout(
        dragmode='zoom',
        clickmode='event+select'
    )

    return fig


