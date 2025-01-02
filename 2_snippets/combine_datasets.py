# We wrote this script to combine the mental health dataset with the additional datasets containing the indicators.
# The script reads the mental health dataset and all additional datasets in the current directory.
# It reshapes each additional dataset from wide format to long format and merges it with the mental health dataset.
# The final combined dataset is saved as 'mental_health_combined.csv' in the current directory.

# Import required libraries
import os  # For file system operations
import pandas as pd  # For data manipulation and analysis

def reshape_dataset(file_path, value_name):
    """
    Reshape dataset from wide format (years as columns) to long format.
    
    Args:
        file_path (str): Path to the CSV file
        value_name (str): Name for the value column in the reshaped dataset
    
    Returns:
        pandas.DataFrame: Reshaped dataset in long format
    """
    # Read CSV file using semicolon as delimiter
    df = pd.read_csv(file_path, sep=';')
   
    # Create list of year columns between 1990-2023
    # Filters columns that are numeric and within the year range
    year_columns = [col for col in df.columns if str(col).isnumeric() and 1990 <= int(col) <= 2023]
   
    # Convert wide format to long format using pd.melt
    # This transforms year columns into rows
    melted = pd.melt(
        df,
        id_vars=['Country Code'],  # Column(s) to keep as identifier
        value_vars=year_columns,   # Columns to convert into rows
        var_name='Year',          # Name for the new column containing years
        value_name=value_name     # Name for the new column containing values
    )
   
    # Convert Year column to integer type for proper sorting and merging
    melted['Year'] = melted['Year'].astype(int)
    return melted

try:
    # Read the primary mental health dataset
    print("Reading mental health dataset...")
    mental_health = pd.read_csv('mental_health.csv', sep=';')
    
    # List all files in current directory
    print(os.listdir())
   
    # Get list of all CSV files except the main mental health dataset
    csv_files = [f for f in os.listdir() if f.endswith('.csv') and f != 'mental_health.csv']
    
    # Process each additional CSV file
    for csv_file in csv_files:
        # Extract feature name from filename by removing .csv extension
        feature_name = csv_file.replace('.csv', '')
        print(f"Processing {feature_name} data...")
       
        # Reshape the current dataset and merge with main dataset
        data = reshape_dataset(csv_file, feature_name)
        mental_health = pd.merge(
            mental_health,
            data,
            left_on=['Code', 'Year'],          # Columns to merge on from left dataset
            right_on=['Country Code', 'Year'],  # Columns to merge on from right dataset
            how='left',                         # Keep all rows from left dataset
            suffixes=('', '_drop')              # Add '_drop' suffix to duplicate columns
        )
    
    # Remove duplicate columns created during merge (those with '_drop' suffix)
    columns_to_drop = [col for col in mental_health.columns if col.endswith('_drop')]
    mental_health = mental_health.drop(columns=columns_to_drop)
    
    # Remove redundant Country Code columns from merged datasets
    columns_to_drop = [col for col in mental_health.columns if col.endswith('Country Code')]
    mental_health = mental_health.drop(columns=columns_to_drop)
    
    # Save the final combined dataset to CSV
    print("Saving combined dataset...")
    mental_health.to_csv('mental_health_combined.csv', index=False, sep=';')
    print("Done! Combined dataset saved as 'mental_health_combined.csv'")

except Exception as e:
    # Error handling: Print both the error message and full traceback
    print(f"An error occurred: {str(e)}")
    import traceback
    print(traceback.format_exc())