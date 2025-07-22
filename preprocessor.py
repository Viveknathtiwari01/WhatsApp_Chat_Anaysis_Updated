
import re

import pandas as pd


def preprocessor(data):
    """
    Preprocess the input data by removing any unwanted characters and converting to lowercase.
    
    Args:
        data (str): The input string to preprocess.
        
    Returns:
        str: The preprocessed string.
    """
    pattern = r"(\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2} [ap]m) - ([^:]+: .+)"
    message = re.split(pattern, data)
    matches = re.findall(pattern, data)
    # unzip the matches into two list
    dates, messages = zip(*matches)

    # convert touple to list
    dates = list(dates)
    messages = list(messages)

    # create dataframe
    df = pd.DataFrame({'user_message':messages, 'message_date':dates})
    # convert message_date type 
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p')
    # rename the column
    df.rename(columns={'message_date':'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:     # user_name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notifications')
            messages.append(entry[0])
                
    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    return df