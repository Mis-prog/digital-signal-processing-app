cmake_minimum_required(VERSION 3.10)

add_subdirectory(external)
add_subdirectory(src)
add_subdirectory(example)

include_directories(external/OpenXLSX/OpenXLSX)

add_custom_target(
        copy_data ALL
        ${CMAKE_COMMAND} -E copy_directory ${CMAKE_SOURCE_DIR}/data ${CMAKE_BINARY_DIR}/data
)
#
add_dependencies(example copy_data)