add_library(metrics_lib INTERFACE)
target_sources(metrics_lib INTERFACE metrics.h metrics_exporter.h registry.h)
target_include_directories(metrics_lib INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(metrics_lib INTERFACE httplib::httplib)