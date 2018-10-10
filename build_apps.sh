#!/usr/bin/bash

kastors_root="$HOME/repos/kastors-1.1"

cd ${kastors_root}
./build_without_tool.sh
./build_with_skeleton_tool.sh
./build_with_event_counter_tool.sh
./build_with_full_tool.sh 
