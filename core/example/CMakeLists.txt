cmake_minimum_required(VERSION 3.10)

file(GLOB SRCS *.cpp)

add_executable(example ${SRCS})

target_include_directories(
        example
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../include
)

set_target_properties(
        example PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED ON
)