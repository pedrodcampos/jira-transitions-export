from os import environ


jira_config = {
    'domain': environ.get('DOMAIN', None),
    'auth': (environ.get('USERNAME', None), environ.get('PASSWORD', None))
}
