cmake_minimum_required(VERSION 3.28.1)
project(hft)

set(CMAKE_CXX_STANDARD 23)

find_package(Boost REQUIRED COMPONENTS beast asio)

enable_testing()

add_subdirectory(streams)