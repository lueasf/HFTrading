#pragma once
#include <memory>

#include "aeron.h"

class AeronPublisher {
public:
    explicit AeronPublisher(std::shared_ptr<AeronConnection> connection)
        : aeronConnection(std::move(connection)) {
        if (!aeronConnection || !aeronConnection->isConnected()) {
            std::cerr << "Aeron connection is not established." << std::endl;
        }
    }

    int publish(const std::string &channel, std::string &message) {
        if (!aeronConnection || !aeronConnection->isConnected()) {
            std::cerr << "Aeron connection is not established." << std::endl;
            return -1;
        }
        auto publication = publications[channel];
        if (!publication) {
            publication = aeronConnection->addPublication(channel);
            if (!publication) {
                std::cerr << "Failed to create or find publication for channel: " << channel << std::endl;
                return -1;
            }
            publications[channel] = publication;
        }
        /*if (!publication->isConnected()) {
            std::cerr << "Publication is not connected." << std::endl;
            return -1;
        }*/
        return AeronConnection::publish(publication, message);
    }

private:
    std::shared_ptr<AeronConnection> aeronConnection;
    std::unordered_map<std::string, std::shared_ptr<aeron::Publication> > publications;
};
