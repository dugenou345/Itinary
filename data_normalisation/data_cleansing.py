import pandas as pd
from decorators import progress_bar
import re
import itertools
import numpy as np
from urllib import request

class Json_Pandas_Cleaner:
    def __init__(self,json_file):
        self.json_file = json_file

    def load_pandas(self):
        self.df = pd.read_json(self.json_file)
        self.df.head(2)
        print(self.df)
        return self.df

    def nan_check_pandas(self):
        # Check if there are any NaN values in each column
        has_nan = self.df.isna().any()

        # Get a list of columns with NaN values
        columns_with_nan = has_nan[has_nan].index.tolist()
        print("columns with NaN: ", columns_with_nan)

