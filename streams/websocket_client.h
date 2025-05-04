#pragma once

#include <boost/beast/core.hpp>
#include <boost/beast/websocket.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <boost/asio/ssl/stream.hpp>
#include <nlohmann/json.hpp>
#include <string>
#include <memory>
#include <boost/beast/ssl/ssl_stream.hpp>

#include "metrics.h"

namespace beast = boost::beast;
namespace http = beast::http;
namespace websocket = beast::websocket;
namespace net = boost::asio;
namespace ssl = boost::asio::ssl;

using tcp = boost::asio::ip::tcp;
using json = nlohmann::json;

class WebSocketClient {
public:
    explicit WebSocketClient(std::string name, std::string host, std::string port, net::io_context &ioc,
                             ssl::context &ctx, const Metrics &metrics)
        : m_metrics(metrics), name(std::move(name)), host(std::move(host)), port(std::move(port)), m_ioc(ioc),
          m_ctx(ctx), m_connected(false) {
    }

    virtual ~WebSocketClient() = default;

    virtual void connect(const std::string &target) = 0;

    virtual void disconnect() = 0;

    virtual void start_reading() = 0;

    [[nodiscard]] virtual bool is_connected() const = 0;

protected:
    void on_message(beast::flat_buffer &buffer);

    void handle_trade_message(const json &j);

    virtual void read_next() = 0;

    Metrics m_metrics;
    std::string name;
    std::string host;
    std::string port;
    net::io_context &m_ioc;
    ssl::context &m_ctx;
    std::unique_ptr<websocket::stream<beast::ssl_stream<tcp::socket> > > m_ws;
    beast::flat_buffer m_buffer;
    bool m_connected;
};
