import pandas as pd
import numpy as np
#import dataframe_image as dfi

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    pd.set_option('display.max_rows', 5000)

    # Dealing with the first table of the detective kusto challenge:
    consumption_df = pd.read_csv('/home/shay_diy/PycharmProjects/kusto_database_tasks/challenge_2/total_log.csv', header=None)
    print(f'number of rows in table:{consumption_df.shape[0]}')
    print(f'number of rows in table:{consumption_df.shape[1]}')

    consumption_df.columns = ['Timestamp','HouseholdId','MeterType','Consumed']
    consumption_df['Consumed'] = consumption_df['Consumed'].astype(float)
    consumption_df['Timestamp'] = pd.to_datetime(consumption_df['Timestamp'])

    print('*')
    # Dealing with the second table of the detective kusto challenge:
    cost_df = pd.DataFrame(data = [['Water','Liter',0.001562],
                                   ['Electricity', 'kwH',0.3016]],
                           columns=['MeterType','Unit','Cost'])
    print('*')


    # Working on the "consumption_df" dataset:
    # Let's find out how many household we have on the dataset
    res = pd.unique(consumption_df['HouseholdId'])
    number_of_HouseholdId = res.shape[0] # 126,185 households

    # Number each of householdid :
    counting_number_of_each_household = consumption_df['HouseholdId'].value_counts() # We have a range of households between 60 to 103
    print('*')

    # Let's find the average consumption for each household in the df:
    consumption_df.groupby(['MeterType'])['Consumed'].sum() # ['MeterType', 'Consumed'].sum()
    aggregate_result = consumption_df.groupby(['HouseholdId', 'MeterType'])['Consumed'].agg(['mean', 'sum']).head(20)
    print('*')

    specific_bills_for_household = consumption_df.loc[consumption_df['HouseholdId'] == 'DTI624E9689E1F73D62', :]
    specific_bills_for_household_2 = consumption_df.loc[consumption_df['HouseholdId'] == 'DTI6F2EB46AD6AE2597', :]
    specific_bills_for_household_times = specific_bills_for_household.shape[0] # This specific household pays 30 over the month of april 30 times a bill
                                                                               # for Electricity & Water.
    print('*')

    # Let's merge between the 2 dataframe:
    merged_df = consumption_df.merge(cost_df, on='MeterType')
    print('*')

    # Adding the "Total cost" column
    merged_df['TotalCost'] = merged_df['Consumed'] * merged_df['Cost']
    print('*')
