#include <boost/beast/core.hpp>
#include <boost/beast/websocket.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <boost/asio/ssl/stream.hpp>
#include <nlohmann/json.hpp>
#include <string>
#include <memory>
#include <functional>
#include <boost/beast/ssl/ssl_stream.hpp>

namespace beast = boost::beast;
namespace http = beast::http;
namespace websocket = beast::websocket;
namespace net = boost::asio;
namespace ssl = boost::asio::ssl;
using tcp = boost::asio::ip::tcp;
using json = nlohmann::json;

class BinanceWebSocketClient {
public:
    BinanceWebSocketClient(net::io_context &ioc, ssl::context &ctx);

    ~BinanceWebSocketClient();

    void connect(const std::string &host, const std::string &port, const std::string &target);

    void disconnect();

    void start_reading();

    bool is_connected() const;

private:
    void on_message(beast::flat_buffer &buffer);

    void handle_trade_message(const json &j);

    void read_next();

    net::io_context &m_ioc;
    ssl::context &m_ctx;
    std::unique_ptr<websocket::stream<beast::ssl_stream<tcp::socket>>> m_ws;
    beast::flat_buffer m_buffer;
    bool m_connected;
};
