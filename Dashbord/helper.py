import pandas as pd

def convert_to_year_rows(df):    

    df_copy = df.copy()
    df_long = pd.melt(
        df_copy,
        id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
        var_name='Year',
        value_name='Value'
    )

    df_long['Year'] = pd.to_numeric(df_long['Year'])

    return df_long  

def remove_nan_values(df, column_name):
    if column_name not in df.columns:
        raise ValueError(f'Column {column_name} not in given dataframe')
    df_cp = df.copy()
    df_cp = df_cp[df_cp[column_name].notna()]
    return df_cp



