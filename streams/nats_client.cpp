#include "nats_client.h"

// https://github.com/nats-io/nats.c
// connect to nats and publish trade events.
NatsClient::NatsClient() {
    m_nc = NULL;
    m_sub = NULL;
    m_msg = NULL;
}

NatsClient::~NatsClient() {
    if (m_nc != NULL) {
        natsConnection_Destroy(m_nc);
        m_nc = NULL;
    }
}

int NatsClient::connect() {
    natsConnection_ConnectTo(&m_nc, NATS_DEFAULT_URL);
    if (m_nc == nullptr) {
        // TODO: try to reconnect until successful
        return -1;
    }
    return 0;
}

void NatsClient::publish(std::string value) const {
    natsConnection_PublishString(m_nc, "foo", value.c_str());
}

void NatsClient::publish(const metric_message &message) const {
    natsConnection_PublishString(m_nc, message.name.c_str(), to_nats_message(message).c_str());
}
