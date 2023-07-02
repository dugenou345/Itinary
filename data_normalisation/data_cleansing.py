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
        df = pd.read_json(self.json_file)
        df.head(2)
        print(df)

        # Supposons que vous ayez un DataFrame appelé df
        #columns_with_lists = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, list)).any()]
        #print("colonnes avec listes:", columns_with_lists)
        return df


    def flatten_list(self,df,column_name):
        self.df = df
        self.column_name = column_name
        self.df[self.column_name] = self.df[[self.column_name]].apply(lambda x: self.flatten_list_nested_two(x) if np.any(pd.notnull(x)) else x, axis=1)
        return self.df[self.column_name]

    def flatten_list_nested_two(self,list):
        self.list = list
        flattened_list = str([value for sublist in self.list for val in sublist for value in val])
        self.list = flattened_list
        return self.list

    def concat_string(self,df,column_name):
        self.df = df
        self.column_name = column_name
        #self.df[self.column_name] = self.df[[self.column_name]].apply(lambda x: self.prim_concat_string(x) if np.any(pd.notnull(x)) else x, axis=1)
        self.df[self.column_name] = self.df[[self.column_name]].apply(lambda x: [value for sublist in x for value in sublist] if np.any(pd.notnull(x)) else x, axis=1)
        #self.df[self.column_name] = self.df[[self.column_name]].apply(lambda x: ','.join(map(str, x)) if np.any(pd.notnull(x)) else x, axis=1)

        return self.df[self.column_name]

    def prim_concat_string(self,list):
        self.list = list
        concat_list = str([value for sublist in self.list])
        self.list = concat_list
        #self.list = [','.join(map(str, l)) for l in self.list if np.any(pd.notnull(l)) else l for l in self.list]
        #self.list = [','.join(map(str, l)) for l in self.list if np.any(pd.notnull(l)) else l for l in self.list]
        #self.list = [','.join(map(str, l)) for l in self.list]
        #self.list = [map(str, l) for l in self.list]
        return self.list
"""
    # Recursive function to remove empty nested list
    def remove_multiple_bracket(self,df):
        self.df = df
        # Remove empty inner brackets from 'col1'
        #df['department'] = df['department'].apply(lambda x: re.sub(r"\[\[.*?\]\]\]", "", str(x)))
        #df = df.apply(lambda x: re.sub(r"\[\[.*?\]\]\]", "", str(x)))
        return self.df

    def parse_value(self,value):
        # Check if the value is a string
        self.value = value
        if isinstance(value, list):
            self.value = str(self.value)
            # Remove brackets and whitespaces
            self.value = re.sub(r'\[\[.*?\]\]\]\s', '', self.value)
        return self.value
        
"""