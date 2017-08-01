#!/bin/bash
# python_project_in_venv.sh: deployment script for installing a project to a
# Python virtual environment to run as an executable

### config
# pyvenv: path to central executable for installing Python virtual environments
pyvenv=

# repo: remote url of the git repository
repo=

# any preliminary commands, exports, etc

if [ ! $pyvenv ] || [ ! $repo ]
then
    echo "Invalid config: ensure that pyvenv and repo are populated"
    exit 1
fi
### end config


if [ $# == 0 ]
then
    echo "Usage: $0 <git_tag> [setlink]"
    exit
fi

scriptpath=$(dirname $(readlink -f $0))
cd $scriptpath
git_tag=$1


if [ "$git_tag" == "master" ]
then
    deployment_suffix=""
else
    deployment_suffix="@$git_tag"
fi

echo "Deploying $git_tag from $repo"

if [ -d "./$git_tag" ]
then
  rm -rf "./$git_tag"
fi

$pyvenv $git_tag
$git_tag/bin/pip install -q "git+$repo$deployment_suffix"

if [ "$2" == "setlink" ]
then
    echo "Setting production link"
    ln -fnvs ./$git_tag ./production
fi

echo "Done"
