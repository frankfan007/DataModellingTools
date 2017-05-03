include_directories(${exe_source_dir}../tester)
link_directories(${exe_source_dir}../tester)

add_executable(exe tester.c)
target_link_libraries(exe tester)

