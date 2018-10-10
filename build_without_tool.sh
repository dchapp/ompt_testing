#!/usr/bin/bash 

kastors_dir="/g/g17/chapp1/repos/kastors-1.1/"
build_dir="/g/g17/chapp1/repos/kastors-1.1/build_no_tool"
mkdir -p ${build_dir}
cd ${build_dir} 
make distclean 
cd ${kastors_dir}
./configure --prefix=${build_dir} CC=clang CXX=clang++ CPPFLAGS=-I/g/g17/chapp1/repos/LLVM-openmp/build/include
echo ${LDFLAGS} 
echo ${LIBS}
make -B
make install
