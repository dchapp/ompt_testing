#!/usr/bin/env bash

kastors_dir="/g/g17/chapp1/repos/kastors-1.1/"
tools=("skeleton"
       "event_counter" 
       "ancestry_tracker"
      )

# Build KASTORS with no tool linked
./build_kastors.sh

# Build KASTORS with each tool listed
for tool in ${tools[@]}
do
    ./build_kastors"_"${tool}".sh"
done
