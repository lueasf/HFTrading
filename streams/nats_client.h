#ifndef NATS_CLIENT_H
#define NATS_CLIENT_H

#include <string>
#include <nats/nats.h>


class NatsClient
{
public:
    NatsClient();
    virtual ~NatsClient();

    int connect();

    void publish(std::string value) const;

private:
    natsConnection* m_nc;
    natsSubscription* m_sub;
    natsMsg* m_msg;
};


#endif //NATS_CLIENT_H
