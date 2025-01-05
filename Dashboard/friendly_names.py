def get_friendly_indicator_text(indicator):
    indicator_name = {
            'gdp': 'the GDP',
            'co2_emissions': 'CO2 emissions',
            'unemployment_rate': 'the unemployment rate',
            'life_expectancy': 'the life expectancy',
            'health_expenditure': 'health expenditure',
    }.get(indicator, indicator)

    return indicator_name

def get_friendly_indicator_title(indicator):
    indicator_name = {
            'gdp': 'GDP',
            'co2_emissions': 'CO2 emissions',
            'unemployment_rate': 'Unemployment rate',
            'life_expectancy': 'Life expectancy',
            'health_expenditure': 'Health expenditure',
    }.get(indicator, indicator)

    return indicator_name

def get_friendly_disorder(disorder):
    return disorder.replace('_', ' ').capitalize()