cmake_minimum_required(VERSION 3.10)

file(GLOB SRCS *.cpp)

add_library(processing STATIC ${SRCS})
target_link_libraries(processing
        PRIVATE
        OpenXLSX::OpenXLSX
)
