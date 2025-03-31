# HFTrading

HFTrading is a group project about creating a High Frequency Trading Tool in C++ & Python.

## How to install

Build aeron first:
```bash
cmake --build cmake-build-debug --target aeron
```

On **Windows**, you will need to install Visual Studio. You need a single version of Visual Studio installed or the aeron
build will fail.

You can check your current installation paths with:

```powershell
&(Join-Path ${env:ProgramFiles(x86)} "\Microsoft Visual Studio\Installer\vswhere.exe") -property installationpath
```

## How to run

### Run the Nats server

```bash
docker run -p 4222:4222 -ti nats:latest
```

## Resources

> Prometheus Client
https://prometheus.github.io/client_python/getting-started/three-step-demo/

> WebSocket Lib in C++
https://github.com/boostorg/beast

> NATS server
https://docs.nats.io/running-a-nats-service/introduction/installation

> NATS messaging system
https://github.com/nats-io/nats.c

> Polars a data manipulation lib
https://github.com/pola-rs/polars

> Aeron for UDP transport
https://github.com/aeron-io/aeron

