## Map functions
import pandas as pd
import plotly.express as px



def normalize_and_classify(df, column):
    """
    Normalize a column by its country-specific range and classify the values.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the data
    column (str): The column name to process

    Returns:
    pd.Series: A Series containing the classification categories
    """
    # Calculate the minimum and maximum values per country
    country_min = df.groupby('Code')[column].transform('min')
    country_max = df.groupby('Code')[column].transform('max')

    # Calculate the range for each country
    country_range = country_max - country_min

    # Create a mask for valid calculations (where we have a meaningful range)
    valid_mask = (country_range > 1e-10) & (~country_range.isna())

    # Initialize classification with None
    classification = pd.Series([None] * len(df), index=df.index)

    # For valid entries, calculate where each value falls in its country's range
    normalized = (df.loc[valid_mask, column] - country_min[valid_mask]) / country_range[valid_mask] * 100

    # Assign classifications based on normalized values
    classification.loc[valid_mask] = normalized.apply(classify_percentage)

    return classification


def classify_disorders(df, columns_to_classify):
    """
    Classify multiple columns into categories 'A', 'B', or 'C' based on
    their position within each country's range of values.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the data
    columns_to_classify (list): List of column names to process

    Returns:
    pd.DataFrame: DataFrame with added classification columns
    """
    # Create a copy to avoid modifying the original DataFrame
    result_df = df.copy()

    for column in columns_to_classify:
        classification_column = f"{column}_classification"
        result_df[classification_column] = normalize_and_classify(result_df, column)

    return result_df


def classify_percentage(percentage):
    """
    Classify a value based on where it falls within its range.

    Parameters:
    percentage (float): The normalized value (0-100) to be classified

    Returns:
    str: Classification category ('A', 'B', or 'C')
    """
    if percentage is None or pd.isna(percentage):
        return None
    elif percentage < 33.33:  # Bottom third of the range
        return 'A'
    elif percentage < 66.67:  # Middle third of the range
        return 'B'
    else:  # Top third of the range
        return 'C'


def create_bivariate_color_mapping(colors):
    return {
        ('A', 'A'): colors[0],
        ('A', 'B'): colors[1],
        ('A', 'C'): colors[2],
        ('B', 'A'): colors[3],
        ('B', 'B'): colors[4],
        ('B', 'C'): colors[5],
        ('C', 'A'): colors[6],
        ('C', 'B'): colors[7],
        ('C', 'C'): colors[8],
    }


def get_color_for_row(row, disorder, factor, color_mapping):
    """
    Get the appropriate color for a row based on its disorder and factor classifications.

    Parameters:
    row (pd.Series): A single row from the DataFrame
    disorder (str): Name of the disorder column
    factor (str): Name of the factor column
    color_mapping (dict): Dictionary mapping classification pairs to colors

    Returns:
    str: Color value from the mapping, or 'gray' if no matching classification
    """
    disorder_class = row[f"{disorder}_classification"]
    factor_class = row[f"{factor}_classification"]
    return color_mapping.get((disorder_class, factor_class), 'gray')


def assign_bivariate_colors(df, disorder, factor, color_mapping):
    """
    Assign colors to each row in the DataFrame based on disorder and factor classifications.

    Parameters:
    df (pd.DataFrame): Input DataFrame with classification columns
    disorder (str): Name of the disorder to use
    factor (str): Name of the factor to use
    color_mapping (dict): Dictionary mapping classification pairs to colors

    Returns:
    pd.DataFrame: DataFrame with added 'color' column
    """
    df['color'] = df.apply(
        get_color_for_row,
        args=(disorder, factor, color_mapping),
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
            'top': 0.4,  # Vertical position of the top right corner (0: bottom, 1: top)
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
        text=f"{conf['legend_x_label']}",
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


def plot_bivariate_map(df, disorder, factor, year, map_colors, highlight_country=None):
    """
    Plot a bivariate choropleth map based on classifications.

    Parameters:
    - df (pd.DataFrame): The DataFrame with classification and color data.
    - disorder (str): The disorder to classify.
    - factor (str): The factor to classify.
    - color_set_name (str): The name of the color set to use (e.g., 'pink-blue').
    - highlight_country (str, optional): ISO-3 country code to highlight

    Returns:
    - go.Figure: The Plotly figure.
    """
    df_year = df[df['Year'] == year].copy()

    # Create a color mapping
    color_mapping = create_bivariate_color_mapping(map_colors)

    # Assign colors to countries
    df = assign_bivariate_colors(df_year, disorder, factor, color_mapping)

    # Create the base choropleth map
    fig = px.choropleth(
        df,
        locations="Code",
        color="color",
        hover_name="Entity",
        hover_data={
            'Entity': False,
            "Code": False

        },
        color_discrete_map="identity"
    )

    # Update the map layout
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="lightgray",
        fitbounds="locations",
        projection=dict(type='equirectangular'),
        visible=False,
        showframe=False
    )

    if highlight_country:
        print(f"highlighted country: {highlight_country}")

        # Create a new trace specifically for the highlighted country
        highlighted_df = df[df['Code'] == highlight_country]

        fig.add_choropleth(
            locations=[highlight_country],
            z=[1],  # Dummy value
            colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],  # Transparent fill
            showscale=False,
            hoverinfo='skip',
            marker=dict(
                line=dict(
                    color='orange',
                    width=2
                )
            )
        )

    fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
    fig.update_layout(showlegend=False)

    # Add the bivariate legend
    add_bivariate_legend(fig, factor.replace('_', ' ').title(), disorder.replace('_', ' ').title(), map_colors)

    return fig

def plot_default_map(df):
    """
    Plot a default choropleth map without any bivariate coloring.

    Parameters:
    - df (pd.DataFrame): The DataFrame with country data.

    Returns:
    - go.Figure: The Plotly figure with default map styling.
    """
    # Add a default color column to ensure all countries are the same color
    df_copy = df.copy()
    df_copy = df_copy[df_copy['Year'] == 1990]
    df_copy['default_color'] = 'lightgray'  # Assign a neutral color

    fig = px.choropleth(
        df_copy,
        locations="Code",  # ISO-3 country codes
        color="default_color",  # Use the default color
        color_discrete_map={'lightgray': 'lightgray'},  # Map lightgray as the color
        hover_data={"Code": True, 'default_color': False},
    )

    #Update the map layout
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="white",  # Set the land to white for a clean background
        projection=dict(type='equirectangular'),
        visible=False,
        showframe=False
    )



    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        showlegend=False,
    )

    return fig
