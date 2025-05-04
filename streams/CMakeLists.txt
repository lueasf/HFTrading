include(FetchContent)
FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_library(streams_lib
        websocket_client.h
        binance_websocket_client.h
        metrics.cpp
        metrics.h
        config.cpp
        stream_metrics.h
        config.h
)

target_include_directories(streams_lib PUBLIC
        ${BOOST_INCLUDE_DIRS}
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_SOURCE_DIR}
)

target_link_libraries(streams_lib PRIVATE Boost::asio
        Boost::beast
        nlohmann_json::nlohmann_json
        fmt::fmt
        OpenSSL::SSL
        OpenSSL::Crypto
        cnats::nats_static
        yaml-cpp::yaml-cpp
        GTest::gtest_main
        GTest::gtest

        $<IF:$<TARGET_EXISTS:hdr_histogram::hdr_histogram>,hdr_histogram::hdr_histogram,hdr_histogram::hdr_histogram_static>

        metrics_lib
        communication_lib
)

add_executable(streams_exec main.cpp)
target_link_libraries(streams_exec PRIVATE argparse::argparse streams_lib)

add_executable(streams_test tests/main_test.cpp tests/metrics_test.cpp tests/nats_client_test.cpp tests/config_test.cpp)
target_link_libraries(streams_test PRIVATE streams_lib GTest::gtest_main GTest::gtest GTest::gmock GTest::gmock_main)

include(GoogleTest)
gtest_discover_tests(streams_test)