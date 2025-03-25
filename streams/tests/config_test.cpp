#include <gtest/gtest.h>
#include <fstream>
#include <cstdio> // for std::remove
#include "config.h"
#include <yaml-cpp/yaml.h>

class ConfigTest : public ::testing::Test
{
protected:
    void SetUp() override
    {
        // Create a temporary config file for testing
        createTestConfigFile();
    }

    void TearDown() override
    {
        // Clean up the temporary file
        std::remove(test_config_file.c_str());
    }

    void createTestConfigFile() const
    {
        std::ofstream config_file(test_config_file);
        config_file << "nats:\n";
        config_file << "  url: nats://localhost:4222\n";
        config_file << "exchanges:\n";
        config_file << "  binance: true\n";
        config_file << "  unknown: false\n";
        config_file << "symbol: BTCUSD\n";
        config_file.close();
    }

    std::string test_config_file = "test_config.yaml";
};

TEST_F(ConfigTest, LoadConfigFile)
{
    // Load the test configuration file
    Config config = load(test_config_file);

    // Check NATS URL
    EXPECT_EQ(config.nats_url, "nats://localhost:4222");

    // Check exchanges, exchanges are on a per-exchange basis and not automatically loaded
    ASSERT_EQ(config.exchanges.size(), 1);
    EXPECT_TRUE(config.exchanges.at("binance"));
    EXPECT_THROW(config.exchanges.at("unknown"), std::out_of_range);

    // Check symbol
    EXPECT_EQ(config.symbol, "BTCUSD");
}

TEST_F(ConfigTest, MissingConfigFile)
{
    // Try to load a non-existent file
    EXPECT_THROW(load("non_existent_config.yaml"), YAML::BadFile);
}

// Test with a malformed YAML file
TEST_F(ConfigTest, MalformedYamlFile)
{
    // Create a malformed YAML file
    std::string malformed_file = "malformed_config.yaml";
    std::ofstream config_file(malformed_file);
    config_file << "nats:\n";
    config_file << "url: nats://localhost:4222\n"; // Intentionally malformed (missing proper indentation)
    config_file << "exchanges:\n";
    config_file << "  binance: true\n";
    config_file.close();

    // Expect a parsing exception
    EXPECT_THROW(load(malformed_file), YAML::RepresentationException);

    // Clean up
    std::remove(malformed_file.c_str());
}

// Test for missing required fields
TEST_F(ConfigTest, MissingRequiredFields)
{
    // Create a config file missing required fields
    std::string incomplete_file = "incomplete_config.yaml";
    std::ofstream config_file(incomplete_file);
    config_file << "nats:\n";
    config_file << "  url: nats://localhost:4222\n";
    // Missing exchanges and symbol
    config_file.close();

    // Expect exception when accessing missing fields
    EXPECT_THROW(load(incomplete_file), YAML::TypedBadConversion<bool>);

    // Clean up
    std::remove(incomplete_file.c_str());
}

// Test with additional fields that aren't used
TEST_F(ConfigTest, AdditionalFields)
{
    // Create a config file with extra fields
    std::string extra_fields_file = "extra_fields_config.yaml";
    std::ofstream config_file(extra_fields_file);
    config_file << "nats:\n";
    config_file << "  url: nats://localhost:4222\n";
    config_file << "  unused_field: value\n";
    config_file << "exchanges:\n";
    config_file << "  binance: true\n";
    config_file << "symbol: BTCUSD\n";
    config_file << "extra:\n";
    config_file << "  field1: value1\n";
    config_file << "  field2: value2\n";
    config_file.close();

    // Should load successfully despite extra fields
    Config config = load(extra_fields_file);

    // Verify the fields we care about are loaded correctly
    EXPECT_EQ(config.nats_url, "nats://localhost:4222");
    EXPECT_TRUE(config.exchanges.at("binance"));
    EXPECT_EQ(config.symbol, "BTCUSD");

    // Clean up
    std::remove(extra_fields_file.c_str());
}

// Test the default config file path
TEST_F(ConfigTest, DefaultConfigPath)
{
    // Create a config file with the default name
    std::string default_file = "config.yaml";
    std::ofstream config_file(default_file);
    config_file << "nats:\n";
    config_file << "  url: nats://default:4222\n";
    config_file << "exchanges:\n";
    config_file << "  binance: true\n";
    config_file << "symbol: XRPUSD\n";
    config_file.close();

    // Load without specifying a path (should use default)
    Config config = load();

    // Verify loaded correctly
    EXPECT_EQ(config.nats_url, "nats://default:4222");
    EXPECT_TRUE(config.exchanges.at("binance"));
    EXPECT_EQ(config.symbol, "XRPUSD");

    // Clean up
    std::remove(default_file.c_str());
}
