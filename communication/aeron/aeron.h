#pragma once
#include <Aeron.h>
#include <Context.h>

class AeronConnection {
public:
    int connect() {
        if (aeron && !aeron->isClosed()) {
            std::cerr << "Already connected to Aeron." << std::endl;
            return 0; // Already connected
        }
        try {
            aeron = aeron::Aeron::connect(context);
            return 0;
        } catch (const std::exception &e) {
            std::cerr << "Error connecting to Aeron: " << e.what() << std::endl;
            return -1;
        }
    }

    bool isConnected() const {
        return aeron && !aeron->isClosed();
    }

    std::shared_ptr<aeron::Publication>
    addPublication(const std::string &channel, const int32_t streamId = 10001) const {
        if (!isConnected()) {
            std::cerr << "Not connected to Aeron." << std::endl;
            return nullptr;
        }
        try {
            const int64_t publicationId = aeron->addPublication(channel, streamId);
            auto publication = aeron->findPublication(publicationId);
            int attempts = 0;
            while (publication == nullptr && attempts < 100) {
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                publication = aeron->findPublication(publicationId);
                attempts++;
            }
            if (publication) {
                std::cout << "Publication added successfully: " << publicationId << std::endl;
                return publication;
            }
            std::cerr << "Failed to find publication after adding." << std::endl;
            return nullptr;
        } catch (const std::exception &e) {
            std::cerr << "Error adding publication: " << e.what() << std::endl;
            return nullptr;
        }
    }

    static int publish(const std::shared_ptr<aeron::Publication> &publication, std::string &message) {
        if (!publication || !publication->isConnected()) {
            std::cerr << "Publication is not yet connected." << std::endl;
            //return -1;
        }
        const size_t messageSize = message.size();

        auto *buffer = reinterpret_cast<uint8_t *>(message.data());
        const aeron::AtomicBuffer messageBuffer(buffer, messageSize);

        return publication->offer(messageBuffer);
    }

    std::shared_ptr<aeron::Subscription> addSubscription(const std::string &channel,
                                                         const int32_t streamId = 10001) const {
        if (!isConnected()) {
            std::cerr << "Not connected to Aeron." << std::endl;
            return nullptr;
        }
        try {
            const int64_t subscriptionId = aeron->addSubscription(channel, streamId);
            auto subscription = aeron->findSubscription(subscriptionId);
            int attempts = 0;
            while (subscription == nullptr && attempts < 100) {
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                subscription = aeron->findSubscription(subscriptionId);
                attempts++;
            }
            if (subscription) {
                std::cout << "Subscription added successfully: " << subscriptionId << std::endl;
                return subscription;
            }
            std::cerr << "Failed to find subscription after adding." << std::endl;
            return nullptr;
        } catch (const std::exception &e) {
            std::cerr << "Error adding subscription: " << e.what() << std::endl;
            return nullptr;
        }
    }

    static void subscribe(const std::shared_ptr<aeron::Subscription> &subscription,
                          std::function<void(const std::string &)> handler) {
        if (!subscription || !subscription->isConnected()) {
            std::cerr << "Subscription is not yet connected." << std::endl;
            //return;
        }
        auto fragmentHandler = [handler](const aeron::AtomicBuffer &buf, const aeron::util::index_t offset,
                                         const aeron::util::index_t length, const aeron::Header &header) {
            const std::string receivedMessage(reinterpret_cast<const char *>(buf.buffer() + offset), length);
            handler(receivedMessage);
        };
        while (subscription->poll(fragmentHandler, 1) == 0) {
        }
    }

private:
    aeron::Context context;
    std::shared_ptr<aeron::Aeron> aeron;
};
