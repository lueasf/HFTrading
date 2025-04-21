#pragma once

#include <thread>
#include <atomic>
#include <httplib.h>
#include "registry.h"

class metrics_exporter {
    std::thread server_thread;
    std::atomic<bool> running{false};

public:
    void start(int port = 8080) {
        running = true;
        server_thread = std::thread([this, port]() {
            httplib::Server svr;

            svr.Get("/metrics", [](const httplib::Request &, httplib::Response &res) {
                res.set_content(MetricsRegistry::instance().render_all(), "text/plain");
            });

            std::cout << "Metrics HTTP server running on http://localhost:" << port << "/metrics\n";
            svr.listen("0.0.0.0", port);
        });
    }

    void stop() {
        running = false;
        if (server_thread.joinable()) server_thread.detach();
    }

    ~metrics_exporter() {
        stop();
    }
};
