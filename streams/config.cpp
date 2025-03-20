#include "config.h"
#include <iostream>
#include <yaml-cpp/yaml.h>

void load(const std::string &config_file) {
    YAML::Node config = YAML::LoadFile(config_file);
    std::cout << config["nats"]["url"] << std::endl;
}
