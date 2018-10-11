#!/usr/bin/env bash 

kastors_event_count_data="$HOME/repos/OMPT_Testing/results/kastors/event_counts/"
for dataset in ${kastors_event_count_data}/[^archive]*/
do
    rm -rfv ${dataset}
done
