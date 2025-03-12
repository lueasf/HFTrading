add_library(streams_lib websocket_client.h binance_websocket_client.cpp)

target_include_directories(streams_lib PUBLIC ${BOOST_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(streams_lib PRIVATE Boost::asio Boost::beast nlohmann_json::nlohmann_json fmt::fmt OpenSSL::SSL OpenSSL::Crypto)

add_executable(streams_exec main.cpp)
target_link_libraries(streams_exec PRIVATE streams_lib)