#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "metrics.h"
#include "nats_client.h"

// Mock NatsClient for testing
class MockNatsClient : public INatsClient
{
public:
    MOCK_METHOD(int, connect, (), (override));
    MOCK_METHOD(void, publish_raw, (std::string), (const, override));
    MOCK_METHOD(void, publish, (const metric_message&), (const, override));
};

class MetricsTest : public ::testing::Test
{
protected:
    MockNatsClient mock_nats_client;
};

TEST_F(MetricsTest, SendOrderBuy)
{
    Metrics metrics(mock_nats_client);

    // Set up expectations
    EXPECT_CALL(mock_nats_client, publish(::testing::_))
        .Times(1)
        .WillOnce([](const metric_message& msg)
                                                        {
                                                            EXPECT_EQ(msg.name, "orders");
                                                            EXPECT_EQ(msg.value, "BUY");
                                                            EXPECT_EQ(msg.labels.at("symbol"), "SYMBOL");
                                                        });

    // Call the method under test
    metrics.send_order("SYMBOL", BUY);
}

TEST_F(MetricsTest, SendOrderSell)
{
    Metrics metrics(mock_nats_client);

    // Set up expectations
    EXPECT_CALL(mock_nats_client, publish(::testing::_))
        .Times(1)
        .WillOnce([](const metric_message& msg)
                                                        {
                                                            EXPECT_EQ(msg.name, "orders");
                                                            EXPECT_EQ(msg.value, "SELL");
                                                            EXPECT_EQ(msg.labels.at("symbol"), "SYMBOL");
                                                        });

    // Call the method under test
    metrics.send_order("SYMBOL", SELL);
}

TEST_F(MetricsTest, SendLatency)
{
    Metrics metrics(mock_nats_client);

    // Set up expectations
    EXPECT_CALL(mock_nats_client, publish(::testing::_))
        .Times(1)
        .WillOnce([](const metric_message& msg)
                                                        {
                                                            EXPECT_EQ(msg.name, "latency");
                                                            EXPECT_EQ(msg.value, "100");
                                                            EXPECT_EQ(msg.labels.at("symbol"), "SYMBOL");
                                                        });

    // Call the method under test
    metrics.send_latency("SYMBOL", 100);
}
