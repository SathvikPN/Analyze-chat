import re
from datetime import datetime
import pandas as pd
import numpy as np

from settings import PATTERN
from emojis import EMOJI, DEMOJI

# ---------------------------------------------------------
emoji_pattern = re.compile('|'.join(re.escape(emoji) for emoji in EMOJI))
demoji_pattern = re.compile('|'.join(DEMOJI))

# ---------------------------------------------------------
def get_pattern(key):
    """ Provide regex pattern for datetime, URL """
    re_pattern = PATTERN[key]
    if isinstance(re_pattern, list):
        re_pattern = '^' + '|'.join(re_pattern)
    return re_pattern


def startswith_datetime(line):
    """ Boolean expression - line starts with date time """
    pattern = get_pattern('date-time')
    match = re.match(pattern, line)
    return match == True


def find_author(message):
    """ Returns author(username) of the message.
    
    Returns None if author not detected."""
    patterns = get_pattern('username')
    match = re.match(patterns, message)

    if match:
        author = message.split(': ')[0]
    else:
        author = None
    
    return author


def get_data_tokens(message_line):
    """ Returns data tokens date,time,author,message from a message_line.
    
    message line is identified as the line starting with date_time stamp. 
    WhatsApp generated messages also have date_time stamps.
    WhatsApp generated messages' author will be set to 'None' 
    """
    date_time_stamp, message = message_line.split(' - ', maxsplit=1) 
    date, time = date_time_stamp.split(', ')
    author = find_author(message)

    if author:
        message = message.split(': ', maxsplit=1)[1]
    
    return date, time, author, message


def chat_parser(chat_file):
    """ Feeds parsed chat to pandas dataframe"""
    parsedData = []     # track data to feed dataframe

    with open(chat_file, mode='r', encoding='utf8') as chat:
        message_buffer = []
        date, time, author = None, None, None

        while True:
            line = chat.readline()  # '\n' is also parsed.
            if line:
                line = line.strip()
                if startswith_datetime(line):   # independent message instance
                    if len(message_buffer) > 0: # adds previous msg_tokens to parsedData
                        parsedData.append([date,time,author,' '.join(message_buffer)])

                    message_buffer.clear() # initialise for message in this iteration
                    date, time, author, message = get_data_tokens(message_line=line)
                    message_buffer.append(message)
                    # adds to parsedData only when it confirms that next line is unique message
                    # else keeps in buffer
                else:
                    message_buffer.append(line)
            else:
                # No line imply end of file
                # adds previous msg_tokens to parsedData (last message)
                if len(message_buffer) > 0: 
                    parsedData.append([date,time,author,' '.join(message_buffer)])
                break
    
    # Feed parsed Data to pandas dataframe
    df = pd.DataFrame(parsedData, columns=['Date','Time','Author','Message'])


# -----------------------------------------------------------------------------
def drop_sys_msg(df):
    """ Drops all system generated messages in dataframe """

    drop_msg_count = df['author'].isnull().sum()

    df.dropna(inplace=True)

    print(f"Detected <{drop_msg_count}> system-generated-messages. Dropping off...")

def url_counter(message_line):
    """ Returns the total number of urls detected in the message """
    url_pattern = get_pattern('URL')
    count = len(re.findall(url_pattern, message_line))
    return count

def chat_analyzer(df):
    """ Analyze chat parsed into pandas dataframe """
    
    df['Date'] = pd.to_datetime(df['Date'])

    drop_sys_msg(df)

    messages_count = df.shape[0]
    media_msg_count = df[df['Message'] == '<Media omitted>'].shape[0]

    df['urlcount'] = df.Message.apply(url_counter)

    links_count = df.urlcount.sum()

    # original df remains unaffected. Operations are not inplace.
    media_messages_df = df[df['Message'] == "<Media omitted>"]
    messages_df = df.drop(media_messages_df.index)

    messages_df['Word_count'] = messages_df['Message'].apply(lambda s: len(s.split(' ')))







