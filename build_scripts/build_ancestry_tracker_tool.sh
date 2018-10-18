#!/usr/bin/env bash 

tools_root="$HOME/repos/ompt_tools"
ancestrytracker_root="${tools_root}/ancestry_tracker" 

# Build the ancestry tracker tool
echo "Building ancestry-tracking OMPT tool"
cd ${ancestrytracker_root}/src
make clean
make
