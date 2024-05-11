cmake_minimum_required(VERSION 3.10)

file(GLOB SRCS *.cpp)

add_executable(example ${SRCS})


target_include_directories(
        example
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../include
)

target_link_libraries(example
        PRIVATE
        processing
        OpenXLSX::OpenXLSX
)