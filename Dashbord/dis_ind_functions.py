def get_friendly_indicator(indicator):
    indicator_name = {
            'GDP': 'the GDP',
            'co2_emissions': 'CO2 emissions',
            'unemployment_rate': 'the unemployment rate'
    }.get(indicator, indicator)

    return indicator_name

def get_friendly_disorder(disorder):
    return disorder.replace('_', ' ').title()