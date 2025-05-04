#### Google Test ####

include(FetchContent)
FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

### Communication Library ####

add_library(communication_lib
        aeron/aeron_publisher.cpp
        aeron/aeron_publisher.h
        nats/nats_client.cpp
        nats/nats_client.h
)

target_include_directories(communication_lib PUBLIC ${BOOST_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(communication_lib ${AERON_LIBS})
add_dependencies(communication_lib aeron)

### Tests ####

add_executable(communication_tests tests/EmbeddedAeronMediaDriver.h tests/main_test.cpp)

target_link_libraries(communication_tests PRIVATE
        communication_lib
        GTest::gtest_main
        GTest::gtest
)

include(GoogleTest)