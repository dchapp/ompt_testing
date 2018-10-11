#!/usr/bin/env bash

tools_root="$HOME/repos/ompt_tools"
eventcounter_root="${tools_root}/event_counter" 

# Build the event-counter tool
echo "Building event-counting OMPT tool"
cd ${eventcounter_root}/src
make clean
make
