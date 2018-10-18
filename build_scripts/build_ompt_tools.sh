#!/usr/bin/env bash 

tools_root="$HOME/repos/ompt_tools"
skeleton_root="${tools_root}/skeleton" 
event_counter_root="${tools_root}/event_counter" 
ancestry_tracker_root="${tools_root}/ancestry_tracker" 
dependency_tracker_root="${tools_root}/dependency_tracker"

# Build the skeleton tool
echo "Building skeleton OMPT tool"
cd ${skeleton_root}/src 
make clean 
make

# Build the event-counter tool
echo "Building event-counting OMPT tool"
cd ${event_counter_root}/src
make clean
make

# Build the ancestry tracker tool
echo "Building ancestry-tracking OMPT tool"
cd ${ancestry_tracker_root}/src
make clean
make

## Build the dependency analysis tool
#echo "Building full dependency analysis OMPT tool"
#cd ${dependency_tracker_root}/src
#make clean
#make 
