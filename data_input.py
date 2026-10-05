import pandas as pd

def load_well_data(filepath):
    """
    Reads well logging data from a CSV file.
    """
    try:
        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(filepath)
        print("✅ Data successfully loaded!")
        print("-" * 30)
        print(df.head()) # Shows the first 5 rows
        return df
    except FileNotFoundError:
        print(f"❌ Error: Could not find the file '{filepath}'")
        return None

# Test the loader
if __name__ == "__main__":
    well_data = load_well_data('well_data.csv')