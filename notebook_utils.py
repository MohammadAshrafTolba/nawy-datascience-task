import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


def change_width(ax, new_value: float) :
    # initialx = 0
    for patch in ax.patches :
        current_width = patch.get_width()
        diff = current_width - new_value

        # change the bar width
        patch.set_width(new_value)

        # recenter the bar
        patch.set_x(patch.get_x() + diff*.5)
        
        # ax.text(patch.get_height(), initialx+patch.get_width()/8, '{:1.0f}'.format(patch.get_width()))
        # initialx += 1

def get_alpha_values(column):
    scaler = MinMaxScaler()
    alphas = scaler.fit_transform(np.flip(column.values.reshape(-1,1)))
    alphas_ret = []
    for value in np.flip(alphas)[:, 0]:
        if value <= 0.2:
            value += 0.2
        elif value == 1.0:
            value -= 0.1
        alphas_ret.append(value)
    # alphas = [value + 0.2 if value <= 0.2 else value for value in np.flip(alphas)[:, 0]]
    return alphas_ret

def get_column_participation_in_high_quality(df, col_name, col_values: list):
    """
    
    returns:
    pandas.Dataframe of columns: []
    """
    # valid_mobile_networks = list(df['lead_mobile_network'].unique())
    high_quality_ratio_per_value_dict = {
        'column unique values': col_values,
        'total qualified leads': [],
        'total leads generated': [],    # qualified + unqualified
        'qualified_leads_ratio_per_column_value': [],
    }
    # total_qualified_leads_number = df['low_qualified'].value_counts()[0]
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

def print_column_value_counts(df, column: str):
    for lead_source, freq in df[column].value_counts().iteritems():
        print(f'{lead_source} - {freq}')

def split_channels(portfolio):
    '''
    INPUTS:
    
    portfolio: dataframe to do operation on
    
    RETURNS:
    
    portfolio: dataframe after splitting channels
    
    '''
    
    # get channels values
    channels_set = set()
    for i in portfolio.channels:
        channels_set.update(set(i))

    # split the channel into different attribute
    for i in channels_set:
        portfolio[i] = portfolio.channels.apply(lambda x: i in x).map({True:1, False: 0})
    
    # drop the channels column as we don't need it anymore
    portfolio.drop('channels', axis=1, inplace=True)
    
    return portfolio   # return the data