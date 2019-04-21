import argparse
from changelogs_export import export
from config import build_jira_config

parser = argparse.ArgumentParser(
    prog="python export.py",
    description="Exports all status change history for all tickets in a jql"
)

parser.add_argument("--jql", help="jql string")
parser.add_argument("-d", "--domain", help="JIRA domain")
parser.add_argument("-u", "--username", help="JIRA username")
parser.add_argument("-p", "--password", help="JIRA passowrd")
parser.add_argument("-f", "--filename", help="Custom export file name")

args = parser.parse_args()

jira_config = build_jira_config(
    args.domain, args.username, args.password)

export(jira_config, args.jql, args.filename)
