import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pd.set_option('display.max_rows', 5000)

    # Dealing with the first table of the detective kusto challenge:
    consumption_df = pd.read_csv('/challenge_2/total_log_challenge_2.csv',
                                 header=None)
    print(f'number of rows in table:{consumption_df.shape[0]}')
    print(f'number of rows in table:{consumption_df.shape[1]}')

    consumption_df.columns = ['Timestamp', 'HouseholdId', 'MeterType', 'Consumed']
    consumption_df['Consumed'] = consumption_df['Consumed'].astype(float)
    consumption_df['Timestamp'] = pd.to_datetime(consumption_df['Timestamp'])

    # Dealing with the second table of the detective kusto challenge:
    cost_df = pd.DataFrame(data=[['Water', 'Liter', 0.001562],
                                 ['Electricity', 'kwH', 0.3016]],
                           columns=['MeterType', 'Unit', 'Cost'])

    # Step 1:  Let's find out how many household we have on the dataset
    res = pd.unique(consumption_df['HouseholdId'])
    number_of_HouseholdId = res.shape[0]  # 126,185 households
    # Number of rows need to be over the consumption_df( Before starting to solve the mystery  ) : 2 * 30 * 126,185
    print(f'Number of rows in the consumption_df :  {2 * 30 * number_of_HouseholdId:,}')
    
    # Step 2: Removing duplicates rows by
    consumption_df_after_removing_dup = consumption_df.drop_duplicates()
    print('*')
    
    # Step 3: Let's merge between the 2 dataframe:
    merged_df = consumption_df_after_removing_dup.merge(cost_df, on='MeterType')
    print('*')

    # Step 4: Perform the multiplication
    merged_df['TotalCost'] = merged_df['Consumed'] * merged_df['Cost']
    print('*')

    # Get all the negative numbers from the 'column_name' column:
    # negative_numbers = row_after_remove_duplicate[row_after_remove_duplicate['Consumed'] < 0]['Consumed']

    # Step 5: Here below we are dealing with negative numbers: 7,571,100  --> 7,571,035
    clean_data = merged_df[merged_df['Consumed'] >= 0]

    print(f'Number of row in the "clean_data" - dataframe:{clean_data.shape[0]:,} ')
    print(f'The total cost of all bills is :{clean_data["TotalCost"].sum():,} ')
