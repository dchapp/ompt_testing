#!/usr/bin/env bash
# [wf] execute setup stage

build_scripts="../../build_scripts/"

# Build the OMPT tool that counts OpenMP runtime events
# [wf] Build event-counter OMPT tool
${build_scripts}/build_event_counter_tool.sh

# Build the KASTORS apps and link them with the tool
# [wf] Building the KASTORS benchmark suite 
${build_scripts}/build_kastors_event_counter.sh
