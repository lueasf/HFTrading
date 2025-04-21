#pragma once

#include <string>

class Metric {
public:
    std::string name;
    std::string help;

    explicit Metric(std::string name, std::string help = "") : name(std::move(name)), help(std::move(help)) {
    }

    virtual ~Metric() = default;

    [[nodiscard]] virtual std::string to_prometheus() const = 0;
};
