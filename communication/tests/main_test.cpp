#include <gtest/gtest.h>
#include "Aeron.h"

int main(int argc, char** argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}


TEST(AeronTest, test)
{
    aeron::Context context;
    std::shared_ptr<aeron::Aeron> aeron = aeron::Aeron::connect(context);
    ASSERT_TRUE(aeron != nullptr);
    aeron->addPublication("aeron:ipc", 1001);
    aeron->addSubscription("aeron:ipc", 1001);
}
