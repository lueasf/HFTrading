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
find_package(argparse CONFIG REQUIRED)

set(BOOST_INCLUDE_DIRS ${Boost_INCLUDE_DIRS})
set(BOOST_LIBRARIES ${Boost_LIBRARIES})

##########################################
# Aeron

include(ExternalProject)

ExternalProject_Add(
        aeron
        GIT_REPOSITORY https://github.com/real-logic/aeron.git
        GIT_TAG 1.47.4
        CMAKE_ARGS "-DAERON_TESTS=OFF" "-DAERON_SYSTEM_TESTS=OFF" "-DAERON_SLOW_SYSTEM_TESTS=OFF" "-DCMAKE_BUILD_TYPE=Release"
        INSTALL_COMMAND ""
)

ExternalProject_Get_Property(aeron source_dir)
set(AERON_SOURCE_DIR ${source_dir})
ExternalProject_Get_Property(aeron binary_dir)
set(AERON_BINARY_DIR ${binary_dir})

set(
        AERON_LIBS
        ${AERON_BINARY_DIR}/lib/${CMAKE_CFG_INTDIR}/${CMAKE_STATIC_LIBRARY_PREFIX}aeron_client${CMAKE_STATIC_LIBRARY_SUFFIX}
        ${AERON_BINARY_DIR}/lib/${CMAKE_CFG_INTDIR}/${CMAKE_SHARED_LIBRARY_PREFIX}aeron_driver${CMAKE_SHARED_LIBRARY_SUFFIX}
)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/binaries")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/lib")

include_directories(${AERON_SOURCE_DIR}/aeron-client/src/main/cpp)
include_directories(${AERON_SOURCE_DIR}/aeron-client/src/main/c)
include_directories(${AERON_SOURCE_DIR}/aeron-driver/src/main/c)

##########################################
# platform specific flags

# all UNIX-based platform compiler flags
if (UNIX)
    add_compile_options(-Wall -Wpedantic -Wextra -Wno-unused-parameter)
    #    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ofast -DDISABLE_BOUNDS_CHECKS")
    add_compile_options($<$<CONFIG:Release>:-Ofast>)
endif ()

if (APPLE)
    add_compile_options(-Wsign-compare)
    add_definitions(-DDarwin)
    add_compile_options(-Wno-deprecated-register)
elseif (CYGWIN)
    add_definitions(-DWIN32)
    #add_definitions(-DGTEST_HAS_PTHREAD)
    string(REPLACE "-std=c++11" "-std=gnu++11" CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS})
elseif (MSVC)
    add_definitions(-DWIN32)
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
    add_definitions(-D_CRT_NONSTDC_NO_WARNINGS)
    add_definitions(-DNOMINMAX)

    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd /Od /Zi /MP /wd4251")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT /MP /wd4251")
    set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} /MTd")
    set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} /MT")

    unset(CMAKE_C_STANDARD) # To avoid `/std:c11` in the compiler options

    if (C_WARNINGS_AS_ERRORS)
        add_compile_options($<$<COMPILE_LANGUAGE:C>:/WX>)
    endif (C_WARNINGS_AS_ERRORS)

    if (CXX_WARNINGS_AS_ERRORS)
        add_compile_options($<$<COMPILE_LANGUAGE:CXX>:/WX>)
    endif (CXX_WARNINGS_AS_ERRORS)
endif ()

##########################################


add_subdirectory(communication)
add_subdirectory(streams)
add_subdirectory(algos)