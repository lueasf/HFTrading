#pragma once
#include <memory>

#include "aeron.h"

class AeronSubscriber {
public:
    int subscribe(const std::string &channel, const std::function<void(const std::string &)> &handler) {
        if (!aeronConnection || !aeronConnection->isConnected()) {
            std::cerr << "Aeron connection is not established." << std::endl;
            return -1;
        }
        auto subscription = subscriptions[channel];
        if (!subscription) {
            subscription = aeronConnection->addSubscription(channel);
            if (!subscription) {
                std::cerr << "Failed to create or find subscription for channel: " << channel << std::endl;
                return -1;
            }
            subscriptions[channel] = subscription;
        }
        if (!subscription->isConnected()) {
            std::cerr << "Subscription is not connected." << std::endl;
            return -1;
        }
        AeronConnection::subscribe(subscription, handler);
        return 0;
    }

private:
    std::shared_ptr<AeronConnection> aeronConnection;
    std::unordered_map<std::string, std::shared_ptr<aeron::Subscription> > subscriptions;
};
