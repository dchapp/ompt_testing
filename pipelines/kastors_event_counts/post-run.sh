#!/usr/bin/env bash
# [wf] execute post-run stage

plotting_script_dir="$HOME/repos/OMPT_Testing/plotting_scripts/"
data_dir="$HOME/repos/OMPT_Testing/results/kastors/event_counts/"

for dir in ${data_dir}/[^archive]*/
do
    echo "Generating event-count plot for ${dir}"
    ${plotting_script_dir}/make_event_count_plots.py ${dir} 
done
