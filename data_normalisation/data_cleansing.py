import pandas as pd
from decorators import progress_bar
import re
import itertools
import numpy as np
from urllib import request

class Json_Pandas_Cleaner:
    def __init__(self,json_file):
        self.json_file = json_file

    @progress_bar
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
        """
        flattened_values = list(itertools.chain.from_iterable(x if np.any(pd.notnull(x)) else [np.nan] for x in self.df[self.column_name]))
        self.df[self.column_name] = flattened_values
        return list(itertools.chain.from_iterable(self.df[self.column_name]))
"""
        #self.df[self.column_name] = [val for sub_sublist in self.df[self.column_name] for sublist in sub_sublist for val in sublist]
        #self.df[self.column_name] = [val for sublist in self.df[self.column_name] for val in sublist]
        #df1 = pd.DataFrame
        self.df[self.column_name] = self.df[[self.column_name]].apply(lambda x: self.flatten_two_nested(x) if np.any(pd.notnull(x)) else x, axis=1)
        #self.df[self.column_name] = self.df[[self.column_name]].apply(lambda x: str([value for sublist in x for val in sublist for value in val]) if np.any(pd.notnull(x)) else x, axis=1)
        return self.df[self.column_name]

    def flatten_two_nested(self,list):
        self.list = list
        #df = pd.DataFrame()
        flattened_list = str([value for sublist in self.list for val in sublist for value in val])
        #df['label'] = flattened_list
        #return df['label']
        self.list = flattened_list
        #self.list = [val for sublist in self.list for val in sublist]
        #self.list = [val for sublist in self.df[self.column_name] for val in sublist]
        return self.list



#    def list_to_string(self,df,column_name):
#       self.df = df
#        self.column_name = column_name
#        #self.df[self.column_name] = self.df[[self.column_name]].apply(lambda x: self.prim_list_to_string(x) if np.any(pd.notnull(x)) else x, axis=1)
#       return self.df[self.column_name]

#    def prim_list_to_string(self,list):
 #       self.list = list
#        #self.list = [','.join(map(str, l)) for l in self.list]
  #      return self.list

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
        """
        else:
            # Convert the list to a string
            self.value = str(self.value)
            # Remove brackets and whitespace from the string
            self.value = re.sub(r'\[\[.*?\]\]\]\s', '', self.value)
        # Return the parsed value
        """
        return self.value
""""
        new_rows = []
        for _, row in df.iterrows():
            for col in columns_with_lists:
                for item in row[col]:
                    new_row = row.copy()
                    new_row[col] = item
                    new_rows.append(new_row)

        new_df = pd.DataFrame(new_rows)


      
        # Vérifier les doublons en fonction de toutes les colonnes du DataFrame
        duplicates = df[df.duplicated()]

        # Afficher les doublons
        print(duplicates)
        """""