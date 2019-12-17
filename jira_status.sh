#!/bin/bash
set -e

options='c:u:U:i:'
while getopts $options option
do
    case "$option" in
        U  ) jira_url=$OPTARG;;
        c  ) command=$OPTARG;;
        u  ) user_cred=$OPTARG;;
        i  ) branch_name=$OPTARG;;
        *  ) echo "Unimplemented option: -$OPTARG" >&2; exit 1;;
    esac
done

issue=$(echo $branch_name | sed -E 's/^(([A-Z]+)-([0-9]+)).*/\1/g')
python ci/update_issue.py $user_cred $jira_url $issue $command