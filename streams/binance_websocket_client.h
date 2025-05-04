#pragma once

#define NATS_HAS_TLS

#include "websocket_client.h"
#include "stream_metrics.h"
#include <fmt/chrono.h>
#include <iostream>
#include <chrono>

class BinanceWebSocketClient final : public WebSocketClient {
public:
    explicit BinanceWebSocketClient(net::io_context &ioc, ssl::context &ctx, const Metrics &metrics)
        : WebSocketClient("Binance", "stream.binance.com", "443", ioc, ctx, metrics) {
    }

    ~BinanceWebSocketClient() override {
        if (m_connected) {
            disconnect();
        }
    }

    void connect(const std::string &target) override {
        // These objects perform our I/O
        tcp::resolver resolver{m_ioc};

        // Create the WebSocket stream with SSL
        m_ws = std::make_unique<websocket::stream<beast::ssl_stream<tcp::socket> > >(m_ioc, m_ctx);

        // Look up the domain name
        auto const results = resolver.resolve(host, port);

        net::connect(get_lowest_layer(*m_ws), results);

        // Update the host_ string. This will provide the value of the
        // Host HTTP header during the WebSocket handshake.
        // See https://tools.ietf.org/html/rfc7230#section-5.4
        const std::string host_port = host + ':' + port;

        // Perform the SSL handshake
        m_ws->next_layer().handshake(ssl::stream_base::client);

        // Set a decorator to change the User-Agent of the handshake
        m_ws->set_option(websocket::stream_base::decorator(
            [](websocket::request_type &req) {
                req.set(http::field::user_agent,
                        std::string(BOOST_BEAST_VERSION_STRING) +
                        " binance-cpp-client");
            }));

        // Perform the websocket handshake
        m_ws->handshake(host_port, target);
        m_connected = true;

        std::cout << "Connected to Binance WebSocket stream: " << target << std::endl;
    }

    void disconnect() override {
        if (!m_connected) return;

        beast::error_code ec;
        m_ws->close(websocket::close_code::normal, ec);

        if (ec) {
            std::cerr << "Error closing WebSocket: " << ec.message() << std::endl;
        }

        m_connected = false;
        std::cout << "Disconnected from Binance WebSocket" << std::endl;
    }

    void start_reading() override {
        if (!m_connected) {
            std::cerr << "Cannot start reading, not connected" << std::endl;
            return;
        }

        read_next();
    }

    [[nodiscard]] bool is_connected() const override {
        return m_connected;
    }

private:
    void read_next() override {
        // Clear the buffer
        m_buffer.consume(m_buffer.size());

        // Read a message into our buffer
        m_ws->async_read(
            m_buffer,
            [this](const beast::error_code &ec, std::size_t bytes_transferred) {
                if (ec) {
                    m_connected = false;
                    std::cerr << "Error reading from WebSocket: " << ec.message() << std::endl;
                    return;
                }

                // Parse the message
                on_message(m_buffer);

                // Queue up another read
                read_next();
            });
    }

    void on_message(beast::flat_buffer &buffer) const {
        try {
            std::string json_str(beast::buffers_to_string(buffer.data()));
            const auto j = json::parse(json_str);

            // Process the trade data
            handle_trade_message(j);
        } catch (const std::exception &e) {
            std::cerr << "Error processing message: " << e.what() << std::endl;
        }
    }

    static long long get_time_utc() {
        using namespace std::chrono;
        const auto now = system_clock::now();

        const auto ms = duration_cast<milliseconds>(now.time_since_epoch()).count();

        return ms;
    }


    // https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams#trade-streams
    void handle_trade_message(const json &j) const {
        if (!j.contains("e") || j["e"] != "trade") return;

        try {
            std::string symbol = j["s"];
            const long long event_time = j["E"]; // the time Binance generates and sends the event
            const long long trade_time = j["T"]; // the time the trade occurred on Binance, usually equal or 1ms lower
            int trade_id = j["t"];
            std::string price = j["p"];
            std::string quantity = j["q"];
            const bool is_buyer_maker = j["m"];

            // UTC timezone using zoned_time
            const long long current_time = get_time_utc();
            long long latency = current_time - event_time; // processing latency
            long long trade_latency = event_time - trade_time; // trade latency

            std::string buy_sell = is_buyer_maker ? "SELL" : "BUY";

            if (buy_sell == "BUY") {
                m_metrics.send_order(symbol, BUY);
            } else {
                m_metrics.send_order(symbol, SELL);
            }
            mark_latency(name, symbol, latency);

            using namespace std::chrono;
            fmt::print("[{}] BTC/USDT {} | Price: {} | Quantity: {} | Latency: {} | Trade ID: {}\n",
                       sys_seconds(seconds(event_time / 1000)), buy_sell, price, quantity, latency, trade_id);
        } catch (const std::exception &e) {
            std::cerr << "Error parsing trade data: " << e.what() << std::endl;
        }
    }
};
