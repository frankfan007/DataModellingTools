include_directories(${exe_source_dir}/tester)

file(GLOB tester_SRC "*.c" "*.h")
add_library(tester ${tester_SRC})
target_link_libraries(tester m)
