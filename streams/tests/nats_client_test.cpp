#include <gtest/gtest.h>
#include "nats_client.h"

// Test utility functions
TEST(NatsClientTest, ToNatsMessage) {
    metric_message msg;
    msg.name = "test_metric";
    msg.value = "42";
    msg.labels["symbol"] = "SYMBOL";
    msg.labels["exchange"] = "EXCHANGE";

    std::string formatted = to_nats_message(msg);

    // Check that it contains the value and labels
    EXPECT_TRUE(formatted.find("42\n") != std::string::npos);
    EXPECT_TRUE(formatted.find("symbol=\"SYMBOL\"") != std::string::npos);
    EXPECT_TRUE(formatted.find("exchange=\"EXCHANGE\"") != std::string::npos);
}

TEST(NatsClientTest, MakeMetricMessage) {
    std::unordered_map<std::string, std::string> labels = {{"symbol", "SYMBOL"}, {"type", "stock"}};
    auto msg = make_metric_message("price", "150.25", labels);

    EXPECT_EQ(msg.name, "price");
    EXPECT_EQ(msg.value, "150.25");
    EXPECT_EQ(msg.labels.size(), 2);
    EXPECT_EQ(msg.labels["symbol"], "SYMBOL");
    EXPECT_EQ(msg.labels["type"], "stock");
}
