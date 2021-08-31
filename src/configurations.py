RE_LINK = '(?:(?:(?:https|http|ftp):\/\/(?:www\.)?)|(?:www\.))((?:[\w\-_]+?\.)?(?:[\w\-_]+?\.)?[\w\-_]+?\.\w+)\S*'

LANGUAGE = {
    'en': {
        'language': 'English',
        'date': '%m/%d/%y, %H:%M',
        'media': 'Media omitted',
        'you': 'You',
        'and': 'and',
        'location': 'live location shared',
        'location2': 'location',
        'contact': 'file attached',
        'deleted': 'This message was deleted',
        'deleted2': 'You deleted this message',
        'events_encripted': 'Messages to this group are now secured with end-to-end encryption.',
        'events_encripted2': 'Messages to this chat and calls are now secured with end-to-end encryption.',
        'event_changed_phone': 'changed their phone number to a new number.',
        'event_changed_phone2': 'changed to',
        'event_admin': "You're now an admin",
        'event_create': 'created group',
        'event_subject': 'changed the subject from',
        'event_icon': "changed this group's icon",
        'event_add': 'added',
        'event_add2': 'added',
        'event_left': 'left'}
}

# values (regex like) will be used as formatted strings
PATTERN = {
    'emoji': '<(?:Emoji)(?:[^>]+)>',
    'link': RE_LINK,
    'mention': '@\d{10,}',
    'media': '<(?:{media})>',
    'location': '(?:{location}|(?:{location2}:\s' + RE_LINK + '))',
    'contact': '^.+\.(vcf \({contact}\))',
    'deleted': '({deleted}|{deleted2})',
    'events': [
        '.+\s({events_encripted})\s.+',
		'.+\s({events_encripted2})\s.+',
        '(.+)\s({event_changed_phone})\s.+',
        '(.+)\s({event_changed_phone2})\s(.+)',
        "^({event_admin})",
        '(.+)\s({event_create})\s"(.+)"',
        '(.+)\s({event_subject})\s".+"\s\w+\s"(.+)"',
        "(.+)\s({event_icon})",
        '(.+?)\s({event_add}|{event_add2})\s(.+)',
        '(.+)\s({event_left})']}
