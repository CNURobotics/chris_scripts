#!/bin/bash

cd $WORKSPACE_ROOT

echo -n "Do you want to clean install, build, and log folders? [y/n] "
read -N 1 REPLY
echo
if test "$REPLY" = "y" -o "$REPLY" = "Y"; then
  rm -rf install build log
  echo " >>> Cleaned install, build, and log directories."
else
  echo " >>> Clean cancelled by user."
fi
