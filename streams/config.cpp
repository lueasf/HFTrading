#include "config.h"
#include <yaml-cpp/yaml.h>

Config load(const std::string& config_file)
{
    YAML::Node config = YAML::LoadFile(config_file);

    // NATS
    std::string nats_url = config["nats"]["url"].as<std::string>();

    // EXCHANGES
    bool binance = config["exchanges"]["binance"].as<bool>();

    // SYMBOL
    std::string symbol = config["symbol"].as<std::string>();

    Config cfg;
    cfg.nats_url = nats_url;
    cfg.exchanges = {{"binance", binance}};
    cfg.symbol = symbol;

    return cfg;
}

std::ostream& operator<<(std::ostream& os, const Config& config)
{
    os << "NATS URL: " << config.nats_url << std::endl;
    os << "Exchanges: " << std::endl;
    for (const auto& exchange : config.exchanges)
    {
        os << "  " << exchange.first << ": " << exchange.second << std::endl;
    }
    os << "Symbol: " << config.symbol << std::endl;
    return os;
}
