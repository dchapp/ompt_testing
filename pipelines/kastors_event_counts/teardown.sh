#!/usr/bin/env bash
# [wf] execute teardown stage

cleanup_script_dir="../../cleanup_scripts/"

# [wf] Back up current KASTORS event count data
${cleanup_script_dir}/archive_kastors_event_count_data.sh
# [wf] Delete KASTORS event count data
${cleanup_script_dir}/clean_kastors_event_count_data.sh
# [wf] Delete KASTORS executables
${cleanup_script_dir}/clean_kastors.sh 
