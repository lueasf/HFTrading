#include "nats_client.h"

// https://github.com/nats-io/nats.c
// connect to nats and publish trade events.
NatsClient::NatsClient() {
    m_nc = nullptr;
    m_sub = nullptr;
    m_msg = nullptr;
}

NatsClient::~NatsClient() {
    if (m_nc != nullptr) {
        natsConnection_Destroy(m_nc);
        m_nc = nullptr;
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

void NatsClient::publish_raw(const std::string subject, const std::string value) const {
    natsConnection_PublishString(m_nc, subject.c_str(), value.c_str());
}
