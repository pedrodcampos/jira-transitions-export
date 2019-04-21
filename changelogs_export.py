from jira import JIRA
from dateutil import parser
from os import path
import csv


def export(jira_config, jql=None, filename='changelogs'):

    jira = JIRA(debug=True, **jira_config)
    print('Downloading tickets...')
    tickets = jira.search(jql=jql,
                          expand='changelog',
                          fields='summary,status,project',
                          max_results=500,
                          validateQuery='strict')

    changelogs = map_changelogs(tickets)

    if len(changelogs) > 0:
        target_file = dict_to_csv(changelogs, filename)
        print(f"Data exported to {target_file}")
    else:
        print("No results found")


def dict_to_csv(data, csv_file_name):
    target_file = path.join(path.curdir, 'exports', f'{csv_file_name}.csv')

    with open(target_file, 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    return target_file


def map_changelogs(tickets):
    changelog = []
    for ticket in tickets:

        for history in ticket['changelog']['histories']:
            for item in history['items']:
                if item['field'] == 'status':
                    changelog.append({
                        'id': history['id'],
                        'created': parser.parse(history['created']).strftime("%Y-%m-%d %H:%M"),
                        'author': history['author']['displayName'],
                        'email': history['author']['emailAddress'],
                        'ticket_id': ticket['id'],
                        'project_key': ticket['fields']['project']['key'],
                        'project_name': ticket['fields']['project']['name'],
                        'from': item['fromString'],
                        'to': item['toString']
                    })
    return changelog
