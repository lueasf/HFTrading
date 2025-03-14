#include "metrics.h"

Metrics::Metrics(NatsClient& nats_client): m_nats_client(nats_client)
{
}


void Metrics::send_order(const OrderType orderType) const
{
    switch (orderType)
    {
    case BUY:
        m_nats_client.publish("BUY");
        break;
    case SELL:
        m_nats_client.publish("SELL");
        break;
    default:
        break;
    }
}
