#ifndef METRICS_H
#define METRICS_H
#include "nats_client.h"

enum OrderType
{
    BUY,
    SELL
};

class Metrics
{
public:
    Metrics(NatsClient &nats_client);

    void send_order(std::string symbol, OrderType orderType) const;
    void send_latency(std::string symbol, long long latency) const;

private:
    NatsClient &m_nats_client;
};


#endif //METRICS_H
