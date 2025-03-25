#pragma once

#include <string>
#include <unordered_map>
#include <nats/nats.h>

struct metric_message
{
    std::string name;
    std::string value;
    std::unordered_map<std::string, std::string> labels;
};

inline metric_message make_metric_message(const std::string& name, const std::string& value,
                                          const std::unordered_map<std::string, std::string>& labels)
{
    return metric_message{name, value, labels};
}

inline std::string to_nats_message(metric_message message)
{
    std::string result;
    result += message.value + "\n";
    for (const auto& label : message.labels)
    {
        result += label.first + "=\"" + label.second + "\",";
    }
    return result;
}

// Interface for NatsClient to enable mocking
class INatsClient
{
public:
    virtual ~INatsClient() = default;
    virtual int connect() = 0;
    virtual void publish_raw(std::string value) const = 0;
    virtual void publish(const metric_message& message) const = 0;
};

class NatsClient : public INatsClient
{
public:
    NatsClient();
    virtual ~NatsClient();

    int connect() override;
    void publish_raw(std::string value) const override;
    void publish(const metric_message& message) const override;

private:
    natsConnection* m_nc;
    natsSubscription* m_sub;
    natsMsg* m_msg;
};
