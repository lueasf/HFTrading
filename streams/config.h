#pragma once

#include <string>
#include <unordered_map>

struct Config
{
    std::string nats_url;
    std::pmr::unordered_map<std::string, bool> exchanges;
    std::string symbol;
};

Config load(const std::string& config_file = "config.yaml");

std::ostream& operator<<(std::ostream& os, const Config& config);
