from jira import JIRA
from config import jira_config
from dateutil import parser
from os import path
import csv

jira = JIRA(**jira_config)

tickets = jira.search(jql='created >= startOfDay()',
                      expand='changelog', fields='summary,status,project', max_results=500)

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

if len(changelog) > 0:
    target_file = path.join(path.curdir, 'exports', 'chagelog.csv')

    with open(target_file, 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, list(changelog[0].keys()))
        writer.writeheader()
        writer.writerows(changelog)
    print('Done.')
