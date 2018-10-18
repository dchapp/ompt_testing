#!/usr/bin/env bash

project_root="${HOME}/repos/OMPT_Testing"
kastors_dir="/g/g17/chapp1/repos/kastors-1.1/"
tools=(
       "skeleton"
       "event_counter" 
       "ancestry_tracker"
      )

# Build KASTORS with no tool linked
${project_root}/build_scripts/build_kastors.sh

# Build KASTORS with each tool listed
for tool in ${tools[@]}
do
    ${project_root}/build_scripts/build_kastors"_"${tool}".sh"
done
