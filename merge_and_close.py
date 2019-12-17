#!/usr/bin/python

# This script Add new Version into jira 
# Update issues - versionFix 

#run script
#python release_jira.py auth version_arg

from jira import JIRA
import re
import sys
print(sys.argv)
if(len(sys.argv) < 4 ):
    print("Error - Please pass Version Varible into script -for example : python release_jira.py auth version_arg")
    sys.exit()

AUTH= sys.argv[1]
VERSION= sys.argv[2]
jira_url= sys.argv[3]
BRANCH_NAME= sys.argv[4]
project_name= ' '.join(sys.argv[5:])

AU = AUTH.split(':')

jira = JIRA( basic_auth=(AU),  options={ "server": jira_url })

projects = jira.projects()
for project in projects:
    if project.name == project_name:
        PROJECT_ID = project.id

print(AUTH + " == " + VERSION + " == " + jira_url + " == " + BRANCH_NAME + " == " + project_name)
PROJECT_OBJ = jira.project(PROJECT_ID)
print(PROJECT_OBJ)
VERSION_OBJ = jira.create_version(VERSION, PROJECT_OBJ, description=None, releaseDate=None, startDate=None, archived=True, released=True)


R= re.findall("^([A-Z]+)-([0-9]+)", BRANCH_NAME )
ISSUE_NAME=R[0][0]+"-"+R[0][1]
print(ISSUE_NAME)

fixVersions = []
issue = jira.issue(ISSUE_NAME)
fixVersions.append({'name': VERSION })
issue.update(fields={'fixVersions': fixVersions})




#PROJECT_OBJ = jira.project(PROJECT_ID)
#issues_in_proj = jira.search_issues('project=10001')

#for issue in issues_in_proj:
#    if(issue.key == ""):
#        fixVersions={'id': '10000'}
#        issue.update(fields={'fixVersions': fixVersions})
