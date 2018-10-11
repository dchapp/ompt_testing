#!/usr/bin/env bash 

tools_root="$HOME/repos/ompt_tools"
dagtool_root="${tools_root}/dagtool"
eventcounter_root="${tools_root}/event_counter" 
skeleton_root="${tools_root}/skeleton" 

# Build the skeleton tool
echo "Building skeleton OMPT tool"
cd ${skeleton_root}/src 
make clean 
make

# Build the event-counter tool
echo "Building event-counting OMPT tool"
cd ${eventcounter_root}/src
make clean
make

# Build the full dependency analysis tool
echo "Building full dependency analysis OMPT tool"
cd ${dagtool_root}/src
make clean
make 
