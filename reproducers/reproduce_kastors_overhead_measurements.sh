#!/usr/bin/env bash 

n_trials=10

project_root="${HOME}/repos/OMPT_Testing"

# Build all of the OMPT tools whose overheads we are measuring
time ${project_root}/build_scripts/build_ompt_tools.sh 

# Build the KASTORS apps with each tool
time ${project_root}/build_scripts/build_kastors_all_tools.sh

# Run the apps
time ${project_root}/job_scripts/collect_kastors_overhead_measurements.sh ${n_trials}

# Generate figures
results_root=${project_root}/results/kastors/overhead_measurements/
for app_dir in ${results_root}/[^archive]*/
do
    echo "Generating plots for: "${app_dir}
    ${project_root}/plotting_scripts/make_overhead_plots.py ${app_dir}
done

# Archival and teardown
${project_root}/cleanup_scripts/archive_kastors_overhead_data.sh
${project_root}/cleanup_scripts/clean_kastors.sh
${project_root}/cleanup_scripts/clean_kastors_overhead_data.sh
