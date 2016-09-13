#!/bin/bash

echo

# Takes us to scripts which is inside workspace, so that's good enough
# for wstool to work
echo ">>> Pulling install folder in $WORKSPACE_SCRIPTS"
cd $WORKSPACE_SCRIPTS
git pull

# Remove obsolete stuff using wstool
$WORKSPACE_SCRIPTS/rm_obsolete_packages.sh

echo ">>> Pulling install folder in $WORKSPACE_ROOT"
cd $WORKSPACE_ROOT
git pull
echo

#echo ">>> Checking package updates"
#./rosinstall/install_scripts/install_package_dependencies.sh
#echo

if [ -d $WORKSPACE_ROOT/rosinstall/optional/custom/.git ]; then
    echo ">>> Pulling custom rosinstalls"
    cd $WORKSPACE_ROOT/rosinstall/optional/custom
    git pull
    echo
fi

if [ -d $WORKSPACE_SCRIPTS/custom/.git ]; then
    echo ">>> Pulling custom scripts"
    cd $WORKSPACE_SCRIPTS/custom
    git pull
    echo
fi

cd $WORKSPACE_ROOT
echo ">>> Merging rosinstall files"
for file in $WORKSPACE_ROOT/rosinstall/*.rosinstall; do
    filename=$(basename ${file%.*})
    if [ -n "$WORKSPACE_MANG_NO_SIM" ] && [ $filename == "thor_mang_simulation" ]; then
        continue;
    else
        echo "Merging to workspace: $filename.rosinstall"
        wstool merge $file -y
    fi
done
echo

echo ">>> Updating catkin workspace"
cd $WORKSPACE_ROOT/src
wstool update
