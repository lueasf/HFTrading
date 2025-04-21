#pragma once

#include <vector>
#include <mutex>
#include <sstream>
#include "metrics.h"

class MetricsRegistry {
    std::vector<std::shared_ptr<Metric> > metrics;
    std::mutex mtx;

public:
    void register_metric(const std::shared_ptr<Metric> &m) {
        std::lock_guard lock(mtx);
        metrics.push_back(m);
    }

    [[nodiscard]] std::string render_all() const {
        std::ostringstream oss;
        for (const auto &m: metrics) {
            oss << m->to_prometheus() << "\n";
        }
        return oss.str();
    }

    static MetricsRegistry &instance() {
        static MetricsRegistry reg;
        return reg;
    }
};
