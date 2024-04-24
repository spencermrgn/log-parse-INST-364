import pandas as pd

def ingest_csv(csv_file):
    # Read the CSV file into a pandas DataFrame
    try:
        df = pd.read_csv(csv_file)
        return df
     # Present error message if .csv does not exist
    except FileNotFoundError:
        print(f"Error: {csv_file} not found.")
        return None
    # Present error if .csv has no data
    except pd.errors.EmptyDataError:
        print(f"Error: {csv_file} is empty.")
        return None
    # Present error if .csv fails to parse provided data
    except pd.errors.ParserError:
        print(f"Error: Unable to parse {csv_file}.")
        return None
    
def filter_event_ids(df):
    # filter dataframe on specified event ids.....modify ids as needed
    filtered_df = df[df['EventID'].isin([4742, 5136])]
    return filtered_df