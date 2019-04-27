# jira-transitions-export
Exports all Jira Ticket's status transitions to a csv file based on a query.

Make sure you have all dependencies installed by running `pip install -r requirements.txt`

## Usage
`python export.py [-h] [--jql JQL] [-d DOMAIN] [-u USERNAME] [-p PASSWORD] [-f FILENAME]`


_optional arguments:_

Argument |Name| Description
---|---|---
-h, --help | HELP | show this help message and exit
--jql| JQL  |jql string. [Check the docs.](https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html#Advancedsearching-ConstructingJQLqueries)
-d, --domain |DOMAIN| JIRA domain
-u, --username| USERNAME| JIRA username
-p, --password |PASSWORD| JIRA passowrd
-f, --filename | FILENAME| Custom export file name

Alternatively you can create a copy of `.config.example.json` file in this repo, rename it to `.config.json` and provide your domain and credentials. Be aware that the `.config.json` will be disregarded if you provide credentials or domain as  arguments.

> if you do not provide a jql string, downloading all data may take a while. Be patient. 