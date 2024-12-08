import numpy as np
from scipy import stats

def get_default_corr_expl(colors):
    return "—", {'font-size': '48px', 'margin': '0', 'font-weight': 'bold', 'color': colors['neutral']}, \
               "Select data to analyze", \
               {'height': '100%', 'width': '0%', 'background-color': colors['neutral']}, \
               "No data", \
               "Please select a country, disorder, and indicator to see the correlation analysis."
               
    
def get_corr_expl(mh_data, country_code, disorder, indicator, colors):           
    # Filter data for selected country
    country_data = mh_data[mh_data['Code'] == country_code].copy()
    country_name = mh_data[mh_data['Code'] == country_code]['Entity'].iloc[0]

    # Calculate correlation
    x = country_data[disorder].values
    y = country_data[indicator].values
    
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

    return [
        f"{correlation:.2f}",  # Correlation value
        {'font-size': '48px', 'margin': '0', 'font-weight': 'bold', 'color': color},  # Value style
        f"{strength} {direction.title()} Correlation",  # Label
        {'height': '100%', 'width': f'{abs_corr * 100}%', 'background-color': color, 'transition': 'all 0.5s ease-in-out'},  # Strength bar
        strength,  # Strength label
        interpretation  # Interpretation text
    ]