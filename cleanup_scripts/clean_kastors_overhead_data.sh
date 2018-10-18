#!/usr/bin/env bash 

kastors_overhead_data="$HOME/repos/OMPT_Testing/results/kastors/overhead_measurements/"
for dataset in ${kastors_overhead_data}/[^archive]*/
do
    rm -rfv ${dataset}

done
