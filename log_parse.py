import pandas as pd
import sys

def ingest_csv(csv_file):
    #Read the CSV file into a pandas DataFrame
    try:
        df = pd.read_csv(csv_file)
        return df
    #Present error message if .csv does not exist
    except FileNotFoundError:
        print(f"Error: {csv_file} not found.")
        return None
    #Present error if .csv has no data
    except pd.errors.EmptyDataError:
        print(f"Error: {csv_file} is empty.")
        return None
    #Present error if .csv fails to parse provided data
    except pd.errors.ParserError:
        print(f"Error: Unable to parse {csv_file}.")
        return None
    
def filter_event_ids(df):
    #filter dataframe on specified event ids.....modify ids as needed
    filtered_df = df[df['EventID'].isin([4742, 5136])]
    return filtered_df

def main():
    if len(sys.argv) != 2:
        print("Usage: python program_name.py <csv_file>")
        sys.exit(1)
    elif ',' in sys.argv[1]:
        print("Error: Please provide only one .csv file.")
        sys.exit(1)

    csv_file = sys.argv[1]
    df = ingest_csv(csv_file)
    if df is not None:
        print(".csv file ingested successfully.")
        # Filter events with EventID 4742 or 5136
        filtered_df = filter_events(df)
        if not filtered_df.empty:
            print("Rows for specified Event IDs:")
            print(filtered_df)
        else:
            print("No rows found for specified Event IDs.")

if __name__ == "__main__":
    main()
