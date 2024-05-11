cmake_minimum_required(VERSION 3.10)

add_subdirectory(example)
add_subdirectory(src)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../OpenXLSX/OpenXLSX)

add_custom_target(
        copy_data ALL
        ${CMAKE_COMMAND} -E copy_directory ${CMAKE_SOURCE_DIR}/data ${CMAKE_BINARY_DIR}/data
)

message(STATUS "Copy folder")

add_dependencies(example copy_data)