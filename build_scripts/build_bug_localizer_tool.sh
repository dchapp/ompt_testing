#!/usr/bin/env bash 

tools_root="$HOME/repos/ompt_tools"
bug_localizer_root="${tools_root}/dependency_tracker" 

# Build the ancestry tracker tool
echo "Building bug-localizer OMPT tool"
cd ${bug_localizer_root}/src
make clean
make
