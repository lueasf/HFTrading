#include <gtest/gtest.h>
#include "Aeron.h"
#include "EmbeddedAeronMediaDriver.h"

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

class AeronTest : public ::testing::Test {
protected:
    aeron::Context context;
    std::shared_ptr<aeron::Aeron> aeron;

    void SetUp() override {
        try {
            aeron = aeron::Aeron::connect(context);
        } catch (const std::exception &e) {
            FAIL() << "Exception during Aeron initialization: " << e.what();
        }
    }
};

TEST_F(AeronTest, ConnectsSuccessfully) {
    ASSERT_NE(aeron, nullptr);
}

TEST_F(AeronTest, CanCreatePublicationAndSubscription) {
    ASSERT_NE(aeron, nullptr);

    const int64_t pubId = aeron->addPublication("aeron:ipc", 1001);
    const int64_t subId = aeron->addSubscription("aeron:ipc", 1001);

    ASSERT_GT(pubId, 0);
    ASSERT_GT(subId, 0);
}

TEST_F(AeronTest, CanFindPublication) {
    ASSERT_NE(aeron, nullptr);

    const int64_t pubId = aeron->addPublication("aeron:ipc", 1001);

    ASSERT_GT(pubId, 0);

    auto publication = aeron->findPublication(pubId);
    // findPublication is non-blocking, so we need to wait until the publication is available
    while (publication == nullptr) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        publication = aeron->findPublication(pubId);
    }

    ASSERT_NE(publication, nullptr);
    EXPECT_EQ(publication->registrationId(), pubId);
}

TEST_F(AeronTest, CanFindSubscription) {
    ASSERT_NE(aeron, nullptr);

    const int64_t subId = aeron->addSubscription("aeron:ipc", 1001);

    ASSERT_GT(subId, 0);

    auto subscription = aeron->findSubscription(subId);
    // findSubscription is non-blocking, so we need to wait until the subscription is available
    while (subscription == nullptr) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        subscription = aeron->findSubscription(subId);
    }

    ASSERT_NE(subscription, nullptr);
    EXPECT_EQ(subscription->registrationId(), subId);
}

TEST_F(AeronTest, SendAndReceiveMessage) {
    ASSERT_NE(aeron, nullptr);

    const int64_t pubId = aeron->addPublication("aeron:ipc", 1001);
    const int64_t subId = aeron->addSubscription("aeron:ipc", 1001);

    ASSERT_GT(pubId, 0);
    ASSERT_GT(subId, 0);

    auto publication = aeron->findPublication(pubId);
    auto subscription = aeron->findSubscription(subId);

    // Wait for publication and subscription to be available
    while (publication == nullptr || subscription == nullptr) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        publication = aeron->findPublication(pubId);
        subscription = aeron->findSubscription(subId);
    }

    // Create a simple message
    std::string message = "Hello Aeron!";
    const size_t messageSize = message.size();

    auto *buffer = reinterpret_cast<uint8_t *>(message.data());
    const aeron::AtomicBuffer messageBuffer(buffer, messageSize);

    // Send the message
    const auto result = publication->offer(messageBuffer);
    ASSERT_GT(result, 0); // Greater than zero indicates success

    // Receive the message
    auto fragmentHandler = [](const aeron::AtomicBuffer &buf, const aeron::util::index_t offset,
                              const aeron::util::index_t length, const aeron::Header &header) {
        const std::string receivedMessage(reinterpret_cast<const char *>(buf.buffer() + offset), length);
        EXPECT_EQ(receivedMessage, "Hello Aeron!");
    };

    while (subscription->poll(fragmentHandler, 1) == 0) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

TEST_F(AeronTest, PublicationAndSubscriptionLifecycle) {
    ASSERT_NE(aeron, nullptr);

    const int64_t pubId = aeron->addPublication("aeron:ipc", 1001);
    const int64_t subId = aeron->addSubscription("aeron:ipc", 1001);

    ASSERT_GT(pubId, 0);
    ASSERT_GT(subId, 0);

    auto publication = aeron->findPublication(pubId);
    auto subscription = aeron->findSubscription(subId);

    // Wait for publication and subscription to be available
    while (publication == nullptr || subscription == nullptr) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        publication = aeron->findPublication(pubId);
        subscription = aeron->findSubscription(subId);
    }

    // Check if publication and subscription are active
    EXPECT_TRUE(publication->isConnected());
    EXPECT_TRUE(subscription->isConnected());

    // Close the publication and subscription
    publication->close();
    subscription->closeAndRemoveImages();

    // Verify they are closed
    EXPECT_FALSE(publication->isConnected());
    EXPECT_FALSE(subscription->isConnected());
}
