import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from dash import html

import friendly_names as fn

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
        margin=dict(t=30, b=30, l=30, r=30),
        xaxis=dict(showticklabels=False),  
        yaxis=dict(showticklabels=False) 
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
    country1_data[indicator] = (country1_data[indicator] - country1_data[indicator].min()) / (country1_data[indicator].max() - country1_data[indicator].min())
    country1_data[disorder] = (country1_data[disorder] - country1_data[disorder].min()) / (country1_data[disorder].max() - country1_data[disorder].min())
    country2_data[indicator] = (country2_data[indicator] - country2_data[indicator].min()) / (country2_data[indicator].max() - country2_data[indicator].min())
    country2_data[disorder] = (country2_data[disorder] - country2_data[disorder].min()) / (country2_data[disorder].max() - country2_data[disorder].min())
    
    # Add traces for both countries
    for country_data, country_code, line_color, dash_color in [
        (country1_data, country_code1, colors['aqua'], colors['aqua']),
        (country2_data, country_code2, colors['blush-pink'], colors['blush-pink'])
    ]:
        indicator_name = fn.get_friendly_indicator_title(indicator)
        disorder_name = fn.get_friendly_disorder(disorder)

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
        secondary_y=False,
        showticklabels=False
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='#f0f0f0',
        secondary_y=True,
        showticklabels=False
    )
    return fig

