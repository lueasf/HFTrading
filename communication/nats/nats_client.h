#pragma once

#include <string>
#include <unordered_map>
#include <nats/nats.h>

struct metric_message {
    std::string name;
    std::string value;
    std::unordered_map<std::string, std::string> labels;
};

// Interface for NatsClient to enable mocking
class INatsClient {
public:
    virtual ~INatsClient() = default;

    virtual int connect() = 0;

    virtual void publish_raw(std::string subject, std::string value) const = 0;
};

class NatsClient final : public INatsClient {
public:
    NatsClient();

    ~NatsClient() override;

    int connect() override;

    void publish_raw(std::string subject, std::string value) const override;

private:
    natsConnection *m_nc;
    natsSubscription *m_sub;
    natsMsg *m_msg;
};
