import pandas as pd
import sys
import matplotlib.pyplot as plt 

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

event_id_description = {
    4624: "Successful account log on",
    4625: "Failed account log on",
    4634: "An account logged off",
    4648: "A logon attempt was made with explicit credentials",
    4719: "System audit policy was changed",
    4964: "A special group has been assigned to a new log on",
    1102: "Audit log was cleared. This can relate to a potential attack",
    4720: "A user account was created",
    4722: "A user account was enabled",
    4723: "An attempt was made to change the password of an account",
    4725: "A user account was disabled",
    4728: "A user was added to a privileged global group",
    4732: "A user was added to a privileged local group",
    4756: "A user was added to a privileged universal group",
    4738: "A user account was changed",
    4740: "A user account was locked out",
    4767: "A user account was unlocked",
    4735: "A privileged local group was modified",
    4737: "A privileged global group was modified",
    4755: "A privileged universal group was modified",
    4772: "A Kerberos authentication ticket request failed",
    4777: "The domain controller failed to validate the credentials of an account",
    4782: "Password hash an account was accessed",
    4616: "System time was changed",
    4657: "A registry value was changed",
    4697: "An attempt was made to install a service",
    4698: "Events related to Windows scheduled tasks being created",
    4699: "Events related to Windows scheduled tasks being modified",
    4700: "Events related to Windows scheduled tasks being deleted",
    4701: "Events related to Windows scheduled tasks being enabled",
    4702: "Events related to Windows scheduled tasks being disabled",
    4946: "A rule was added to the Windows Firewall exception list",
    4947: "A rule was modified in the Windows Firewall exception list",
    4950: "A setting was changed in Windows Firewall",
    4954: "Group Policy settings for Windows Firewall has changed",
    5025: "The Windows Firewall service has been stopped",
    5031: "Windows Firewall blocked an application from accepting incoming traffic",
    5152: "A network packet was blocked by Windows Filtering Platform",
    5153: "A network packet was blocked by Windows Filtering Platform",
    5155: "Windows Filtering Platform blocked an application or service from listening on a port",
    5157: "Windows Filtering Platform blocked a connection",
    5447: "A Windows Filtering Platform filter was changed",
}
    
def filter_event_ids(df):
    suspicious_ids = [4624, 4625, 4634,
                      4648, 4719, 4964,
                      1102, 4720, 4722,
                      4723, 4725, 4728,
                      4732, 4756, 4738,
                      4740, 4767, 4735,
                      4737, 4755, 4772,
                      4777, 4782, 4616,
                      4657, 4697, 4698,
                      4699, 4700, 4701,
                      4702, 4946, 4947,
                      4950, 4954, 5025,
                      5031, 5152, 5153,
                      5155, 5157, 5447]
    # filter dataframe on specified event ids.....modify ids as needed
    filtered_df = df[df['EventID'].isin(suspicious_ids)]
    return filtered_df

def main():
    if len(sys.argv) < 3:
        print("Usage: python program_name.py <input_csv_file> <output_csv_file>")
        sys.exit(1)
    elif ',' in sys.argv[1] or ',' in sys.argv[2]:
        print("Error: Please provide only one input and one output .csv file.")
        sys.exit(1)

    input_csv_file = sys.argv[1]
    output_csv_file = sys.argv[2]
    df = ingest_csv(input_csv_file)
    if df is not None:
        print("CSV file ingested successfully.")
        # Filter events with EventIDs listed in filtered_df
        filtered_df = filter_event_ids(df)
        if not filtered_df.empty:
            print("Rows for specified Event IDs:")
            print(filtered_df)
            # List event ids of interest and their description at top of output file
            with open(output_csv_file, 'w') as f:
                f.write("Event ID,Description\n")
                for event_id, meaning in event_id_description.items():
                    f.write(f"{event_id},{meaning}\n")
                f.write("\n")  # Add a blank line before writing the filtered data
            # Append the filtered results to the output file
            filtered_df.to_csv(output_csv_file, mode='a', index=False)
            print(f"Filtered results saved to '{output_csv_file}'.")
            
            # Plotting the pie chart
            plt.figure(figsize=(8, 8))
            event_counts = filtered_df['EventID'].value_counts()
            plt.pie(event_counts, labels=event_counts.index, autopct='%1.1f%%')
            plt.title('Event ID Distribution')
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.tight_layout()
            plt.savefig("suspicious_event_ids.png")  # Save the plot as an image
            plt.close()
            print("Pie chart showing distribution of Event IDs saved as 'event_id_distribution.png'.")
        else:
            print("No rows found for specified Event IDs.")

if __name__ == "__main__":
    main()