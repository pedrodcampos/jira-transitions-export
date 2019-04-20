import requests
import time
from config import jira_config


class JiraEndpoint():
    __endpoint__ = ""

    def __init__(self, session):
        self.session = session

    def __url(self):
        return self.session.url+self.__endpoint__

    def __strip_none_params(self, params):
        return {key: value for key, value in params.items() if value}

    def get(self, params):
        params = self.__strip_none_params(params)
        url = self.__url()

        tries = 0
        while True and tries <= 3:
            result = self.session.get(url,  params=params)
            if result.status_code == 200:
                break
            elif result.status_code == 500:
                tries += 1
                print('retrying..')
                time.sleep(5)

        if result.status_code == 200:
            return result.json()
        else:
            raise Exception(result.status_code)


class JIRASearch(JiraEndpoint):
    __endpoint__ = 'search'

    def get(self, params):
        issues = []
        page = 1
        total = 0
        while True:
            result = super().get(params)
            if len(result['issues']) > 0:

                issues = issues + result['issues']
                total = result['total']
                max_results = result['maxResults']
                total_pages = (round(total/max_results+0.5))
                params.update({'startAt': page*params['maxResults']})
                print(f'Got page {page}/{int(total_pages)}')
                page += 1
                time.sleep(1)
            else:
                break
        return issues


class JIRA():
    def __init__(self, domain, auth):
        self.__session = requests.session()
        self.__session.url = f"https://{domain}/rest/api/2/"
        self.__session.headers.update({'Accept': 'application/json'})
        self.__session.auth = auth
        self.__session.get(
            f'https://jira.devfactory.com/rest/api/2/user?username={auth[0]}')

    def search(self, jql=None,  **kwargs):
        params = {'jql': jql}
        params.update({'maxResults': kwargs.get('max_results', 50)})
        params.update({'fields': kwargs.get('fields', None)})
        params.update(
            {'validateQuery': kwargs.get('validate_query', None)})
        params.update({'expand': kwargs.get('expand', None)})
        return JIRASearch(self.__session).get(params)
