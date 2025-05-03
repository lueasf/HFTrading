#pragma once
#include "hdr/hdr_histogram.h"
#include <mutex>
#include <thread>
#include <atomic>
#include <chrono>
#include <string>
#include <sstream>
#include <map>
#include <memory>

#include "metrics.h"

#define INTERVAL_MS 5000

// Helper struct to hold a pair of histograms
struct HistogramPair {
    hdr_histogram *hist_a;
    hdr_histogram *hist_b;
    hdr_histogram *active;
    hdr_histogram *inactive;

    HistogramPair() : hist_a(nullptr), hist_b(nullptr), active(nullptr), inactive(nullptr) {
        hdr_init(1, 3600000000LL, 3, &hist_a);
        hdr_init(1, 3600000000LL, 3, &hist_b);
        active = hist_a;
        inactive = hist_b;
    }

    ~HistogramPair() {
        if (hist_a) hdr_close(hist_a);
        if (hist_b) hdr_close(hist_b);
    }

    void swap_active_inactive() {
        std::swap(active, inactive);
        hdr_reset(active);
    }
};

class RollingHistogram final : public Metric {
    std::map<std::string, std::unique_ptr<HistogramPair> > histograms;
    std::mutex histograms_mtx;
    std::thread swap_thread;
    std::atomic<bool> running{false};
    std::string prometheus_output;
    int swap_interval_ms = 5000;

    void swap_loop() {
        while (running) {
            std::this_thread::sleep_for(std::chrono::milliseconds(swap_interval_ms));
            std::lock_guard lock(histograms_mtx);
            for (auto &[_, hist_pair]: histograms) {
                hist_pair->swap_active_inactive();
            }
            generate_prometheus_output();
        }
    }

    void generate_prometheus_output() {
        std::ostringstream oss;
        oss << "# HELP " << name << " " << help << "\n";
        oss << "# TYPE " << name << " summary\n";

        for (const auto &[key, hist_pair]: histograms) {
            // Parse the key back into labels
            std::map<std::string, std::string> labels;
            std::istringstream key_stream(key);
            std::string label_pair;
            while (std::getline(key_stream, label_pair, ';')) {
                if (label_pair.empty()) continue;
                size_t pos = label_pair.find('=');
                if (pos != std::string::npos) {
                    labels[label_pair.substr(0, pos)] = label_pair.substr(pos + 1);
                }
            }

            std::string base_labels = format_labels(labels);

            for (const double p: {50.0, 90.0, 95.0, 99.0, 99.9}) {
                oss << name;
                if (base_labels.empty()) {
                    oss << "{quantile=\"" << p / 100 << "\"}";
                } else {
                    oss << base_labels.substr(0, base_labels.length() - 1)
                            << ",quantile=\"" << p / 100 << "\"}";
                }
                oss << " " << hdr_value_at_percentile(hist_pair->inactive, p) << "\n";
            }

            double sum = hdr_mean(hist_pair->inactive) * static_cast<double>(hist_pair->inactive->total_count);

            oss << name << "_sum" << base_labels << " " << sum << "\n";
            oss << name << "_count" << base_labels << " " << hist_pair->inactive->total_count << "\n";
        }

        prometheus_output = oss.str();
    }

    static std::string make_label_key(const std::map<std::string, std::string> &labels) {
        std::ostringstream oss;
        for (const auto &[key, value]: labels) {
            oss << key << "=" << value << ";";
        }
        return oss.str();
    }

    static std::string format_labels(const std::map<std::string, std::string> &labels) {
        if (labels.empty()) return "";

        std::ostringstream oss;
        oss << "{";
        bool first = true;
        for (const auto &[key, value]: labels) {
            if (!first) oss << ",";
            oss << key << "=\"" << value << "\"";
            first = false;
        }
        oss << "}";
        return oss.str();
    }

public:
    explicit RollingHistogram(const std::string &name, const std::string &help,
                              const int interval_ms = INTERVAL_MS) : Metric(name, help),
                                                                     swap_interval_ms(interval_ms) {
        running = true;
        swap_thread = std::thread([this]() { swap_loop(); });
    }

    void record(const int64_t value, const std::map<std::string, std::string> &labels) {
        std::lock_guard lock(histograms_mtx);
        const std::string key = make_label_key(labels);
        auto &hist_pair = histograms[key];
        if (!hist_pair) {
            hist_pair = std::make_unique<HistogramPair>();
        }
        hdr_record_value(hist_pair->active, value);
    }

    std::string_view to_prometheus() override {
        return prometheus_output;
    }

    ~RollingHistogram() override {
        running = false;
        if (swap_thread.joinable()) swap_thread.join();
    }
};
