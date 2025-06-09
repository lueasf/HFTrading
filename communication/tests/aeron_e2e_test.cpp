#include <gtest/gtest.h>
#include "Aeron.h"
#include "aeron/aeron.h"
#include "aeron/publisher.h"
#include "aeron/subscriber.h"

TEST(AeronE2ETest, SubscribeAndPublish) {
    AeronConnection aeronConnection;
    const int result = aeronConnection.connect();
    ASSERT_EQ(result, 0) << "Failed to connect to Aeron";

    const auto connection = std::make_shared<AeronConnection>(aeronConnection);
    AeronSubscriber aeronSubscriber(connection);
    std::atomic gotResult = false;
    const int subscriptionResult = aeronSubscriber.subscribe(
        "aeron:ipc",
        [&gotResult](const std::string &message) {
            EXPECT_EQ(message, "Hello Aeron!");
            gotResult = true;
        }
    );
    ASSERT_EQ(subscriptionResult, 0) << "Failed to subscribe to channel";

    AeronPublisher aeronPublisher(connection);
    std::string message = "Hello Aeron!";
    const int publishResult = aeronPublisher.publish("aeron:ipc", message);
    ASSERT_GT(publishResult, 0) << "Failed to publish message";

    // Wait for the message to be received
    std::this_thread::sleep_for(std::chrono::seconds(1));
    ASSERT_TRUE(gotResult) << "Message was not received by subscriber";
}
