cmake_minimum_required(VERSION 3.10)

find_package(Xlnt CONFIG REQUIRED)

file(GLOB SRCS *.cpp)

#pybind11_add_module(lib example.cpp)

add_library(processing SHARED ${SRCS})

target_link_libraries(processingм
        PRIVATE
        xlnt::xlnt
)
