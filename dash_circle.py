from dash import Dash, html, dcc
import plotly.graph_objects as go
import pandas as pd

# Initialize the Dash app
app = Dash(__name__)

# Variables for selection
selected_year = 2002
selected_country = 'CHE'

# Read and filter data
df = pd.read_csv('mental_health.csv', delimiter=";")

# Define the columns and labels
mental_health_columns = ['schizophrenia', 'depressive_disorder',
                        'anxiety_disorders', 'bipolar_disorders',
                        'eating_disorders']
labels = [col.replace('_', ' ').title() for col in mental_health_columns]

# Filter data
filtered_df = df[(df['Code'] == selected_country) & (df['Year'] == selected_year)]

# Extract values for pie chart
values = filtered_df[mental_health_columns].values.flatten()

# Create the donut chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.4,
    textinfo='label+percent',
    textposition='outside',
    texttemplate='%{label}<br>%{percent:.1%}',
    marker=dict(colors=['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'])
)])

# Update layout
country_name = df[df['Code'] == selected_country]['Entity'].iloc[0]
fig.update_layout(
    title={
        'text': f"Mental Health Distribution - {country_name} ({selected_year})",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    width=800,
    height=600,
    margin=dict(t=100, b=100, l=50, r=50)
)

# Define the app layout
app.layout = html.Div([
    html.Div([
        dcc.Graph(figure=fig)
    ])
], style={'padding': '20px'})

if __name__ == '__main__':
    app.run_server(debug=True)