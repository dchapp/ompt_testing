#!/usr/bin/env bash 

kastors_root="$HOME/repos/kastors-1.1"

echo "Deleting KASTORS executables"
cd ${kastors_root}
echo "Deleting no-tool apps"
rm -rfv ${kastors_root}/build_no_tool/bin/*
echo "Deleting skeleton-tool apps"
rm -rfv ${kastors_root}/build_skeleton_tool/bin/*
echo "Deleting event-counter-tool apps"
rm -rfv ${kastors_root}/build_event_counter_tool/bin/*
echo "Deleting full-tool apps"
rm -rfv ${kastors_root}/build_full_tool/bin/*
