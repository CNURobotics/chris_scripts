#!/bin/bash

cd $WORKSPACE_ROOT

echo -n "Do you want to clean devel and build? [y/n] "
read -N 1 REPLY
echo
if test "$REPLY" = "y" -o "$REPLY" = "Y"; then
  catkin clean --all
  echo " >>> Cleaned devel and build directories."
else
  echo " >>> Clean cancelled by user."
fi
