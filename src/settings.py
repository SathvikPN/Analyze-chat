from log.Reference.settings import PATTERN


APP_NAME = 'Analyze-chat'

COPYRIGHT = 'Copyright \U000000A9 Sathvik PN'

SOURCE_CODE_URL = 'https://github.com/SathvikPN/Analyze-chat'

CONTACT_LINKEDIN = 'https://www.linkedin.com/in/sathvik-p-n/'

PATTERN = {
    'date-time': '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -',
    'URL': '(?:(?:(?:https|http|ftp):\/\/(?:www\.)?)|(?:www\.))((?:[\w\-_]+?\.)?(?:[\w\-_]+?\.)?[\w\-_]+?\.\w+)\S*',
    'username': [
        '([\w]+):',                     # First_name (1+ alphanumeric characters)
        '([\w]+)[\s]+([\w]+):',         # fname lname
        '([\w]+[\s]+[\w]+[\s]+[\w]+):', # fname Mname lname
        '([+]\d{2} \d{5} \d{5}):',      # mobile number (India)
    ]
}