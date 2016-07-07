cmake_minimum_required(VERSION 2.6)
project(tester)

set(CMAKE_C_FLAGS "-std=c11")

include_directories(${cmake_source_dir}/tester)


subdirs(tester)

