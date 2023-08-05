import pandas as pd
import numpy as np

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