def three_to_two_letter_code(code):

    #249 elements
    country_codes = {
        'AFG': 'af', 'ALB': 'al', 'DZA': 'dz', 'ASM': 'as', 'AND': 'ad', 'AGO': 'ao', 'AIA': 'ai', 'ATA': 'aq', 
        'ATG': 'ag', 'ARG': 'ar', 'ARM': 'am', 'ABW': 'aw', 'AUS': 'au', 'AUT': 'at', 'AZE': 'az', 'BHS': 'bs', 
        'BHR': 'bh', 'BGD': 'bd', 'BRB': 'bb', 'BLR': 'by', 'BEL': 'be', 'BLZ': 'bz', 'BEN': 'bj', 'BMU': 'bm', 
        'BTN': 'bt', 'BOL': 'bo', 'BES': 'bq', 'BIH': 'ba', 'BWA': 'bw', 'BVT': 'bv', 'BRA': 'br', 'IOT': 'io', 
        'BRN': 'bn', 'BGR': 'bg', 'BFA': 'bf', 'BDI': 'bi', 'CPV': 'cv', 'KHM': 'kh', 'CMR': 'cm', 'CAN': 'ca', 
        'CYM': 'ky', 'CAF': 'cf', 'TCD': 'td', 'CHL': 'cl', 'CHN': 'cn', 'CXR': 'cx', 'CCK': 'cc', 'COL': 'co', 
        'COM': 'km', 'COD': 'cd', 'COG': 'cg', 'COK': 'ck', 'CRI': 'cr', 'HRV': 'hr', 'CUB': 'cu', 'CUW': 'cw', 
        'CYP': 'cy', 'CZE': 'cz', 'CIV': 'ci', 'DNK': 'dk', 'DJI': 'dj', 'DMA': 'dm', 'DOM': 'do', 'ECU': 'ec', 
        'EGY': 'eg', 'SLV': 'sv', 'GNQ': 'gq', 'ERI': 'er', 'EST': 'ee', 'SWZ': 'sz', 'ETH': 'et', 'FLK': 'fk', 
        'FRO': 'fo', 'FJI': 'fj', 'FIN': 'fi', 'FRA': 'fr', 'GUF': 'gf', 'PYF': 'pf', 'ATF': 'tf', 'GAB': 'ga', 
        'GMB': 'gm', 'GEO': 'ge', 'DEU': 'de', 'GHA': 'gh', 'GIB': 'gi', 'GRC': 'gr', 'GRL': 'gl', 'GRD': 'gd', 
        'GLP': 'gp', 'GUM': 'gu', 'GTM': 'gt', 'GGY': 'gg', 'GIN': 'gn', 'GNB': 'gw', 'GUY': 'gy', 'HTI': 'ht', 
        'HMD': 'hm', 'VAT': 'va', 'HND': 'hn', 'HKG': 'hk', 'HUN': 'hu', 'ISL': 'is', 'IND': 'in', 'IDN': 'id', 
        'IRN': 'ir', 'IRQ': 'iq', 'IRL': 'ie', 'IMN': 'im', 'ISR': 'il', 'ITA': 'it', 'JAM': 'jm', 'JPN': 'jp', 
        'JEY': 'je', 'JOR': 'jo', 'KAZ': 'kz', 'KEN': 'ke', 'KIR': 'ki', 'PRK': 'kp', 'KOR': 'kr', 'KWT': 'kw', 
        'KGZ': 'kg', 'LAO': 'la', 'LVA': 'lv', 'LBN': 'lb', 'LSO': 'ls', 'LBR': 'lr', 'LBY': 'ly', 'LIE': 'li', 
        'LTU': 'lt', 'LUX': 'lu', 'MAC': 'mo', 'MDG': 'mg', 'MWI': 'mw', 'MYS': 'my', 'MDV': 'mv', 'MLI': 'ml', 
        'MLT': 'mt', 'MHL': 'mh', 'MTQ': 'mq', 'MRT': 'mr', 'MUS': 'mu', 'MYT': 'yt', 'MEX': 'mx', 'FSM': 'fm', 
        'MDA': 'md', 'MCO': 'mc', 'MNG': 'mn', 'MNE': 'me', 'MSR': 'ms', 'MAR': 'ma', 'MOZ': 'mz', 'MMR': 'mm', 
        'NAM': 'na', 'NRU': 'nr', 'NPL': 'np', 'NLD': 'nl', 'NCL': 'nc', 'NZL': 'nz', 'NIC': 'ni', 'NER': 'ne', 
        'NGA': 'ng', 'NIU': 'nu', 'NFK': 'nf', 'MNP': 'mp', 'NOR': 'no', 'OMN': 'om', 'PAK': 'pk', 'PLW': 'pw', 
        'PSE': 'ps', 'PAN': 'pa', 'PNG': 'pg', 'PRY': 'py', 'PER': 'pe', 'PHL': 'ph', 'PCN': 'pn', 'POL': 'pl', 
        'PRT': 'pt', 'PRI': 'pr', 'QAT': 'qa', 'MKD': 'mk', 'ROU': 'ro', 'RUS': 'ru', 'RWA': 'rw', 'REU': 're', 
        'BLM': 'bl', 'SHN': 'sh', 'KNA': 'kn', 'LCA': 'lc', 'MAF': 'mf', 'SPM': 'pm', 'VCT': 'vc', 'WSM': 'ws', 
        'SMR': 'sm', 'STP': 'st', 'SAU': 'sa', 'SEN': 'sn', 'SRB': 'rs', 'SYC': 'sc', 'SLE': 'sl', 'SGP': 'sg', 
        'SXM': 'sx', 'SVK': 'sk', 'SVN': 'si', 'SLB': 'sb', 'SOM': 'so', 'ZAF': 'za', 'SGS': 'gs', 'SSD': 'ss', 
        'ESP': 'es', 'LKA': 'lk', 'SDN': 'sd', 'SUR': 'sr', 'SJM': 'sj', 'SWE': 'se', 'CHE': 'ch', 'SYR': 'sy', 
        'TWN': 'tw', 'TJK': 'tj', 'TZA': 'tz', 'THA': 'th', 'TLS': 'tl', 'TGO': 'tg', 'TKL': 'tk', 'TON': 'to', 
        'TTO': 'tt', 'TUN': 'tn', 'TUR': 'tr', 'TKM': 'tm', 'TCA': 'tc', 'TUV': 'tv', 'UGA': 'ug', 'UKR': 'ua', 
        'ARE': 'ae', 'GBR': 'gb', 'UMI': 'um', 'USA': 'us', 'URY': 'uy', 'UZB': 'uz', 'VUT': 'vu', 'VEN': 've', 
        'VNM': 'vn', 'VGB': 'vg', 'VIR': 'vi', 'WLF': 'wf', 'ESH': 'eh', 'YEM': 'ye', 'ZMB': 'zm', 'ZWE': 'zw', 
        'ALA': 'ax'
    }
    return country_codes.get(code.upper(), None)

