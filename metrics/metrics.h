#pragma once

#include <string>
#include <boost/algorithm/string.hpp>

static void normalize_name(std::string &name) {
    boost::trim(name);
    boost::to_lower(name);
    boost::replace_all(name, " ", "_");

    name = "streams_" + name;
}

class Metric {
public:
    std::string name;
    std::string help;

    explicit Metric(std::string name, std::string help = "") : name(std::move(name)), help(std::move(help)) {
        normalize_name(this->name);
    }

    virtual ~Metric() = default;

    [[nodiscard]] virtual std::string_view to_prometheus() = 0;
};
