#!/usr/bin/env bash 

kastors_root="$HOME/repos/kastors-1.1"

echo "Deleting base KASTORS executables"
cd ${kastors_root}
echo "Deleting no-tool versions"
rm -rfv ${kastors_root}/build_no_tool/bin/*
echo "Deleting skeleton-tool versions"
rm -rfv ${kastors_root}/build_skeleton_tool/bin/*
echo "Deleting event-counter-tool versions"
rm -rfv ${kastors_root}/build_event_counter_tool/bin/*
echo "Deleting ancestry-tracker-tool versions"
rm -rfv ${kastors_root}/build_ancestry_tracker_tool/bin/*
