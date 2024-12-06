import pandas as pd

def convert_to_year_rows(df):    
    df_copy = df.copy()
    
    # Check which columns exist in the DataFrame
    standard_columns = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
    existing_columns = [col for col in standard_columns if col in df_copy.columns]
    
    # Get year columns (assuming they're numeric or can be converted to numeric)
    year_columns = [col for col in df_copy.columns if col not in standard_columns]
    
    # Perform melt operation with only existing columns
    df_long = pd.melt(
        df_copy,
        id_vars=existing_columns,
        value_vars=year_columns,
        var_name='Year',
        value_name='Value'
    )
    
    # Convert Year to numeric, coercing errors to NaN
    df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
    
    return df_long

def remove_nan_values(df, column_name):
    if column_name not in df.columns:
        raise ValueError(f'Column {column_name} not in given dataframe')
    df_cp = df.copy()
    df_cp = df_cp[df_cp[column_name].notna()]
    return df_cp