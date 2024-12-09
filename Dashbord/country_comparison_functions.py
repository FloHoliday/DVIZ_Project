import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from dash import html

from dis_ind_functions import get_friendly_disorder, get_friendly_indicator

def get_default_comparison_graph(colors):
    """Returns a default empty comparison graph with instructions"""
    fig = go.Figure()
    fig.add_annotation(
        text="Select two countries and a disorder/indicator to compare",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color="#666")
    )
    fig.update_layout(
        height=400,
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(t=30, b=30, l=30, r=30)
    )
    return fig

def format_dropdown_options(unique_countries):
    """
    Format dropdown options with label, value, and search fields
    
    Parameters:
    unique_countries (pandas.DataFrame): DataFrame containing Entity and Code columns
    
    Returns:
    list: Formatted dropdown options for Dash
    """
    options = []
    for _, row in unique_countries.iterrows():
        if pd.notna(row['Code']):  # Check if code is not NaN
            two_letter_code = three_to_two_letter_code(row['Code'])
            if two_letter_code:  # Only add if we have a valid country code
                options.append({
                    'label': html.Div([
                        html.Img(
                            src=f'https://flagcdn.com/w20/{two_letter_code.lower()}.png',
                            style={
                                'height': '12px',
                                'margin-right': '10px'
                            }
                        ),
                        html.Span(row['Entity'])
                    ], style={'display': 'flex', 'align-items': 'center'}),
                    'value': row['Code'],
                    'search': row['Entity']  # Add the country name as a search term
                })
    return sorted(options, key=lambda x: str(x['search']))


def create_country_comparison(df, country_code1, country_code2, disorder, indicator, country_dict, colors):
    """Creates a comparison graph showing trends for two selected countries"""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Filter data for each country
    country1_data = df[df['Code'] == country_code1].sort_values('Year')
    country2_data = df[df['Code'] == country_code2].sort_values('Year')
    
    # Add traces for both countries
    for country_data, country_code, line_color, dash_color in [
        (country1_data, country_code1, colors['blue'], colors['dense_pink']),
        (country2_data, country_code2, colors['midlbue'], colors['green'])
    ]:
        indicator_name = get_friendly_indicator(indicator)
        disorder_name = get_friendly_disorder(disorder)

        # Add disorder trace
        fig.add_trace(
            go.Scatter(
                x=country_data['Year'],
                y=country_data[disorder],
                name=f"{country_dict[country_code]} - {disorder_name}",
                line=dict(color=line_color),
            ),
            secondary_y=False,
        )
        
        # Add indicator trace
        fig.add_trace(
            go.Scatter(
                x=country_data['Year'],
                y=country_data[indicator],
                name=f"{country_dict[country_code]} - {indicator_name}",
                line=dict(color=dash_color, dash='dash'),
            ),
            secondary_y=True,
        )
    
    # Update layout
    fig.update_layout(
        title=f"Comparison: {disorder_name} vs {indicator_name}",
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update axes
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='#f0f0f0',
        title_text=disorder.replace('_', ' ').title(), 
        secondary_y=False
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='#f0f0f0',
        title_text=indicator.replace('_', ' ').title(), 
        secondary_y=True
    )
    
    return fig

def three_to_two_letter_code(code):
    country_codes = {
        "AFG": "af", "ALB": "al", "DZA": "dz", "AND": "ad", "AGO": "ao",
        "ARG": "ar", "ARM": "am", "AUS": "au", "AUT": "at", "AZE": "az",
        "BHR": "bh", "BGD": "bd", "BRB": "bb", "BLR": "by", "BEL": "be",
        "BLZ": "bz", "BEN": "bj", "BTN": "bt", "BOL": "bo", "BIH": "ba",
        "BWA": "bw", "BRA": "br", "BRN": "bn", "BGR": "bg", "BFA": "bf",
        "BDI": "bi", "KHM": "kh", "CMR": "cm", "CAN": "ca", "CPV": "cv",
        "CAF": "cf", "TCD": "td", "CHL": "cl", "CHN": "cn", "COL": "co",
        "COM": "km", "COG": "cg", "CRI": "cr", "HRV": "hr", "CUB": "cu",
        "CYP": "cy", "CZE": "cz", "DNK": "dk", "DJI": "dj", "DOM": "do",
        "ECU": "ec", "EGY": "eg", "SLV": "sv", "GNQ": "gq", "ERI": "er",
        "EST": "ee", "ETH": "et", "FJI": "fj", "FIN": "fi", "FRA": "fr",
        "GAB": "ga", "GMB": "gm", "GEO": "ge", "DEU": "de", "GHA": "gh",
        "GRC": "gr", "GTM": "gt", "GIN": "gn", "GUY": "gy", "HTI": "ht",
        "HND": "hn", "HUN": "hu", "ISL": "is", "IND": "in", "IDN": "id",
        "IRN": "ir", "IRQ": "iq", "IRL": "ie", "ISR": "il", "ITA": "it",
        "JAM": "jm", "JPN": "jp", "JOR": "jo", "KAZ": "kz", "KEN": "ke",
        "KIR": "ki", "PRK": "kp", "KOR": "kr", "KWT": "kw", "KGZ": "kg",
        "LAO": "la", "LVA": "lv", "LBN": "lb", "LSO": "ls", "LBR": "lr",
        "LBY": "ly", "LIE": "li", "LTU": "lt", "LUX": "lu", "MDG": "mg",
        "MWI": "mw", "MYS": "my", "MDV": "mv", "MLI": "ml", "MLT": "mt",
        "MRT": "mr", "MUS": "mu", "MEX": "mx", "MDA": "md", "MCO": "mc",
        "MNG": "mn", "MNE": "me", "MAR": "ma", "MOZ": "mz", "MMR": "mm",
        "NAM": "na", "NRU": "nr", "NPL": "np", "NLD": "nl", "NZL": "nz",
        "NIC": "ni", "NER": "ne", "NGA": "ng", "NOR": "no", "OMN": "om",
        "PAK": "pk", "PLW": "pw", "PAN": "pa", "PNG": "pg", "PRY": "py",
        "PER": "pe", "PHL": "ph", "POL": "pl", "PRT": "pt", "QAT": "qa",
        "ROU": "ro", "RUS": "ru", "RWA": "rw", "KNA": "kn", "LCA": "lc",
        "VCT": "vc", "WSM": "ws", "SMR": "sm", "STP": "st", "SAU": "sa",
        "SEN": "sn", "SRB": "rs", "SYC": "sc", "SLE": "sl", "SGP": "sg",
        "SVK": "sk", "SVN": "si", "SLB": "sb", "SOM": "so", "ZAF": "za",
        "ESP": "es", "LKA": "lk", "SDN": "sd", "SUR": "sr", "SWZ": "sz",
        "SWE": "se", "CHE": "ch", "SYR": "sy", "TKL": "TK", "TWN": "tw", 
        "TJK": "tj", "TZA": "tz", "THA": "th", "TLS": "tl", "TGO": "tg", 
        "TON": "to", "TTO": "tt", "TUN": "tn", "TUR": "tr", "TKM": "tm", 
        "TUV": "tv", "UGA": "ug", "UKR": "ua", "ARE": "ae", "GBR": "gb", 
        "USA": "us", "URY": "uy", "UZB": "uz", "VUT": "vu", "VEN": "ve",
        "VNM": "vn", "YEM": "ye", "ZMB": "zm", "ZWE": "zw", "VIR": "vi"
    }
    
    return country_codes.get(code.upper(), None)

