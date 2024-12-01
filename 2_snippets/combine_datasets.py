import pandas as pd

def reshape_dataset(file_path, value_name):
    """Reshape dataset from wide (years as columns) to long format."""
    # Read CSV with semicolon delimiter
    df = pd.read_csv(file_path, sep=';')
    
    # Identify year columns
    year_columns = [col for col in df.columns if str(col).isnumeric() and 1960 <= int(col) <= 2023]
    
    # Melt the dataframe to convert years from columns to rows
    melted = pd.melt(
        df,
        id_vars=['Country Code'],
        value_vars=year_columns,
        var_name='Year',
        value_name=value_name
    )
    
    # Convert Year to integer
    melted['Year'] = melted['Year'].astype(int)
    return melted

try:
    # Read the main dataset with semicolon separator
    print("Reading mental health dataset...")
    mental_health = pd.read_csv('mental_health.csv', sep=';')

    # Process and merge unemployment data
    print("Processing unemployment data...")
    unemployment = reshape_dataset('unemployment_rate.csv', 'unemployment_rate')
    mental_health = pd.merge(
        mental_health,
        unemployment,
        left_on=['Code', 'Year'],
        right_on=['Country Code', 'Year'],
        how='left'
    )

    # Process and merge CO2 emissions data
    print("Processing CO2 emissions data...")
    co2 = reshape_dataset('co2_emissions.csv', 'co2_emissions')
    mental_health = pd.merge(
        mental_health,
        co2,
        left_on=['Code', 'Year'],
        right_on=['Country Code', 'Year'],
        how='left'
    )

    # Process and merge GDP data
    print("Processing GDP data...")
    gdp = reshape_dataset('gdp.csv', 'gdp')
    mental_health = pd.merge(
        mental_health,
        gdp,
        left_on=['Code', 'Year'],
        right_on=['Country Code', 'Year'],
        how='left'
    )

    # Clean up duplicate Country Code columns
    columns_to_drop = [col for col in mental_health.columns if col.endswith('Country Code')]
    mental_health = mental_health.drop(columns=columns_to_drop)

    # Save the merged dataset
    print("Saving combined dataset...")
    mental_health.to_csv('mental_health_combined.csv', index=False, sep=';')
    print("Done! Combined dataset saved as 'mental_health_combined.csv'")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    import traceback
    print(traceback.format_exc())