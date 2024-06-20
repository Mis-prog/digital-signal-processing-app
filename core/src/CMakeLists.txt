cmake_minimum_required(VERSION 3.10)


file(GLOB SRCS *.cpp)

#pybind11_add_module(lib example.cpp)

add_library(processing STATIC ${SRCS})

target_link_libraries(processing
        PRIVATE
        OpenXLSX::OpenXLSX
)
