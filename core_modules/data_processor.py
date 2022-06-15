from typing import Type
import pandas as pd
import pathlib
import os


base_path = pathlib.Path(__file__).parent.resolve()

class DataProcessor:

    def __init__(self, *, df: Type[pd.DataFrame]=None) -> None:
        self.df = df

    def get_unique_df(self) -> Type[pd.DataFrame]:
        return self.df.drop_duplicates(subset ="lead_id", keep='first')

    def do_onehot_encoding(self, col_name) -> Type[pd.DataFrame]:
        # do onehot encoding on column
        one_hot = pd.get_dummies(self.df[col_name], drop_first=True, prefix=col_name)
        # drop original column as it is now encoded
        self.df = self.df.drop(col_name, axis=1)
        # join the encoded df
        self.df = self.df.join(one_hot)
        return self.df

    def update_df(self, df: Type[pd.DataFrame]):
        self.df = df

    def get_column_analysis(self, df: Type[pd.DataFrame], col_name: str, col_values: list) -> Type[pd.DataFrame]:
        """
        params:

        df -- pandas dataframe containing data
        col_name -- str -- column's name that we need to analyze
        col_values -- lsit -- unique columns values
        
        returns:
        pandas.Dataframe of columns: []
        """

        high_quality_ratio_per_value_dict = {
            'column unique values': col_values,
            'total qualified leads': [],
            'total leads generated': [],    # (TOTAL) qualified + unqualified
            'qualified_leads_ratio_per_column_value': [],
        }

        for col_value in col_values:
            filtered_df = df[df[col_name] == col_value]
            qualified_leads_ratio = 0.0
            number_of_qualified_leads_per_value = 0
            if len(filtered_df):
                try:
                    number_of_qualified_leads_per_value = filtered_df['low_qualified'].value_counts()[0]
                    qualified_leads_ratio = number_of_qualified_leads_per_value / len(filtered_df)
                except:
                    pass
        
            high_quality_ratio_per_value_dict['total qualified leads'].append(number_of_qualified_leads_per_value)
            high_quality_ratio_per_value_dict['total leads generated'].append(len(filtered_df))
            high_quality_ratio_per_value_dict['qualified_leads_ratio_per_column_value'].append(qualified_leads_ratio)
            
        return pd.DataFrame(high_quality_ratio_per_value_dict)

    
    def prepare_data(self):

        # original_data = pd.read_csv(os.path.join(base_path, 'nawy_dataset.csv'))

        cols_to_drop = [col for col in self.df.columns if 'Unnamed' in col]
        self.df.drop(columns=cols_to_drop, inplace=True)

        # parse timestamps in the lead_time column properly

        if 'lead_time' in self.df.keys():
            self.df['lead_time'] = pd.to_datetime(self.df['lead_time'], errors='coerce')
            self.df.dropna(subset=['lead_time'], inplace=True)
            self.df['lead_time'] = self.df['lead_time'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S")) 

            self.df['lead_time'] = pd.to_datetime(self.df['lead_time'])

            self.df.insert(5, 'month', self.df['lead_time'].dt.month)
            self.df.insert(6, 'year', self.df['lead_time'].dt.year)

        if 'low_qualified' in self.df.keys():
            print(self.df['low_qualified'].value_counts())
            self.df['low_qualified'] = self.df['low_qualified'].astype('int64')

        cols = ['lead_source', 'method_of_contact']
        for col_name in cols:
            if col_name in self.df.keys():
                ambigious = ['Unknown', 'None', 'Localhost', 'Test', 'Unkown']
                ambigious_combinations = []
                for word in ambigious:
                    ambigious_combinations.append(word)
                    ambigious_combinations.append(f'({word})')
                    ambigious_combinations.append(word.lower())
                    ambigious_combinations.append(f'({word.lower()})')

                self.df.loc[(self.df[col_name].str.contains('what')) | (self.df[col_name].str.contains('whast')), col_name] = 'whatsapp'
                self.df.loc[self.df[col_name] == 'youtube.com', col_name] = 'youtube'
                self.df.loc[self.df[col_name].str.contains('linkedin'), col_name] = 'linkedin'
                self.df.loc[self.df[col_name].str.contains('telegram'), col_name] = 'telegram'
                self.df.loc[self.df[col_name].str.contains('|'.join(ambigious_combinations)), col_name] = 'unknown'

                personal_methods = [method for method in self.df[col_name].unique()  if ('personal' in method or 'referral' in method or 'client' in method)]# and 'instagram' not in method and 'page' not in method]
                self.df.loc[self.df[col_name].isin(personal_methods), col_name] = 'personal'

                exceptions = ['fb', 'comment', 'message', 'message']
                facebook_methods = [method for method in self.df[col_name].unique() if 'facebook' in method and not any(x in method for x in exceptions)]
                self.df.loc[self.df[col_name].isin(facebook_methods), col_name] = 'facebook'

                call_methods = [method for method in self.df[col_name].unique() if 'call' in method or 'sms' in method or 'phone' in method or 'hotline' in method]
                self.df.loc[self.df[col_name].isin(call_methods), col_name] = 'call'

                self.df.loc[self.df[col_name].isin(['resale form', 'custom form', 'form src=newsletter', 'sahel_map_form', 'type form']), col_name] = 'form'
                
                search_engines = ['google', 'yahoo', 'ecosia',  'bing', 'duckduckgo']
                for search_engine in search_engines:
                    self.df.loc[self.df[col_name].str.contains(search_engine), col_name] = search_engine

                websites_identifiers = ['com', 'net', 'org', 'io']
                websites_identifiers_all = []
                for identifier in websites_identifiers:
                    websites_identifiers_all.append('.'+identifier)
                    websites_identifiers_all.append(identifier+'.')

                websites_methods = [method for method in self.df[col_name].unique() if any(x in method for x in websites_identifiers_all)]
                websites_methods.extend(['propertyfinder', 'criteo', 'newsletter', 'blog', 'social buildingz campaign'])

                unique_df = self.get_unique_df()

                websites_analysis_df = self.get_column_analysis(unique_df, col_name, websites_methods)

                low_quality_websites = []
                for idx, row in websites_analysis_df.iterrows():
                    if row['total leads generated'] < 5 or row['qualified_leads_ratio_per_column_value'] < 0.70:
                        low_quality_websites.append(row['column unique values'])

                self.df.loc[self.df[col_name].isin(low_quality_websites), col_name] = 'miscellaneous'

        self.df.drop(columns=['lead_id', 'customer_name', 'message', 'lead_time', 'ad_group', 'campaign', 'location'], inplace=True, errors='ignore')

        cols_need_onehot_encoding = ['lead_mobile_network', 'method_of_contact', 'lead_source']
        for col in cols_need_onehot_encoding:
            self.df = self.do_onehot_encoding(col)

        return self.df
            