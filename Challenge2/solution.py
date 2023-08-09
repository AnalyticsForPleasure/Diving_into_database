import pandas as pd
import numpy as np
#import dataframe_image as dfi

########################################################################################################################
###################################################### Given Hints #####################################################
# Hint number 1 : What can explain double billing for some of the customers?
# Hint number 2 : Check the "Train Me" section - It has references to 'summarize' operator that can help dealing with it
# Hint number 3 : There might be more than one issues with the data. Perhaps, there are some records that just don't make
#                  any sense and should be discarded all together.
########################################################################################################################


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

    #Let's merge between the 2 dataframe:
    merged_df = consumption_df.merge(cost_df, on='MeterType')
    print('*')

    # Perform the multiplication
    merged_df['TotalCost'] = merged_df['Consumed'] * merged_df['Cost']
    print('*')
    # Display the final DataFrame
    print(merged_df)

    # Let's calculate the "totalcost" of the entire column ( All meterType together )
    sum_of_total_cost =merged_df['TotalCost'].sum()
    print('*')

    # Let's now calculate the "totalcost" of the entire column by separating the category between 'Electricity' vs 'Water':

    separating_the_costs = merged_df.groupby(['MeterType'])['TotalCost'].agg(['sum'])
    print('*')

    # My logic thinking here is once a day each households pays 2 bills for the same property: 1) Water 2) electricity.
    # Therefore, we need to check out the households how  many times each household pays once a day a bill. if he is
    # paying more than twice, it doesn't make any sense. ( using Hint number 1 + 3 ) 
    
    counter_payments_for_each_household = consumption_df.groupby(['HouseholdId', 'Timestamp'])['Consumed'].agg(['count']) # Using grouping in order to create a counter for finding the number of bills payed each day.
    counter_payments_for_each_household_sorted = counter_payments_for_each_household.sort_values(by=['count'], ascending=[False]) # As we can see there are many rows more than 2 payments a day. #TODO continue from here
    print('*')

    # Number of payment each day during the april month:
    counting_number_of_payments_each_day_over_the_month = merged_df['Timestamp'].value_counts()
    print('*')

    merged_df
    # In the next line I want to calculate the sum of water and electricity for each household in each day of April month
    result = merged_df.groupby(['MeterType','HouseholdId', 'Timestamp'])['TotalCost'].agg(['sum'])
    print('*')

    sorted_result = result.sort_values(by=["MeterType", "Timestamp"], ascending=[True, True])
    print('*')

    #solved_first = all_case_solved.groupby('case_id').first().reset_index()
