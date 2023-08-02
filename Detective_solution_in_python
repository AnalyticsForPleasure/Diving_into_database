import numpy as np
import pandas as pd

# In this function we removed the curly brackets from the value number.
def get_bounty(input_str):
    res = input_str.split(':')[1]
    res = int(res[:-1])
    return res


if __name__ == '__main__':
    pd.set_option('display.max_rows', 500)  # To see all rows
    pd.set_option('display.max_columns', 500)  # To see all columns
    pd.set_option('display.width', 1000)

    df = pd.read_csv(r"data/log_all.csv", header=None)
    df.columns = ["date", "case_status", "detective_id", "case_id", "bounty_dict"]
    df['date'] = pd.to_datetime(df['date']) # Changing the column named 'date' format from DatetimeArray to differnt format using to_datetime in pandas
    print('*')
    number_of_rows =df.shape[0]
    print('*')


    #print(df.iloc[:50, :])

    print(np.unique(df["case_status"]))

    # First step - Dealing with the bounty_table
    all_case_opened = df.loc[df["case_status"] == "CaseOpened", :]
    all_case_opened["bounty"] = all_case_opened["bounty_dict"].apply(lambda x: get_bounty(x)) # adding another column by removing the curly brakets.
    all_case_opened.sort_values(by=["bounty"], ascending=False,inplace=True)
    all_case_opened.reset_index(drop=True, inplace=True)
    print('*')

    # Second step - Dealing with the detective_table
    all_case_solved = df.loc[df["case_status"] == "CaseSolved", :]
    all_case_solved.reset_index(drop=True, inplace=True)
    all_case_solved.drop("bounty_dict", axis=1, inplace=True) # Removing the 'bounty_dict' column
    all_case_solved.sort_values(by=["date", "detective_id"], ascending=[True, True])
    print('*')
    # the row below is a important row which we used the groupby & first together - The 'first()' returns the first row of each group.
    # The row with the smallest index within each group. This essentially extracts the earliest record for each unique 'case_id'.
    solved_first = all_case_solved.groupby('case_id').first().reset_index()
    solved_first = solved_first.sort_values(by=["date", "detective_id"], ascending=[True, True]) # everything is working until here
    print('*')

    single_detective = solved_first.loc[solved_first['detective_id'] == 'kvc13cf8063ec5941cc1f3', :]
    print('*')
    # Inner join
    res_df = pd.merge(all_case_opened, solved_first, on='case_id', how='inner')
    res_df = res_df.sort_values(by=['detective_id_y'], ascending=False)
    res_df = res_df.sort_values(by=['detective_id_y'], ascending=False).head(100)
    #, inplace=True)
    print('*')
    #res_df =res_df['detective_id_y'].value_counts()


    solved_first = res_df.groupby('detective_id_y')['bounty'].agg('sum').reset_index() # after joining the two tables we have the same column names with X and Y
    #solved_first.sort_values(['bounty'], ascending=False, inplace=True)
    solved_first.sort_values(['bounty'], ascending=False, inplace=True)

    print("#" * 50)
    print(f'{solved_first.iloc[0, :]}')
    print("#" * 50)

    # 3 first places for the detective_id :
    # 1) kvc12a22e9e9e65c1694f1  -> bounty : 385704
    # 2) kvc61fOb891ee26195970a
    # 3) kvc33c12db9f71d2d4866c

    # Last - kvc6583091bd8c2c0a0078

