cmake_minimum_required(VERSION 3.28.1)
project(hft)

set(CMAKE_CXX_STANDARD 23)

find_package(Boost REQUIRED COMPONENTS beast asio)
find_package(nlohmann_json CONFIG REQUIRED)

enable_testing()
set(BOOST_INCLUDE_DIRS ${Boost_INCLUDE_DIRS})
set(BOOST_LIBRARIES ${Boost_LIBRARIES})


add_subdirectory(streams)