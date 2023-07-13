import pandas as pd

class Pandas_Cleaner:
    def __init__(self,filtered_data):
        #self.json_file_filtered = json_file_filtered
        self.filtered_data = filtered_data

    def load_pandas(self):
        #self.df_from_json = pd.read_json(self.json_file_filtered)
        self.df = pd.DataFrame(self.filtered_data)
        pd.set_option('display.max_columns', None)
        print(self.df)
        return self.df

    def nan_check_pandas(self):
        # Check if there are any NaN values in each column
        has_nan = self.df.isna().any()

        # Get a list of columns with NaN values
        columns_with_nan = has_nan[has_nan].index.tolist()
        print("columns with NaN: ", columns_with_nan)

    def number_duplicates(self):
        print("Number of duplicates: ", self.df.duplicated().sum())

