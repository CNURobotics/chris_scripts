#!/bin/bash

# Simplified scripts based on Team ViGIR version

if [ -z "$WORKSPACE_ROOT" ]; then
    WORKSPACE_ROOT=$(cd `dirname $0`; pwd)
    echo "Setting workspace root of $WORKSPACE_ROOT"
else
    echo "Using workspace root of $WORKSPACE_ROOT"
fi

echo ">>> Updating ROS workspace"
cd $WORKSPACE_ROOT/src
wstool update
