from os import environ


def build_jira_config(domain=None, username=None, password=None):

    return {"domain": domain if domain else environ.get('DOMAIN', None),
            "auth": (
                username
                if username else environ.get('USERNAME', None),
                password
                if password else environ.get('PASSWORD', None))
            }
