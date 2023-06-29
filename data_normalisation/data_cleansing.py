import pandas as pd
from decorators import progress_bar
import re
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

    # Recursive function to remove empty nested lists
    def remove_multiple_bracket(self,df):
        self.df = df
        # Remove empty inner brackets from 'col1'
        #df['department'] = df['department'].apply(lambda x: re.sub(r"\[\[.*?\]\]\]", "", str(x)))
        df = df.apply(lambda x: re.sub(r"\[\[.*?\]\]\]", "", str(x)))
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