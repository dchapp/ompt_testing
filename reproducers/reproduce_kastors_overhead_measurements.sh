#!/usr/bin/env bash 

n_trials=10

# Build all of the OMPT tools whose overheads we are measuring
../build_scripts/build_ompt_tools.sh 

# Build the KASTORS apps with each tool
../build_scripts/build_kastors_all_tools.sh

# Run the apps
../collect_kastors_overhead_measurements.sh 
