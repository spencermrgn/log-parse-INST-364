import pandas as pd

def ingest_csv(csv_file):
    # Read the CSV file into a pandas DataFrame
    try:
        df = pd.read_csv(csv_file)
        return df
    except FileNotFoundError:
        print(f"Error: {csv_file} not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: {csv_file} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: Unable to parse {csv_file}.")
        return None