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
    







