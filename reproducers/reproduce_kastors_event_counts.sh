#!/usr/bin/env bash 

n_trials=10
project_root="${HOME}/repos/OMPT_Testing"

${project_root}/build_scripts/build_event_counter_tool.sh
${project_root}/build_scripts/build_kastors_event_counter.sh
${project_root}/job_scripts/collect_kastors_event_counts.sh ${n_trials} 

data=${project_root}/results/kastors/event_counts/
for dir in "${data}"/[^archive]*/
do
    echo "Generating event-count plot for ${dir}"
    ${project_root}/plotting_scripts/make_event_count_plots.py ${dir}
done

${project_root}/cleanup_scripts/archive_kastors_event_count_data.sh
${project_root}/cleanup_scripts/clean_kastors.sh
${project_root}/cleanup_scripts/clean_kastors_event_count_data.sh
