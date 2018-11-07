#!/usr/bin/env bash 

# What are we using and where is it
CC=clang
CXX=clang++
omp_home=$HOME/repos/LLVM-openmp/build
project_home=$HOME/repos/OMPT_Testing
bug_injector_home=$HOME/repos/llvm_passes/bug_injector
error_lib_home=$bug_injector_home/error_lib
bug_localizer_home=$HOME/repos/ompt_tools/dependency_tracker
demo_app_home=$project_home/test_apps

# Build the bug injector
echo "Building bug-injection LLVM pass..."
cd $bug_injector_home
mkdir -p build
cd build
export LLVM_DIR="/opt/llvm/5.0/lib/cmake"
cmake ..
make 
echo "Done!"
echo

# Build the bug localizer
echo "Building bug-localization OMPT tool..."
$project_home/build_scripts/build_bug_localizer_tool.sh
echo "Done!"
echo 

# Compile the bug code prior 
$CC -c -fPIC $error_lib_home/error_lib.c -o $error_lib_home/error_lib.o

# Compile the demo application, injecting bugs as requested
pass_lib=$bug_injector_home/build/bug_injector/libBugInjectorPass.so
pass_options="-Xclang -load -Xclang $pass_lib"
$CC -fopenmp -I$omp_home/include $pass_options -c $demo_app_home/demo.c -o $demo_app_home/demo.o

# Link the demo application with the bug code and with the bug localizer library
$CC -fopenmp -L$bug_localizer_home/build/lib $demo_app_home/demo.o $error_lib_home/error_lib.o -ldependency_tracker -o $demo_app_home/demo.exe

# Run the demo code 
$demo_app_home/demo.exe

