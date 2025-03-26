#define NATS_HAS_TLS

#include <config.h>
#include <iostream>
#include "websocket_client.h"
#include "nats_client.h"
#include <boost/asio/io_context.hpp>
#include <boost/asio/signal_set.hpp>
#include <boost/asio/ssl/context.hpp>
#include <argparse/argparse.hpp>

int main(int argc, char* argv[])
{
    using namespace std;
    cout << "Hello" << endl;

    argparse::ArgumentParser program("hft_streams");

    program.add_argument("--config")
           .help("Path to the configuration file")
           .default_value("config.yaml");

    try
    {
        program.parse_args(argc, argv);
    }
    catch (const std::runtime_error& err)
    {
        std::cout << err.what() << std::endl;
        std::cout << program;
        exit(0);
    }

    auto configFile = program.get<string>("config");

    Config cfg = load(configFile);
    cout << cfg << endl;

    NatsClient natsClient;
    natsClient.connect();

    Metrics metrics(natsClient);

    try
    {
        // Create the required Boost ASIO io_context and SSL context
        net::io_context ioc;
        ssl::context ctx{ssl::context::tlsv12_client};

        // Load the system root certificates
        ctx.set_default_verify_paths();

        // Create our WebSocket client
        BinanceWebSocketClient client(ioc, ctx, metrics);

        // Set up signal handling
        net::signal_set signals(ioc, SIGINT, SIGTERM);
        signals.async_wait([&](beast::error_code const&, int)
        {
            std::cout << "\nReceived shutdown signal" << std::endl;
            if (client.is_connected())
            {
                client.disconnect();
            }
            ioc.stop();
        });

        // Binance WebSocket URL components
        std::string target = "/ws/" + cfg.symbol + "@trade";

        // Connect to Binance WebSocket
        client.connect(target);

        // Start reading messages
        client.start_reading();

        // Run the I/O service
        std::cout << "Waiting for " << cfg.symbol << " trades... (Press Ctrl+C to exit)" << std::endl;
        ioc.run();
    }
    catch (const std::exception& e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
