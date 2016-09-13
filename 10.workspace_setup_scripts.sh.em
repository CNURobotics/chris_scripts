#!/bin/sh

@[if DEVELSPACE]@
export WORKSPACE_SCRIPTS=@(PROJECT_SOURCE_DIR)/scripts
@[else]@
export WORKSPACE_SCRIPTS=@(CMAKE_INSTALL_PREFIX)/@(CATKIN_PACKAGE_SHARE_DESTINATION)/scripts
@[end if]@
export WORKSPACE_ROOT=$(cd "@(CMAKE_SOURCE_DIR)/../.."; pwd)

# set CHRIS_* environment variables

# include CHRIS_scripts hooks
#if [ -d $WORKSPACE_SCRIPTS ]; then
#  . $WORKSPACE_SCRIPTS/functions.sh
#  . $WORKSPACE_SCRIPTS/robot.sh ""

#  if [ -r "$WORKSPACE_SCRIPTS/$HOSTNAME/setup.sh" ]; then
#      echo "Including $WORKSPACE_SCRIPTS/$HOSTNAME/setup.sh..." >&2
#      . "$WORKSPACE_SCRIPTS/$HOSTNAME/setup.sh"
#  fi
#fi


# export some variables
export PATH=$WORKSPACE_SCRIPTS/helper:$PATH
export ROS_WORKSPACE=$WORKSPACE_ROOT/src

# Load gazebo setup if gazebo is installed
if [ -f /usr/share/gazebo/setup.sh ]; then
  . /usr/share/gazebo/setup.sh 
fi


