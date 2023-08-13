import pandas as pd
import json
import datetime

# **************************************************************************************************************
# Function  name: extract_dict_to_array
# input: Dealing with the 'Properties' column - This column is written with a json format - I need to extract information
# return value:
# ****************************************************************************************************************
def extract_dict_to_array(given_string):
    # print(given_string)
    output_dict = json.loads(given_string)
    # '{"Origin":"06585714867","Destination":"06535838110","IsHidden":false}'
    if "Origin" in output_dict.keys() and "Destination" in output_dict.keys() and "IsHidden" in output_dict.keys():
        row = pd.Series([output_dict["Origin"], output_dict["Destination"], bool(output_dict["IsHidden"]), ''])
        return row
    elif "DisconnectedBy" in output_dict.keys():
        row = pd.Series(['', '', '', output_dict["DisconnectedBy"]])
        return row
    else:
        print(given_string)
        print("Error")
        exit()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pd.set_option('display.max_rows', 5000)
    phonecalls_df = pd.read_csv('all_logs_challenge3.csv', header=None, nrows=10000)
    # Timestamp:datetime, EventType:string, CallConnectionId:string, Properties:dynamic
    phonecalls_df.columns = ['Timestamp', 'EventType', 'CallConnectionId', 'Properties']
    phonecalls_df['Timestamp'] = pd.to_datetime(phonecalls_df['Timestamp'])

    print(f'number of rows in table:{phonecalls_df.shape[0]:,}')
    print(f'number of columns in table:{phonecalls_df.shape[1]:,}')

    # In the upcoming row, we will be extracting information from the 'Properties' column, which is currently stored
    # in a dictionary format containing four key-value pairs. Each of these keys will be allocated its own distinct column
    phonecalls_df[["Origin", "Destination", "IsHidden", "DisconnectBy"]] = phonecalls_df["Properties"].apply(lambda x: extract_dict_to_array(x))

    # After we extracted the values from the 'Properties' column, we can drop this column.
    phonecalls_df.drop("Properties", axis=1, inplace=True)
    print('*')
    # Let's find out how many phonecalls are connected or disconnected.
    phonecalls_df_connected = phonecalls_df.loc[(phonecalls_df["EventType"] == "Connect")]
    phonecalls_df_disconnected = phonecalls_df.loc[(phonecalls_df["EventType"] == "Disconnect")]

    # In the next step, I am willing to find out the duration of each phonecall. therefore, In order to achive
    # and created another column named 'duration', we need to use the inner join for having 2 Timestamps in the same row.

    res = phonecalls_df_connected.merge(phonecalls_df_disconnected, how="inner", on='CallConnectionId')
    res['duration'] = res["Timestamp_y"] - res["Timestamp_x"] # Time of the end of the call minus starting time of the calls.
    print(res['duration'][0])

    # After we extracted the values from the 'Properties' column, we can drop this column.

    #print(res.columns)

    column_which_are_duplicate =['EventType_y','Origin_y','Destination_y','IsHidden_y','DisconnectBy_y']
    res.drop(column_which_are_duplicate, axis=1, inplace=True)
    print('*')

    # Adding a column named 'short_calls' in order to find fishing calls. I am assuming the duration of
    # the phone call by person how is calling , won't be longer than 2 minutes
    res['short_calls'] = res['duration'].apply(lambda x: x < datetime.timedelta(minutes=2))

    print(res['short_calls'].value_counts())

    groups = phonecalls_df.groupby("CallConnectionId")

    for group_name, mini_df in groups:
        print()

    phonecalls_hidden = phonecalls_df.loc[phonecalls_df["IsHidden"] == True, :]
    phonecalls_disconnected_by_people = phonecalls_df.loc[(phonecalls_df["EventType"] == "Disconnect") &
                                                          (phonecalls_df["DisconnectBy"] == "Destination")]
    print(phonecalls_df["Origin"].value_counts()[:10])

    print('*')
