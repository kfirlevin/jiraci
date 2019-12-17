#!/bin/bash
set -e

options='h:u:i:U:'
while getopts $options option
do
    case "$option" in
        U  ) jira_url=$OPTARG;;
        h  ) commit_hash=$OPTARG;;
        u  ) user_cred=$OPTARG;;
        i  ) branch_name=$OPTARG;;
        *  ) echo "Unimplemented option: -$OPTARG" >&2; exit 1;;
    esac
done

issue=$(echo $branch_name | sed -E 's/^(([A-Z]+)-([0-9]+)).*/\1/g')
message="commit hash:$commit_hash, message:"$(git show --pretty=format:%s -s $commit_hash)
#  '{"transition":{"id": '"$id_needed"'}}'
#  echo '{"body": '\"$commit_hash-$message\"'}'
python ci/update_issue.py $user_cred $jira_url $issue $message
