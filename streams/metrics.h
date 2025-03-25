#pragma once
#include "nats_client.h"

enum OrderType
{
    BUY,
    SELL
};

class Metrics
{
public:
    Metrics(INatsClient& nats_client);

    void send_order(std::string symbol, OrderType orderType) const;
    void send_latency(std::string symbol, long long latency) const;

private:
    INatsClient& m_nats_client;
};
