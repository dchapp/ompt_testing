#!/usr/bin/env bash 

DATE=`date '+%Y.%m.%d.%H.%M.%S'`

project_root="${HOME}/repos/OMPT_Testing"
echo "Archiving current data and figures" 
data="${project_root}/results/kastors/overhead_measurements/"
data_dirs=""
for dir in ${data}/[^archive]*/
do
    app=`basename ${dir}`
    data_dirs=${data_dirs}" ${app}"
done
archive_dir="${data}/archive/"
mkdir -p ${archive_dir}
cd ${data}
tar -czvf "${archive_dir}/${DATE}.tar.gz" ${data_dirs}
cd -



