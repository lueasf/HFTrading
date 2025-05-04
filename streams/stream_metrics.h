#pragma once

#include "metrics/registry.h"
#include "metrics/rolling_histogram.h"
#include "metrics/metrics_exporter.h"

inline std::shared_ptr<RollingHistogram> latency_metric;

inline void init_metrics() {
    latency_metric = std::make_shared<RollingHistogram>("Trade latency", "Trade latency in ms");

    MetricsRegistry::instance().register_metric(latency_metric);

    metrics_exporter exporter;
    exporter.start();
}

inline void mark_latency(const std::string &exchange, const std::string &symbol, const long long latency) {
    latency_metric->record(latency, {{"exchange", exchange}, {"symbol", symbol}});
}
