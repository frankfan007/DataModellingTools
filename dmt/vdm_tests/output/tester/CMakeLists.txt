include_directories(${exe_source_dir}/tester)
add_definitions(-DASN1SCC_MAPPING)

file(GLOB tester_SRC "*.c" "*.h")
add_library(tester ${tester_SRC})
target_link_libraries(tester m)
