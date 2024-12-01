import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys


# Function to load factor data (unemployment, GDP, CO2)
def load_factor_data(filename):
    try:
        # Read the CSV with semicolon delimiter
        df = pd.read_csv(filename, delimiter=';')
        
        # Melt the year columns into rows
        year_columns = [col for col in df.columns if col.isdigit()]  # Get columns that are years
        id_vars = ['Country Name', 'Country Code']
        
        melted_df = df.melt(
            id_vars=id_vars,
            value_vars=year_columns,
            var_name='Year',
            value_name='Value'
        )
        
        # Convert Year to integer
        melted_df['Year'] = pd.to_numeric(melted_df['Year'])
        
        return melted_df
        
    except Exception as e:
        print(f"Error loading {filename}: {str(e)}")
        print("First few lines of the file:")
        with open(filename, 'r') as f:
            print(f.readline())
            print(f.readline())
        sys.exit(1)
# Function to load mental health data
def load_mental_health_data(filename):
    try:
        return pd.read_csv(filename)
    except Exception as e:
        print(f"Error loading {filename}: {str(e)}")
        sys.exit(1)

# Load datasets
print("Loading datasets...")
mental_health = pd.read_csv('mental_health.csv')
unemployment = load_factor_data('unemployment_rate.csv')
gdp = load_factor_data('gdp.csv')
co2 = load_factor_data('co2_emissions.csv')

# Print data info for debugging
print("\nDataset shapes:")
print(f"Mental Health: {mental_health.shape}")
print(f"Unemployment: {unemployment.shape}")
print(f"GDP: {gdp.shape}")
print(f"CO2: {co2.shape}")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    # Main container
    html.Div([
        # Left content area (90% width)
        html.Div([
            # Timeline slider
            html.Div([
                dcc.Slider(
                    id='year-slider',
                    min=mental_health['Year'].min(),
                    max=mental_health['Year'].max(),
                    value=mental_health['Year'].min(),
                    marks={str(year): str(year) for year in mental_health['Year'].unique()},
                    step=None
                )
            ], style={'padding': '20px'}),
            
            # Map container
            html.Div([
                dcc.Graph(id='world-map')
            ])
        ], style={'width': '90%', 'display': 'inline-block'}),
        
        # Sidebar (10% width)
        html.Div([
            html.H3('Filters', style={'textAlign': 'center'}),
            
            # Mental Illness Dropdown
            html.Div([
                html.Label('Mental Illness'),
                dcc.Dropdown(
                    id='mental-illness-dropdown',
                    options=[
                        {'label': col.replace('_', ' ').title(), 'value': col}
                        for col in mental_health.columns 
                        if col not in ['Entity', 'Code', 'Year']
                    ],
                    value='schizophrenia'
                )
            ], style={'padding': '10px'}),
            
            # Factors Dropdown
            html.Div([
                html.Label('Factors'),
                dcc.Dropdown(
                    id='factors-dropdown',
                    options=[
                        {'label': 'Unemployment Rate', 'value': 'unemployment'},
                        {'label': 'GDP', 'value': 'gdp'},
                        {'label': 'CO2 Emissions', 'value': 'co2'}
                    ],
                    value='unemployment'
                )
            ], style={'padding': '10px'})
        ], style={
            'width': '10%',
            'display': 'inline-block',
            'vertical-align': 'top',
            'position': 'fixed',
            'right': '0',
            'height': '100vh',
            'backgroundColor': '#f8f9fa',
            'padding': '20px',
            'borderLeft': '1px solid #dee2e6'
        })
    ])
])

# Callback to update the map
@app.callback(
    Output('world-map', 'figure'),
    [Input('year-slider', 'value'),
     Input('mental-illness-dropdown', 'value'),
     Input('factors-dropdown', 'value')]
)

def update_map(selected_year, mental_illness, factor):
    try:
        # Filter mental health data for selected year
        mh_data = mental_health[mental_health['Year'] == selected_year]
        
        # Get factor data for selected year
        if factor == 'unemployment':
            factor_data = unemployment
        elif factor == 'gdp':
            factor_data = gdp
        else:
            factor_data = co2
            
        # Filter factor data for selected year
        factor_data = factor_data[factor_data['Year'] == selected_year]
        
        # Merge the datasets
        merged_data = mh_data.merge(
            factor_data,
            left_on=['Code', 'Year'],
            right_on=['Country Code', 'Year'],
            how='left'
        )
        
        # Create bivariate choropleth
        fig = px.choropleth(
            merged_data,
            locations='Code',
            color=mental_illness,
            hover_name='Entity',
            hover_data={
                mental_illness: ':.2f',
                'Value': ':.2f',
            },
            color_continuous_scale=[
                [0, 'rgb(220,220,220)'],  # Light grey for missing data
                [0.01, 'rgb(145,191,219)'],  # Light blue
                [0.5, 'rgb(69,117,180)'],  # Medium blue
                [1, 'rgb(33,102,172)']  # Dark blue
            ],
            title=f'{mental_illness.replace("_", " ").title()} vs {factor} ({selected_year})'
        )
        
        # Update layout
        fig.update_layout(
            margin={"r": 0, "t": 30, "l": 0, "b": 0},
            height=600,
            geo=dict(showframe=False, showcoastlines=True),
            # Update color axis to handle missing values
            coloraxis_showscale=True,
            coloraxis_colorbar=dict(
                title=mental_illness.replace('_', ' ').title(),
                tickformat='.2f'
            )
        )
        
        # Update hover template to show "No data" for missing values
        fig.update_traces(
            hovertemplate=(
                '<b>%{hovertext}</b><br>' +
                f'{mental_illness.replace("_", " ").title()}: ' + 
                '%{customdata[0]:.2f}<br>' +
                f'{factor.title()}: ' + 
                '%{customdata[1]:.2f}<br>' +
                '<extra></extra>'
            ).replace('nan', 'No data')
        )
        
        return fig
    except Exception as e:
        print(f"Error updating map: {str(e)}")
        return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)