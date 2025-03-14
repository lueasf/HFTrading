#include "nats_client.h"

NatsClient::NatsClient()
{
    m_nc = NULL;
    m_sub = NULL;
    m_msg = NULL;
}

NatsClient::~NatsClient()
{
    if (m_nc != NULL)
    {
        natsConnection_Destroy(m_nc);
        m_nc = NULL;
    }
}

int NatsClient::connect()
{
    natsConnection_ConnectTo(&m_nc, NATS_DEFAULT_URL);
    if (m_nc == nullptr)
    {
        return -1;
    }
    return 0;
}

void NatsClient::publish(std::string value) const
{
    natsConnection_PublishString(m_nc, "foo", value.c_str());
}
