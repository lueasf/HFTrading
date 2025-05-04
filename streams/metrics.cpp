#include "metrics.h"
#include "communication/nats/nats_client.h"


// handle trade events and send them to NATS
Metrics::Metrics(INatsClient &nats_client): m_nats_client(nats_client) {
}

std::string make_metric_message(const std::string &name, const std::string &value,
                                const std::unordered_map<std::string, std::string> &labels) {
    const auto message = metric_message{name, value, labels};
    std::string result;
    result += message.value + "\n";
    for (const auto &[labelName, labelValue]: message.labels) {
        result += labelName + "=\"" + labelValue + "\",";
    }
    return result;
}

void Metrics::send_order(const std::string &symbol, const OrderType orderType) const {
    std::unordered_map<std::string, std::string> labels;
    labels["symbol"] = symbol;
    switch (orderType) {
        case BUY:
            m_nats_client.publish_raw("orders", make_metric_message("orders", "BUY", labels));
            break;
        case SELL:
            m_nats_client.publish_raw("orders", make_metric_message("orders", "SELL", labels));
            break;
        default:
            break;
    }
}

void Metrics::send_latency(const std::string &symbol, const long long latency) const {
    std::unordered_map<std::string, std::string> labels;
    labels["symbol"] = symbol;
    m_nats_client.publish_raw("latency", make_metric_message("latency", std::to_string(latency), labels));
}
