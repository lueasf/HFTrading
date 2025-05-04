#pragma once
#include "communication/nats/nats_client.h"

enum OrderType
{
    BUY,
    SELL
};

class Metrics
{
public:
    Metrics(INatsClient& nats_client);

    void send_order(const std::string &symbol, OrderType orderType) const;
    void send_latency(const std::string &symbol, long long latency) const;

private:
    INatsClient& m_nats_client;
};
