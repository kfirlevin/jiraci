from jira import JIRA
import sys


def get_issues():
    issues = []
    for project in jira.projects():
        
        issues_in_proj = jira.search_issues('project='+project.key)
        for issue in issues_in_proj:
            
            transitions = []
            for t in jira.transitions(issue.key):
                transition = {
                    "name": t['name'],
                    "id": t['id']
                }
                transitions.append(transition)

            issue_more = jira.issue(issue.key)

            iss = {
                "assignee": issue_more.fields.assignee,
                "reporter": issue_more.fields.reporter,
                "key": issue.key,
                "status": issue.fields.status.name,
                "transitions": transitions
            }
            issues.append(iss)
    return issues
def add_comment(args):
    issues = get_issues()
    issue_exist = False

    for i in issues:
        if i['key'] == args[3]:
            issue_exist = True
            if i['assignee'] is None:
                 sys.exit('No assignee')
            issue = jira.issue(args[3])
            message = (' '.join(args[4:]))
            jira.add_comment(issue, message)
            return
    if not issue_exist:
        sys.exit('Issue does not exist')

def change_status(args):
    issues = get_issues()
    issue_exist = False
    for i in issues:
        if i['key'] == args[3] and i['status'] != 'Done': 
            issue_exist = True
            if i['assignee'] is None:
                 sys.exit('No assignee')
            issue = jira.issue(args[3])
            for t in i['transitions']:
                if  args[4] == "start" and  t['name'] == 'Start Progress':
                    jira.transition_issue(args[3], t['id'])
                elif args[4] == "close" and t['name'] == 'Done':
                    jira.transition_issue(args[3], t['id'])
            jira.assign_issue(issue, i['assignee'].key)
            return

    if not issue_exist:
        sys.exit('Issue does not exist or closed!')       

args=[]
# 0 - username, 1 - password, 2 - url, 3 - issue key, 4 - task status / message
args.extend(sys.argv[1].split(':'))
for arg in sys.argv[2:]:
    args.append(arg)

jira = JIRA(
    basic_auth=(args[0], args[1]), 
    options={ "server": args[2] }
    )

if args[4] == 'start' or args[4] == 'close':
    change_status(args)
else:
    add_comment(args)
