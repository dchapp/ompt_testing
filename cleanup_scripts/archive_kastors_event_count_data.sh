#!/usr/bin/env bash 

DATE=`date '+%Y.%m.%d.%H.%M.%S'`

echo "Archiving current data and figures" 
data="../results/kastors/event_counts/"
data_dirs=""
for dir in ${data}/[^archive]*/
do
    data_dirs=${data_dirs}" ${dir}"
done
archive_dir="${data}/archive/"
mkdir -p ${archive_dir}

tar -czvf "${archive_dir}/${DATE}.tar.gz" ${data_dirs}



