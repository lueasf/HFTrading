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
    std::unique_ptr<aeron::EmbeddedMediaDriver> driver;
    std::shared_ptr<aeron::Aeron> aeron;

    void SetUp() override {
        driver = std::make_unique<aeron::EmbeddedMediaDriver>();
        driver->start();

        try {
            aeron = aeron::Aeron::connect(context);
        } catch (const std::exception &e) {
            FAIL() << "Exception during Aeron initialization: " << e.what();
        }
    }

    void TearDown() override {
        if (driver) {
            driver->stop();
        }
    }
};

TEST_F(AeronTest, ConnectsSuccessfully) {
    ASSERT_NE(aeron, nullptr);
}

TEST_F(AeronTest, CanCreatePublicationAndSubscription) {
    ASSERT_NE(aeron, nullptr);

    int64_t pubId = aeron->addPublication("aeron:ipc", 1001);
    int64_t subId = aeron->addSubscription("aeron:ipc", 1001);

    ASSERT_GT(pubId, 0);
    ASSERT_GT(subId, 0);
}
