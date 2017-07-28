#!/bin/bash

# python_project_from_source.sh
# Deployment script for setting up a project to run from source

if [ $# == 0 ]
then
    echo "Usage: $0 <git_tag> [setlink]"
    exit
fi

scriptpath=$(dirname $(readlink -f $0))
cd $scriptpath
git_tag=$1

# config
# pip: relative or absolute path to pip
pip=

# repo: remote url of the git repository
repo=

# any preliminary commands, exports, etc

# end config

git --git-dir=git_repo fetch --tags $repo
mkdir $git_tag
git --git-dir=git_repo --work-tree=$git_tag checkout -f $git_tag
chmod -R a-w $git_tag

$pip install -q -r $git_tag/requirements.txt

if [ "$2" == "setlink" ]
then
    ln -fnvs $git_tag production
fi
