cmake_minimum_required(VERSION 3.10)

file(GLOB SRCS *.cpp)

add_library(test SHARED ${SRCS})

target_include_directories(
        test
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../include
)

set_target_properties(
        test PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED ON
)