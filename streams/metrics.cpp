#include "metrics.h"
#include "nats_client.h"


// handle trade events and send them to NATS
Metrics::Metrics(INatsClient& nats_client): m_nats_client(nats_client)
{
}


void Metrics::send_order(std::string symbol, const OrderType orderType) const
{
    std::unordered_map<std::string, std::string> labels;
    labels["symbol"] = symbol;
    switch (orderType)
    {
    case BUY:
        m_nats_client.publish(make_metric_message("orders", "BUY", labels));
        break;
    case SELL:
        m_nats_client.publish(make_metric_message("orders", "SELL", labels));
        break;
    default:
        break;
    }
}

void Metrics::send_latency(std::string symbol, long long latency) const
{
    std::unordered_map<std::string, std::string> labels;
    labels["symbol"] = symbol;
    m_nats_client.publish(make_metric_message("latency", std::to_string(latency), labels));
}
