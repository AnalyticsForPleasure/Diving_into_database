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


    #Let's merge between the 2 dataframe:
    merged_df = consumption_df.merge(cost_df, on='MeterType')
    print('*')

    # Perform the multiplication
    merged_df['TotalCost'] = merged_df['Consumed'] * merged_df['Cost']
    print('*')
    # Display the final DataFrame
    print(merged_df)
    print('*')

    # As we can see from the next 3 rows - we are dealing with duplicates: 7,617,835 --> 7,571,244
    number_of_row_before_remove_duplicate =merged_df.shape[0]
    row_after_remove_duplicate = merged_df.drop_duplicates()
    number_of_row_after_remove_duplicate = row_after_remove_duplicate.shape[0]
    print('*')

    # Get all the negative numbers from the 'column_name' column:
    #negative_numbers = row_after_remove_duplicate[row_after_remove_duplicate['Consumed'] < 0]['Consumed']

    # Here below we are dealing with negative numbers: 7,571,244--> 7,571,100
    clean_data = row_after_remove_duplicate[row_after_remove_duplicate['Consumed'] >= 0]
    print('*')


    # Getting the max value of the 'Consumed' column for 'Water' and 'Electricity' for each  HouseholdId:
    #aggregate_result_max = clean_data.groupby(['Timestamp','HouseholdId', 'MeterType'])['Consumed'].agg(['max'])
    #aggregate_result_max = aggregate_result_max.drop_duplicates()
    #summing_the_all_max_values_of_consumed = aggregate_result_max['max'].sum()
    print('*')

    # My logic thinking here is once a day each households pays 2 bills for the same property: 1) Water 2) electricity.
    # Therefore, we need to check out the households - how  many times each household pays once a day a bill. if he is
    # paying more than twice,  I should discarded.

    counter_payments_for_each_household = clean_data.groupby(['HouseholdId', 'Timestamp'])['Consumed'].agg(['count'])  # Using grouping in order to create a counter for finding the number of bills payed each day.
    counter_payments_for_each_household_sorted = counter_payments_for_each_household.sort_values(by=['count'],ascending=[False])  # As we can see there are many rows more than 2 payments a day. 
    # specific_bills_for_household_1 = specific_bills_for_household_1.
    print('*')


    # Getting the max value of the 'Consumed' column for 'Water' and 'Electricity' for each  HouseholdId:
    aggregate_result_max = clean_data.groupby(['Timestamp', 'HouseholdId', 'MeterType'])['Consumed'].agg(['max'])
    summing_the_all_max_values_of_consumed = aggregate_result_max['max'].sum()
    print('*')
    # https://stackoverflow.com/questions/64721116/pandas-fastest-way-to-group-by-max-and-summing-over-the-group
