#include <iostream>
#include <yaml-cpp/yaml.h>

void load()
{
    const auto file = "config.yaml";
    YAML::Node config = YAML::LoadFile(file);
    std::cout << config["nats"]["url"] << std::endl;
}
