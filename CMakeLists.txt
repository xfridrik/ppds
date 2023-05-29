cmake_minimum_required(VERSION 3.25)
project(PROJEKT)

set(CMAKE_CXX_STANDARD 17)
# Add MPI Package to Project
include_directories(SYSTEM ${MPI_INCLUDE_PATH})
find_package(MPI REQUIRED)
add_executable(PROJEKT main.cpp)
# Add libraries for code completion and compiling
target_link_libraries(PROJEKT PUBLIC MPI::MPI_CXX)
