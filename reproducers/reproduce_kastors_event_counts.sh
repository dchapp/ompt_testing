#!/usr/bin/env bash 

n_trials=10

../build_scripts/build_event_counter_tool.sh
../build_scripts/build_kastors_event_counter.sh
../job_scripts/collect_kastors_event_counts.sh ${n_trials} 

data=../results/kastors/event_counts/
for dir in "${data}"/[^archive]*/
do
    echo "Generating event-count plot for ${dir}"
    ../plotting_scripts/make_event_count_plots.py ${dir}
done

../cleanup_scripts/archive_kastors_event_count_data.sh
../cleanup_scripts/clean_kastors.sh
../cleanup_scripts/clean_kastors_event_count_data.sh
