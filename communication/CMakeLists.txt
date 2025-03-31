include(FetchContent)
FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

include(ExternalProject)
set(AERON_SOURCE_DIR ${CMAKE_BINARY_DIR}/communication/aeron-prefix/src/aeron)
set(AERON_BUILD_DIR ${AERON_SOURCE_DIR}/cppbuild/Release)
set(AERON_INSTALL_DIR ${CMAKE_BINARY_DIR}/aeron-install)

# Define platform-specific build commands
if (WIN32)
    set(AERON_BUILD_COMMAND Powershell.exe -File "${AERON_SOURCE_DIR}/cppbuild/cppbuild.ps1")
else ()
    set(AERON_BUILD_COMMAND bash "${AERON_SOURCE_DIR}/cppbuild/cppbuild")
endif ()

ExternalProject_Add(
        aeron
        GIT_REPOSITORY https://github.com/real-logic/aeron.git
        GIT_TAG 1.47.4
        UPDATE_COMMAND ""
        CONFIGURE_COMMAND ""
        BUILD_COMMAND ${AERON_BUILD_COMMAND}
        INSTALL_COMMAND ${CMAKE_COMMAND} -E copy_directory "${AERON_BUILD_DIR}/lib" "${AERON_INSTALL_DIR}/lib"
        LOG_BUILD ON
)

add_library(communication_lib
        aeron_publisher.cpp
        aeron_publisher.h
)

add_dependencies(communication_lib aeron)

ExternalProject_Get_Property(aeron INSTALL_DIR)
target_include_directories(communication_lib PUBLIC ${BOOST_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR} ${AERON_SOURCE_DIR}/aeron-client/src/main/cpp)
target_link_directories(communication_lib PRIVATE ${AERON_INSTALL_DIR}/lib/Release)

target_link_libraries(communication_lib PRIVATE ${AERON_INSTALL_DIR}/lib/Release/aeron.lib)
target_link_libraries(communication_lib PRIVATE ${AERON_INSTALL_DIR}/lib/Release/aeron_client.lib)

add_executable(communication_tests tests/main_test.cpp)

target_link_libraries(communication_tests PRIVATE
        communication_lib
        GTest::gtest_main
        GTest::gtest
)

include(GoogleTest)
