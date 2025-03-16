#ifndef NATS_CLIENT_H
#define NATS_CLIENT_H

#include <map>
#include <string>
#include <unordered_map>
#include <nats/nats.h>


struct metric_message {
    std::string name;
    std::string value;
    std::unordered_map<std::string, std::string> labels;
};

inline metric_message make_metric_message(const std::string &name, const std::string &value,
                                          const std::unordered_map<std::string, std::string> &labels) {
    return metric_message{name, value, labels};
}

inline std::string to_nats_message(metric_message message) {
    std::string result;
    result += message.value + "\n";
    for (const auto &label : message.labels) {
        result += label.first + "=\"" + label.second + "\",";
    }
    return result;
}

class NatsClient {
public:
    NatsClient();

    virtual ~NatsClient();

    int connect();

    void publish(std::string value) const;

    void publish(const metric_message &message) const;

private:
    natsConnection *m_nc;
    natsSubscription *m_sub;
    natsMsg *m_msg;
};


#endif //NATS_CLIENT_H
