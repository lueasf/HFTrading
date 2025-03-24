cmake_minimum_required(VERSION 3.28.1)
project(hft)

set(CMAKE_CXX_STANDARD 23)

enable_testing()

find_package(Boost REQUIRED COMPONENTS beast asio)
find_package(nlohmann_json CONFIG REQUIRED)
find_package(fmt CONFIG REQUIRED)
find_package(OpenSSL REQUIRED)
find_package(cnats CONFIG REQUIRED)
find_package(yaml-cpp CONFIG REQUIRED)

set(BOOST_INCLUDE_DIRS ${Boost_INCLUDE_DIRS})
set(BOOST_LIBRARIES ${Boost_LIBRARIES})


add_subdirectory(communication)
add_subdirectory(streams)
add_subdirectory(algos)