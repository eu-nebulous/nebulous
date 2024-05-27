#!/bin/bash

set -e
set -u

BRANCH=$1

cd ..

for project in *; do
    if [[ $project == "nebulous" ]]; then
        continue
    fi
    cd $project
    if ! git fetch origin &>/dev/null; then
        echo "$project has no origin"
        continue
    fi
    if ! git show origin/$BRANCH &>/dev/null; then
        echo "$project is missing $BRANCH"
        continue
    fi
    git fetch origin
    git reset --hard &>/dev/null
    git clean -df &>/dev/null
    git checkout origin/$BRANCH &>/dev/null
    sed -i "s/defaultbranch=master/defaultbranch=$BRANCH/" .gitreview
    git add .gitreview
    if git commit -m "Set the repo up for $BRANCH"; then
        git review -t "nebulous-$BRANCH-gerrit-branch"
    fi
done
