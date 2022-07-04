#!/bin/bash

function blueEcho()
{
  echo -ne '\e[0;34m'
  echo $1
  echo -ne '\e[0m'
}

function findCanonicalBranch()
{
  dir=$1
  rosinstalldir=$2

  #echo "Checking ${dir}  using ${rosinstalldir} ..."

  if [ -e "$rosinstalldir/.rosinstall" ]
  then
    name=$(basename $dir)
    desiredBranch=$(perl -0 -ne 'print qq($1\n) if /\b'$name'\b.*\n.*version: ([^}]+)/mg' ${rosinstalldir}/.rosinstall)
  fi

  echo $desiredBranch
}

function displayStatus()
{
  old_d=`pwd`
  dir=$1
  desiredBranch=$2

  cd $dir
  if [ -z "$desiredBranch" ]
  then
    desiredBranch=$(git log --pretty='%d' -1 HEAD | perl -ne 'm#(?<=origin/)([^,]*)# && print "$1\n"')
  fi

  if [ -e "$dir/.git" ]
  then
    echo "----------------------------------------"
    echo "$PWD :"
    echo "$(git remote -v)"
    #echo "   $(git status)"
    if [ "$(git rev-parse --abbrev-ref HEAD)" != "$desiredBranch" ] \
       || [ -n "$(git status --porcelain)" ] \
       || [ -n "$(git status | grep -P 'branch is (ahead|behind)')" ]
    then
      if [ "$(git rev-parse --abbrev-ref HEAD)" != "$desiredBranch" ]
      then
        #git status | grep "   On branch" | perl -pe "chomp"
        echo -e "   $(git rev-parse --abbrev-ref HEAD)"
        echo -e "      (should be on branch $desiredBranch)"
      fi
      git status | grep -P 'branch is (ahead|behind)'
      git status | grep "modified"
      git status | grep "new file"
      git status | grep "deleted"
      if [ -n "$(git status | grep 'Untracked files')" ]
      then
        git status --porcelain | grep '??' | sed -r 's/^.{3}//' \
        | xargs -I file echo -e '\tuntracked:  '"file"
      fi
      echo
    else
      echo "    On branch $desiredBranch - No changes!"
      echo ""
    fi
  elif [ -e "$dir/.hg" ]; then
    if [ "$(hg branch)" != "$desiredBranch" ] \
       || [ -n "$(hg status)" ]
    then
      echo "On hg branch `hg branch`"
      hg status
      hg incoming | grep "changes"
      echo
    fi
  #else
    #echo "$PWD is not a repository!"
    #echo
  fi
  cd $old_d
}

if [ -z $WORKSPACE_ROOT ]; then
  echo "Variable WORKSPACE_ROOT not set, make sure the workspace is set up properly!"
  exit 1
fi

ros2_src=$WORKSPACE_ROOT/src
cd $ros2_src
displayStatus $PWD

blueEcho "Looking for changes in ${ros2_src} ..."
for d in `find  ${ros2_src} -mindepth 1 -maxdepth 3 -type d`;
do
  branch=$(findCanonicalBranch $d ${ros2_src}/..)
  displayStatus $d $branch
done
