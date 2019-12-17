#/bin/sh

#increase hotfix versioning
#getting 2 params: branch name of git repo (version/*) and increase versioning or not
#return version number as stdout 

set -e

BRANCH_NAME=$1
increase=$2

    major=$(echo $BRANCH_NAME | cut -d'/' -f2)
    tags=$(git tag -l |grep "^$major" | wc -l)
    if [ $tags -gt 0 ]
    then
        hotfix=$(git tag -l | grep -i "^$major" | cut -d . -f3 | sort -n | tail -1 )
        if [ "$increase" = true ]
        then
            hotfix=$((hotfix+1))
        else
            : #do not increase hotfix versioning
        fi
        newtag=$major.$hotfix
        increment=$newtag              
    else
        tag=$(echo $BRANCH_NAME | cut -d'/' -f2)
        newtag=$tag.0
        increment=$newtag
    fi

echo $increment