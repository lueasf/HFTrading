include(FetchContent)
FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_library(algos_lib
        regression.cpp
)

target_include_directories(algos_lib PUBLIC ${BOOST_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(algos_lib PRIVATE Boost::asio
        nlohmann_json::nlohmann_json
        fmt::fmt
        OpenSSL::SSL
        OpenSSL::Crypto
        yaml-cpp::yaml-cpp
        GTest::gtest_main
        GTest::gtest
)

add_executable(algos_exec main.cpp)
target_link_libraries(algos_exec PRIVATE algos_lib)

include(GoogleTest)